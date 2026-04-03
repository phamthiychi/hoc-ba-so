from pydantic import BaseModel
from typing import Optional

class ContactInfosCreateAndUpate(BaseModel):
    student_code: str
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
