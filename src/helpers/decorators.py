from functools import wraps
from flask import abort, request
import requests
import jwt
from environs import Env

from src.helpers.responses import invalid_auth_header, no_auth_header_present, access_forbidden
from src.database.models import USER

env = Env()
env.read_env()


def authorize(f):
    @wraps(f)
    def decorated_function(*args, **kws):
        if not 'Authorization' in request.headers:
            return no_auth_header_present()

        user_id = None
        data = request.headers['Authorization']
        token = str.replace(str(data), 'Bearer ', '')
        try:
            user_id = USER.decode_auth_token(token)
        except:
            return invalid_auth_header()
        print(user_id)    
        kws['user_id'] = user_id 
        return f(*args, **kws)

    return decorated_function


def authorize_admin(f):
    @wraps(f)
    def decorated_function(*args, **kws):
        # print(request.cookies['auth'])
        if not 'auth' in request.cookies and not 'Authorization' in request.headers:
            return no_auth_header_present()

        tokenHeader = request.headers.get('Authorization') or 'Bearer ' + \
            request.cookies.get('auth')
        forwardRequest = requests.get(env('TELYPORT_API_URL') +
                                      '/m/admin/is_admin',
                                      headers={"Authorization": tokenHeader})
        if (forwardRequest.status_code != 200):
            return invalid_auth_header()

        kws['super_admin'] = forwardRequest.json()
        return f(*args, **kws)

    return decorated_function


def authorize_super_admin(f):
    @wraps(f)
    def decorated_function(*args, **kws):
        # print(kws['super_admin'])
        if not kws['super_admin'].get('super'):
            return access_forbidden()
        return f(*args, **kws)

    return decorated_function
