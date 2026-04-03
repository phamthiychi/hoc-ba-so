from pydantic import BaseModel
from typing import Optional

class ScoreCreate(BaseModel):
    code: str
    name: str
    description: Optional[str] = None

class ScoreUpdate(BaseModel):
    code: str
    name: Optional[str] = None
    description: Optional[str] = None