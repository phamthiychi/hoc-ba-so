from pydantic import BaseModel
from typing import Optional, Any

class StudentCreate(BaseModel):
    academic_year : str
    class_name: str
    name: str
    date_of_birth: str
    gender: str
    ethnicity: str
    nationality: str
    card_id: str
    edu_id: str
    phone: str
    address: str
    status: str
    place_of_birth: Optional[str] = None

class StudentUpdate(BaseModel):
    code: str
    nationality: Optional[str] = None
    status: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    place_of_birth: Optional[str] = None
    father_name: Optional[str] = None
    father_job: Optional[str] = None
    father_phone: Optional[str] = None
    father_card_id: Optional[str] = None
    mother_name: Optional[str] = None
    mother_job: Optional[str] = None
    mother_phone: Optional[str] = None
    mother_card_id: Optional[str] = None
    guardian_name: Optional[str] = None
    guardian_job: Optional[str] = None
    guardian_phone: Optional[str] = None
    guardian_card_id: Optional[str] = None
