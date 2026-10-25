"""Regression selection, malformed registry and evidence safety contracts."""
import copy
import json
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch

import assist
import regression_registry as registry
from run_evidence import learning_candidates, report_valid


class TestAssist(unittest.TestCase):
    def setUp(self):
        self.data = registry.load_registry()

    def test_main_preflight_only_clean_synced_ci_green_allows_planning(self):
        sha = 'a' * 40
        local = {'head': sha, 'branch': 'main', 'clean': True, 'origin_valid': True,
                 'pending_branches': [], 'stash_count': 0}
        good = {'path': assist.MAIN_WORKFLOW, 'event': 'push', 'head_sha': sha,
                'status': 'completed', 'conclusion': 'success', 'id': 42,
                'created_at': '2026-10-25T19:00:00Z'}
        passed = assist.decide_preflight(local, sha, [], [good])
        self.assertTrue(passed['planning_allowed'])
        self.assertEqual(passed['result'], 'MAIN_VERIFIED')
        cases = [(dict(local, clean=False), sha, [], [good]),
                 (dict(local, branch='feature'), sha, [], [good]),
                 (dict(local, origin_valid=False), sha, [], [good]),
                 (dict(local, pending_branches=['unmerged']), sha, [], [good]),
                 (dict(local, stash_count=1), sha, [], [good]),
                 (local, 'b' * 40, [], [good]),
                 (local, sha, [{'number': 7}], [good]),
                 (local, sha, [], []),
                 (local, sha, [], [dict(good, conclusion='failure')]),
                 (local, sha, [], [good, dict(good, id=43, conclusion='failure',
                                             created_at='2026-10-25T19:01:00Z')])]
        for facts, remote, prs, runs in cases:
            with self.subTest(local=facts, remote=remote, prs=prs, runs=runs):
                blocked = assist.decide_preflight(facts, remote, prs, runs)
                self.assertFalse(blocked['planning_allowed'])
                self.assertEqual(blocked['result'], 'BLOCKED')

    def test_preflight_remote_failure_overwrites_stale_success(self):
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / 'start.json'
            target.write_text('{"result":"MAIN_VERIFIED"}')
            with patch.object(assist, 'START_REPORT', target), \
                 patch.object(assist, 'git_value', return_value='main'), \
                 patch.object(assist, 'github_json', side_effect=OSError('offline')):
                self.assertEqual(assist.main_preflight(), 1)
            report = json.loads(target.read_text())
            self.assertEqual(report['result'], 'BLOCKED')
            self.assertFalse(report['planning_allowed'])

    def test_preflight_invalid_api_payload_is_blocked(self):
        with tempfile.TemporaryDirectory() as directory:
            with patch.object(assist, 'START_REPORT', Path(directory) / 'start.json'), \
                 patch.object(assist, 'git_value', return_value='main'), \
                 patch.object(assist, 'github_json', side_effect=[{'commit': {'sha': 'short'}}, [], {}]):
                self.assertEqual(assist.main_preflight(), 1)

    def test_unknown_impact_expands_suite(self):
        self.assertIsNone(registry.select_tests(self.data, ['unmapped/new.py']))
        self.assertIsNone(registry.select_tests(self.data, []))

    def test_known_impact_selects_protection(self):
        selected = registry.select_tests(self.data, ['scripts/render_todo.py'])
        self.assertIn('test_render_todo.TestTodo.test_completion_requires_dependencies', selected)
        self.assertIn('test_assist.TestAssist.test_missing_test_is_failure', selected)

    def test_missing_test_is_failure(self):
        self.assertFalse(assist.test_selection_valid(['test_assist.TestAssist.test_does_not_exist']))
        names = sorted({name for item in self.data['families'] for name in item['test_ids']})
        self.assertTrue(assist.test_selection_valid(names))

    def test_registry_rejects_invalid_trigger_and_duplicate(self):
        for change in ('trigger', 'duplicate', 'shell', 'root', 'family'):
            data = copy.deepcopy(self.data)
            if change == 'trigger':
                data['families'][0]['trigger_paths'] = ['../outside/*']
            elif change == 'duplicate':
                data['families'].append(data['families'][0])
            elif change == 'shell':
                data['families'][0]['test_ids'] = ['echo unsafe; command']
            elif change == 'root':
                data = []
            else:
                data['families'] = [None]
            with self.subTest(change=change), tempfile.TemporaryDirectory() as directory:
                path = Path(directory) / 'registry.yaml'
                path.write_text(json.dumps(data))
                with self.assertRaises(ValueError):
                    registry.load_registry(path)

    def test_evidence_detects_content_and_toolchain_drift(self):
        current = {'source_sha': 'a' * 40, 'content_sha256': 'b' * 64,
                   'plan_sha256': 'c' * 64, 'python': '3.12'}
        report = {'schema': 'provoware-check-run/1', 'context': dict(current),
                  'context_after': dict(current), 'result': 'PASS',
                  'checks': [{'id': 'negative-test', 'result': 'PASS', 'returncode': 0}]}
        self.assertTrue(report_valid(report, current, ['negative-test']))
        for key in current:
            self.assertFalse(report_valid(report, dict(current, **{key: 'changed'}), ['negative-test']))
        report['context_after']['content_sha256'] = 'changed during run'
        self.assertFalse(report_valid(report, current, ['negative-test']))
        report['context_after'] = dict(current)
        report['checks'][0]['returncode'] = 1
        self.assertFalse(report_valid(report, current, ['negative-test']))
        report['checks'][0]['returncode'] = 0
        self.assertFalse(report_valid(report, current, ['another-mandatory-check']))
        self.assertFalse(report_valid(report, current, ['negative-test', 'negative-test']))
        report['checks'] = []
        self.assertFalse(report_valid(report, current, ['negative-test']))

    def test_failed_check_and_timeout_cannot_pass(self):
        with patch('assist.subprocess.run', return_value=subprocess.CompletedProcess([], 1)):
            self.assertEqual(assist.run_check('failure', ['ignored'])['result'], 'FAIL')
        with patch('assist.subprocess.run', side_effect=subprocess.TimeoutExpired('test', 120)):
            result = assist.run_check('timeout', ['ignored'])
            self.assertEqual(result['returncode'], 124)
            self.assertEqual(result['result'], 'FAIL')

    def test_repeat_failure_is_learning_candidate_without_raw_text(self):
        checks = [{'id': 'test_assist.TestAssist.test_missing_test_is_failure',
                   'result': 'FAIL', 'returncode': 1}]
        first = learning_candidates(checks, {})
        second = learning_candidates(checks, {'candidates': first})
        self.assertEqual(second[0]['occurrences'], 2)
        self.assertEqual(first[0]['signature'], second[0]['signature'])
        self.assertEqual(learning_candidates([], {'candidates': None}), [])
        retained = learning_candidates([], {'candidates': second})
        self.assertEqual(retained[0]['occurrences'], 2)
        self.assertNotIn('traceback', second[0])
        self.assertEqual(learning_candidates([dict(checks[0], result='PASS')], {}), [])

    def test_early_failure_overwrites_previous_pass_report(self):
        with tempfile.TemporaryDirectory() as directory:
            report = Path(directory) / 'latest.json'
            report.write_text('{"result":"PASS"}')
            with patch('assist.REPORT', report), patch('sys.argv', ['assist.py']), \
                    patch('assist.registry.load_registry', side_effect=ValueError('invalid')):
                self.assertEqual(assist.main(), 1)
            saved = json.loads(report.read_text())
            self.assertEqual(saved['result'], 'FAIL')
            self.assertEqual(saved['phase'], 'BLOCKED')
