"""Cross-field consistency guards against contradictory design claims."""
import copy
import unittest

import yaml

from check_governance import ROOT, UniqueLoader
from contract_view import build


class TestContractConsistency(unittest.TestCase):
    def setUp(self):
        self.data = yaml.load((ROOT / 'blueprint/architecture.yaml').read_text(), Loader=UniqueLoader)

    def test_missing_examples_ack_and_byte_budget_rejected(self):
        for mode in ('examples', 'ack', 'bytes'):
            data = copy.deepcopy(self.data)
            c = data['contracts']
            if mode == 'examples':
                c['examples'] = {}
            elif mode == 'ack':
                c['payloads']['note_response']['required'].remove('durable')
            else:
                c['http_boundary']['max_request_bytes'] = 0
            with self.subTest(mode=mode), self.assertRaises(ValueError):
                build(data)

    def test_writable_legacy_false_error_status_and_owner_rejected(self):
        for mode in ('legacy', 'error', 'owner', 'capability'):
            data = copy.deepcopy(self.data)
            if mode == 'legacy':
                data['contracts']['data_ownership']['legacy_sources'] = 'WRITABLE'
            elif mode == 'error':
                data['contracts']['error_statuses']['PERMISSION_DENIED'] = 200
            elif mode == 'owner':
                data['checker_contract']['execution_owner'] = 'app/core/config.py'
            else:
                data['contracts']['api_capabilities']['AIMP']['apply'] = 'catalog.read'
            with self.subTest(mode=mode), self.assertRaises(ValueError):
                build(data)

    def test_standalone_model_rejects_broken_path_and_unsafe_import(self):
        self.data['scenarios']['song_save']['path'].remove('ASNG')
        with self.assertRaises(ValueError):
            build(self.data)
        self.setUp()
        self.data['contracts']['payloads']['import_preview']['properties']['apply']['const'] = True
        with self.assertRaises(ValueError):
            build(self.data)

    def test_unsupported_schema_keyword_cannot_silently_pass(self):
        self.data['contracts']['payloads']['note_request']['properties']['text']['pattern'] = '^never$'
        with self.assertRaisesRegex(ValueError, 'unterstütztes'):
            build(self.data)
