from functools import wraps
from flask_login import current_user

def auth_required():
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if current_user.is_authenticated:
                return func(*args, **kwargs)
            else:
                return {'message': 'Unauthorized'}, 403
        return wrapper
    
    return decorator