"""A technical check is distinct from an explicit gate decision."""
import copy
import json
from pathlib import Path
import tempfile
import unittest

from completion_contract import digest
from gate_contract import enforce_gate_entry, gate_states
from plan_contract import fingerprint, plan_fingerprint


class TestGates(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.route = {'completion_policy': {'approval_actors': ['provoware']},
                      'repository': 'provoware/TOOL_ZENTRALE',
                      'gates': {'G-1': {}, 'G0': {}},
                      'steps': {'B001': {'gate': 'G-1'}, 'P001': {'gate': 'G0'}},
                      'evidence_by_step': {'B001': {'record': 'a', 'sha256': 'b'}},
                      'gate_decisions': {}, 'progress_overrides': {}}
        self.actual = {'B001': True, 'P001': False}

    def decision(self, state='CHECKED'):
        sha = fingerprint({'B001': self.route['evidence_by_step']['B001']})
        self.route['gate_decisions']['G-1'] = {'state': state, 'evidence_sha256': sha}
        return sha

    def test_checked_does_not_open_next_gate(self):
        self.decision()
        self.route['progress_overrides']['P001'] = 'READY'
        with self.assertRaisesRegex(ValueError, 'nicht freigegeben'):
            enforce_gate_entry(self.route, self.actual, self.root)

    def test_missing_incomplete_or_stale_gate_evidence_rejected(self):
        self.decision()
        with self.assertRaises(ValueError):
            gate_states(self.route, dict(self.actual, B001=False), self.root)
        self.route['gate_decisions']['G-1']['evidence_sha256'] = 'wrong'
        with self.assertRaises(ValueError):
            gate_states(self.route, self.actual, self.root)
        self.route['gate_decisions'] = {'UNKNOWN': {}}
        with self.assertRaises(ValueError):
            gate_states(self.route, self.actual, self.root)

    def test_approved_requires_bound_decision(self):
        sha = self.decision('APPROVED')
        with self.assertRaises(ValueError):
            gate_states(self.route, self.actual, self.root)
        approval = {'schema': 'provoware-gate-approval/1', 'gate_id': 'G-1', 'decision': 'APPROVED', 'plan_sha256': plan_fingerprint(self.route),
                    'evidence_sha256': sha, 'approved_by': 'provoware',
                    'decided_at': '2026-10-25T17:00:00Z',
                    'decision_url': 'https://github.com/provoware/TOOL_ZENTRALE/pull/2#issuecomment-1'}
        path = self.root / 'governance/approvals/G-1.json'
        path.parent.mkdir(parents=True)
        path.write_text(json.dumps(approval))
        self.route['gate_decisions']['G-1']['approval'] = 'governance/approvals/G-1.json'
        self.route['gate_decisions']['G-1']['approval_sha256'] = digest(path)
        self.assertEqual(gate_states(self.route, self.actual, self.root)['G-1'], 'APPROVED')
        self.route['progress_overrides']['P001'] = 'READY'
        enforce_gate_entry(self.route, self.actual, self.root)
        approval['evidence_sha256'] = 'stale'
        path.write_text(json.dumps(approval))
        with self.assertRaises(ValueError):
            gate_states(self.route, self.actual, self.root)

    def test_later_gate_cannot_skip_previous_approval(self):
        self.route['evidence_by_step']['P001'] = {'record': 'p', 'sha256': 'q'}
        self.route['gate_decisions']['G0'] = {'state': 'CHECKED', 'evidence_sha256':
                                          fingerprint({'P001': self.route['evidence_by_step']['P001']})}
        with self.assertRaisesRegex(ValueError, 'Vorgängergate'):
            gate_states(self.route, dict(self.actual, P001=True), self.root)

    def test_active_subtask_also_requires_previous_gate(self):
        self.route['steps']['P001']['substeps'] = [{'id': 'P001.01'}]
        self.actual['P001.01'] = False
        for state in ('READY', 'PATCHED'):
            self.route['progress_overrides']['P001.01'] = state
            with self.assertRaisesRegex(ValueError, 'Vorgängergate'):
                enforce_gate_entry(self.route, self.actual, self.root)
