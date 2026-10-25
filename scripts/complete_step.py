#!/usr/bin/env python3
"""Attach exact passing scope evidence; never approves gates."""
import argparse
import copy
import json
import os
import re
import tempfile
from pathlib import Path

import render_todo
from completion_contract import completion_checks, digest, step_inputs
from plan_contract import plan_fingerprint
from run_evidence import context, report_valid

ROOT = Path(__file__).resolve().parents[1]


def build_record(route, sid, report, root):
    if not report_valid(report, context(root), completion_checks(route, sid)):
        raise ValueError('Abschluss benötigt aktuellen vollständigen PASS-Lauf')
    if report.get('changed_paths') != []:
        raise ValueError('Gezielter Lauf genügt nicht als Abschlussbeleg')
    inputs = step_inputs(route, sid)
    manifest = {item['path']: item['sha256'] for item in report['context']['file_manifest']}
    if any(name not in manifest for name in inputs):
        raise ValueError('Prüfgegenstand fehlt im Laufmanifest')
    return {'schema': 'provoware-completion/1', 'step_id': sid,
            'subject_kind': 'base_commit_plus_tested_worktree_scope',
            'plan_sha256': plan_fingerprint(route),
            'inputs': {name: manifest[name] for name in inputs}, 'report': report}


def output_path(root, sid):
    if not isinstance(sid, str) or not re.fullmatch(r'[A-Z][A-Z0-9]*(?:\.[0-9]+)?', sid):
        raise ValueError('Unsichere Abschluss-ID')
    path = root / 'governance/evidence' / (sid + '.json')
    if path.resolve() != path.absolute() or path.is_symlink() or (path.exists() and not path.is_file()):
        raise ValueError('Abschlussziel enthält Symlink oder unzulässigen Dateityp')
    return path


def atomic_write(path, content):
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(dir=path.parent, delete=False) as stream:
            temporary = Path(stream.name)
            stream.write(content)
            stream.flush()
            os.fsync(stream.fileno())
        if path.is_symlink():
            raise ValueError('Schreibziel wurde durch Symlink ersetzt')
        os.replace(temporary, path)
    finally:
        if temporary and temporary.exists():
            temporary.unlink()


def apply_completion(route, ids, report, root):
    if len(ids) != len(set(ids)):
        raise ValueError('Doppelte Abschluss-ID')
    targets = {sid: output_path(root, sid) for sid in ids}  # all paths before first mutation
    route_path = root / 'governance/route.json'
    if route_path.resolve() != route_path.absolute() or route_path.is_symlink():
        raise ValueError('Unsicheres Routenziel')
    records = {sid: build_record(route, sid, report, root) for sid in ids}
    updated = copy.deepcopy(route)
    old = {path: path.read_bytes() if path.exists() else None for path in targets.values()}
    try:
        for sid, path in targets.items():
            path.parent.mkdir(parents=True, exist_ok=True)
            atomic_write(path, (json.dumps(records[sid], ensure_ascii=False, indent=2) + '\n').encode())
            updated['evidence_by_step'][sid] = {
                'record': path.relative_to(root).as_posix(), 'sha256': digest(path)}
            queued = next((item for item in updated.get('iteration_queue', []) if item['id'] == sid), None)
            if queued:
                queued['status'] = 'VERIFIED'
            else:
                updated['progress_overrides'][sid] = 'VERIFIED'
        render_todo.resolve(updated)
        atomic_write(route_path, (json.dumps(updated, ensure_ascii=False, indent=2) + '\n').encode())
    except Exception:
        for path, content in old.items():
            if content is None:
                path.unlink(missing_ok=True)
            else:
                atomic_write(path, content)
        raise
    return updated


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('step_id', nargs='+', help='Eine oder mehrere abhängige Schritt-IDs')
    args = parser.parse_args()
    try:
        route = render_todo.load_route(ROOT / 'governance/route.json')
        report = json.loads((ROOT / 'work/regression/latest.json').read_text())
        apply_completion(route, args.step_id, report, ROOT)
    except (OSError, ValueError, KeyError, TypeError) as error:
        print(f'Abschluss blockiert: {error}. Vollständig prüfen; keine Gatefreigabe.')
        return 1
    print('VERIFIED: ' + ', '.join(args.step_id) + '. Ansichten mit assist.py --refresh erneuern.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
