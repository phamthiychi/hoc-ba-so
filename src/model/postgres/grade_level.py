from sqlalchemy import String, Integer, event
from sqlalchemy.orm import Mapped, mapped_column

from src.model.postgres.base import Base

class GradeLevel(Base):
    __tablename__ = "grade_level"
    code: Mapped[str] = mapped_column(String(20), primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    max_students: Mapped[int] = mapped_column(Integer, nullable=False)

@event.listens_for(GradeLevel, "before_insert")
@event.listens_for(GradeLevel, "before_update")
def validate(mapper, connection, target):
    if not target.code:
        raise ValueError("grade level's code cannot be empty")
    if not target.name:
        raise ValueError("grade level's name cannot be empty")
    if target.max_students is None:
        raise ValueError("grade level's max students cannot be empty")
    if target.max_students < 0:
        raise ValueError("grade level's max students must be greater than or equal to 0")