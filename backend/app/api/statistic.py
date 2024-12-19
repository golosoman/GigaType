import json
import pprint
from typing import List

from flask import Blueprint, request, make_response
from sqlalchemy import select, and_, delete, func

from app import db
from app.models import Statistic, Task, User, Difficulty
from app.utils import (admin_required, message, send_json_data, check_all_args, check_one_arg, make_json_response,
                       util_round, login_required, is_logged, get_args)

statistic_api = Blueprint('statistic_api', __name__, url_prefix="/stat")


@statistic_api.route("/create", methods=["POST"])
@login_required
def create():
    _, token_data = is_logged()
    user = db.session.execute(select(User).where(
        and_(
            User.id == token_data["id"],
            User.uuid == token_data["uuid"]
        )
    )).first()
    if not user:
        return message("Неверный uuid пользователя", 404)
    user: User = user[0]
    data = request.json
    if check_all_args(Statistic, data, additional=["task_uid"], exclude=["user_id", "task_id", "timestamp", "clicks_per_minute"]):
        task = db.session.execute(select(Task).where(Task.uid == data['task_uid'])).first()
        if not task:
            return message("Неверный uid задания.", 404)
        task: Task = task[0]
        try:
            db.session.add(Statistic(
                user_id=user.id,
                task_id=task.id,
                used_time=data['used_time'],
                mistakes=data["mistakes"],
                clicks_number=data["clicks_number"],
                success=data['success'],
                score=data['score']
            ))
            db.session.commit()
            return message("Okay")
        except BaseException as e:
            print(str(e))
            db.session.rollback()
            db.session.commit()
            return message("Произошла ошибка", 500)
    else:
        return message("Недостаточно данных", 406)


@statistic_api.route("/get", methods=["GET"])
@login_required
def get():
    _, token_data = is_logged()
    if "user_uuid" in request.args and "difficulty_uid" in request.args:

        user = db.session.execute(select(User).where(User.uuid == request.args["user_uuid"])).first()
        if not user:
            return message("Неверный uuid пользователя.", 404)
        user: User = user[0]

        if user.status_id == 2:
            return message("Пользователь заблокирован", 418)

        difficulty = db.session.execute(
            select(Difficulty).where(Difficulty.uid == request.args["difficulty_uid"])).first()
        if not difficulty:
            return message("Неверный uid сложности.", 404)
        difficulty: Difficulty = difficulty[0]

        statistic_list = []

        from app.api.task import get
        tasks_data = json.loads(get()[0])
        for task_data in tasks_data:
            task_id = db.session.execute(select(Task.id).where(Task.uid == task_data["uid"])).first()[0]

            query = select(Statistic).where(
                and_(
                    Statistic.user_id == user.id,
                    Statistic.task_id == task_id
                )
            ).order_by(Statistic.timestamp)

            statistic_list += [stat[0] for stat in db.session.execute(query).all()]

        task_args = get_args(Task)
        task_args.remove("name")

        resp = make_json_response(
            statistic_list,
            additional=["task"],
            exclude=["user_id", "task_id"] + task_args,
            get={
                "difficulty": "max_mistakes"
            })
        for stat in resp:
            stat["max_mistakes"] = stat["task"][0]["max_mistakes"]
            stat['name'] = stat['task'][0]['name']
            stat.pop("task")
        return send_json_data(resp)

    elif "difficulty_uid" in request.args:
        class StatisticInfo:
            name = ""
            attempts = []

            def __init__(self):
                pass

        difficulty = db.session.execute(
            select(Difficulty).where(Difficulty.uid == request.args["difficulty_uid"])).first()
        if not difficulty:
            return message("Неверный uid сложности.", 404)
        difficulty: Difficulty = difficulty[0]

        stat_info_list = []

        from app.api.task import get
        tasks_data = json.loads(get()[0])
        for task_data in tasks_data:
            task_id = db.session.execute(select(Task.id).where(Task.uid == task_data["uid"])).first()[0]
            query = select(func.count()).where(and_(
                Statistic.task_id == task_id,
                User.status_id != 2
            )).group_by(Statistic.task_id).join(User).select_from(Statistic)
            all_amount = db.session.execute(query).first()

            if not all_amount:
                continue

            all_amount = all_amount[0]

            success_amount = db.session.execute(query.where(Statistic.success==True)).first()
            if not success_amount:
                success_amount = 0
            else:
                success_amount = success_amount[0]

            temp = StatisticInfo()

            temp.name = task_data["name"]
            temp.attempts = [all_amount, success_amount]

            stat_info_list.append(temp)

        return send_json_data(make_json_response(stat_info_list))

    elif "user_uuid" in request.args:
        user = db.session.execute(select(User).where(User.uuid == request.args["user_uuid"])).first()
        if not user:
            return message("Неверный uuid пользователя.", 404)
        user: User = user[0]

        if user.status_id == 2:
            return message("Пользователь заблокирован", 418)

        statistics = [statistic[0] for statistic in
                      db.session.execute(select(Statistic)
                                         .where(
                          Statistic.user_id == user.id
                      ).order_by(Statistic.timestamp)).all()]
        return send_json_data(
            make_json_response(statistics, "clicks_per_minute", "timestamp", "task", exclude=["task"], get={"task": "uid"}))


@statistic_api.route("/top", methods=["GET"])
@login_required
def top():
    class TopInfo:
        login = ""
        scores = 0

        def __init__(self):
            pass
    query = (select(User.login, func.sum(Statistic.score).label("scores"))
        .where(
            and_(
                Statistic.user_id != 1,
                Statistic.success == 1,
                User.status_id != 2
            )
        ).group_by(Statistic.user_id)
        .join(User).select_from(Statistic))
    statistics = db.session.execute(query).all()
    top_list = []
    for statistic in statistics:
        temp = TopInfo()
        temp.login = statistic[0]
        temp.scores = int(statistic[1])
        top_list.append(temp)
    top_list.sort(key=lambda x: x.scores)
    top_list.reverse()
    return send_json_data(make_json_response(top_list))