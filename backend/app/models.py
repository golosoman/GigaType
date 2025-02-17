import datetime
from typing import List
from uuid import uuid4
from sqlalchemy.orm import DeclarativeBase, declared_attr, Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey, Table, Column
from datetime import datetime, timezone

from app import db


class Base(db.Model):
    __abstract__ = True
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    @declared_attr.directive
    def __tablename__(self) -> str:
        # if self.__name__.lower()[]
        return self.__name__.lower()


class Status(Base):
    # __tablename__ = "statuses"
    status: Mapped[str] = mapped_column(String(16), unique=True)

    def __init__(self, status: str):
        self.status = status


class User(Base):
    login: Mapped[str] = mapped_column(String(10), unique=True)
    uuid: Mapped[str] = mapped_column(String(36), unique=True)
    password_hash: Mapped[str] = mapped_column(String(256))
    status_id: Mapped[int] = mapped_column(ForeignKey('status.id'))
    statistic: Mapped[List["Statistic"]] = relationship(
        back_populates="user",
        cascade="all, delete",
        passive_deletes=True,
    )
    photo_path: Mapped[str] = mapped_column(String(128))

    def __init__(self,
                 login: str,
                 password_hash: str
                 ):
        self.login = login
        self.uuid = str(uuid4())
        self.password_hash = password_hash
        self.status_id = 1
        # TODO: выбрать оптимальный способ хранения пути до фото (абсолютный, но с перезаписью, если нужно
        #  разворачивать на другой системе, относительный или просто хранить название файла) separator = os.path.sep
        #  self.photo_path = f"{os.getcwd()}{separator}app{separator}static{separator}profiles_photo{separator}{
        #  self.uuid}.png"
        self.photo_path = f"{self.uuid}.png"


difficulty_zone = Table(
    "difficulty_zone",
    Base.metadata,
    Column("difficulty_id", ForeignKey("difficulty.id", ondelete="CASCADE")),
    Column("keyboardzone_id", ForeignKey("keyboardzone.id", ondelete="CASCADE"))
)

task_zone = Table(
    "task_zone",
    Base.metadata,
    Column("task_id", ForeignKey("task.id", ondelete="CASCADE")),
    Column("keyboardzone_id", ForeignKey("keyboardzone.id", ondelete="CASCADE"))
)


class KeyBoardZone(Base):
    uid: Mapped[str] = mapped_column(String(36), unique=True)
    keys: Mapped[str] = mapped_column(String(32), unique=True)
    difficulty: Mapped[List["Difficulty"]] = relationship(
        secondary=difficulty_zone,
        back_populates="zones",
    )
    task: Mapped[List["Task"]] = relationship(
        secondary=task_zone,
        back_populates="zones"
    )

    def __init__(self, keys: str):
        self.uid = str(uuid4())
        self.keys = keys


class Task(Base):
    uid: Mapped[str] = mapped_column(String(36), unique=True)
    name: Mapped[str] = mapped_column(String(16))
    content: Mapped[str] = mapped_column(String(256))
    difficulty_id: Mapped[int] = mapped_column(ForeignKey("difficulty.id", ondelete="CASCADE"))
    difficulty: Mapped["Difficulty"] = relationship(
        back_populates="tasks",
        uselist=False
    )
    zones: Mapped[List["KeyBoardZone"]] = relationship(
        secondary=task_zone,
        back_populates="task"
    )

    def __init__(self,
                 name: str,
                 content: str,
                 difficulty_id: int = None,
                 difficulty=None,
                 zones=None
                 ):
        self.uid = str(uuid4())
        self.name = name
        self.content = content
        if difficulty_id:
            self.difficulty_id = difficulty_id
        if difficulty:
            self.difficulty = difficulty
        if zones:
            self.zones = zones


class Difficulty(Base):
    # __tablename__ = "difficulties"
    uid: Mapped[str] = mapped_column(String(36), unique=True)
    name: Mapped[str] = mapped_column(String(8), unique=True)
    min_length: Mapped[int]
    max_length: Mapped[int]
    key_press_time: Mapped[float]
    max_mistakes: Mapped[int]
    zones: Mapped[List["KeyBoardZone"]] = relationship(
        secondary=difficulty_zone,
        back_populates="difficulty"
    )
    tasks: Mapped[List["Task"]] = relationship(
        back_populates="difficulty",
        cascade="all, delete",
        passive_deletes=True,
    )

    def __init__(self,
                 name: str,
                 min_length: int,
                 max_length: int,
                 key_press_time: float,
                 max_mistakes: int,
                 zones: KeyBoardZone | List["KeyBoardZone"],
                 tasks: Task | List["Task"] = None):
        self.uid = str(uuid4())
        self.name = name
        self.min_length = min_length
        self.max_length = max_length
        self.key_press_time = key_press_time
        self.max_mistakes = max_mistakes
        if type(zones) is list:
            self.zones = zones
        else:
            self.zones = [zones]
        if tasks:
            if type(tasks) is list:
                self.tasks = tasks
            else:
                self.tasks = [tasks]


class Statistic(Base):
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id", ondelete="CASCADE"))
    user: Mapped["User"] = relationship(back_populates="statistic")
    task_id: Mapped[int] = mapped_column(ForeignKey("task.id", ondelete="CASCADE"))
    task: Mapped["Task"] = relationship()
    timestamp: Mapped[datetime] = mapped_column(default=lambda: datetime.now(timezone.utc))
    used_time: Mapped[float]
    mistakes: Mapped[int]
    # average_key_press_time: Mapped[float]
    clicks_number: Mapped[int]
    clicks_per_minute: Mapped[int]
    success: Mapped[bool]
    score: Mapped[int]

    def __init__(self,
                 user_id: int,
                 task_id: int,
                 used_time: float,
                 mistakes: int,
                 clicks_number: int,
                 success: bool,
                 score: int,
                 clicks_per_minute: int = None,
                 timestamp: datetime = None
                 ):
        self.user_id = user_id
        self.task_id = task_id
        self.used_time = used_time
        self.mistakes = mistakes
        self.clicks_number = clicks_number
        self.success = success
        self.score = score
        if clicks_per_minute:
            self.clicks_per_minute = clicks_per_minute
        else:
            from app.utils import correct_rounding
            self.clicks_per_minute = correct_rounding(clicks_number*60/used_time)
        if timestamp:
            self.timestamp = timestamp
