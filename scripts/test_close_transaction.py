"""Closing must validate paths first and preserve originals on write failure."""
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import complete_step


class TestCloseTransaction(unittest.TestCase):
    def test_symlink_or_traversal_rejected_before_write(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            folder = root / 'governance/evidence'
            folder.mkdir(parents=True)
            outside = root / 'protected.txt'
            outside.write_text('protected')
            (folder / 'Q001.json').symlink_to(outside)
            for sid in ('Q001', '../escape'):
                with self.subTest(sid=sid), self.assertRaises(ValueError):
                    complete_step.apply_completion({}, [sid], {}, root)
            self.assertEqual(outside.read_text(), 'protected')

    def test_route_write_failure_restores_existing_artifact(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            folder = root / 'governance/evidence'
            folder.mkdir(parents=True)
            artifact = folder / 'Q001.json'
            artifact.write_text('old artifact')
            route_path = root / 'governance/route.json'
            route_path.write_text('old route')
            route = {'evidence_by_step': {}, 'progress_overrides': {},
                     'iteration_queue': [{'id': 'Q001', 'status': 'PLANNED'}]}
            real_write = complete_step.atomic_write

            def write(path, content):
                if path == route_path:
                    raise OSError('simulated failure')
                real_write(path, content)

            with patch('complete_step.build_record', return_value={}), \
                    patch('complete_step.render_todo.resolve', return_value={}), \
                    patch('complete_step.atomic_write', side_effect=write):
                with self.assertRaises(OSError):
                    complete_step.apply_completion(route, ['Q001'], {}, root)
            self.assertEqual(route_path.read_text(), 'old route')
            self.assertEqual(artifact.read_text(), 'old artifact')
            self.assertEqual(list(folder.iterdir()), [artifact])
