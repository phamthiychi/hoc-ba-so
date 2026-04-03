from pydantic import BaseModel
from typing import Optional

class AcademicYearCreate(BaseModel):
    code: str
    name: str
    start_date: str
    end_date: str

class AcademicYearUpdate(BaseModel):
    code: str
    name: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None