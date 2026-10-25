#!/usr/bin/env python3
"""Derived design-contract and scenario report, never a runtime test certificate."""
import argparse
import json

import yaml

from check_governance import ROOT, UniqueLoader
from contract_rules import validate_contracts, validate_checker
from scenario_rules import validate_scenarios

DOC = ROOT / 'docs/VERTRAEGE_B007_B009.md'


def build(blueprint=None):
    if blueprint is None:
        blueprint = yaml.load((ROOT / 'blueprint/architecture.yaml').read_text(), Loader=UniqueLoader)
    validate_contracts(blueprint)
    validate_checker(blueprint)
    result = validate_scenarios(blueprint)
    return dict(result, contracts=blueprint['contracts'], checker=blueprint['checker_contract'],
                scenarios_detail=blueprint['scenarios'], codes=len(blueprint['codebook']),
                planned_files=len(blueprint['files']))


def render(result):
    contracts = result['contracts']
    lines = ['# Verträge, Szenarien und Prüfautomat B007–B009', '',
             '**Modell:** MODEL_CONTRACT_PASS. **Reale Browser-/DB-/Pluginausführung:** NOT_TESTED.',
             f"**Umfang:** {result['scenarios']} Szenarien, {result['cases']} Fälle, "
             f"{result['codes']} Codes und {result['planned_files']} Sollpfade – dynamisch ermittelt.", '',
             '## Daten und Versionen', '',
             'Nutzdaten bleiben außerhalb Git/Release. Legacyquellen werden ausschließlich gelesen.',
             'Dokumente, Notizen und Medien besitzen getrennte Speicher-/Rechtegrenzen.',
             'Versionsachsen sind unabhängig; eine kleine Änderung erhöht nicht automatisch alle Werte.', '',
             '| Achse | Geplanter Vertrag |', '|---|---|']
    lines += [f'| {key} | {value} |' for key, value in contracts['version_axes'].items()]
    lines += ['', '## Request- und Antwortfelder (Sollschema)', '',
              'Die Beispiele werden gegen den verwendeten JSON-Schema-Teilumfang geprüft.',
              'Das ist keine implementierte Endpunktvalidierung oder Speicherbestätigung.', '',
              '| Schema | Pflichtfelder und Typen |', '|---|---|']
    for name, schema in contracts['payloads'].items():
        fields = ', '.join(key + ': ' + schema['properties'][key]['type'] for key in schema['required'])
        lines.append(f'| {name} | {fields} |')
    lines += ['', '## API-Aktionen und Rechte', '', '| API | Aktion / Capability |', '|---|---|']
    for code, actions in contracts['api_capabilities'].items():
        lines.append(f"| {code} | {', '.join(key + ': ' + value for key, value in actions.items())} |")
    lines += ['', '## Notizen und Fehlerhilfe', '',
              'Gleiche Request-ID mit gleichem Inhalt: dieselbe Bestätigung, kein zweiter Schreibakt.',
              'Gleiche ID mit anderem Inhalt: Konflikt, keine Mutation. Erfolg erst nach dauerhaftem Schreiben.',
              'Zeit, Appversion und Buildkennung stammen vom Server. Clientseitige Versionsfelder werden abgelehnt.',
              f"Grenzen: {contracts['payloads']['note_request']['properties']['text']['maxLength']} Textzeichen und {contracts['note_semantics']['max_request_bytes']} Notiz-Request-Bytes; Entwurf bei Fehler erhalten.",
              f"HTTP-Gesamtgrenze: {contracts['http_boundary']['max_request_bytes']} Bytes; engere Endpointbudgets stehen im Blueprint.",
              'note_id im Datensatz entspricht der validierten Request-ID. Die bisherige TXT-Feldstruktur bleibt erhalten.',
              'Fehler nennen Code, verständliche Meldung, Korrelation, Wiederholbarkeit und nächste Korrektur.', '',
              '## Capabilities und Vertrauen', '',
              'Standard und unbekannte Fähigkeiten: DENY. Katalogmetadaten erteilen keine Ausführungsrechte.',
              ', '.join(contracts['permissions']['capabilities']), '',
              '| Vertrauensstufe | Geplanter Zugriff |', '|---|---|']
    lines += [f'| {key} | {value} |' for key, value in contracts['permissions']['trust_levels'].items()]
    lines += ['', '## Szenariofälle (modelliert)', '',
              'Die ursprünglichen drei und fünf ergänzenden Wege sind erhalten. Hinzu kommt der Notiz-ID-Konflikt.',
              'Jeder Weg besitzt mindestens vier Fälle, positive/negative Erwartungen und erreichbare Schutzpunkte.',
              'Vorstartprüfungen von LBOOT sind als guard_contracts deklariert, keine versteckten Laufzeitimporte.', '',
              '<details><summary>Alle geplanten Fälle anzeigen</summary>', '',
              '| Szenario / Fall | Art | Eingabe → erwartetes Verhalten |', '|---|---|---|']
    for name, scenario in result['scenarios_detail'].items():
        for case in scenario['simulation_cases']:
            lines.append(f"| {name} / {case['id']} | {case['kind']} | {case['input']} → {case['expected']} |")
    lines += ['', '</details>', '', '## Prüfautomat und Grenzen', '',
              'Bestehende Werkzeuge unter assist.py ausführen; keine zweite Prüfarchitektur.',
              'Die folgenden Phasen benennen feste Prüfdimensionen, keine ausführbare Planungssprache:',
              ', '.join(result['checker']['phases']), '',
              'Inputs sind Blueprint, Route, Regressionen, tatsächlicher Dateibestand und erreichbare Git-Historie.',
              'Outputs sind Modellresultat, dynamische Zählwerte, abgeleitete Ansichten und lokaler Laufbeleg.',
              'Bei Fehler FAIL und Abbruch. Keine Quellcode-Selbstreparatur und kein ungeprüfter PASS-Cache.',
              'Nur bekannte Ansichten dürfen bei --refresh neu erzeugt werden; Berichte liegen in work/.',
              'Die ausdrücklich stabilen 112 Haupt-IDs und 13 Gates bleiben geschützt; sonst keine festen Katalogzahlen.',
              'G-1/G0 und spätere Produktabnahmen werden durch diese Modellprüfung nicht freigegeben.', '']
    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    parser.add_argument('--json', action='store_true')
    args = parser.parse_args()
    result = build()
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    elif args.check:
        if not DOC.exists() or DOC.read_text() != render(result):
            raise SystemExit('STALE: Vertragsansicht mit assist.py --refresh aktualisieren')
        print('CONTRACT VIEW PASS; RUNTIME NOT_TESTED')
    else:
        DOC.write_text(render(result), encoding='utf-8')
        print('CONTRACT VIEW GENERATED')


if __name__ == '__main__':
    main()
