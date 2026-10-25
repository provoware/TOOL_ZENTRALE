#!/usr/bin/env python3
"""Rebuild content inventory and beginner status; --check never writes."""
import argparse
import hashlib
import json
import subprocess
from pathlib import Path

import render_todo

ROOT = Path(__file__).resolve().parents[1]
INDEX = 'governance/file_state.json'
STATUS = 'docs/STATUS_KURZ.md'


def snapshot(root):
    paths = subprocess.check_output(
        ['git', 'ls-files', '--cached', '--others', '--exclude-standard', '-z'],
        cwd=root).decode('utf-8').split('\0')
    records = []
    for name in sorted(set(paths) - {'', INDEX, STATUS}):
        if any(part in {'work', 'output', '__pycache__', '.pytest_cache'}
               for part in Path(name).parts) or name.endswith('.pyc'):
            continue
        path = root / name
        if path.is_symlink():
            raise ValueError(f'Symlink im registrierten Scope: {name}')
        if not path.is_file():
            continue  # Deleted tracked paths disappear from the next snapshot.
        content = path.read_bytes()
        records.append({'path': name, 'sha256': hashlib.sha256(content).hexdigest(),
                        'bytes': len(content), 'state': 'PRESENT_HASHED'})
    return {'schema': 'provoware-file-state/1',
            'meaning': 'content_snapshot_not_test_or_gate_evidence',
            'excluded_generated': [INDEX, STATUS], 'files': records}


def short_status(route):
    actual = render_todo.resolve(route)
    ids = render_todo.next_three(route, actual)
    entries = dict(route['steps'])
    entries.update({item['id']: item for item in route.get('iteration_queue', [])})
    done = sum(actual[sid] for sid in route['steps'])
    lines = ['# Projektstatus', '',
             '**Phase:** Planung; noch keine startbare Anwendung.',
             f'**Belegt abgeschlossen:** {done}/112 Hauptschritte ({done * 100 // 112} %).',
             f"**Planstatus:** `{route['plan_status']}`; keine automatische Freigabe.", '',
             '## Nächste drei Schritte', '',
             'Bedingte Vorschau: jeder Folgeschritt setzt den Erfolg seiner Vorgänger',
             'und die erforderliche Freigabe voraus. Keine Ausführungszusage.', '']
    lines += [f"{n}. **{sid}:** {entries[sid]['title']}"
              for n, sid in enumerate(ids, 1)]
    if len(ids) < 3:
        lines += ['', 'Weniger als drei zulässige Vorschaupunkte: Blocker oder Routenende prüfen.']
    lines += ['', '## So geht es weiter', '',
              'Entwicklungsregeln: [Arbeitsweise](ARBEITSWEISE.md).',
              'Details: [TODO](TODO_V3_2.md); Befunde: [Audit](AUDIT_2026_10_25.md).',
              'Dateihashes: [maschinenlesbares Register](../governance/file_state.json).',
              'Vorhanden/gehasht bedeutet nicht funktionsgeprüft.', '',
              'Erzeugt mit `python3 scripts/project_state.py`; nicht manuell bearbeiten.', '']
    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    route = render_todo.load_route(ROOT / 'governance/route.json')
    targets = {INDEX: json.dumps(snapshot(ROOT), ensure_ascii=False, indent=2) + '\n',
               STATUS: short_status(route)}
    stale = [name for name, value in targets.items()
             if not (ROOT / name).exists() or (ROOT / name).read_text(encoding='utf-8') != value]
    if args.check and stale:
        raise SystemExit('STALE: ' + ', '.join(stale) + ' – project_state.py ausführen')
    if not args.check:
        for name, value in targets.items():
            (ROOT / name).write_text(value, encoding='utf-8')
    print('STATE CHECK PASS' if args.check else 'STATE GENERATED')


if __name__ == '__main__':
    main()
