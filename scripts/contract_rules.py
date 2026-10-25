"""Validate design contracts without a runtime API."""
VERSIONS = {'product', 'build', 'api', 'database', 'module', 'config'}
CAPABILITIES = {'catalog.read', 'catalog.manage', 'notes.append', 'songs.read', 'songs.write', 'projects.read',
                'projects.import_preview', 'projects.import_apply', 'media.read', 'tool.launch'}


from schema_examples import validate_example


def validate_contracts(blueprint):
    contracts = blueprint['contracts']
    if contracts.get('schema') != 'provoware-design-contracts/1' or contracts.get('status') != 'PLANNED_NOT_RUNTIME_IMPLEMENTED':
        raise ValueError('Vertragsschema oder Planungsstatus unbekannt')
    if set(contracts['version_axes']) != VERSIONS or contracts.get('independent_versions') is not True:
        raise ValueError('Versionsachsen fehlen oder sind unzulässig gekoppelt')
    if len(set(contracts['version_axes'].values())) != len(VERSIONS):
        raise ValueError('Versionsschemata müssen getrennte Bedeutung besitzen')
    for name, schema in contracts['payloads'].items():
        props, required = schema['properties'], schema['required']
        if (schema.get('type') != 'object' or schema.get('additionalProperties') is not False
                or not required or len(required) != len(set(required)) or set(required) - set(props)
                or any(p.get('type') not in {'string', 'integer', 'boolean', 'array'} for p in props.values())):
            raise ValueError(f'{name}: unvollständiges Sollschema')
    required_payloads = {'song_request', 'song_response', 'note_request', 'note_response', 'error',
                         'project_query', 'project_response', 'module_manifest', 'catalog_response',
                         'import_preview', 'import_apply', 'import_response', 'media_request', 'media_response',
                         'launch_request', 'launch_response'}
    if not required_payloads <= set(contracts['payloads']):
        raise ValueError('Request-/Antwort-/Fehlervertrag fehlt')
    for name, fields in {'song_request': {'document_id', 'title', 'sections', 'expected_revision', 'request_id'},
                         'song_response': {'document_id', 'revision', 'saved_at', 'saved'}}.items():
        if set(contracts['payloads'][name]['required']) != fields:
            raise ValueError('Songrevision oder Speicherbestätigung fehlt')
    error = contracts['payloads']['error']['required']
    if not {'code', 'message', 'correlation_id', 'retryable', 'next_action'} <= set(error):
        raise ValueError('Fehlerkorrektur oder Korrelationsbeleg fehlt')
    if set(contracts['examples']) != set(contracts['payloads']):
        raise ValueError('Pflichtbeispiele nicht vollständig')
    if set(contracts['payloads']['note_response']['required']) != {'note_id', 'utc_iso8601', 'app_version', 'build_sha', 'durable'}:
        raise ValueError('Notizbestätigung unvollständig')
    for name, field in (('note_response', 'durable'), ('song_response', 'saved')):
        if contracts['payloads'][name]['properties'][field].get('const') is not True:
            raise ValueError('Erfolgsantwort muss dauerhaft bestätigt sein')
    for name, sample in contracts['examples'].items():
        validate_example(contracts['payloads'][name], sample)
    permissions = contracts['permissions']
    if (set(permissions['capabilities']) != CAPABILITIES or permissions.get('default') != 'DENY'
            or permissions.get('unknown_capability') != 'DENY'
            or permissions['trust_levels'] != {'BUILTIN': 'REVIEWED_MANIFEST_CAPABILITIES',
                                               'DECLARATIVE': 'METADATA_ONLY',
                                               'LOCAL_TOOL': 'EXPLICIT_ALLOWLIST_ONLY', 'FOREIGN_CODE': 'DENY'}):
        raise ValueError('Capability- oder Vertrauensgrenze verletzt')
    note = contracts['note_semantics']
    if (note.get('same_id_same_content') != 'SAME_ACK_NO_SECOND_WRITE'
            or note.get('same_id_other_content') != 'CONFLICT_NO_WRITE'
            or note.get('success_after') != 'DURABLE_WRITE'
            or note.get('record_id') != 'VALIDATED_REQUEST_ID'
            or set(note.get('server_fields', [])) != {'utc_iso8601', 'app_version', 'build_sha'}
            or note.get('client_version_policy') != 'REJECT_UNKNOWN_REQUEST_FIELDS'
            or note.get('max_request_bytes', 0) < 4096):
        raise ValueError('Notiz bestätigt unsicher, doppelt oder mit falscher Version')
    request = contracts['payloads']['note_request']
    if (set(request['required']) != {'request_id', 'text'}
            or set(request['properties']) != {'request_id', 'text'}
            or request['properties']['text'].get('maxLength') != blueprint['tool_local_log']['max_text_characters_initial']):
        raise ValueError('Notizanfrage oder Größenvertrag widersprüchlich')
    expected_owners = {'runtime_data': 'OUTSIDE_GIT_AND_RELEASE', 'documents': 'USER_PRIVATE_DOCUMENT_STORE',
                       'notes': 'TOOL_PRIVATE_APPEND_STORE', 'media': 'AUTHORIZED_ASSET_REGISTRY', 'legacy_sources': 'READ_ONLY'}
    if contracts['data_ownership'] != expected_owners:
        raise ValueError('Datenbesitz oder Legacy-Lesegrenze verletzt')
    expected_errors = {'VALIDATION': 400, 'PERMISSION_DENIED': 403, 'NOT_FOUND': 404,
                       'REVISION_CONFLICT': 409, 'LIMIT_EXCEEDED': 413, 'STORAGE_UNAVAILABLE': 503}
    if contracts['error_statuses'] != expected_errors:
        raise ValueError('Fehlerstatus widerspricht Schutzvertrag')
    http = contracts['http_boundary']
    if type(http['max_request_bytes']) is not int or not 0 < note['max_request_bytes'] <= http['max_request_bytes']:
        raise ValueError('Request-Bytebudgets widersprüchlich')
    limits = contracts['payload_byte_limits']
    request_names = {'song_request', 'note_request', 'project_query', 'module_manifest',
                     'import_preview', 'import_apply', 'media_request', 'launch_request'}
    if (set(limits) != request_names or limits['note_request'] != note['max_request_bytes']
            or any(type(n) is not int or not 0 < n <= http['max_request_bytes'] for n in limits.values())):
        raise ValueError('Endpointbudgets fehlen oder überschreiten die Servergrenze')
    from api_contract_rules import validate_api_contracts
    validate_api_contracts(blueprint)
    if (http['bind'] != '127.0.0.1' or http['origin_policy'] != 'SAME_ORIGIN_ONLY'
            or http['remote_access'] != 'OUT_OF_V1_SCOPE' or http['api_major'] != 1):
        raise ValueError('Lokaler HTTP-/Originvertrag verletzt')
    if set(contracts['log_sensitive_fields_forbidden']) != {'note_text', 'document_text', 'tokens', 'absolute_paths'}:
        raise ValueError('Redaktionsgrenze fehlt')
    return True


