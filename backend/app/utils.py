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


def send_json_data(data: dict | List[dict] , code: int = 200):
    return json.dumps(data), code, {'Content-Type': 'application/json'}


get_args = lambda class_: [arg for arg in list(class_.__init__.__code__.co_varnames) if
                           arg not in ["self", "new_state"]]


def check_all_args(class_: Type["Base"], data, *args, **kwargs):
    isOkay = True
    if not args:
        args = get_args(class_)
    if kwargs and "exclude" in kwargs:
        for arg in kwargs["exclude"]:
            args.remove(arg)
    for arg in args:
        isOkay = isOkay and arg in data
    return isOkay


def check_one_arg(class_: Type["Base"], data, *args, **kwargs):
    isOkay = False
    if not args:
        args = get_args(class_)
    if kwargs and "additional" in kwargs:
        args += kwargs["additional"]
    for arg in args:
        isOkay = isOkay or arg in data
    if kwargs and "should_be" in kwargs:
        for arg in kwargs['should_be']:
            isOkay = isOkay and arg in data
    return isOkay


def make_json_response(obj_list: Base | List["Base"], *args: str, **kwargs) -> List[dict]:
    response = []
    if obj_list:
        if not type(obj_list) is list:
            obj_list = [obj_list]
        if not args:
            args = get_args(obj_list[0])
        if kwargs and "additional" in kwargs:
            args += kwargs["additional"]
        exclude = []
        if kwargs and "exclude" in kwargs:
            exclude = kwargs['exclude']
        for i, obj in enumerate(obj_list):
            response.append({})
            for arg in args:
                if arg not in exclude:
                    if isinstance(getattr(obj, arg), List) and len(getattr(obj, arg)) != 0 and isinstance(getattr(obj, arg)[0],
                                                                                                          Base):
                        response[i][arg] = make_json_response(list(getattr(obj, arg)), **kwargs)
                    else:
                        response[i][arg] = getattr(obj, arg)
                elif kwargs and "get" in kwargs and arg in kwargs['get']:
                    if type(kwargs['get'][arg]) is list:
                        response[i][arg] = {}
                        for arg_ in kwargs['get'][arg]:
                            response[i][arg][arg_] = (getattr(getattr(obj, arg), arg_))
                    else:
                        response[i][arg] = getattr(getattr(obj, arg), kwargs['get'][arg])
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


def login_required(func):
    @functools.wraps(func)
    def wrap(*args, **kwargs):
        authenticated, jwt = is_logged()
        if not authenticated:
            return abort(401)

        if db.session.execute(select(User).where(User.uuid == jwt['uuid'])).first():
            return func(*args, **kwargs)

        return abort(403)

    return wrap


def util_round(digit: float):
    integer = int(digit)
    return integer + (digit - integer >= 0.5)
