from pydantic import BaseModel
from typing import Optional

class GradeLevelCreate(BaseModel):
    code: str
    name: str
    max_students: int

class GradeLevelUpdate(BaseModel):
    code: str
    name: Optional[str] = None
    max_students: Optional[int] = None