from typing import List, Literal
from pydantic import BaseModel

class StudentAssessment(BaseModel):
    name: str
    level: Literal["Hoàn thành tốt", "Hoàn thành"]
    evidence: str

    def to_dict(self):
        return self.model_dump()

class StudentReport(BaseModel):
    code: str
    contact_info: List[dict]
    subject_assessments: List[dict]
    quality: List[StudentAssessment]
    general_abilities: List[StudentAssessment]
    special_abilities: List[StudentAssessment]

    def to_dict(self):
        return self.model_dump()

