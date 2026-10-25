"""Validate and render the first three blueprint decisions from inspected sources."""
import json
from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'governance/foundation.json'
DOC = ROOT / 'docs/GRUNDLAGE_B001_B003.md'


def validate(data, blueprint, route, remote):
    if data.get('schema') != 'provoware-foundation/1':
        raise ValueError('Unbekanntes Grundlagenschema')
    repo = blueprint['target_repository']
    identity = blueprint['identity']
    if (repo != 'provoware/TOOL_ZENTRALE' or identity['repository_slug'] != 'TOOL_ZENTRALE'
            or identity['git_root'] != 'PROVOWARE/TOOL_ZENTRALE/'
            or remote.removesuffix('.git') != 'https://github.com/' + repo):
        raise ValueError('Repositoryidentität oder Remote widersprüchlich')
    ref = data['reference']
    if (ref['repository'] != blueprint['reference_repo'].removeprefix('https://github.com/')
            or ref['commit'] != blueprint['reference_commit']
            or not re.fullmatch(r'[0-9a-f]{40}', ref['commit']) or ref['truncated'] is not False):
        raise ValueError('Referenzstand unvollständig')
    sources = {entry['id']: entry for entry in ref['files']}
    if len(sources) != len(ref['files']):
        raise ValueError('Doppelte Quell-ID')
    for source in sources.values():
        path = source['path']
        prefix = f"https://github.com/{ref['repository']}/blob/{ref['commit']}/"
        if (Path(path).is_absolute() or '..' in Path(path).parts
                or source['url'] != prefix + path
                or not re.fullmatch(r'[0-9a-f]{40}', source['blob_sha'])
                or not re.fullmatch(r'[0-9a-f]{64}', source['sha256'])):
            raise ValueError('Quellbeleg nicht unveränderlich gebunden')
    covered, ids = set(), set()
    for case in data['use_cases']:
        if case['id'] in ids:
            raise ValueError('Doppelte Nutzungsfall-ID')
        ids.add(case['id'])
        if (case.get('target_status') != 'PLANNED'
                or case.get('legacy_evidence') not in {'CODE_READ', 'DOCUMENTATION_READ'}):
            raise ValueError('Quellenlektüre und Produktnachweis vermischt')
        for field in ('goal', 'input', 'output', 'state', 'failure', 'owner', 'gap'):
            if not isinstance(case.get(field), str) or not case[field].strip():
                raise ValueError(f"{case['id']}: {field} fehlt")
        if not case['sources'] or any(s not in sources for s in case['sources']):
            raise ValueError('Unbelegter Nutzungsfall')
        if (not isinstance(case.get('target_steps'), list) or not case['target_steps']
                or any(not isinstance(sid, str) or sid not in route['steps'] for sid in case['target_steps'])):
            raise ValueError('Unbekannter Zielschritt')
        covered.add(case['area'])
    if not {'songs', 'projects', 'plugins', 'import', 'media', 'quick_notes', 'backup'} <= covered:
        raise ValueError('MVP-Nutzungsweg nicht vollständig zugeordnet')
    if not data.get('reuse'):
        raise ValueError('Wiederverwendungsmatrix fehlt')
    contracts = data.get('shared_contracts', [])
    required = {'document', 'search', 'tags', 'templates', 'help', 'logging', 'versions', 'export'}
    if len(contracts) != len(required) or {item['id'] for item in contracts} != required:
        raise ValueError('Gemeinsame Verträge unvollständig')
    for item in contracts:
        if (not all(item.get(k) for k in ('owner', 'interface', 'boundary'))
                or item.get('target_status') != 'PLANNED'
                or item.get('source_status') not in {'CODE_READ', 'OPEN'}
                or (item['source_status'] == 'CODE_READ' and not item['sources'])
                or any(source not in sources for source in item['sources'])):
            raise ValueError('Unbelegter gemeinsamer Vertrag')
    for item in data['reuse']:
        if (not item['sources'] or any(s not in sources for s in item['sources'])
                or item['direct_copy_allowed'] is not False
                or item['license_status'] != 'UNRESOLVED'
                or not item['reason'] or not item['dependencies']):
            raise ValueError('Wiederverwendung ohne Herkunft, Grenze oder Lizenzklärung')
    return True


