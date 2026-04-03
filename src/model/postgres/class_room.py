from sqlalchemy import String, Integer, event, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from src.model.postgres.base import Base

class ClassRoom(Base):
    __tablename__ = "class_room"
    code: Mapped[str] = mapped_column(String(20), primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    size: Mapped[int] = mapped_column(Integer, nullable=False)
    special_program: Mapped[str | None] = mapped_column(String(50))
    grade_level_code : Mapped[str] = mapped_column(
        String(20),
        ForeignKey("grade_level.code"),
        nullable=False
    )

@event.listens_for(ClassRoom, "before_insert")
@event.listens_for(ClassRoom, "before_update")
def validate(mapper, connection, target):
    if not target.code:
        raise ValueError("class's code cannot be empty")
    if not target.grade_level_code :
        raise ValueError("class's grade level code cannot be empty")
    if not target.name:
        raise ValueError("class's name cannot be empty")
    if target.size is None:
        raise ValueError("class's size cannot be empty")
    if target.size < 0:
        raise ValueError("class's size must be greater than or equal to 0")
