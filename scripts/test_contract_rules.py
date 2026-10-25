"""Design examples and trust/version boundaries."""
import copy
import unittest

import yaml

from check_governance import ROOT, UniqueLoader
from contract_rules import validate_contracts, validate_checker


class TestContractRules(unittest.TestCase):
    def setUp(self):
        self.data = yaml.load((ROOT / 'blueprint/architecture.yaml').read_text(), Loader=UniqueLoader)

    def test_real_contracts_and_checker(self):
        self.assertTrue(validate_contracts(self.data))
        self.assertTrue(validate_checker(self.data))

    def test_unknown_capability_or_trust_escalation_rejected(self):
        for mode in ('capability', 'trust'):
            data = copy.deepcopy(self.data)
            p = data['contracts']['permissions']
            if mode == 'capability':
                p['capabilities'].append('shell.anything')
            else:
                p['trust_levels']['FOREIGN_CODE'] = 'ALLOW'
            with self.subTest(mode=mode), self.assertRaises(ValueError):
                validate_contracts(data)

    def test_note_duplicate_conflict_and_durability_contract(self):
        for field, value in (('same_id_other_content', 'SAME_ACK'), ('success_after', 'BUFFERED'),
                             ('client_version_policy', 'TRUST_CLIENT'), ('max_request_bytes', 1024)):
            data = copy.deepcopy(self.data)
            data['contracts']['note_semantics'][field] = value
            with self.subTest(field=field), self.assertRaises(ValueError):
                validate_contracts(data)

    def test_oversized_text_and_client_version_fields_rejected(self):
        for mode in ('large', 'version'):
            data = copy.deepcopy(self.data)
            sample = data['contracts']['examples']['note_request']
            if mode == 'large':
                sample['text'] = 'x' * 1001
            else:
                sample['app_version'] = 'forged'
            with self.subTest(mode=mode), self.assertRaises(ValueError):
                validate_contracts(data)

    def test_version_coupling_and_missing_error_help_rejected(self):
        self.data['contracts']['version_axes']['database'] = self.data['contracts']['version_axes']['product']
        with self.assertRaises(ValueError):
            validate_contracts(self.data)
        self.setUp()
        self.data['contracts']['payloads']['error']['required'].remove('next_action')
        with self.assertRaises(ValueError):
            validate_contracts(self.data)

    def test_nested_schema_and_local_network_boundary(self):
        self.data['contracts']['examples']['song_request']['sections'] = [{}]
        with self.assertRaises(ValueError):
            validate_contracts(self.data)
        self.setUp()
        self.data['contracts']['http_boundary']['bind'] = '0.0.0.0'
        with self.assertRaises(ValueError):
            validate_contracts(self.data)

    def test_checker_cannot_skip_phase_write_source_or_claim_runtime_pass(self):
        for mode in ('phase', 'write', 'runtime', 'target'):
            data = copy.deepcopy(self.data)
            checker = data['checker_contract']
            if mode == 'phase':
                checker['phases'].remove('evidence_gates')
            elif mode == 'write':
                checker['source_mutation'] = True
            elif mode == 'runtime':
                checker['runtime_result'] = 'PASS'
            else:
                checker['refresh_outputs'].append('app/core/config.py')
            with self.subTest(mode=mode), self.assertRaises(ValueError):
                validate_checker(data)
