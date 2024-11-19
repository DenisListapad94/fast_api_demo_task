
from datetime import datetime

from sqlalchemy import DateTime, String, Integer, Enum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.const import TaskStatuses, Roles
from src.core.orm.base import Base

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)
    first_name: Mapped[str] = mapped_column(String, nullable=True)
    last_name: Mapped[str] = mapped_column(String, nullable=True)
    role: Mapped[Roles] = mapped_column(String, nullable=True)
    password: Mapped[str] = mapped_column(String, nullable=False)
    email: Mapped[str]= mapped_column(String, nullable=False)

    created: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated: Mapped[datetime] = mapped_column(DateTime,nullable=True)

    tasks: Mapped[list["Tasks"]] = relationship(
        argument="Tasks",
        back_populates='user',
        lazy="selectin"
    )
