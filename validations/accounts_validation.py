accounts_register_schema = {
    'account_type': {'type': 'string', 'required': True},
    'balance': {'type': 'integer', 'required': True, 'min': 10000}
}

accounts_update_schema = {
    'account_type': {'type': 'string'},
    'balance': {'type': 'integer', 'min': 10000}
}