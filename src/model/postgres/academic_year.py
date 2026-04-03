from datetime import date, datetime
from sqlalchemy import Date, String, event
from sqlalchemy.orm import Mapped, mapped_column

from src.model.postgres.base import Base

class AcademicYear(Base):
    __tablename__ = "academic_year"
    code: Mapped[str] = mapped_column(String(20), primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    start_date: Mapped[date] = mapped_column(Date, nullable=False)
    end_date: Mapped[date] = mapped_column(Date, nullable=False)

@event.listens_for(AcademicYear, "before_insert")
@event.listens_for(AcademicYear, "before_update")
def validate(mapper, connection, target):
    if not target.code:
        raise ValueError("academic year's code cannot be empty")
    if not target.name:
        raise ValueError("academic year's name cannot be empty")
    if not target.start_date:
        raise ValueError("academic year's start date cannot be empty")
    if not target.end_date:
        raise ValueError("academic year's end date cannot be empty")
    try:
        if not isinstance(target.start_date, date):
            start = datetime.strptime(target.start_date, "%Y-%m-%d")
        if not isinstance(target.end_date, date):
            end = datetime.strptime(target.end_date, "%Y-%m-%d")
    except ValueError:
        raise ValueError("academic year's date must be in format YYYY-MM-DD")
    if start > end:
        raise ValueError("academic year's start date must be before end date")