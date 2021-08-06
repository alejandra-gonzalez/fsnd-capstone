import json
from flask import request, abort
from functools import wraps
from jose import jwt
from urllib.request import urlopen

AUTH0_DOMAIN = 'alex-fsnd.us.auth0.com'
ALGORITHMS = ['RS256']
API_AUDIENCE = 'skylight'

'''
AuthError Exception:
    Standardized way to communicate Auth failure modes
'''
class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code

'''
get_token_auth_header() method:
    Attempts to get the auth header from the request and split it into bearer
    and the token part. Raises AuthError if no header is present OR header is
    malformed. Returns the token part of the header.
'''
def get_token_auth_header():
    auth = request.headers.get('Authorization', None)
    if not auth:
        raise AuthError({
            'code': 'authorization_header_missing',
            'description': 'Authorization header is required.'
        }, 401)
    parts = auth.split()
    if len(parts) != 2:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization malformed.'
        }, 401)
    elif parts[0].lower() != 'bearer':
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization header must start with "Bearer".'
        }, 401)
    return parts[1]

'''
check_permissions(permission, payload) method:
    INPUTS:
        permission: string permission (i.e. 'post:drink')
        payload: decoded jwt payload
    Raises an AuthError if permissions are not included in the payload OR if
    the requested permission string is not in the payload permissions array. 
    Returns true otherwise.
'''
def check_permissions(permission, payload):
    if 'permissions' not in payload:
        raise AuthError({
            'code': 'invalid_claims',
            'description': 'Permissions not included in JWT.'
        }, 400)
    if permission not in payload['permissions']:
        raise AuthError({
            'code': 'unauthorized',
            'description': 'Permission Not found',
        }, 401)
    return True

'''
verify_decode_jwt(token) method:
    INPUTS:
        token: a json web token (string)
    Verifies the Auth0 token that has key id (kid) using Auth0 
    /.well-known/jwks.json, then decodes the payload from the token and checks
    the claims. Returns the decoded payload.
'''
def verify_decode_jwt(token):
    jsonurl = urlopen(f'https://{AUTH0_DOMAIN}/.well-known/jwks.json')
    jwks = json.loads(jsonurl.read())
    unverified_header = jwt.get_unverified_header(token)
    rsa_key = {}
    if 'kid' not in unverified_header:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization malformed.'
        }, 401)
    for key in jwks['keys']:
        if key['kid'] == unverified_header['kid']:
            rsa_key = {
                'kty': key['kty'],
                'kid': key['kid'],
                'use': key['use'],
                'n': key['n'],
                'e': key['e']
            }
    if rsa_key:
        try:
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=ALGORITHMS,
                audience=API_AUDIENCE,
                issuer='https://' + AUTH0_DOMAIN + '/'
            )
            return payload
        except jwt.ExpiredSignatureError:
            raise AuthError({
                'code': 'token_expired',
                'description': 'Token expired.'
            }, 401)
        except jwt.JWTClaimsError:
            raise AuthError({
                'code': 'invalid_claims',
                'description': 'Incorrect claims. Please, check the audience and issuer.'
            }, 401)
        except Exception:
            raise AuthError({
                'code': 'invalid_header',
                'description': 'Unable to parse authentication token.'
            }, 400)
    raise AuthError({
        'code': 'invalid_header',
        'description': 'Unable to find the appropriate key.'
    }, 400)

'''
@requires_auth(permission) decorator method:
    INPUTS:
        permission: string permission (i.e. 'post:drink')
    Uses get_token_auth_header method to get the token. Uses verify_decode_jwt
    method to decode the jwt and uses check_permissions method to check claims
    and the requested permission. Returns the decorator which passes the
    decoded payload to the decorated method.
'''
def requires_auth(permission=''):
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = get_token_auth_header()
            payload = verify_decode_jwt(token)
            check_permissions(permission, payload)
            return f(payload, *args, **kwargs)
        return wrapper
    return requires_auth_decorator