import re
import string
from functools import wraps, partial
from flask import session, redirect, url_for, flash

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('loggedin'):
            flash('You must be logged in to access this page.', 'warning')
            return redirect(url_for('user.login'))
        
       
        return f(*args, **kwargs)
    return decorated_function

def _role_required_decorator(f, roles):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('loggedin'):
            flash('Please log in to view this page.', 'warning')
            return redirect(url_for('user.login'))
        
        if session.get('role') not in roles:
            flash('You do not have permission to access this page.', 'danger')
            return redirect(url_for('user.access_denied'))
        
        return f(*args, **kwargs)
    return decorated_function

def role_required(*roles):
    return partial(_role_required_decorator, roles=roles)

def is_password_strong(password):
    """
    Check if your password meets the strength requirements.
    Requirement: At least 8 characters, including uppercase and lowercase letters, numbers, and special characters.
    """
    
    if len(password) < 8:
        return False, "Password must be at least 8 characters long."

    
    if not re.search(r"[a-z]", password):
        return False, "Password must contain at least one lowercase letter."
    if not re.search(r"[A-Z]", password):
        return False, "Password must contain at least one uppercase letter."
    if not re.search(r"[0-9]", password):
        return False, "Password must contain at least one number."
    if not re.search(f"[{re.escape(string.punctuation)}]", password):
        return False, "Password must contain at least one special character."

    
    return True, "Password is strong."