def validate_checker(blueprint):
    checker = blueprint['checker_contract']
    if checker.get('schema') != 'provoware-checker/1' or checker.get('execution_owner') != 'scripts/assist.py':
        raise ValueError('Prüferschema oder Ausführungsbesitzer ungültig')
    required = {'parse_unique_keys', 'contracts', 'ids_graph_layers', 'catalog',
                'scenario_contracts', 'evidence_gates', 'views', 'regression_tests'}
    if (len(checker['phases']) != len(required) or set(checker['phases']) != required
            or checker['failure_policy'] != 'STOP_WITH_FAIL'
            or checker['source_mutation'] is not False
            or checker['result_kind'] != 'MODEL_CONTRACT_PASS'
            or checker['runtime_result'] != 'NOT_TESTED'
            or checker['cache'] != 'PROCESS_LOCAL_HISTORY_ONLY_NO_PASS_REUSE'):
        raise ValueError('Prüferphasen oder Nachweisgrenzen verletzt')
    if (not {'blueprint/architecture.yaml', 'governance/route.json', 'reachable_git_history',
             'git_index_and_worktree', 'governance/regressions.yaml'} <= set(checker['inputs'])
            or set(checker['outputs']) != {'model_result', 'dynamic_counts', 'derived_views', 'local_run_evidence'}):
        raise ValueError('Prüferinputs/-outputs unvollständig')
    allowed = {'docs/REGRESSION_INFO.md', 'docs/GRUNDLAGE_B001_B003.md', 'docs/ARCHITEKTUR_B004_B006.md',
               'docs/VERTRAEGE_B007_B009.md', 'docs/TODO_V3_2.md', 'docs/assets/todo_progress.svg',
               'governance/file_state.json', 'docs/STATUS_KURZ.md'}
    if set(checker['refresh_outputs']) != allowed:
        raise ValueError('Nicht erlaubtes Aktualisierungsziel')
    return True
