"""Reject unbound, stale or incomplete step and gate records."""
import importlib.metadata
import hashlib
import json
import platform
import re
import subprocess
from pathlib import Path

from plan_contract import fingerprint, plan_fingerprint


def safe_file(root, name):
    if not isinstance(name, str) or not name or Path(name).is_absolute() or '..' in Path(name).parts:
        raise ValueError('Ungültiger Evidenzpfad')
    path = root / name
    if path.resolve() != path.absolute() or not path.is_file():
        raise ValueError('Evidenzpfad fehlt oder enthält Symlink')
    return path


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def step_node(route, sid):
    nodes = dict(route['steps'])
    nodes.update({item['id']: item for item in route.get('iteration_queue', [])})
    for parent in route['steps'].values():
        for sub in parent.get('substeps', []):
            nodes[sub['id']] = dict(parent, **sub)
    return nodes.get(sid, {})


def completion_checks(route, sid):
    node = step_node(route, sid)
    extra = node.get('completion_checks', [])
    if not isinstance(extra, list) or any(not isinstance(c, str) for c in extra):
        raise ValueError('Ungültige Schrittprüfungen')
    base = route['completion_policy']['required_checks']
    if sid.startswith('P') and node.get('patch') != 'PLAN' and not any(c not in base for c in extra):
        raise ValueError(f'{sid}: reale Produktprüfungen fehlen')
    return base + extra


def step_inputs(route, sid):
    inputs = step_node(route, sid).get('completion_inputs')
    if not isinstance(inputs, list) or not inputs or len(inputs) != len(set(inputs)):
        raise ValueError(f'{sid}: expliziter Prüfscope fehlt')
    if any(not isinstance(name, str) or name.startswith(('governance/evidence/', 'work/'))
           or name in {'governance/route.json', 'governance/file_state.json', 'docs/TODO_V3_2.md',
                       'docs/STATUS_KURZ.md', 'docs/assets/todo_progress.svg'} for name in inputs):
        raise ValueError(f'{sid}: Verwaltungsdatei im Prüfscope')
    return sorted(inputs)


def record_valid(entry, route, sid, root):
    try:
        if not isinstance(entry, dict) or not entry.get('record', '').startswith('governance/evidence/'):
            return False
        path = safe_file(root, entry['record'])
        if digest(path) != entry.get('sha256'):
            return False
        record = json.loads(path.read_text())
        if (record['schema'] != 'provoware-completion/1' or record['step_id'] != sid
                or record['plan_sha256'] != plan_fingerprint(route)):
            return False
        report = record['report']
        ctx = report['context']
        if (report['schema'] != 'provoware-check-run/1' or report['result'] != 'PASS'
                or report['context_after'] != ctx or report.get('changed_paths') != []
                or ctx['plan_contract_sha256'] != record['plan_sha256']):
            return False
        checks = report['checks']
        expected = completion_checks(route, sid)
        if not expected or len(expected) != len(set(expected)):
            return False
        if (sorted(check['id'] for check in checks) != sorted(expected)
                or any(c['result'] != 'PASS' or type(c['returncode']) is not int
                       or c['returncode'] != 0 for c in checks)):
            return False
        manifest = ctx['file_manifest']
        if fingerprint(manifest) != ctx['content_sha256']:
            return False
        files = {item['path']: item['sha256'] for item in manifest}
        inputs = step_inputs(route, sid)
        if record['inputs'] != {name: files.get(name) for name in inputs}:
            return False
        if any(not files.get(name) or digest(safe_file(root, name)) != files[name] for name in inputs):
            return False
        if (ctx['implementation'] != platform.python_implementation()
                or '.'.join(ctx['python'].split('.')[:2]) != '.'.join(platform.python_version().split('.')[:2])
                or ctx.get('dependencies') != {'PyYAML': importlib.metadata.version('PyYAML')}):
            return False
        sha = ctx['source_sha']
        if not isinstance(sha, str) or not re.fullmatch(r'[0-9a-f]{40}', sha):
            return False
        return subprocess.run(['git', 'merge-base', '--is-ancestor', sha, 'HEAD'],
                              cwd=root, capture_output=True).returncode == 0
    except (OSError, ValueError, KeyError, TypeError, AttributeError):
        return False

