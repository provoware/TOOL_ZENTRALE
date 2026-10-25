"""Bind local check results to exact content and runtime; no gate authority."""
import hashlib
import json
import platform
import subprocess
import sys

from project_state import snapshot


def fingerprint(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, ensure_ascii=False,
                                     separators=(',', ':')).encode()).hexdigest()


def context(root):
    files = snapshot(root)['files']
    by_path = {item['path']: item['sha256'] for item in files}
    generated = {}
    for name in ('governance/file_state.json', 'docs/STATUS_KURZ.md'):
        path = root / name
        generated[name] = hashlib.sha256(path.read_bytes()).hexdigest() if path.is_file() else None
    return {'source_sha': subprocess.check_output(
                ['git', 'rev-parse', 'HEAD'], cwd=root, text=True).strip(),
            'content_sha256': fingerprint(files), 'generated_sha256': generated,
            'plan_sha256': by_path.get('governance/route.json'),
            'registry_sha256': by_path.get('governance/regressions.yaml'),
            'python': platform.python_version(),
            'implementation': platform.python_implementation(), 'platform': sys.platform}


def report_valid(report, current, expected_ids):
    if not isinstance(report, dict) or report.get('schema') != 'provoware-check-run/1':
        return False
    checks = report.get('checks')
    if not isinstance(checks, list) or not all(isinstance(c, dict) for c in checks):
        return False
    ids = [check.get('id') for check in checks]
    if any(not isinstance(item, str) for item in ids) or sorted(ids) != sorted(expected_ids):
        return False
    return (report.get('context') == current and report.get('context_after') == current
            and isinstance(checks, list) and bool(checks)
            and all(isinstance(check, dict) and check.get('result') == 'PASS'
                    and type(check.get('returncode')) is int and check['returncode'] == 0
                    for check in checks)
            and report.get('result') == 'PASS')


def learning_candidates(checks, previous):
    history = previous.get('candidates', []) if isinstance(previous, dict) else []
    if not isinstance(history, list):
        history = []
    observations = {}
    for item in history[-100:]:
        if (isinstance(item, dict) and isinstance(item.get('signature'), str)
                and isinstance(item.get('check_id'), str)
                and type(item.get('occurrences')) is int and item['occurrences'] > 0):
            observations[item['signature']] = {
                key: item[key] for key in ('signature', 'check_id', 'occurrences')}
    for check in checks:
        if check['result'] == 'PASS':
            continue
        signature = fingerprint({'id': check['id'], 'returncode': check['returncode']})
        before = observations.get(signature, {}).get('occurrences', 0)
        observations[signature] = {'signature': signature, 'check_id': check['id'],
                                   'occurrences': before + 1}
    return [dict(item, state='NEEDS_REPRODUCTION',
                 next_action='Ursache reproduzieren und Schutztest im Register zuordnen.')
            for item in list(observations.values())[-100:]]
