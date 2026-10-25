"""Guard source traceability, MVP coverage, repository boundaries and reuse policy."""
import copy
import json
import unittest

import yaml

from check_governance import ROOT, UniqueLoader
from foundation import DATA, validate
from render_todo import load_route


class TestFoundation(unittest.TestCase):
    def setUp(self):
        self.data = json.loads(DATA.read_text())
        self.blueprint = yaml.load((ROOT / 'blueprint/architecture.yaml').read_text(), Loader=UniqueLoader)
        self.route = load_route(ROOT / 'governance/route.json')

    def test_sources_cover_mvp_without_unlicensed_copying(self):
        self.assertTrue(validate(self.data, self.blueprint, self.route,
                                 'https://github.com/provoware/TOOL_ZENTRALE.git'))

    def test_wrong_repository_and_mutable_source_links_rejected(self):
        with self.assertRaises(ValueError):
            validate(self.data, self.blueprint, self.route, 'https://github.com/other/repo.git')
        self.data['reference']['files'][0]['url'] = 'https://github.com/provoware/TOOL_2026_Multi/blob/main/file.py'
        with self.assertRaises(ValueError):
            validate(self.data, self.blueprint, self.route, 'https://github.com/provoware/TOOL_ZENTRALE')

    def test_missing_mvp_goal_or_unknown_source_rejected(self):
        for mode in ('missing', 'unknown'):
            data = copy.deepcopy(self.data)
            if mode == 'missing':
                data['use_cases'] = [case for case in data['use_cases'] if case['area'] != 'import']
            else:
                data['use_cases'][0]['sources'] = ['UNREAD']
            with self.subTest(mode=mode), self.assertRaises(ValueError):
                validate(data, self.blueprint, self.route, 'https://github.com/provoware/TOOL_ZENTRALE')

    def test_direct_reuse_cannot_bypass_license_review(self):
        self.data['reuse'][0]['direct_copy_allowed'] = True
        with self.assertRaises(ValueError):
            validate(self.data, self.blueprint, self.route, 'https://github.com/provoware/TOOL_ZENTRALE')

    def test_empty_targets_or_reuse_and_missing_contracts_rejected(self):
        for mode in ('targets', 'reuse', 'contracts'):
            data = copy.deepcopy(self.data)
            if mode == 'targets':
                data['use_cases'][0]['target_steps'] = []
            else:
                data['reuse' if mode == 'reuse' else 'shared_contracts'] = []
            with self.subTest(mode=mode), self.assertRaises(ValueError):
                validate(data, self.blueprint, self.route, 'https://github.com/provoware/TOOL_ZENTRALE')

    def test_rewritten_receipts_cannot_change_pinned_reference(self):
        self.data['reference']['commit'] = 'a' * 40
        for source in self.data['reference']['files']:
            source['url'] = source['url'].replace(self.blueprint['reference_commit'], 'a' * 40)
        with self.assertRaises(ValueError):
            validate(self.data, self.blueprint, self.route, 'https://github.com/provoware/TOOL_ZENTRALE')
