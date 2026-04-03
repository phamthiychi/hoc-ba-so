from pydantic import BaseModel
from typing import Optional

class SubjectCreate(BaseModel):
    code: str
    name: str
    total_periods: int

class SubjectUpdate(BaseModel):
    code: str
    name: Optional[str] = None
    total_periods: Optional[int] = None