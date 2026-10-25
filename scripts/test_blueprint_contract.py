"""Negative contracts for layer policy, file ownership and semantic reservations."""
import copy
import unittest

import yaml

from blueprint_contract import historical_codes, validate_model
from check_governance import ROOT, UniqueLoader


class TestBlueprintContract(unittest.TestCase):
    def setUp(self):
        self.data = yaml.load((ROOT / 'blueprint/architecture.yaml').read_text(), Loader=UniqueLoader)
        self.history = historical_codes(ROOT)

    def test_real_model_respects_historical_reservations(self):
        coverage = validate_model(self.data, self.history)
        self.assertIn('KCFG', self.history)
        self.assertIn('TTXT', coverage['KTXT'])

    def test_policy_cannot_authorize_domain_ui_dependency(self):
        self.data['layers']['DOMAIN']['may_depend_on'] = ['UI']
        self.data['codebook']['DDOC']['requires'] = ['UGRD']
        with self.assertRaisesRegex(ValueError, 'Schichtenpolicy'):
            validate_model(self.data, self.history)

    def test_alias_paths_and_invalid_file_metadata_rejected(self):
        for field, value in (('owner', 'UNKNOWN'), ('stability', 'S9'), ('catalog', 'DONE')):
            data = copy.deepcopy(self.data)
            data['files']['app/core/config.py'][field] = value
            with self.subTest(field=field), self.assertRaises(ValueError):
                validate_model(data, self.history)
        self.data['files']['a//b.py'] = {'owner': 'CORE', 'stability': 'S1', 'catalog': 'CONFIRMED'}
        with self.assertRaises(ValueError):
            validate_model(self.data, self.history)

    def test_code_identity_and_required_interface_protected(self):
        self.data['codebook']['KCFG']['path'] = 'app/core/errors.py'
        with self.assertRaisesRegex(ValueError, 'Codeidentität'):
            validate_model(self.data, self.history)
        self.data['codebook']['KCFG']['path'] = 'app/core/config.py'
        self.data['codebook']['KCFG'].pop('interface')
        with self.assertRaises(ValueError):
            validate_model(self.data, self.history)

    def test_unknown_test_target_or_missing_test_trace_rejected(self):
        self.data['codebook']['TTXT']['verifies'] = ['UNKNOWN']
        with self.assertRaises(ValueError):
            validate_model(self.data, self.history)
        self.data['codebook']['TTXT']['verifies'] = ['KCFG']
        with self.assertRaisesRegex(ValueError, 'Testzuordnung'):
            validate_model(self.data, self.history)

    def test_plugin_cannot_bypass_capability_contract(self):
        self.data['codebook']['PLOD']['requires'] = ['DPLG']
        with self.assertRaisesRegex(ValueError, 'Capability'):
            validate_model(self.data, self.history)

    def test_media_import_catalog_must_be_complete(self):
        self.data['files'].pop('app/features/media/help/de.md')
        with self.assertRaisesRegex(ValueError, 'media'):
            validate_model(self.data, self.history)

    def test_core_and_cross_feature_internal_access_rejected(self):
        for source, target in (('KCFG', 'DSNG'), ('SSNG', 'DPRJ')):
            data = copy.deepcopy(self.data)
            data['codebook'][source]['requires'] = [target]
            with self.subTest(source=source), self.assertRaisesRegex(ValueError, 'Fachmodulinterna'):
                validate_model(data, self.history)

    def test_file_directory_or_parent_file_collision_rejected(self):
        for mode in ('directory', 'parent'):
            data = copy.deepcopy(self.data)
            meta = {'owner': 'CORE', 'stability': 'S1', 'catalog': 'CONFIRMED'}
            if mode == 'directory':
                data['files']['app'] = meta
            else:
                data['files']['reserved'] = meta
                data['files']['reserved/child.py'] = meta
            with self.subTest(mode=mode), self.assertRaisesRegex(ValueError, 'kollision'):
                validate_model(data, self.history)

    def test_conflicting_foreign_code_flags_rejected(self):
        self.data['module_contract']['arbitrary_foreign_code_v1'] = True
        with self.assertRaisesRegex(ValueError, 'Fremdcode'):
            validate_model(self.data, self.history)
