#!/usr/bin/env python3
"""Permanent blueprint, step-evidence and gate validation; never grants approval."""
from pathlib import Path
import re

import yaml

import render_todo

ROOT = Path(__file__).resolve().parents[1]


class UniqueLoader(yaml.SafeLoader):
    pass


def unique_mapping(loader, node, deep=False):
    output = {}
    for key_node, value in node.value:
        key = loader.construct_object(key_node, deep=deep)
        if key in output:
            raise ValueError(f'Doppelter YAML-Schlüssel: {key}')
        output[key] = loader.construct_object(value, deep=deep)
    return output


UniqueLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, unique_mapping)


def validate_blueprint(blueprint, route):
    codes, files, layers = (blueprint[name] for name in ('codebook', 'files', 'layers'))
    for name in files:
        if Path(name).is_absolute() or '..' in Path(name).parts:
            raise ValueError('Unsicherer Sollpfad')
    for code, item in codes.items():
        if not re.fullmatch(blueprint['standards']['code_regex'], code) or item['path'] not in files:
            raise ValueError(f'{code}: ungültiger Code oder Dateiverweis')
        if item['layer'] not in layers:
            raise ValueError(f'{code}: unbekannter Layer')
        for dep in item.get('requires', []):
            if dep not in codes or codes[dep]['layer'] not in layers[item['layer']]['may_depend_on']:
                raise ValueError(f'{code}: unzulässige Abhängigkeit')
    visiting, visited = set(), set()

    def visit(code):
        if code in visiting:
            raise ValueError('Blueprint-Zyklus')
        if code in visited:
            return
        visiting.add(code)
        for dep in codes[code].get('requires', []):
            visit(dep)
        visiting.remove(code)
        visited.add(code)

    for code in codes:
        visit(code)
    for name, scenario in blueprint['scenarios'].items():
        refs = sum((scenario.get(field, []) for field in ('path', 'guards', 'tests', 'side_contracts')), [])
        if not scenario.get('tests') or any(code not in codes for code in refs):
            raise ValueError(f'{name}: fehlender Szenariobeleg')
        for first, second in zip(scenario['path'], scenario['path'][1:]):
            if second not in codes[first].get('requires', []):
                raise ValueError(f'{name}: unterbrochener Szenariopfad')
    for case in blueprint['ux_traceability']['cases'].values():
        if case['earliest_gate'] not in route['gates'] or any(code not in codes for code in case['codes']):
            raise ValueError('Ungültiger UX-/Gateverweis')
    return True


def main():
    route = render_todo.load_route(ROOT / 'governance/route.json')
    render_todo.resolve(route)
    data = yaml.load((ROOT / 'blueprint/architecture.yaml').read_text(), Loader=UniqueLoader)
    from blueprint_view import DOC as VIEW, build, render as render_view
    if not VIEW.exists() or VIEW.read_text() != render_view(build(data, route)):
        raise ValueError('Architekturansicht fehlt oder ist veraltet')
    from foundation import DOC, load, render
    if not DOC.exists() or DOC.read_text() != render(load()):
        raise ValueError('Grundlagenansicht fehlt oder ist veraltet')
    from contract_view import DOC as CONTRACT_DOC, build as build_contract, render as render_contract
    if not CONTRACT_DOC.exists() or CONTRACT_DOC.read_text() != render_contract(build_contract(data)):
        raise ValueError('Vertragsansicht fehlt oder ist veraltet')
    print('GOVERNANCE PASS: Blueprint, Evidenz und Gates geprüft; keine Freigabe erteilt.')


if __name__ == '__main__':
    main()
