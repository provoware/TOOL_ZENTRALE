"""Persistent model checks and early-user-route dependency regressions."""
import copy
import json
from pathlib import Path
import unittest

import yaml

from check_governance import ROOT, UniqueLoader, validate_blueprint
import render_todo


class TestBlueprint(unittest.TestCase):
    def setUp(self):
        self.route = render_todo.load_route(ROOT / 'governance/route.json')
        self.blueprint = yaml.load((ROOT / 'blueprint/architecture.yaml').read_text(), Loader=UniqueLoader)

    def test_duplicate_yaml_keys_and_forbidden_edges_rejected(self):
        with self.assertRaises(ValueError):
            yaml.load('same: 1\nsame: 2', Loader=UniqueLoader)
        self.blueprint['codebook']['DDOC']['requires'] = ['KCFG']
        with self.assertRaises(ValueError):
            validate_blueprint(self.blueprint, self.route)

    def test_real_blueprint_and_early_song_path(self):
        self.assertTrue(validate_blueprint(self.blueprint, self.route))
        steps = self.route['steps']
        self.assertEqual(steps['P047']['depends_on'], ['P043'])
        self.assertEqual(steps['P056']['depends_on'], ['P050'])
        self.assertEqual(steps['P063']['depends_on'], ['P056'])
        self.assertEqual(steps['P044']['gate'], 'G6')
        self.assertEqual([sid for sid, item in steps.items() if item['gate'] == 'G5'],
                         ['P047', 'P048', 'P049', 'P050', 'P056'])
        self.assertEqual(len(steps), 112)
