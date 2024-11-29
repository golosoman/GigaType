import jwt
from flask import Blueprint, request, make_response, jsonify
from sqlalchemy import select, and_
from werkzeug.security import generate_password_hash, check_password_hash

from app import db
from app.models import User
from app.utils import message, check_all_args, admin_required
from config import JWT_SECRET_KEY

user_api = Blueprint('user_api', __name__, url_prefix="/user")


@user_api.route("/register", methods=["POST"])
def register():
    """
    URL запроса: /api/user/register
    Payload: json{login: str, password: str}
    :return: cookie | {message: str}, code, Content-Type
    """
    data = request.json
    if check_all_args(User, data, "login", "password"):
        try:
            if db.session.execute(select(User).where(User.login == data["login"])).first():
                return message("Пользователь с таким именем уже существует.", 406)
            password_hash = generate_password_hash(data['password'])
            new_user = User(data['login'], password_hash)
            db.session.add(new_user)
            db.session.commit()
            resp = make_response()
            cookie = jwt.encode({"id": new_user.id, "uuid": new_user.uuid, "login": new_user.login}, JWT_SECRET_KEY, algorithm="HS256")
            resp.set_cookie('auth', cookie, secure=True, httponly=False)
            resp.status = 200
            return resp
        except BaseException as e:
            db.session.rollback()
            db.session.commit()
            print(str(e))
            return message("Произошла ошибка.", 500)
    else:
        return message("Недостаточно данных", 406)


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
        id_, uuid, login = (jwt.decode(token, JWT_SECRET_KEY, algorithms=["HS256"])).values()
        exist_user = db.session.execute(select(User).where(and_(User.id == id_, User.uuid == uuid))).first()
        if exist_user:
            exist_user: User = exist_user[0]
            if exist_user.status_id == 2:
                resp = make_response(jsonify({"message": "Вы заблокированы"}))
                resp.status = 403
                resp.set_cookie("auth", '', expires=0, secure=True, httponly=False)
                return resp
            resp = make_response()
            cookie = jwt.encode({"id": exist_user.id, "uuid": exist_user.uuid, "login": exist_user.login}, JWT_SECRET_KEY, algorithm="HS256")
            resp.set_cookie('auth', cookie, secure=True, httponly=False)
            resp.status = 200
            return resp
        else:
            resp = make_response(jsonify({"message": "Неверные cookie"}))
            resp.status = 403
            resp.set_cookie("auth", '', expires=0, secure=True, httponly=False)
            return resp
    elif check_all_args(User, data, "login", "password"):
        exist_user = db.session.execute(select(User).where(User.login == data['login'])).first()
        if not exist_user:
            return message("Неверный логин", 404)
        exist_user: User = exist_user[0]
        if exist_user.status_id == 2:
            resp = make_response(jsonify({"message": "Вы заблокированы"}))
            resp.status = 403
            resp.set_cookie("auth", '', expires=0, secure=True, httponly=False)
            return resp
        if not check_password_hash(exist_user.password_hash, data['password']):
            return message("Неверный пароль.", 403)
        resp = make_response()
        cookie = jwt.encode({"id": exist_user.id, "uuid": exist_user.uuid, "login": exist_user.login}, JWT_SECRET_KEY, algorithm="HS256")
        resp.set_cookie('auth', cookie, secure=True, httponly=False)
        resp.status = 200
        return resp
    else:
        return message("Недостаточно данных", 406)


def change_user_status(status_id: int, message_: str):
    data = request.json
    if "uuid" in data:
        user = db.session.execute(select(User).where(User.uuid == data['uuid'])).first()
        if not user:
            return message("Неверный uuid пользователя", 404)
        user: User = user[0]
        if user.status_id == status_id:
            return message(message_, 406)
        user.status_id = status_id
        db.session.commit()
        return message("Okay")
    else:
        return message("Недостаточно данных", 406)


@user_api.route("/block", methods=["POST"])
@admin_required
def block():
    return change_user_status(2, "Пользователь уже заблокирован")


@user_api.route("/unblock", methods=["POST"])
@admin_required
def unblock():
    return change_user_status(1, "Пользователь уже разблокирован")