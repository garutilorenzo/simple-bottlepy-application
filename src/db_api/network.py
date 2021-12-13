from schema.network import Sites

def get(network_name):
    errors = []
    if not network_name:
        errors.append('no network_name provided')
        return {'errors': errors, 'result': 0}
    for site in Sites:
        if site.name == network_name:
            return {'errors': errors, 'result': site}
    return {'errors': errors, 'result': None}

def get_all():
    errors = []
    return {'errors': errors, 'result': Sites}