def load():
    import yaml
    from check_governance import UniqueLoader
    from render_todo import load_route
    data = json.loads(DATA.read_text())
    blueprint = yaml.load((ROOT / 'blueprint/architecture.yaml').read_text(), Loader=UniqueLoader)
    route = load_route(ROOT / 'governance/route.json')
    remote = subprocess.check_output(['git', 'config', '--get', 'remote.origin.url'], cwd=ROOT, text=True).strip()
    if Path(subprocess.check_output(['git', 'rev-parse', '--show-toplevel'], cwd=ROOT, text=True).strip()) != ROOT:
        raise ValueError('Arbeitsbaum liegt im falschen Repository')
    validate(data, blueprint, route, remote)
    return data


def render(data):
    ref = data['reference']
    lines = ['# Geprüfte Grundlage B001–B003', '',
             '## Repositorygrenzen', '',
             'Ein Schreibziel: `provoware/TOOL_ZENTRALE`; technischer Slug `TOOL_ZENTRALE`.',
             'Der geplante lokale Container heißt PROVOWARE, der Git-Root liegt darunter.',
             'Der Ausführungsort dieser Sitzung /workspace/TOOL_ZENTRALE ist nur ein Checkout.',
             'Produktanzeigename und Checkoutpfad dürfen abweichen. Keine verschachtelten Repos.',
             'Andere Repositories sind Lesereferenzen. Nutzdaten liegen außerhalb Git/Release.', '',
             '## Quellen und Prüfumfang', '',
             f"Referenz: `{ref['repository']}@{ref['commit']}`; vollständiger Baum mit {ref['blob_count']} Dateien.",
             f"Gezielt gelesen: {len(ref['files'])} Dateien; Git-Blobhashes der Scratchkopien exakt geprüft.",
             'Quelltexte und vorhandene Legacytests wurden gelesen, nicht ausgeführt oder übernommen.',
             'Quellebelege mit Blob-/SHA-256-Hash: `governance/foundation.json`.',
             'Keine eigenständige Lizenzdatei im fixierten Baum: Codeübernahme bleibt ungeklärt.', '',
             '## Nutzungsfälle statt Desktopdetails', '',
             'Alle Web-Ziele sind PLANNED; CODE_READ/DOCUMENTATION_READ belegt ausschließlich die Quellenlektüre.', '',
             '| Fall / Eigentümer | Ziel und Eingabe | Ergebnis / Zustand | Fehler und Anpassungsbedarf |',
             '|---|---|---|---|']
    for case in data['use_cases']:
        lines.append(f"| {case['id']} / {case['owner']} | {case['goal']}; {case['input']} | "
                     f"{case['output']}; {case['state']} | {case['failure']}; {case['gap']} |")
    lines += ['', '## Gemeinsame Bausteine und Übernahmegrenzen', '',
              '| Baustein | Entscheidung | Abhängigkeiten und Begründung |', '|---|---|---|']
    for item in data['reuse']:
        lines.append(f"| {item['component']} | {item['decision']} | {item['dependencies']}; {item['reason']} |")
    lines += ['', '## Gemeinsame Schnittstellen (geplant)', '',
              '| Vertrag / Eigentümer | Schnittstelle | Grenze / Herkunft |', '|---|---|---|']
    for item in data['shared_contracts']:
        lines.append(f"| {item['id']} / {item['owner']} | `{item['interface']}` | {item['boundary']}; {item['source_status']} |")
    lines += ['', '## Offene Punkte in sinnvoller Reihenfolge', '']
    for item in data['open_points']:
        lines.append(f"- **{item['id']} – {item['title']}**: {item['next_action']} ({item['gate']}).")
    lines += ['', '## Weiterentwicklung', '',
              'B004 prüft Schichten und erlaubte Abhängigkeiten, B005 gleicht reale und virtuelle',
              'Dateien ab, B006 prüft stabile Codes. Bestehende Modelle werden gezielt bestätigt,',
              'nicht neu erfunden. G-1/G0 bleiben bis zur dokumentierten Entscheidung offen.',
              'Die Planung ist kein Nachweis einer funktionierenden Webanwendung.', '',
              'Erzeugt aus `governance/foundation.json`; mit assist.py --refresh aktualisieren.', '']
    return '\n'.join(lines)


def main():
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    text = render(load())
    if args.check:
        if not DOC.exists() or DOC.read_text() != text:
            raise SystemExit('STALE: Grundlage mit assist.py --refresh aktualisieren')
    else:
        DOC.write_text(text, encoding='utf-8')
    print('FOUNDATION PASS' if args.check else 'FOUNDATION GENERATED')


if __name__ == '__main__':
    main()
