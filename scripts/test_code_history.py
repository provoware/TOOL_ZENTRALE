"""Transient IDs from a merged side branch stay reserved without a shadow registry."""
import json
from pathlib import Path
import subprocess
import tempfile
import unittest

from blueprint_contract import historical_codes


class TestCodeHistory(unittest.TestCase):
    def test_merged_transient_code_remains_reserved(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)

            def git(*args):
                subprocess.run(['git', '-c', 'user.name=Test', '-c', 'user.email=test@example.invalid',
                                *args], cwd=root, check=True, capture_output=True)

            git('init', '-q', '-b', 'main')
            path = root / 'blueprint/architecture.yaml'
            path.parent.mkdir()
            data = {'codebook': {'KCFG': {'path': 'app/core/config.py', 'layer': 'CORE'}}}

            def commit(message):
                path.write_text(json.dumps(data))
                git('add', 'blueprint/architecture.yaml')
                git('commit', '-qm', message)

            commit('base')
            git('checkout', '-qb', 'side')
            data['codebook']['HIST'] = {'path': 'retired.py', 'layer': 'DOMAIN'}
            commit('reserve transient code')
            data['codebook'].pop('HIST')
            commit('remove before merge')
            git('checkout', '-q', 'main')
            git('merge', '--no-ff', '-qm', 'merge side history', 'side')
            self.assertEqual(historical_codes(root)['HIST'], ('retired.py', 'DOMAIN'))
