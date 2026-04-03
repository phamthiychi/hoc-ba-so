from sqlalchemy import String, event
from sqlalchemy.orm import Mapped, mapped_column

from src.model.postgres.base import Base

class Score(Base):
    __tablename__ = "score"
    code: Mapped[str] = mapped_column(String(20), primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)

@event.listens_for(Score, "before_insert")
@event.listens_for(Score, "before_update")
def validate(mapper, connection, target):
    if not target.code:
        raise ValueError("score's code cannot be empty")
    if not target.name:
        raise ValueError("score's name cannot be empty")