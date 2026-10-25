"""Verify content drift and deletion detection in an isolated repository."""
import subprocess
import tempfile
import unittest
from pathlib import Path

from project_state import snapshot


class TestState(unittest.TestCase):
    def test_changes_additions_deletions_and_exclusions(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            subprocess.run(['git', 'init', '-q', str(root)], check=True)
            source = root / 'info.txt'
            source.write_text('first', encoding='utf-8')
            subprocess.run(['git', 'add', 'info.txt'], cwd=root, check=True)
            first = snapshot(root)
            self.assertEqual(first, snapshot(root))
            source.write_text('second', encoding='utf-8')
            self.assertNotEqual(first, snapshot(root))
            source.unlink()
            self.assertEqual(snapshot(root)['files'], [])
            (root / 'new.txt').write_text('new', encoding='utf-8')
            self.assertEqual(snapshot(root)['files'][0]['path'], 'new.txt')
            (root / 'governance').mkdir()
            (root / 'governance/file_state.json').write_text('{}')
            self.assertEqual(len(snapshot(root)['files']), 1)

    def test_symlink_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            subprocess.run(['git', 'init', '-q', str(root)], check=True)
            (root / 'link').symlink_to('/etc/passwd')
            with self.assertRaisesRegex(ValueError, 'Symlink'):
                snapshot(root)
