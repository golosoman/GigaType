from typing import List

import jwt
from flask import Blueprint, request, make_response
from sqlalchemy import select, and_, delete
from werkzeug.security import generate_password_hash, check_password_hash

from app import db
from app.models import Difficulty, KeyBoardZone
from app.utils import admin_required, message, check_all_args, check_one_arg
from config import JWT_SECRET_KEY

difficulty_api = Blueprint('difficulty_api', __name__, url_prefix="/difficulty")


@difficulty_api.route("/create", methods=["POST"])
@admin_required
def create():
    """
    URL запроса: /api/difficulty/create
    Payload: json{name: str, min_length: int, max_length: int, key_press_time: float, max_mistakes: int, zones: list[str]}
    :return: {message: str}, code, Content-Type
    """
    data = request.json
    if 'tasks' not in data:
        data['tasks'] = []
    if check_all_args(Difficulty, data):
        if db.session.execute(select(Difficulty).where(Difficulty.name == data['name'])).first():
            return message("Название уже используется.", 406)
        if not data['zones']:
            return message("Должна быть выбрана хотя бы одна зона клавиатуры", 406)
        zones: List["KeyBoardZone"] = []
        for uid in data['zones']:
            zone = db.session.execute(select(KeyBoardZone).where(KeyBoardZone.uid == uid)).first()
            if not zone:
                return message("Неверный id зоны клавиатуры", 404)
            zones.append(zone[0])
        try:
            db.session.add(
                Difficulty(
                    data['name'],
                    data['min_length'],
                    data['max_length'],
                    data['key_press_time'],
                    data['max_mistakes'],
                    zones
                )
            )
            db.session.commit()
            return message("Okay", 200)
        except BaseException as e:
            print(str(e))
            db.session.rollback()
            return message("Произошла ошибка", 500)
    else:
        return message("Недостаточно данных", 406)


@difficulty_api.route("/update", methods=["PATCH"])
@admin_required
def update_():
    """
    URL запроса: /api/difficulty/update
    Payload: json{uid:str, name: str | min_length: int | max_length: int | key_press_time: float | max_mistakes: int | zones: list[str]}
    :return: {message: str}, code, Content-Type
    """
    data: dict = request.json
    if check_one_arg(Difficulty, data) and 'uid' in data:
        difficulty = db.session.execute(select(Difficulty).where(Difficulty.uid == data['uid'])).first()
        if not difficulty:
            return message("Неверный id сложности.", 404)
        difficulty: Difficulty = difficulty[0]
        data.pop('uid')
        try:
            for arg in data:
                if arg == "zones":
                    zones: List["KeyBoardZone"] = []
                    for uid in data['zones']:
                        zone = db.session.execute(select(KeyBoardZone).where(KeyBoardZone.uid == uid)).first()
                        if not zone:
                            return message("Неверный id зоны клавиатуры", 404)
                        zones.append(zone[0])
                    difficulty.zones = zones
                else:
                    difficulty.__setattr__(arg, data[arg])
                db.session.commit()
        except BaseException as e:
            print(str(e))
            db.session.rollback()
            db.session.commit()
            return message("Произошла ошибка", 500)

        return message("Okay", 200)
    else:
        return message("Недостаточно данных", 406)


@difficulty_api.route("/delete", methods=["DELETE"])
@admin_required
def delete_():
    """
    URL запроса: /api/difficulty/update
    Payload: json{uid:str}
    :return: {message: str}, code, Content-Type
    """
    data: dict = request.json
    if 'uid' in data:
        difficulty = db.session.execute(select(Difficulty).where(Difficulty.uid == data['uid'])).first()
        if not difficulty:
            return message("Неверный id сложности.", 404)
        try:
            db.session.execute(delete(Difficulty).where(Difficulty.uid == data['uid']))
            db.session.commit()
            return message("Okay", 200)
        except BaseException as e:
            print(str(e))
            db.session.rollback()
            db.session.commit()
            return message("Произошла ошибка", 500)
    else:
        return message("Недостаточно данных", 406)


