# import datetime
# import os.path
#
#
# class Fs:
#     @staticmethod
#     def name():
#         if Fs.__name__.lower().endswith(("ch", "sh", "s", "x")):
#             print(Fs.__name__.lower()+"es")
#         elif Fs.__name__.lower().endswith("y") and Fs.__name__.lower()[-2] in set("bcdfghjklmnpqrstvwxyz"):
#             print(Fs.__name__.lower()[:-2]+"ies")
#
# Fs.name()
#
# print(type(datetime.datetime.now()))
# print(datetime.datetime.now())
import datetime

from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session
from werkzeug.security import generate_password_hash
from config import Config

from app.models import *

db = create_engine(Config.SQLALCHEMY_DATABASE_URI)
with Session(db) as session:
    if len(session.execute(select(Status)).all()) == 0:
        session.add_all([Status("trainee"), Status("banned")])
        session.commit()
    if len(session.execute(select(KeyBoardZone)).all()) == 0:
        session.add_all([
            KeyBoardZone("фываолдж"),
            KeyBoardZone("пр"),
            KeyBoardZone("кенг"),
            KeyBoardZone("мить"),
            KeyBoardZone("усшб"),
            KeyBoardZone("цчщю"),
            KeyBoardZone("ёйязхъэ.,"),
            KeyBoardZone("1234567890"),
            # '!', '"', '№', ';', '%', ':', '?', '*', '(', ')', '_', '-', '+', '='
            KeyBoardZone("""!\"№;%:?*()_-+=""")
        ])
        session.commit()
    if len(session.execute(select(User).where(User.login == "admin")).all()) == 0:
        session.add(User("admin", generate_password_hash("123456789!")))
        session.commit()
    if len(session.execute(select(Difficulty)).all()) == 0:
        zones = [zone[0] for zone in session.execute(select(KeyBoardZone))]
        print(zones)
        session.add_all([
            Difficulty("10", 1, 1, 0.5, 5, zones, None),
            Difficulty("11", 1, 1, 0.5, 5, zones, None),
            Difficulty("12", 1, 1, 0.5, 5, zones, None)
        ])
        session.commit()
    # session.add_all([
    #     Statistic(2, 2, 12, 1, 20, True, 201),
    #     Statistic(2, 2, 10, 1, 15, True, 100),
    #     Statistic(2, 2, 21, 5, 20, False, 0),
    #     Statistic(2, 1, 12, 1, 20, True, 201),
    #     Statistic(2, 1, 5, 6, 20, False, 0)
    # ])
    # session.commit()
