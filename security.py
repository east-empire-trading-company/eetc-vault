from functools import wraps

from flask import request, abort

import settings


def require_api_key(view_function):
    """
    Decorator for checking API Key authentication used on Flask view functions.
    Example usage: @require_api_key
    """

    @wraps(view_function)
    def decorated_function(*args, **kwargs):
        api_key = settings.API_KEY

        if request.headers.get("API_KEY") == api_key:
            return view_function(*args, **kwargs)
        else:
            abort(401)

    return decorated_function
