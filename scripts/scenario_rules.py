"""Validate model scenarios and declared guard reachability without running them."""
from blueprint_contract import reachable, planned_tests

REQUIRED = {'song_save', 'project_search', 'plugin_load', 'quick_note_append',
            'offline_launch', 'import_preview', 'media_open', 'plugin_trusted_launch'}


def validate_scenarios(blueprint):
    codes, scenarios = blueprint['codebook'], blueprint['scenarios']
    policy = blueprint['simulation_policy']
    if (not REQUIRED <= set(scenarios) or policy.get('runtime_status') != 'NOT_TESTED'
            or policy.get('no_claim_of_real_execution') is not True):
        raise ValueError('Szenarien fehlen oder Modell behauptet Laufzeitprüfung')
    for code, item in codes.items():
        guards = item.get('guard_contracts', [])
        if guards and (item['layer'] != 'TOOL' or len(guards) != len(set(guards))
                       or any(g not in codes or codes[g]['layer'] != 'CORE' for g in guards)):
            raise ValueError(f'{code}: ungültiger Vorstart-Prüfvertrag')
    coverage = planned_tests(codes)
    case_ids = set()
    total = 0
    for name, scenario in scenarios.items():
        if not scenario.get('objective') or not scenario.get('path'):
            raise ValueError('Ziel oder Szenariopfad fehlt')
        if any(code not in codes for code in scenario['path']):
            raise ValueError('Unbekannter Szenariocode')
        for first, second in zip(scenario['path'], scenario['path'][1:]):
            if second not in codes[first].get('requires', []):
                raise ValueError('Unterbrochene Szenariopfadkante')
        tests = scenario.get('tests', [])
        if not tests or any(test not in codes or codes[test]['layer'] != 'QA' for test in tests):
            raise ValueError('Szenario benötigt echte QA-Codezuordnung')
        if any(not set(tests) & set(coverage[code]) for code in scenario['path']):
            raise ValueError('Szenariopfad nicht durch geplante Tests abgedeckt')
        reachable_codes = reachable(codes, scenario['path'])
        for code in list(reachable_codes):
            reachable_codes.update(codes[code].get('guard_contracts', []))
        required = {'KCFG', 'KLOG'} if name == 'offline_launch' else {'KSEC', 'KERR', 'KLOG'}
        if name == 'quick_note_append':
            required.add('KVER')
        guards = scenario.get('guards', [])
        if (not required <= set(guards) or not set(guards) <= reachable_codes
                or len(guards) != len(set(guards))):
            raise ValueError(f'{name}: Schutzpunkte fehlen oder sind unerreichbar')
        cases = scenario.get('simulation_cases', [])
        if len(cases) < 4 or {case.get('kind') for case in cases} != {'POSITIVE', 'NEGATIVE'}:
            raise ValueError('Mindestens vier positive/negative Modellfälle erforderlich')
        for case in cases:
            if (any(not isinstance(case.get(field), str) or not case[field].strip()
                    for field in ('id', 'input', 'expected')) or case['id'] in case_ids):
                raise ValueError('Doppelte Fall-ID oder leere Erwartung')
            case_ids.add(case['id'])
            total += 1
        if not scenario.get('unresolved_until_real_code'):
            raise ValueError('Offene reale Nachweise fehlen')
    return {'scenarios': len(scenarios), 'cases': total,
            'result_kind': 'MODEL_CONTRACT_PASS', 'runtime_result': 'NOT_TESTED'}
