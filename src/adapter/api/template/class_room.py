from pydantic import BaseModel
from typing import Optional

class ClassRoomCreate(BaseModel):
    code: str
    name: str
    size: int
    grade_level_code: str
    special_program: Optional[str] = None

class ClassRoomUpdate(BaseModel):
    code: str
    size: Optional[int] = None
    special_program: Optional[str] = None