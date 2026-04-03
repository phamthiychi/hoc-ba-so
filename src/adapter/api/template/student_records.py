from pydantic import BaseModel
from typing import Optional
from fastapi import UploadFile

class StudentRecords(BaseModel):
    academic_year: str
    file_profiles: Optional[UploadFile]
    file_reports: Optional[UploadFile]
