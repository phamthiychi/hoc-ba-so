from sqlalchemy import String, Integer, event
from sqlalchemy.orm import Mapped, mapped_column

from src.model.postgres.base import Base

class Subject(Base):
    __tablename__ = "subject"
    code: Mapped[str] = mapped_column(String(20), primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    total_periods: Mapped[int] = mapped_column(Integer, nullable=False)

@event.listens_for(Subject, "before_insert")
@event.listens_for(Subject, "before_update")
def validate(mapper, connection, target):
    if not target.code:
        raise ValueError("subject's code cannot be empty")
    if not target.name:
        raise ValueError("subject's name cannot be empty")
    if target.total_periods is None:
        raise ValueError("subject's total periods cannot be empty")
    if target.total_periods < 0:
        raise ValueError("subject's total periods be greater than or equal to 0")