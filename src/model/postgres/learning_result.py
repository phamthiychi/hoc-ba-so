from datetime import date, datetime
from sqlalchemy import String, Date, ForeignKey, Text, event
from sqlalchemy.orm import Mapped, mapped_column

from src.model.postgres.base import Base

class LearningResult(Base):
    __tablename__ = "learning_result"
    student_code: Mapped[str] = mapped_column(
        String(20),
        ForeignKey("student.code"),
        primary_key=True
    )
    class_code: Mapped[str] = mapped_column(
        String(20),
        ForeignKey("class_room.code"),
        primary_key=True
    )
    academic_year_code: Mapped[str] = mapped_column(
        String(20),
        ForeignKey("academic_year.code"),
        primary_key=True
    )
    semester_code: Mapped[str] = mapped_column(
        String(20),
        ForeignKey("semester.code"),
        primary_key=True
    )
    score_code: Mapped[str] = mapped_column(
        String(20),
        ForeignKey("score.code"),
        primary_key=True
    )
    subject_code: Mapped[str] = mapped_column(
        String(20),
        ForeignKey("subject.code"),
        primary_key=True
    )
    enrollment_date: Mapped[date] = mapped_column(Date, nullable=False)
    note: Mapped[str | None] = mapped_column(Text)

@event.listens_for(LearningResult, "before_insert")
@event.listens_for(LearningResult, "before_update")
def validate(mapper, connection, target):
    if not target.student_code:
        raise ValueError("class enrollment's student code cannot be empty")
    if not target.class_code:
        raise ValueError("class enrollment's class code cannot be empty")
    if not target.academic_year_code:
        raise ValueError("class enrollment's academic year code cannot be empty")
    if not target.semester_code:
        raise ValueError("class enrollment's semester code cannot be empty")
    if not target.score_code:
        raise ValueError("class enrollment's score code cannot be empty")
    if not target.subject_code:
        raise ValueError("class enrollment's subject code cannot be empty")
    if not target.enrollment_date:
        raise ValueError("class enrollment's enrollment date cannot be empty")
    try:
        if not isinstance(target.enrollment_date, date):
            datetime.strptime(target.enrollment_date, "%Y-%m-%d")
    except ValueError:
        raise ValueError("class enrollment's enrollment date must be in format YYYY-MM-DD")