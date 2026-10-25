"""Model cases need unique expectations, QA trace and declared reachable guards."""
import copy
import unittest

import yaml

from check_governance import ROOT, UniqueLoader
from scenario_rules import CRITICAL_FAULTS, validate_scenarios


class TestScenarioRules(unittest.TestCase):
    def setUp(self):
        self.data = yaml.load((ROOT / 'blueprint/architecture.yaml').read_text(), Loader=UniqueLoader)

    def test_all_existing_cases_have_model_only_evidence(self):
        result = validate_scenarios(self.data)
        self.assertEqual(result['runtime_result'], 'NOT_TESTED')
        self.assertEqual(result['cases'], sum(len(s['simulation_cases']) for s in self.data['scenarios'].values()))

    def test_duplicate_case_or_empty_expectation_rejected(self):
        for mode in ('duplicate', 'empty'):
            data = copy.deepcopy(self.data)
            cases = data['scenarios']['song_save']['simulation_cases']
            if mode == 'duplicate':
                cases[1]['id'] = cases[0]['id']
            else:
                cases[0]['expected'] = ''
            with self.subTest(mode=mode), self.assertRaises(ValueError):
                validate_scenarios(data)

    def test_too_few_cases_or_missing_negative_case_rejected(self):
        for mode in ('few', 'negative'):
            data = copy.deepcopy(self.data)
            cases = data['scenarios']['song_save']['simulation_cases']
            if mode == 'few':
                cases.pop()
            else:
                for case in cases:
                    case['kind'] = 'POSITIVE'
            with self.subTest(mode=mode), self.assertRaises(ValueError):
                validate_scenarios(data)

    def test_missing_qa_target_or_required_guard_rejected(self):
        self.data['scenarios']['song_save']['tests'] = ['USNG']
        with self.assertRaises(ValueError):
            validate_scenarios(self.data)
        self.setUp()
        self.data['scenarios']['song_save']['guards'].remove('KSEC')
        with self.assertRaises(ValueError):
            validate_scenarios(self.data)

    def test_startup_guard_must_be_explicit_and_reachable(self):
        self.data['codebook']['LBOOT'].pop('guard_contracts')
        with self.assertRaises(ValueError):
            validate_scenarios(self.data)

    def test_fabricated_runtime_pass_rejected(self):
        self.data['simulation_policy']['runtime_status'] = 'PASS'
        with self.assertRaises(ValueError):
            validate_scenarios(self.data)

    def test_critical_txt_and_offline_faults_cannot_disappear_or_change(self):
        for name, required in CRITICAL_FAULTS.items():
            for case_id in required:
                for mutation in ('missing', 'expected', 'kind', 'input'):
                    data = copy.deepcopy(self.data)
                    cases = data['scenarios'][name]['simulation_cases']
                    case = next(item for item in cases if item['id'] == case_id)
                    if mutation == 'missing':
                        cases.remove(case)
                    else:
                        case[mutation] = 'POSITIVE' if mutation == 'kind' else 'false_pass'
                        if mutation == 'kind' and required[case_id][0] == 'POSITIVE':
                            case['kind'] = 'NEGATIVE'
                    with self.subTest(name=name, case_id=case_id, mutation=mutation):
                        with self.assertRaises(ValueError):
                            validate_scenarios(data)
