import jwt
from flask import Blueprint, request, make_response, jsonify
from sqlalchemy import select, and_
from werkzeug.security import generate_password_hash, check_password_hash

from app import db
from app.models import User
from app.utils import message, check_all_args, admin_required, login_required, send_json_data, make_json_response
from config import JWT_SECRET_KEY

user_api = Blueprint('user_api', __name__, url_prefix="/user")


def send_cookie(id_: int, uuid: str, login: str):
    resp = make_response(jsonify({"uuid": uuid}))
    cookie = jwt.encode({"id": id_, "uuid": uuid, "login": login}, JWT_SECRET_KEY, algorithm="HS256")
    resp.set_cookie('auth', cookie, max_age=14 * 24 * 3600, secure=False, httponly=False)
    resp.status = 200
    return resp


def delete_cookie(message_):
    resp = make_response(jsonify({"message": message_}))
    resp.status = 403
    resp.set_cookie("auth", '', expires=0, secure=False, httponly=False)
    return resp


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
            if "auth" not in request.cookies:
                return send_cookie(new_user.id, new_user.uuid, new_user.login)
            token = request.cookies['auth']
            id_, uuid, login = (jwt.decode(token, JWT_SECRET_KEY, algorithms=["HS256"])).values()
            exist_user = db.session.execute(select(User).where(and_(User.id == id_, User.uuid == uuid))).first()
            if not exist_user:
                return send_cookie(new_user.id, new_user.uuid, new_user.login)
            exist_user: User = exist_user[0]
            if exist_user.login == "admin":
                return message("Пользователь создан")
            else:
                return send_cookie(new_user.id, new_user.uuid, new_user.login)
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
    data = {}
    try:
        data = request.json
    except BaseException as e:
        pass
    if "auth" in request.cookies:
        token = request.cookies['auth']
        id_, uuid, login = (jwt.decode(token, JWT_SECRET_KEY, algorithms=["HS256"])).values()
        exist_user = db.session.execute(select(User).where(and_(User.id == id_, User.uuid == uuid))).first()
        if exist_user:
            exist_user: User = exist_user[0]
            if exist_user.status_id == 2:
                return delete_cookie("Вы заблокированы")
            return send_cookie(exist_user.id, exist_user.uuid, exist_user.login)
        else:
            return delete_cookie("Неверные cookie")
    elif check_all_args(User, data, "login", "password"):
        exist_user = db.session.execute(select(User).where(User.login == data['login'])).first()
        if not exist_user:
            return message("Неверный логин", 404)
        exist_user: User = exist_user[0]
        if exist_user.status_id == 2:
            return delete_cookie("Вы заблокированы")
        if not check_password_hash(exist_user.password_hash, data['password']):
            return message("Неверный пароль.", 403)
        return send_cookie(exist_user.id, exist_user.uuid, exist_user.login)
    else:
        return message("Недостаточно данных", 406)


@user_api.route("/logout", methods=["GET", "POST"])
def logout():
    resp = make_response(jsonify({"message": "Okay"}))
    resp.status = 200
    resp.set_cookie("auth", '', expires=0, secure=False, httponly=False)
    return resp


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


@user_api.route("/get", methods=["GET"])
@login_required
def get():
    @admin_required
    def get_all_users():
        users = [user[0] for user in db.session.execute(select(User).where(User.login != "admin")).all()]
        return send_json_data(make_json_response(
            users,
            additional=["uuid", "status_id"],
            exclude=["statistic", "password_hash"],
        ))

    uuid = None
    login = None
    if 'auth' in request.cookies:
        token = request.cookies['auth']
        id_, uuid, login = (jwt.decode(token, JWT_SECRET_KEY, algorithms=["HS256"])).values()
    if "uuid" in request.args:
        if not uuid or login == "admin":
            uuid = request.args['uuid']
        user = db.session.execute(select(User).where(User.uuid == uuid)).first()
        if not user:
            return message("Неверный uuid.", 404)
        user: User = user[0]
        return send_json_data(make_json_response(
            user,
            additional=["uuid"],
            exclude=["statistic", "password_hash"],
        ))
    else:
        return get_all_users()
