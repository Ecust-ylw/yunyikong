from functools import wraps
from flask import session, url_for, redirect


def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if session.get('id'):
            return func(*args, **kwargs)
        else:
            return redirect(url_for('user.login_page'))

    return wrapper