from pydantic import BaseModel
from typing import Optional


class SemesterCreate(BaseModel):
    code: str
    name: str
    start_date: str
    end_date: str

class SemesterUpdate(BaseModel):
    code: str
    start_date: Optional[str] = None
    end_date: Optional[str] = None
