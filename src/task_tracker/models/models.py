from datetime import datetime

from sqlalchemy import DateTime, String, Integer, Enum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.const import TaskStatuses
from src.core.orm.base import Base


class Tasks(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)
    title: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=True)
    status: Mapped[TaskStatuses] = mapped_column(String, nullable=True)
    created: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated: Mapped[datetime] = mapped_column(DateTime,nullable=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    comments: Mapped[list["Comment"]] = relationship(
        argument="Comment",
        back_populates='task',
        lazy="selectin"
    )

    tags_list: Mapped[list["Tag"]] = relationship(
        argument="TaskTag",
        back_populates='task',
        lazy="selectin"
    )

    user: Mapped[list["User"]] = relationship(
        argument="User",
        back_populates='tasks',
        lazy="selectin"
    )


class Comment(Base):
    __tablename__ = "comments"
    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)

    comment: Mapped[str] = mapped_column(String, nullable=False)
    rating: Mapped[int] = mapped_column(Integer, nullable=True )
    created: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated: Mapped[datetime] = mapped_column(DateTime,nullable=True)


    task: Mapped["Tasks"] = relationship(
        argument="Tasks",
        back_populates='comments',
        lazy='selectin'
    )

    task_id: Mapped[int] = mapped_column(ForeignKey("tasks.id"))


class TaskTag(Base):
    __tablename__ = "task_tags"
    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)

    task_id: Mapped[int] = mapped_column(ForeignKey("tasks.id"))
    tag_id: Mapped[int] = mapped_column(ForeignKey("tags.id"))

    task: Mapped[list["Tasks"]] = relationship(
        argument="Tasks",
        back_populates='tags_list',
    )

    tag: Mapped[list["Tag"]] = relationship(
        argument="Tag",
        back_populates='tasks_list',
    )

class Tag(Base):
    __tablename__ = "tags"

    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)

    created: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated: Mapped[datetime] = mapped_column(DateTime,nullable=True)

    tasks_list: Mapped["Tag"] = relationship(
        argument="TaskTag",
        back_populates='tag',
        lazy="selectin"
    )




# class User(Base):
#     __tablename__ = "comments"
#     id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True, unique=True)
#
#     comment: Mapped[str] = mapped_column(String, nullable=True)
#
#     created: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
#     updated: Mapped[datetime] = mapped_column(DateTime, nullable=True)
