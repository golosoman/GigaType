import copy
from typing import List

from flask import Blueprint, request
from sqlalchemy import select, delete

from app import db
from app.api.task import check_content
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
        return message("Достигнуто максимальное количество уровней сложности (12).", 418)
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
                return message("Неверный uid зоны клавиатуры", 404)
            zones.append(zone[0])

        # Проверка уникальности по параметрам
        existing_difficulties = db.session.execute(
            select(Difficulty).where(
                    Difficulty.min_length == data['min_length'],
                    Difficulty.max_length == data['max_length'],
                    Difficulty.key_press_time == data['key_press_time'],
                    Difficulty.max_mistakes == int(data['max_mistakes']),
            )
        ).all()

        for existing_difficulty_tuple in existing_difficulties:
            existing_difficulty = existing_difficulty_tuple[0]  # Извлекаем объект Difficulty
            existing_zones = existing_difficulty.zones  # Получаем связанные зоны
            existing_zone_ids = {zone.uid for zone in existing_zones}
            # print(existing_zone_ids)
            new_zone_ids = set(data['zones'])
            # print(new_zone_ids)
            if existing_zone_ids == new_zone_ids:
                return message("Уровень сложности с такими параметрами уже существует", 406)
            
        try:
            db.session.add(
                Difficulty(
                    data['name'],
                    data['min_length'],
                    data['max_length'],
                    data['key_press_time'],
                    int(data['max_mistakes']),
                    zones
                )
            )
            db.session.commit()
            difficulty = db.session.execute(select(Difficulty).where(Difficulty.name == data['name'])).first()
            if not difficulty:
                return message("Неверный uid.", 404)
            difficulty: Difficulty = difficulty[0]
            return send_json_data(make_json_response(difficulty, additional=['uid'], exclude=["difficulty"]))
            # return send_json_data(make_json_response(last_difficulty, additional=['uid'], exclude=["difficulty"]))
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
    data: dict = copy.copy(request.json)
    if check_one_arg(Difficulty, data, should_be=["uid"]):
        difficulty = db.session.execute(select(Difficulty).where(Difficulty.uid == data['uid'])).first()
        if not difficulty:
            return message("Неверный id сложности.", 404)
        difficulty: Difficulty = difficulty[0]
        data.pop('uid')
        try:
            # Проверка уникальности по параметрам
            existing_difficulties = db.session.execute(
                select(Difficulty).where(
                        Difficulty.min_length == data['min_length'],
                        Difficulty.max_length == data['max_length'],
                        Difficulty.key_press_time == data['key_press_time'],
                        Difficulty.max_mistakes == int(data['max_mistakes']),
                )
            ).all()

            for existing_difficulty_tuple in existing_difficulties:
                existing_difficulty = existing_difficulty_tuple[0]  # Извлекаем объект Difficulty
                existing_zones = existing_difficulty.zones  # Получаем связанные зоны
                existing_zone_ids = {zone.uid for zone in existing_zones}
                # print(existing_zone_ids)
                new_zone_ids = set(data['zones'])
                # print(new_zone_ids)
                if existing_zone_ids == new_zone_ids:
                    return message("Уровень сложности с такими параметрами уже существует", 406)
            for arg in data:
                if arg == "zones":
                    zones: List["KeyBoardZone"] = []
                    for uid in data['zones']:
                        zone = db.session.execute(select(KeyBoardZone).where(KeyBoardZone.uid == uid)).first()
                        if not zone:
                            return message("Неверный id зоны клавиатуры", 404)
                        zones.append(zone[0])
                    if difficulty.zones != zones:
                        difficulty.zones = zones
                        for task in difficulty.tasks:
                            request.json['uids'] = request.json["zones"]
                            check_content(task, zones)
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
        return send_json_data(make_json_response(difficulty, additional=['uid'], exclude=["difficulty"]))
    else:
        difficulties = [difficulty[0] for difficulty in db.session.execute(select(Difficulty)).all()]
        difficulties.sort(key=lambda x: int(x.__getattribute__("name")))
        return send_json_data(make_json_response(difficulties, additional=["uid"], exclude=["difficulty", "difficulty_id"]))

