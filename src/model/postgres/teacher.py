from datetime import date, datetime
from sqlalchemy import String, Date, Integer, event
from sqlalchemy.orm import Mapped, mapped_column

from src.model.postgres.base import Base

class Teacher(Base):
    __tablename__ = "teacher"
    code: Mapped[str] = mapped_column(String(20), primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    card_id: Mapped[str | None] = mapped_column(String(20))
    edu_id: Mapped[str | None] = mapped_column(String(20))
    date_of_birth: Mapped[date] = mapped_column(Date, nullable=False)
    gender: Mapped[str] = mapped_column(String(10), nullable=False)
    ethnicity: Mapped[str] = mapped_column(String(20), nullable=False)
    status: Mapped[str | None] = mapped_column(String(30))
    specialization: Mapped[str | None] = mapped_column(String(50))
    position: Mapped[str | None] = mapped_column(String(50))
    phone: Mapped[str | None] = mapped_column(String(15))
    nationality: Mapped[str] = mapped_column(String(50), nullable=False)

@event.listens_for(Teacher, "before_insert")
@event.listens_for(Teacher, "before_update")
def validate(mapper, connection, target):
    if not target.code:
        raise ValueError("teacher's code cannot be empty")
    if not target.name:
        raise ValueError("teacher's name cannot be empty")
    if not target.date_of_birth:
        raise ValueError("teacher's date of birth cannot be empty")
    try:
        if not isinstance(target.date_of_birth, date):
            datetime.strptime(target.date_of_birth, "%Y-%m-%d")
    except ValueError:
        raise ValueError("teacher's date of birth must be in format YYYY-MM-DD")
    if not target.gender:
        raise ValueError("teacher's gender cannot be empty")
    if not target.nationality:
        raise ValueError("teacher's nationality cannot be empty")