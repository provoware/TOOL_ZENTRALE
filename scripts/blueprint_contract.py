"""Layer, ownership, code identity and planned-test trace contracts."""
from functools import lru_cache
from pathlib import PurePosixPath
import re
import subprocess

import yaml

ALLOWED = {
    'UI': {'UI', 'API'}, 'API': {'API', 'SERVICE', 'CORE'},
    'SERVICE': {'SERVICE', 'DOMAIN', 'STORAGE', 'CORE', 'PLUGIN'}, 'DOMAIN': {'DOMAIN'},
    'STORAGE': {'STORAGE', 'DOMAIN', 'CORE'}, 'CORE': {'CORE', 'DOMAIN'},
    'PLUGIN': {'PLUGIN', 'DOMAIN', 'CORE'}, 'QA': set(), 'GOV': set(), 'TOOL': set()}
CODE_PATTERN = r'^[A-Z][A-Z0-9]{1,7}$'


def valid_path(name):
    return (isinstance(name, str) and name not in {'', '.'} and '\\' not in name and '\0' not in name
            and not re.match(r'^[A-Za-z]:', name) and not name.startswith('/')
            and '..' not in name.split('/') and PurePosixPath(name).as_posix() == name)


@lru_cache(maxsize=4)
def historical_codes(root):
    """Git owns the reservation history; no second manually maintained codebook."""
    from check_governance import UniqueLoader
    if subprocess.check_output(['git', 'rev-parse', '--is-shallow-repository'], cwd=root, text=True).strip() != 'false':
        raise ValueError('Vollständige Git-Historie für Codesperre erforderlich')
    commits = subprocess.check_output(['git', 'log', '--full-history', '--reverse', '--format=%H', '--',
                                       'blueprint/architecture.yaml'], cwd=root, text=True).split()
    identities = {}
    for commit in commits:
        raw = subprocess.check_output(['git', 'show', commit + ':blueprint/architecture.yaml'], cwd=root, text=True)
        for code, item in yaml.load(raw, Loader=UniqueLoader).get('codebook', {}).items():
            identity = (item['path'], item['layer'])
            if code in identities and identities[code] != identity:
                raise ValueError(f'{code}: widersprüchliche historische Codeidentität')
            identities[code] = identity
    return identities


def reachable(codes, start):
    seen = set()
    pending = list(start)
    while pending:
        code = pending.pop()
        if code not in seen:
            seen.add(code)
            pending.extend(codes[code].get('requires', []))
    return seen


def planned_tests(codes):
    coverage = {code: [] for code in codes}
    for test, item in codes.items():
        if item['layer'] == 'QA':
            for target in reachable(codes, item['verifies']):
                coverage[target].append(test)
    return {code: sorted(tests) for code, tests in coverage.items()}


def validate_model(blueprint, history):
    layers, files, codes = (blueprint[key] for key in ('layers', 'files', 'codebook'))
    if set(layers) != set(ALLOWED) or any(set(layers[k]['may_depend_on']) != v for k, v in ALLOWED.items()):
        raise ValueError('Schichtenpolicy verändert oder unerlaubt erweitert')
    if any(not isinstance(v.get('responsibility'), str) or not v['responsibility'].strip() for v in layers.values()):
        raise ValueError('Schichtverantwortung fehlt')
    if blueprint['standards']['code_regex'] != CODE_PATTERN:
        raise ValueError('Codes müssen normalisierte 2–8 ASCII-Zeichen besitzen')
    directories = blueprint['directories']
    if len(directories) != len(set(directories)) or any(not valid_path(p) for p in directories):
        raise ValueError('Verzeichnisnamen nicht eindeutig oder ungültig')
    if set(files) & set(directories) or any(
            parent.as_posix() in files for name in list(files) + directories
            for parent in PurePosixPath(name).parents):
        raise ValueError('Datei-/Verzeichniskollision im Sollkatalog')
    for path, item in files.items():
        if (not valid_path(path) or item.get('owner') not in ALLOWED
                or item.get('stability') not in {'S0', 'S1', 'S2'}
                or item.get('catalog') not in {'CONFIRMED', 'RESERVED', 'OPTIONAL'}):
            raise ValueError(f'{path}: Pfad, Besitzer oder Klassifikation ungültig')
    for code, item in codes.items():
        if (not re.fullmatch(CODE_PATTERN, code) or not isinstance(item.get('interface'), str)
                or not item['interface'].strip() or item.get('path') not in files
                or files[item['path']]['owner'] != item['layer']):
            raise ValueError(f'{code}: Schnittstelle oder Dateiverantwortung unklar')
        for key in ('requires', 'verifies'):
            refs = item.get(key, [])
            if (not isinstance(refs, list) or any(not isinstance(ref, str) or ref not in codes for ref in refs)
                    or len(refs) != len(set(refs))):
                raise ValueError(f'{code}: unbekannte oder doppelte Referenz')
        source = PurePosixPath(item['path']).parts
        for ref in item.get('requires', []):
            target = PurePosixPath(codes[ref]['path']).parts
            if (source[:2] == ('app', 'core') and target[:2] == ('app', 'features')
                    or source[:2] == target[:2] == ('app', 'features') and source[2] != target[2]):
                raise ValueError(f'{code}: direkter Zugriff auf Fachmodulinterna')
        if item['layer'] == 'QA':
            if not item.get('verifies') or any(codes[ref]['layer'] == 'QA' for ref in item['verifies']):
                raise ValueError(f'{code}: Testziel fehlt oder ist selbst ein Test')
        elif item.get('verifies'):
            raise ValueError(f'{code}: Prüfbeziehungen nur auf QA-Codes')
    for code, identity in history.items():
        if code not in codes or (codes[code]['path'], codes[code]['layer']) != identity:
            raise ValueError(f'{code}: vergebene Codeidentität entfernt oder wiedervergeben')
    for code, item in codes.items():
        if item['layer'] == 'PLUGIN' and 'KCAP' not in reachable(codes, [code]):
            raise ValueError(f'{code}: Pluginpfad ohne Capability-Vertrag')
    if any(blueprint['module_contract'].get(key) is not False for key in
           ('executable_external_plugins_v1', 'arbitrary_foreign_code_v1')):
        raise ValueError('Freie Fremdcodeausführung in V1 unzulässig')
    coverage = planned_tests(codes)
    if any(not coverage[code] for code, item in codes.items() if item['layer'] != 'QA'):
        raise ValueError('Komponente ohne geplante Testzuordnung')
    minimum = {'media': ['manifest.yaml', 'backend/domain.py', 'backend/service.py', 'backend/routes.py',
                         'public/media.js', 'tests/test_media.py', 'help/de.md'],
               'import_tool': ['manifest.yaml', 'backend/routes.py', 'public/import_ui.js',
                               'tests/test_import.py', 'help/de.md']}
    for module, required in minimum.items():
        root = blueprint['modules'][module]['root']
        if any(root + '/' + path not in files for path in required):
            raise ValueError(f'{module}: Dateikatalog unvollständig')
    return coverage
