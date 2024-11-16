from typing import List

from flask import Blueprint, request, make_response
from sqlalchemy import select, and_, delete

from app import db
from app.models import Difficulty, KeyBoardZone
from app.utils import (admin_required, message, send_json_data, check_all_args, check_one_arg, make_json_response,
                       util_round, login_required)

difficulty_api = Blueprint('difficulty_api', __name__, url_prefix="/difficulty")


@difficulty_api.route("/create", methods=["POST"])
@admin_required
def create():
    """
    URL запроса: /api/difficulty/create
    Payload: json{name: str, min_length: int, max_length: int, key_press_time: float, max_mistakes: int, zones: list[str]}
    :return: {message: str}, code, Content-Type
    """
    if len(db.session.execute(select(Difficulty)).all()) == 12:
        return message("Достигнуто максимальное количество уровней сложности (12).", 403)
    data = request.json
    if check_all_args(Difficulty, data, exclude=["tasks", "name", "max_mistakes"]):
        if len(db.session.execute(select(Difficulty)).all()) == 3:
            data['name'] = "1"
        else:
            name = db.session.execute(select(Difficulty.name).order_by(Difficulty.id.desc())).first()
            data['name'] = str(int(name[0])+1)
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
                    util_round(int(data['max_length'])*0.1),
                    zones
                )
            )
            db.session.commit()
            return message("Okay", 200)
        except BaseException as e:
            print(str(e))
            db.session.rollback()
            db.session.commit()
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
                    if difficulty.__getattribute__(arg)!=data[arg]:
                        difficulty.__setattr__(arg, data[arg])
            db.session.commit()
            return message("Okay", 200)
        except BaseException as e:
            print(str(e))
            db.session.rollback()
            db.session.commit()
            return message("Произошла ошибка", 500)
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


@difficulty_api.route("/get", methods=["GET"])
@login_required
def get():
    uid = None
    if 'uid' in request.args:
        uid = request.args['uid']
    if uid:
        difficulty = db.session.execute(select(Difficulty).where(Difficulty.uid == uid)).first()
        if not difficulty:
            return message("Неверный uid.", 404)
        difficulty: Difficulty = difficulty[0]
        return send_json_data(make_json_response(difficulty))
    else:
        difficulties = [difficulty[0] for difficulty in db.session.execute(select(Difficulty)).all()]
        difficulties.sort(key=lambda x: int(x.__getattribute__("name")))
        return send_json_data(make_json_response(difficulties, additional=["uid"], exclude=["difficulty"]))

