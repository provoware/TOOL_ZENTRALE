"""Validate JSON-compatible YAML and derive the beginner regression guide."""
import fnmatch
import json
import re
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / 'governance/regressions.yaml'
INFO = ROOT / 'docs/REGRESSION_INFO.md'


def load_registry(path=REGISTRY):
    data = json.loads(path.read_text(encoding='utf-8'))
    if not isinstance(data, dict) or data.get('schema') != 'provoware-regressions/1':
        raise ValueError('Unbekanntes Regressionsschema')
    if not isinstance(data.get('families'), list):
        raise ValueError('Fehlerfamilien müssen eine Liste sein')
    ids = set()
    for entry in data['families']:
        if not isinstance(entry, dict):
            raise ValueError('Ungültiger Fehlerfamilieneintrag')
        rid = entry.get('id', '')
        if not re.fullmatch(r'RG[0-9]{3}', rid) or rid in ids:
            raise ValueError('Ungültige oder doppelte Regressions-ID')
        ids.add(rid)
        for field in ('title', 'symptom', 'cause', 'source', 'prevention', 'next_action'):
            if not isinstance(entry.get(field), str) or not entry[field].strip():
                raise ValueError(f'{rid}: {field} fehlt')
        if entry.get('kind') not in {'CONFIRMED', 'PREVENTIVE'}:
            raise ValueError(f'{rid}: ungültige Belegklasse')
        if entry.get('severity') not in {'HIGH', 'MEDIUM', 'LOW'}:
            raise ValueError(f'{rid}: ungültiger Schweregrad')
        for field in ('trigger_paths', 'test_ids'):
            if not isinstance(entry.get(field), list) or not entry[field]:
                raise ValueError(f'{rid}: {field} muss gefüllt sein')
        for pattern in entry['trigger_paths']:
            if (not isinstance(pattern, str) or not pattern or '\\' in pattern
                    or PurePosixPath(pattern).is_absolute() or '..' in pattern.split('/')):
                raise ValueError(f'{rid}: ungültiger Trigger')
        for test in entry['test_ids']:
            if not isinstance(test, str) or not re.fullmatch(
                    r'test_[a-z0-9_]+\.Test[A-Za-z0-9_]+\.test_[a-z0-9_]+', test):
                raise ValueError(f'{rid}: ungültige Test-ID')
            if not (ROOT / 'scripts' / (test.split('.')[0] + '.py')).is_file():
                raise ValueError(f'{rid}: Testmodul fehlt')
    if not ids:
        raise ValueError('Leeres Register')
    return data


def select_tests(data, changed):
    """Unknown or absent impact means full suite, represented by None."""
    if not changed:
        return None
    selected = set()
    for path in changed:
        matches = [entry for entry in data['families']
                   if any(fnmatch.fnmatchcase(path, pattern) for pattern in entry['trigger_paths'])]
        if not matches:
            return None
        for entry in matches:
            selected.update(entry['test_ids'])
    # Always exercise registry/runner safety when using targeted selection.
    return sorted(selected | {'test_assist.TestAssist.' + name for name in (
        'test_unknown_impact_expands_suite', 'test_missing_test_is_failure',
        'test_evidence_detects_content_and_toolchain_drift')})


def render_info(data):
    lines = ['# Lernende Regression und automatische Hilfe', '',
             '**Start:** `python3 scripts/assist.py` – prüft selbstständig und erklärt das Ergebnis.',
             '**Ansichten aktualisieren:** `python3 scripts/assist.py --refresh`.',
             'Mit `--changed scripts/render_todo.py` gezielt prüfen; unbekannte Pfade',
             'oder keine Pfadangabe erweitern auf alle vorhandenen Tests.', '',
             '## Was automatisch geschieht', '',
             '1. Register, Testzuordnung und Informationsdateien prüfen.',
             '2. Passende Tests ausführen; jeder Fehler, Timeout oder Inhaltswechsel verhindert PASS.',
             '3. Bericht und Lernkandidaten unter `work/regression/latest.json` speichern.',
             '4. Die drei nächsten bedingten Schritte aus der Route anzeigen.', '',
             'Push, Pull Request und manueller Workflowstart lösen dieselbe Hilfe in CI aus.',
             'Es läuft kein dauernder Hintergrunddienst. --refresh verändert ausschließlich',
             'die fünf bekannten abgeleiteten Ansichten, niemals Produktcode oder Nutzdaten.', '',
             '## Wie das System lernt', '',
             'Ein fehlgeschlagener Lauf erzeugt automatisch Kandidaten mit Prüf-ID und',
             'stabiler Signatur (Test-ID bei gezielter Auswahl, Suite-ID im Gesamtlauf).',
             'Wiederholungen werden gezählt, solange der lokale Bericht',
             'vorliegt (höchstens 100 Kandidaten, auch über erfolgreiche Folgeläufe hinweg).',
             'Es werden keine Rohfehlertexte oder Nutzinhalte in Git gespeichert.',
             'Ursache reproduzieren, Negativtest ergänzen, Trigger und Schutzregel prüfen,',
             'dann das führende Register gezielt erweitern. Keine ungeprüfte Selbstreparatur.',
             'Der Bericht ist lokaler Prüfbeleg, keine signierte Freigabe. Alte Ergebnisse',
             'sind bei verändertem Dateiinhalt, Plan oder Python-Kontext STALE.', '',
             'Prüfen: `python3 scripts/assist.py --verify-report` (führt keine Tests erneut aus).',
             'Ein frischer Bericht mit FAIL bleibt FAIL. Ein gültiger Bericht hebt weder',
             'Schrittstatus noch Gatefreigaben automatisch an; Q001 bleibt bis zur',
             'verbindlichen Einbindung in die Schritt-/Gateprüfung offen.', '',
             '## Registrierte Fehlerfamilien', '',
             '| ID | Klasse | Problem | Sichere nächste Hilfe |',
             '|---|---|---|---|']
    for entry in data['families']:
        lines.append(f"| {entry['id']} | {entry['kind']} | {entry['title']} | {entry['next_action']} |")
    lines += ['', '## Pflege und Grenzen', '',
              'Quelle: `governance/regressions.yaml` (JSON-kompatibles YAML, ohne Zusatzpaket).',
              'Diese Infodatei wird daraus erzeugt. CONFIRMED bezieht sich auf belegte',
              'Entwicklungsfehler, PREVENTIVE auf Schutzfälle; keine behaupteten Produktfehler.',
              'Die Hilfe prüft Entwicklungsartefakte. Browser, Datenbank, Barrierefreiheit',
              'und Offlineinstallation bleiben bis zur vorhandenen Anwendung NOT_TESTED.', '']
    return '\n'.join(lines)
