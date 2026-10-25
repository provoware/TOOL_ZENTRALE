#!/usr/bin/env python3
"""Local/CI checks and evidence."""
import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import subprocess
import sys
import unittest

import regression_registry as registry
import render_todo
from run_evidence import context, learning_candidates, report_valid

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / 'work/regression/latest.json'


def test_selection_valid(names):
    loader = unittest.TestLoader()
    for name in names:
        suite = loader.loadTestsFromName(name)
        if not suite.countTestCases() or loader.errors:
            return False
    return True


def run_check(check_id, arguments, cwd=ROOT):
    print(f'Prüfe: {check_id}', flush=True)
    try:
        run = subprocess.run([sys.executable, *arguments], cwd=cwd,
                             env=dict(os.environ, PYTHONDONTWRITEBYTECODE='1'),
                             timeout=120, check=False)
        code = run.returncode
    except subprocess.TimeoutExpired:
        code = 124
    return {'id': check_id, 'result': 'PASS' if code == 0 else 'FAIL', 'returncode': code}


def write_report(report):
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    temporary = REPORT.with_suffix('.tmp')
    temporary.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    temporary.replace(REPORT)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--changed', action='append', default=[], help='Repo-relativer Änderungspfad')
    parser.add_argument('--refresh', action='store_true', help='Nur bekannte Ansichten neu erzeugen')
    parser.add_argument('--verify-report', action='store_true', help='Vorigen Lauf auf Aktualität prüfen')
    args = parser.parse_args()
    if args.verify_report:
        if args.refresh or args.changed:
            parser.error('--verify-report wird allein verwendet')
        try:
            previous = json.loads(REPORT.read_text())
            if not isinstance(previous, dict):
                raise ValueError('Bericht ist kein Objekt')
            changed = previous.get('changed_paths')
            if not isinstance(changed, list) or any(not isinstance(p, str) for p in changed):
                raise ValueError('Ungültiger Prüfumfang')
            selected = registry.select_tests(registry.load_registry(), changed)
            expected = ['regression-info', 'render_todo.py', 'project_state.py', 'governance-contract']
            expected += ['development-suite'] if selected is None else selected
            valid = report_valid(previous, context(ROOT), expected)
        except (OSError, ValueError, KeyError):
            valid = False
        print('EVIDENCE PASS' if valid else 'EVIDENCE FAIL/STALE: Hilfe erneut ausführen.')
        return 0 if valid else 1
    try:
        data = registry.load_registry()
        all_ids = sorted({name for entry in data['families'] for name in entry['test_ids']})
        if not test_selection_valid(all_ids):
            raise ValueError('Registrierte Test-ID nicht auffindbar')
        guide = registry.render_info(data)
        if args.refresh:
            registry.INFO.write_text(guide, encoding='utf-8')
            for script in ('foundation.py', 'contract_view.py', 'blueprint_view.py', 'render_todo.py', 'project_state.py'):
                if run_check('refresh:' + script, ['scripts/' + script])['result'] != 'PASS':
                    raise ValueError('Aktualisierung fehlgeschlagen: ' + script)
        selected = registry.select_tests(data, args.changed)
        before = context(ROOT)
        checks = [{'id': 'regression-info', 'result': 'PASS' if registry.INFO.exists()
                   and registry.INFO.read_text(encoding='utf-8') == guide else 'FAIL',
                   'returncode': 0 if registry.INFO.exists()
                   and registry.INFO.read_text(encoding='utf-8') == guide else 1}]
        for script in ('render_todo.py', 'project_state.py'):
            checks.append(run_check(script, ['scripts/' + script, '--check']))
        checks.append(run_check('governance-contract', ['scripts/check_governance.py']))
        if selected is None:
            print('Testauswahl: vollständige vorhandene Entwicklungssuite.', flush=True)
            checks.append(run_check('development-suite',
                                    ['-m', 'unittest', 'discover', '-s', 'scripts', '-p', 'test_*.py']))
        else:
            print(f'Testauswahl: {len(selected)} zugeordnete Schutzfälle.', flush=True)
            for name in selected:
                checks.append(run_check(name, ['-m', 'unittest', name], ROOT / 'scripts'))
        after = context(ROOT)
        if before != after:
            checks.append({'id': 'content-changed-during-run', 'result': 'FAIL', 'returncode': 1})
        try:
            previous = json.loads(REPORT.read_text())
            if not isinstance(previous, dict):
                previous = {}
        except (OSError, ValueError):
            previous = {}
        report = {'schema': 'provoware-check-run/1',
                  'created_at': datetime.now(timezone.utc).isoformat(),
                  'context': before, 'context_after': after, 'changed_paths': args.changed,
                  'checks': checks, 'result': 'PASS' if all(c['result'] == 'PASS' for c in checks) else 'FAIL',
                  'candidates': learning_candidates(checks, previous)}
        write_report(report)
        print(f"Ergebnis: {report['result']}. Bericht: work/regression/latest.json")
        route = render_todo.load_route(ROOT / 'governance/route.json')
        print('Nächste Schritte (bedingt): ' + ', '.join(render_todo.next_three(route, render_todo.resolve(route))))
        if report['result'] != 'PASS':
            print('Hilfe: bei veralteter Ansicht --refresh; bei Testfehler zuerst Ursache reproduzieren.')
        return 0 if report['result'] == 'PASS' else 1
    except (OSError, ValueError, KeyError, TypeError) as error:
        blocked = {'schema': 'provoware-check-run/1',
                   'created_at': datetime.now(timezone.utc).isoformat(),
                   'result': 'FAIL', 'phase': 'BLOCKED', 'context': None, 'context_after': None,
                   'changed_paths': args.changed,
                   'checks': [{'id': 'validation-or-refresh', 'result': 'FAIL', 'returncode': 1}],
                   'candidates': []}
        try:
            write_report(blocked)
        except OSError:
            print('FAIL-Bericht konnte nicht gespeichert werden.', file=sys.stderr)
        print(f'HILFE BLOCKIERT: {error}. Register/Dateien prüfen; keine Freigabe.', file=sys.stderr)
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
