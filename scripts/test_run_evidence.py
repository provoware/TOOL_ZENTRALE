"""Generated views must invalidate evidence even though inventory excludes them."""
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch

import assist

from run_evidence import context


class TestGeneratedEvidence(unittest.TestCase):
    def test_generated_view_drift_invalidates_context(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            subprocess.run(['git', 'init', '-q', str(root)], check=True)
            subprocess.run(['git', '-c', 'user.name=Test', '-c', 'user.email=test@example.invalid',
                            'commit', '--allow-empty', '-qm', 'fixture'], cwd=root, check=True)
            for name in ('governance/file_state.json', 'docs/STATUS_KURZ.md'):
                path = root / name
                path.parent.mkdir(exist_ok=True)
                path.write_text('original')
            before = context(root)
            for name in ('governance/file_state.json', 'docs/STATUS_KURZ.md'):
                with self.subTest(name=name):
                    path = root / name
                    path.write_text('changed')
                    after = context(root)
                    self.assertEqual(before['content_sha256'], after['content_sha256'])
                    self.assertNotEqual(before, after)
                    path.write_text('original')

    def test_malformed_report_root_fails_cleanly(self):
        with tempfile.TemporaryDirectory() as directory:
            report = Path(directory) / 'latest.json'
            for raw in ('[]', 'null'):
                with self.subTest(raw=raw):
                    report.write_text(raw)
                    with patch('assist.REPORT', report), patch('sys.argv', ['assist.py', '--verify-report']):
                        self.assertEqual(assist.main(), 1)
