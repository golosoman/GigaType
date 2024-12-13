import pprint
from typing import List

from flask import Blueprint, request, make_response
from sqlalchemy import select, and_, delete

from app import db
from app.models import Task, Difficulty
from app.utils import (admin_required, message, send_json_data, check_all_args, check_one_arg, make_json_response,
                       util_round, login_required)

task_api = Blueprint('task_api', __name__, url_prefix="/task")


@task_api.route("/create", methods=["POST"])
@admin_required
def create():
    """
    URL запроса: /api/task/create
    Payload: json{content: str, difficulty_id: str}
    :return: {message: str}, code, Content-Type
    """
    data = request.json
    if check_all_args(Task, data, exclude=["difficulty", "name"]):
        difficulty = db.session.execute(select(Difficulty).where(Difficulty.uid == data['difficulty_id'])).first()
        if not difficulty:
            return message("Неверный uid сложности.", 404)
        difficulty: Difficulty = difficulty[0]

        if len(db.session.execute(select(Task).where(Task.difficulty_id==difficulty.id)).all()) == 20:
            return message("Достигнуто максимальное количество упражнений для данного уровня.", 418)

        if len(db.session.execute(select(Task).where(Task.difficulty_id == difficulty.id)).all()) == 0:
            data["name"] = "1"
        else:
            name = db.session.execute(select(Task.name).where(Task.difficulty_id==difficulty.id).order_by(Task.id.desc())).first()
            data["name"] = str(int(name[0])+1)
        if db.session.execute(select(Task).where(and_(Task.name==data['name'], Task.difficulty_id==difficulty.id))).first():
            return message("Название уже используется.", 406)
        try:
            db.session.add(
                Task(
                    name=data['name'],
                    content=data['content'],
                    difficulty=difficulty
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
        message("Недостаточно данных", 406)


@task_api.route("/update", methods=["PATCH"])
@admin_required
def update_():
    """
    URL запроса: /api/task/update
    Payload: json{uid: str, content: str, difficulty_id: str}
    :return: {message: str}, code, Content-Type
    """
    data: dict = request.json
    if check_one_arg(Task, data, should_be=['uid']):
        task = db.session.execute(select(Task).where(Task.uid==data['uid'])).first()
        if not task:
            return message("Неверный uid задания.", 404)
        task: Task = task[0]
        data.pop('uid')
        try:
            for arg in data:
                if arg == "difficulty_id":
                    difficulty = db.session.execute(select(Difficulty).where(Difficulty.uid == data[arg])).first()
                    if not difficulty:
                        return message("Неверный uid сложности", 404)
                    task.difficulty = difficulty[0]
                else:
                    if task.__getattribute__(arg) != data[arg]:
                        task.__setattr__(arg, data[arg])
            db.session.commit()
            return message("Okay", 200)
        except BaseException as e:
            print(str(e))
            db.session.rollback()
            db.session.commit()
            return message("Произошла ошибка", 500)
    else:
        return message("Недостаточно данных", 406)


@task_api.route("/delete", methods=["DELETE"])
@admin_required
def delete_():
    """
    URL запроса: /api/task/update
    Payload: json{uid:str}
    :return: {message: str}, code, Content-Type
    """
    data: dict = request.json
    if 'uid' in data:
        task = db.session.execute(select(Task).where(Task.uid==data['uid'])).first()
        if not task:
            return message("Неверный uid задания", 404)
        try:
            db.session.execute(delete(Task).where(Task.uid==data['uid']))
            db.session.commit()
            return message("Okay", 200)
        except BaseException as e:
            print(str(e))
            db.session.rollback()
            db.session.commit()
            return message("Произошла ошибка", 500)
    else:
        return message("Недостаточно данных", 406)


@task_api.route("/get", methods=["GET"])
@login_required
def get():
    uid = None
    if 'uid' in request.args:
        uid = request.args['uid']
    if uid:
        task = db.session.execute(select(Task).where(Task.uid==uid)).first()
        if not task:
            return message("Неверный uid задания", 404)
        task: Task = task[0]
        return send_json_data(make_json_response(task, additional=['uid'], exclude=["difficulty", "difficulty_id"], get={"difficulty": ["uid", "name"]}))
    elif "difficulty_uid" in request.args:
        difficulty = db.session.execute(select(Difficulty).where(Difficulty.uid==request.args['difficulty_uid'])).first()
        if not difficulty:
            return message("Неверный uid сложности", 404)
        difficulty: Difficulty = difficulty[0]
        tasks = [task[0] for task in db.session.execute(select(Task).where(Task.difficulty_id==difficulty.id)).all()]
        tasks.sort(key=lambda x: int(x.__getattribute__("name")))
        return send_json_data(make_json_response(tasks, additional=['uid'], exclude=["difficulty", "difficulty_id"], get={"difficulty": ["uid", "name"]}))
    else:
        tasks = [task[0] for task in db.session.execute(select(Task)).all()]
        tasks.sort(key=lambda x: (int(getattr(getattr(x, "difficulty"), "name")), int(getattr(x, "name"))))
        return send_json_data(make_json_response(tasks, additional=['uid'], exclude=["difficulty", "difficulty_id"], get={"difficulty": ["uid", "name"]}))