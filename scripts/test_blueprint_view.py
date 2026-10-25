"""Inventory and legend are derived and do not pretend virtual files are implemented."""
import unittest

import yaml

from blueprint_contract import historical_codes
from blueprint_view import audit, render
from check_governance import ROOT, UniqueLoader
from render_todo import load_route


class TestBlueprintView(unittest.TestCase):
    def setUp(self):
        self.data = yaml.load((ROOT / 'blueprint/architecture.yaml').read_text(), Loader=UniqueLoader)
        self.route = load_route(ROOT / 'governance/route.json')
        self.history = historical_codes(ROOT)

    def test_virtual_catalog_and_derived_consumers(self):
        result = audit(self.data, {'README.md'}, self.history, self.route)
        virtual = {item['path']: item['presence'] for item in result['inventory']}
        self.assertEqual(virtual['README.md'], 'PRESENT')
        self.assertEqual(virtual['app/core/config.py'], 'VIRTUAL')
        self.assertEqual(virtual['tests/unit/test_text_catalog.py'], 'VIRTUAL')
        legend = {item['code']: item for item in result['code_legend']}
        self.assertIn('KLOG', legend['KCFG']['consumers'])
        self.assertIn('TTXT', legend['KTXT']['planned_tests'])
        self.assertIn('keine Produktprüfung', render(result))

    def test_new_actual_file_requires_catalog_entry(self):
        with self.assertRaisesRegex(ValueError, 'ohne Katalogeintrag'):
            audit(self.data, {'README.md', 'scripts/unregistered.py'}, self.history, self.route)

    def test_runtime_cycle_is_rejected(self):
        self.data['codebook']['DDOC']['requires'] = ['DSNG']
        with self.assertRaisesRegex(ValueError, 'Zyklus'):
            audit(self.data, {'README.md'}, self.history, self.route)

    def test_rendering_does_not_depend_on_new_commit_history_count(self):
        result = audit(self.data, {'README.md'}, self.history, self.route)
        before = render(result)
        result['historical_reserved_codes'] += 1
        self.assertEqual(before, render(result))
