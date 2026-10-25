"""Exact scope evidence must reject legacy, forged, stale and misbound closures."""
import copy
import json
from pathlib import Path
import subprocess
import tempfile
import unittest

from complete_step import build_record
from completion_contract import digest, record_valid
from plan_contract import plan_fingerprint
from run_evidence import context


class TestCompletion(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        subprocess.run(['git', 'init', '-q', str(self.root)], check=True)
        subprocess.run(['git', '-c', 'user.name=Test', '-c', 'user.email=test@example.invalid',
                        'commit', '--allow-empty', '-qm', 'fixture'], cwd=self.root, check=True)
        self.route = {'steps': {'B001': {'completion_inputs': ['source.py', 'test_source.py']}},
                      'iteration_queue': [], 'progress_overrides': {}, 'evidence_by_step': {},
                      'completion_policy': {'required_checks': ['development-suite']}}
        (self.root / 'governance').mkdir()
        (self.root / 'governance/route.json').write_text(json.dumps(self.route))
        (self.root / 'source.py').write_text('value = 1\n')
        (self.root / 'test_source.py').write_text('assert value == 1\n')
        ctx = context(self.root)
        self.report = {'schema': 'provoware-check-run/1', 'result': 'PASS',
                       'context': ctx, 'context_after': copy.deepcopy(ctx), 'changed_paths': [],
                       'checks': [{'id': 'development-suite', 'result': 'PASS', 'returncode': 0}]}
        self.record = build_record(self.route, 'B001', self.report, self.root)
        self.entry = self.save(self.record)

    def save(self, record):
        path = self.root / 'governance/evidence/B001.json'
        path.parent.mkdir(exist_ok=True)
        path.write_text(json.dumps(record))
        return {'record': 'governance/evidence/B001.json', 'sha256': digest(path)}

    def test_valid_scope_and_status_do_not_create_hash_cycle(self):
        self.assertTrue(record_valid(self.entry, self.route, 'B001', self.root))
        changed = copy.deepcopy(self.route)
        changed['progress_overrides']['B001'] = 'VERIFIED'
        changed['evidence_by_step']['B001'] = self.entry
        self.assertEqual(plan_fingerprint(changed), plan_fingerprint(self.route))
        self.assertTrue(record_valid(self.entry, changed, 'B001', self.root))
        (self.root / 'unrelated.md').write_text('unrelated documentation')
        self.assertTrue(record_valid(self.entry, changed, 'B001', self.root))

    def test_legacy_pass_and_wrong_target_are_rejected(self):
        self.assertFalse(record_valid({'source_sha': 'a' * 40, 'test_run': 'fake', 'result': 'PASS'},
                                      self.route, 'B001', self.root))
        self.assertFalse(record_valid(self.entry, self.route, 'B002', self.root))
        self.assertFalse(record_valid(dict(self.entry, sha256='0' * 64), self.route, 'B001', self.root))

    def test_source_test_and_plan_drift_rejected(self):
        for name in ('source.py', 'test_source.py'):
            path = self.root / name
            original = path.read_bytes()
            path.write_bytes(b'changed')
            self.assertFalse(record_valid(self.entry, self.route, 'B001', self.root))
            path.write_bytes(original)
        changed = copy.deepcopy(self.route)
        changed['steps']['B001']['depends_on'] = ['other']
        self.assertFalse(record_valid(self.entry, changed, 'B001', self.root))

    def test_missing_checks_or_nonexistent_commit_rejected(self):
        record = copy.deepcopy(self.record)
        record['report']['checks'] = []
        self.assertFalse(record_valid(self.save(record), self.route, 'B001', self.root))
        record = copy.deepcopy(self.record)
        for key in ('context', 'context_after'):
            record['report'][key]['source_sha'] = 'a' * 40
        self.assertFalse(record_valid(self.save(record), self.route, 'B001', self.root))

    def test_targeted_or_stale_report_cannot_close_step(self):
        report = copy.deepcopy(self.report)
        report['changed_paths'] = ['source.py']
        with self.assertRaises(ValueError):
            build_record(self.route, 'B001', report, self.root)
        (self.root / 'source.py').write_text('changed')
        with self.assertRaises(ValueError):
            build_record(self.route, 'B001', self.report, self.root)

    def test_development_suite_cannot_certify_product_step(self):
        self.route['steps']['P009'] = {'patch': 'K', 'completion_inputs': ['source.py']}
        with self.assertRaisesRegex(ValueError, 'Produktprüfungen'):
            build_record(self.route, 'P009', self.report, self.root)
