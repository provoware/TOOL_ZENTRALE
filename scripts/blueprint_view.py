#!/usr/bin/env python3
"""Read-only catalog reconciliation and derived semantic code legend."""
import argparse
import json
from pathlib import Path

import yaml

from blueprint_contract import historical_codes, validate_model
from check_governance import ROOT, UniqueLoader, validate_blueprint
from project_state import INDEX, STATUS, snapshot
from render_todo import load_route

DOC = ROOT / 'docs/ARCHITEKTUR_B004_B006.md'


def audit(blueprint, actual, history, route):
    validate_blueprint(blueprint, route)
    coverage = validate_model(blueprint, history)
    planned = set(blueprint['files'])
    unknown = sorted(set(actual) - planned)
    if unknown:
        raise ValueError('Vorhandene Dateien ohne Katalogeintrag: ' + ', '.join(unknown))
    inventory = [dict(item, path=path, presence='PRESENT' if path in actual else 'VIRTUAL')
                 for path, item in sorted(blueprint['files'].items())]
    legend = []
    for code, item in blueprint['codebook'].items():
        consumers = sorted(other for other, value in blueprint['codebook'].items()
                           if code in value.get('requires', []))
        legend.append(dict(code=code, **item, consumers=consumers,
                           planned_tests=coverage[code]))
    return {'schema': 'provoware-blueprint-audit/1', 'evidence_kind': 'MODEL_AND_INVENTORY_ONLY',
            'inventory': inventory, 'code_legend': legend, 'layers': blueprint['layers'],
            'present': len(actual), 'virtual': len(planned - set(actual)),
            'historical_reserved_codes': len(history)}


def build(blueprint=None, route=None):
    blueprint = blueprint if blueprint is not None else yaml.load((ROOT / 'blueprint/architecture.yaml').read_text(), Loader=UniqueLoader)
    route = route if route is not None else load_route(ROOT / 'governance/route.json')
    actual = {entry['path'] for entry in snapshot(ROOT)['files']}
    actual.update(name for name in (INDEX, STATUS) if (ROOT / name).is_file())
    # The current output is included; --check separately verifies its real existence.
    actual.add(DOC.relative_to(ROOT).as_posix())
    return audit(blueprint, actual, historical_codes(ROOT), route)


def render(result):
    lines = ['# Schichten, Dateikatalog und Codelegende B004–B006', '',
             '**Nachweis:** statisches Modell und tatsächlicher Dateibestand; keine Produktprüfung.',
             f"**Bestand:** {result['present']} vorhanden, {result['virtual']} nur geplant; "
             f"{len(result['code_legend'])} Codes.", '',
             'PRESENT bedeutet vorhandene Datei, nicht implementierte oder geprüfte Produktfunktion.',
             'VIRTUAL bedeutet nur Sollpfad. Es werden keine Produktstubs angelegt.',
             'Die eigene erzeugte Ansicht ist eingerechnet; --check prüft ihre Existenz und Aktualität.', '',
             '## Schichten und Grenzen', '',
             'Domain bleibt unabhängig von API, UI und Speicherimplementierung. UI kennt nur UI/API.',
             'Core importiert keine Fachmodulinterna. Pluginpfade benötigen den Capability-Vertrag.',
             'Laufzeitabhängigkeiten und Prüfbeziehungen sind getrennt; Zyklen sind unzulässig.',
             'Diese Regeln gelten für den geplanten Graphen. Reale Import-/Browserprüfung folgt mit Produktcode.', '',
             '| Schicht | Verantwortung | Darf nutzen | Erlaubte Verbraucher |', '|---|---|---|---|']
    for name, layer in result['layers'].items():
        users = [other for other, value in result['layers'].items() if name in value['may_depend_on']]
        lines.append(f"| {name} | {layer['responsibility']} | {', '.join(layer['may_depend_on']) or '—'} | {', '.join(users) or '—'} |")
    lines += ['', '<details><summary>Vollständigen Dateikatalog anzeigen</summary>', '', '## Dateiabgleich', '',
              '| Pfad | Ist | Besitzer | Stabilität | Katalog |', '|---|---|---|---|---|']
    for item in result['inventory']:
        lines.append(f"| `{item['path']}` | {item['presence']} | {item['owner']} | {item['stability']} | {item['catalog']} |")
    lines += ['', '</details>', '', '<details><summary>Vollständige Codelegende anzeigen</summary>', '',
              '## Semantische Codelegende (geplante Schnittstellen)', '',
              '| Code / Name | Pfad / Schicht | Schnittstelle | Verbraucher | Geplante Tests |',
              '|---|---|---|---|---|']
    for item in result['code_legend']:
        tests = ', '.join(item['planned_tests']) if item['layer'] != 'QA' else 'Prüfvertrag: ' + ', '.join(item['verifies'])
        lines.append(f"| {item['code']} / {item['label']} | `{item['path']}` / {item['layer']} | "
                     f"{item['interface']} | {', '.join(item['consumers']) or '—'} | {tests} |")
    lines += ['', '</details>', '', '## Einordnung und Pflege', '',
              'Verbraucher und Testzuordnungen sind aus requires/verifies abgeleitet, keine zweite Codequelle.',
              'Die transitive Testzuordnung ist ein Planbezug, kein Nachweis tatsächlicher Testausführung.',
              'Historische IDs bleiben aus der vollständigen Git-Historie gesperrt; keine manuelle Schattenliste.',
              'KTXT erhielt den fehlenden geplanten Prüfvertrag TTXT. Der Testpfad bleibt VIRTUAL.',
              'Quellen: blueprint/architecture.yaml, Git und der bestehende File-State-Snapshot.',
              'Aktualisieren: assist.py --refresh. Maschinenansicht ohne zusätzliche Datei: blueprint_view.py --json.',
              'G-1/G0 bleiben ohne separate menschliche Entscheidungsakte offen.', '']
    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    parser.add_argument('--json', action='store_true', help='Abgeleiteten Maschinenbericht ausgeben')
    args = parser.parse_args()
    result = build()
    text = render(result)
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    elif args.check:
        if not DOC.exists() or DOC.read_text() != text:
            raise SystemExit('STALE: Architekturansicht mit assist.py --refresh aktualisieren')
        print('BLUEPRINT VIEW PASS')
    else:
        DOC.write_text(text, encoding='utf-8')
        print('BLUEPRINT VIEW GENERATED')


if __name__ == '__main__':
    main()
