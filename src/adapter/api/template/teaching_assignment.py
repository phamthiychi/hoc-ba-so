from pydantic import BaseModel
from typing import Optional

class TeachingAssignmentCreate(BaseModel):
    teacher_id: str
    class_id: str
    subject_id: str
    academic_year_id: str
    semester_id: str
    role: str
    periods_per_week: int
    note: Optional[str] = None

class TeachingAssignmentUpdate(BaseModel):
    teacher_id: str
    class_id: str
    subject_id: str
    academic_year_id: str
    semester_id: str
    role: Optional[str] = None
    periods_per_week: Optional[int] = None
    note: Optional[str] = None
