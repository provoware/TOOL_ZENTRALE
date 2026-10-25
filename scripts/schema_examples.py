"""Validate only the declared JSON-schema subset used by design examples."""

def validate_example(schema, value):
    types = {'object': dict, 'string': str, 'integer': int, 'boolean': bool, 'array': list}
    kind = schema['type']
    keywords = {'object': {'required', 'properties', 'additionalProperties'},
                'array': {'items', 'minItems', 'maxItems'}, 'string': {'minLength', 'maxLength'},
                'integer': {'minimum', 'maximum'}, 'boolean': set()}
    if kind not in types or set(schema) - (keywords.get(kind, set()) | {'type', 'const', 'enum'}):
        raise ValueError('Nicht unterstütztes Beispielschema')
    if kind not in types or type(value) is not types[kind]:
        raise ValueError('Beispieltyp widerspricht Sollschema')
    if 'const' in schema and value != schema['const'] or 'enum' in schema and value not in schema['enum']:
        raise ValueError('Beispiel verletzt feste Werte')
    if kind == 'object':
        if set(schema['required']) - set(value) or set(value) - set(schema['properties']):
            raise ValueError('Beispiel widerspricht Pflichtfeldern')
        for key, item in value.items():
            validate_example(schema['properties'][key], item)
    elif kind == 'array':
        if not schema.get('minItems', 0) <= len(value) <= schema.get('maxItems', 100000):
            raise ValueError('Beispielarray zu kurz')
        for item in value:
            validate_example(schema['items'], item)
    elif kind == 'string' and not schema.get('minLength', 0) <= len(value) <= schema.get('maxLength', 100000):
        raise ValueError('Beispiel verletzt Längengrenze')
    elif kind == 'integer' and not schema.get('minimum', value) <= value <= schema.get('maximum', value):
        raise ValueError('Beispiel verletzt Zahlengrenze')

