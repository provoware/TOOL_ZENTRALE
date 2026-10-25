#!/usr/bin/env python3
"""Local/CI checks and evidence."""
import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import unittest
import urllib.request

import regression_registry as registry
import render_todo
from run_evidence import context, learning_candidates, report_valid

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / 'work/regression/latest.json'
START_REPORT = ROOT / 'work/iteration/start.json'
GITHUB_API = 'https://api.github.com/repos/provoware/TOOL_ZENTRALE'
MAIN_WORKFLOW = '.github/workflows/todo-check.yml'


def github_json(path):
    headers = {'Accept': 'application/vnd.github+json', 'User-Agent': 'PROVOWARE-preflight'}
    token = os.environ.get('GH_TOKEN') or os.environ.get('GITHUB_TOKEN')
    if token:
        headers['Authorization'] = 'Bearer ' + token
    with urllib.request.urlopen(urllib.request.Request(GITHUB_API + path, headers=headers), timeout=12) as response:
        return json.load(response)


def git_value(*args):
    return subprocess.check_output(['git', *args], cwd=ROOT, text=True).strip()


def decide_preflight(local, sha, pulls, runs):
    blockers = []
    if not local['origin_valid']:
        blockers.append('Falsches oder unbekanntes origin-Repository')
    if local['branch'] != 'main':
        blockers.append('Lokaler Checkout ist nicht main')
    if not local['clean']:
        blockers.append('Lokale Reständerungen müssen geprüft werden')
    if local['pending_branches']:
        blockers.append('Nicht integrierte lokale Branches benötigen Prüfung')
    if local['stash_count']:
        blockers.append('Lokale Stashes benötigen Prüfung')
    if local['head'] != sha:
        blockers.append('Lokaler HEAD weicht von aktuellem GitHub-Main ab')
    if pulls:
        blockers.append('Offene Pull Requests benötigen eine Integrationsprüfung')
    if len(pulls) == 100:
        blockers.append('PR-Liste möglicherweise unvollständig (Pagination)')
    matching = [run for run in runs if isinstance(run, dict)
                and run.get('path') == MAIN_WORKFLOW and run.get('event') == 'push'
                and run.get('head_sha') == sha]
    matching.sort(key=lambda run: (run.get('created_at') or '', run.get('run_attempt') or 0),
                  reverse=True)
    latest = matching[0] if matching else {}
    if latest.get('status') != 'completed' or latest.get('conclusion') != 'success':
        blockers.append('Aktueller Main-Push-CI-Erfolg nicht nachgewiesen')
    return {'schema': 'provoware-iteration-start/1',
            'checked_at_utc': datetime.now(timezone.utc).isoformat(),
            'main_sha': sha, 'local_head': local['head'], 'branch': local['branch'],
            'worktree_clean_at_start': local['clean'],
            'pending_local_branches': local['pending_branches'],
            'stash_count': local['stash_count'],
            'open_prs': [p['number'] for p in pulls],
            'transferable_parts': [], 'integrated_prs': [],
            'blocked_parts': [{'reason': reason} for reason in blockers],
            'main_ci': {'run_id': latest.get('id'),
                        'conclusion': latest.get('conclusion') or 'UNKNOWN',
                        'url': latest.get('html_url')},
            'result': 'BLOCKED' if blockers else 'MAIN_VERIFIED',
            'planning_allowed': not bool(blockers)}


def main_preflight():
    """Fresh read-only remote checks; an incomplete response is never success."""
    try:
        origin = git_value('remote', 'get-url', 'origin').removesuffix('.git').rstrip('/')
        local = {'head': git_value('rev-parse', 'HEAD'),
                 'branch': git_value('branch', '--show-current'),
                 'clean': not bool(git_value('status', '--porcelain')),
                 'pending_branches': git_value('for-each-ref', '--no-merged=refs/heads/main',
                                               '--format=%(refname:short)', 'refs/heads').splitlines(),
                 'stash_count': len(git_value('stash', 'list', '--format=%gd').splitlines()),
                 'origin_valid': origin in {'https://github.com/provoware/TOOL_ZENTRALE',
                                            'git@github.com:provoware/TOOL_ZENTRALE'}}
        branch = github_json('/branches/main')
        pulls = github_json('/pulls?state=open&per_page=100')
        runs = github_json('/actions/runs?branch=main&per_page=100')
        sha = branch.get('commit', {}).get('sha') if isinstance(branch, dict) else None
        if (not isinstance(sha, str) or not re.fullmatch(r'[0-9a-f]{40}', sha)
                or not isinstance(pulls, list)
                or not all(isinstance(p, dict) and type(p.get('number')) is int for p in pulls)
                or not isinstance(runs, dict) or not isinstance(runs.get('workflow_runs'), list)):
            raise ValueError('Unvollständige GitHub-Daten')
        report = decide_preflight(local, sha, pulls, runs['workflow_runs'])
    except (OSError, ValueError, KeyError, subprocess.CalledProcessError):
        report = {'schema': 'provoware-iteration-start/1',
                  'checked_at_utc': datetime.now(timezone.utc).isoformat(),
                  'main_sha': None, 'local_head': None, 'worktree_clean_at_start': None,
                  'open_prs': [], 'transferable_parts': [], 'integrated_prs': [],
                  'blocked_parts': [{'reason': 'Git-/GitHub-Abfrage nicht vollständig'}],
                  'main_ci': {'conclusion': 'UNKNOWN'},
                  'result': 'BLOCKED', 'planning_allowed': False}
    START_REPORT.parent.mkdir(parents=True, exist_ok=True)
    temp = START_REPORT.with_suffix('.tmp')
    temp.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    temp.replace(START_REPORT)
    print('MAIN-VORPRÜFUNG: ' + report['result'])
    for item in report['blocked_parts']:
        print('BLOCKER: ' + item['reason'])
    return 0 if report['planning_allowed'] else 1


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
    parser.add_argument('--main-preflight', action='store_true', help='Main/PR/CI vor neuer Planung lesen')
    args = parser.parse_args()
    if args.main_preflight:
        if args.refresh or args.changed or args.verify_report:
            parser.error('--main-preflight wird allein verwendet')
        return main_preflight()
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
