import csv
import jwt
import sys
import pandas as pd
from datetime import datetime, timedelta, timezone
from flask import make_response, current_app as app, request, session, render_template
from functools import wraps

USERS_FILE = 'dataset\\users.csv'
def encode_auth_token(id):
    """Generates the Auth Token."""
    try:
        token = jwt.encode(
        payload={
            "exp": datetime.now(timezone.utc) + timedelta(minutes=5),
            "iat": datetime.now(timezone.utc),
            "sub": id,
        },
        key=app.secret_key,
        algorithm='HS256',
    )
        return token
    except Exception as e:
        return e


def decode_auth_token(auth_token):
    """Decodes the auth token."""
    try:
        payload = jwt.decode(auth_token, app.secret_key, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        return make_response({'message': "Token expired. Please log in again."}, 401)
    except jwt.InvalidTokenError:
        return make_response({'message': "Invalid token. Please log in again."}, 401)


def get_user(id):
    """Get user details from CSV."""
    df = pd.read_csv(USERS_FILE)
    if id in df['id'].values:
        return df[df['id'] == id].to_dict('records')[0]
    return None


def token_required(f):
    """Require valid jwt for a route."""
    @wraps(f)
    def decorator(*args, **kwargs):
        if "token" in session.keys(): token = session['token']
        else: token = None
        if not token: return render_template('log-in-page.html',error="Authentication Token missing, please log in")
        token_payload = decode_auth_token(token)
        try: id = token_payload["sub"]
        except TypeError: return render_template('log-in-page.html', error = "Authentication Token expired, please log in again")
        user = get_user(id)
        if not user: return render_template('log-in-page.html',error="Invalid or missing user id, please log in again")

        return f(*args, **kwargs)
    return decorator
 
