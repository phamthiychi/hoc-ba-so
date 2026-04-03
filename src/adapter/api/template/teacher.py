from pydantic import BaseModel
from typing import Optional

class TeacherCreate(BaseModel):
    code: str
    name: str
    date_of_birth: str
    gender: str
    ethnicity: str
    nationality: str
    card_id: Optional[str] = None
    edu_id: Optional[str] = None
    status: Optional[str] = None
    phone: Optional[str] = None
    specialization: Optional[str] = None
    position: Optional[str] = None

class TeacherUpdate(BaseModel):
    code: str
    status: Optional[str] = None
    phone: Optional[str] = None
    nationality: Optional[str] = None
    card_id: Optional[str] = None
    edu_id: Optional[str] = None
    specialization: Optional[str] = None
    position: Optional[str] = None
