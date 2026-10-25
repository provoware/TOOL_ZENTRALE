"""Bind declared API actions to known capabilities and safe payload boundaries."""
EXPECTED = {'ASNG': {'read': 'songs.read', 'write': 'songs.write'}, 'APSR': {'query': 'projects.read'},
            'APLG': {'catalog': 'catalog.read', 'manage': 'catalog.manage'}, 'ANOTE': {'append': 'notes.append'},
            'AIMP': {'preview': 'projects.import_preview', 'apply': 'projects.import_apply'},
            'AMED': {'read': 'media.read'}, 'APLX': {'launch': 'tool.launch'}}


def validate_api_contracts(blueprint):
    c = blueprint['contracts']
    if c['api_capabilities'] != EXPECTED:
        raise ValueError('API-Aktion ohne eindeutige Capability-Zuordnung')
    for code, actions in c['api_capabilities'].items():
        if (blueprint['codebook'][code]['layer'] != 'API'
                or any(cap not in c['permissions']['capabilities'] for cap in actions.values())):
            raise ValueError('Capability-Ziel oder API-Schicht unbekannt')
    boundaries = {'project_query': {'query', 'scope_id', 'limit'},
                  'module_manifest': {'module_id', 'version', 'contract_major', 'capabilities'},
                  'import_preview': {'source_id', 'strategy', 'apply'},
                  'import_apply': {'preview_id', 'request_id', 'confirmed', 'expected_revision'},
                  'media_request': {'asset_id', 'purpose'}, 'launch_request': {'tool_id', 'request_id', 'confirmed'}}
    for name, fields in boundaries.items():
        schema = c['payloads'][name]
        if set(schema['required']) != fields or set(schema['properties']) != fields:
            raise ValueError('Fachlicher Request-Vertrag unvollständig')
    for name, field, value in (('import_preview', 'apply', False), ('import_apply', 'confirmed', True),
                               ('launch_request', 'confirmed', True), ('catalog_response', 'executable', False)):
        if c['payloads'][name]['properties'][field].get('const') is not value:
            raise ValueError('Bestätigungs- oder Fremdcodegrenze fehlt')
    return True
