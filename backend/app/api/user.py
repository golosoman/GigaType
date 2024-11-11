import json

import jwt
from flask import Blueprint, request, make_response
from sqlalchemy import select, and_
from werkzeug.security import generate_password_hash, check_password_hash

from backend.app import db
from backend.app.models import User
from backend.app.utils import *
from backend.config import JWT_SECRET_KEY

user_api = Blueprint('user_api', __name__, url_prefix="/user")


@user_api.route("/register", methods=["POST"])
def register():
    """
    URL запроса: /api/user/register
    Payload: json{login: str, password: str}
    :return: cookie | {message: str}, code, Content-Type
    """
    data = request.json
    if "login" in data and "password" in data:
        try:
            if len(db.session.execute(select(User).where(User.login == data["login"])).scalars().all()) != 0:
                return message("Пользователь с таким именем уже существует.", 500)
            password_hash = generate_password_hash(data['password'])
            new_user = User(data['login'], password_hash)
            db.session.add(new_user)
            db.session.commit()
            resp = make_response()
            cookie = jwt.encode({"id": new_user.id, "uuid": new_user.uuid}, JWT_SECRET_KEY, algorithm="HS256")
            resp.set_cookie('auth', cookie, secure=True, httponly=False)
            resp.status = 200
            return resp
        except BaseException as e:
            db.session.rollback()
            db.session.commit()
            print(str(e))
            return message("Произошла ошибка.", 500)
    else:
        return message("Недостаточно данных", 403)


@user_api.route("/login", methods=["POST"])
def login():
    """
    URL запроса: /api/user/login
    Payload: json{login: str, password: str} | cookie
    :return: cookie | {message: str}, code, Content-Type
    """
    data = request.json
    if "auth" in request.cookies:
        token = request.cookies['auth']
        id_, uuid = (jwt.decode(token, JWT_SECRET_KEY, algorithms=["HS256"])).values()
        exist_user = db.session.execute(select(User).where(and_(User.id == id_, User.uuid == uuid))).first()
        if exist_user:
            exist_user: User = exist_user[0]
            resp = make_response()
            cookie = jwt.encode({"id": exist_user.id, "uuid": exist_user.uuid}, JWT_SECRET_KEY, algorithm="HS256")
            resp.set_cookie('auth', cookie, secure=True, httponly=False)
            resp.status = 200
            return resp
        else:
            return message("Неверные cookie", 500)
    elif "login" in data and "password" in data:
        exist_user = db.session.execute(select(User).where(User.login == data['login'])).first()
        if not exist_user:
            return message("Неверный логин", 404)
        exist_user: User = exist_user[0]
        if not check_password_hash(exist_user.password_hash, data['password']):
            return message("Неверный пароль.", 403)
        resp = make_response()
        cookie = jwt.encode({"id": exist_user.id, "uuid": exist_user.uuid}, JWT_SECRET_KEY, algorithm="HS256")
        resp.set_cookie('auth', cookie, secure=True, httponly=False)
        resp.status = 200
        return resp
    else:
        return message("Недостаточно данных", 403)
