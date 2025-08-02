from functools import wraps
from flask import session, redirect, url_for, flash

def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if not session.get('loggedin'):
            flash('You must be logged in to access this page.')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return wrapper

def role_required(*roles):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            if not session.get('loggedin') or session.get('role') not in roles:
                flash('Access denied.')
                return redirect(url_for('login'))
            return f(*args, **kwargs)
        return wrapper
    return decorator
