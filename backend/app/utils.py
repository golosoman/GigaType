import functools
import json

from flask import request, abort
from jwt import decode, DecodeError

from config import JWT_SECRET_KEY


def message(message_: str, code: int):
    return json.dumps({"message": message_}), code, {'Content-Type': 'application/json'}


def json_data(data: dict, code: int):
    return json.dumps(data), code, {'Content-Type': 'application/json'}


get_args = lambda class_: [arg for arg in list(class_.__init__.__code__.co_varnames) if
                           arg not in ["self", "new_state"]]
def check_all_args(class_, data):
    isOkay = True
    for arg in get_args(class_):
        isOkay = isOkay and arg in data
    return isOkay

def check_one_arg(class_, data):
    isOkay = False
    for arg in get_args(class_):
        isOkay = isOkay or arg in data
    return isOkay


def is_logged():
    try:
        return True, decode(request.cookies.get('auth'), JWT_SECRET_KEY, algorithms=['HS256'])

    except DecodeError:
        return False, {}


def admin_required(func):
    @functools.wraps(func)
    def wrap(*args, **kwargs):
        authenticated, jwt = is_logged()
        if not authenticated:
            return abort(401)

        if jwt['login'] == "admin":
            return func(*args, **kwargs)

        return abort(403)

    return wrap
