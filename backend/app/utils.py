import functools
import json
from typing import List, Type

from flask import request, abort
from jwt import decode, DecodeError
from sqlalchemy import select

from app.models import Base, User
from app import db
from config import JWT_SECRET_KEY


def message(message_: str, code: int = 200):
    return json.dumps({"message": message_}), code, {'Content-Type': 'application/json'}


def send_json_data(data: dict, code: int = 200):
    return json.dumps(data), code, {'Content-Type': 'application/json'}


get_args = lambda class_: [arg for arg in list(class_.__init__.__code__.co_varnames) if
                           arg not in ["self", "new_state"]]


def check_all_args(class_: Type["Base"], data, *args):
    isOkay = True
    if not args:
        args = get_args(class_)
    for arg in args:
        isOkay = isOkay and arg in data
    return isOkay


def check_one_arg(class_: Type["Base"], data, *args):
    isOkay = False
    if not args:
        args = get_args(class_)
    for arg in args:
        isOkay = isOkay or arg in data
    return isOkay


def make_json_response(obj_list: Base | List["Base"], *args: str, **kwargs):
    response = []
    if not type(obj_list) is list:
        obj_list = [obj_list]
    if not args:
        args = get_args(obj_list[0])
    if kwargs:
        args += kwargs.values()
    for i, obj in enumerate(obj_list):
        response.append({})
        for arg in args:
            if isinstance(getattr(obj, arg), List) and len(getattr(obj, arg)) != 0 and isinstance(getattr(obj, arg)[0],
                                                                                                  Base):
                response[i][arg] = make_json_response(list(getattr(obj, arg)))
            else:
                response[i][arg] = getattr(obj, arg)
    return response


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

        if jwt['login'] == "admin" and db.session.execute(select(User).where(User.uuid == jwt['uuid'])).first():
            return func(*args, **kwargs)

        return abort(403)

    return wrap
