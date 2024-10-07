users_register_schema = {
    'username': {'type': 'string', 'required': True, 'minlength': 2},
    'email': { 
        'type': 'string',
        'regex': '^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+.[a-zA-Z0-9-.]+$',
        'required': True
    }
}

users_login_schema = {
    'email': {
        'type': 'string',
        'regex': '^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+.[a-zA-Z0-9-.]+$',
        'required': True
    }
}

users_update_schema = {
    'username': {'type': 'string', 'minlength': 2},
    'email': { 
        'type': 'string',
        'regex': '^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+.[a-zA-Z0-9-.]+$'
    }
}