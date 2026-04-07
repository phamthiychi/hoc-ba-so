from pydantic import BaseModel
from typing import Optional

class Comment(BaseModel):
    code: str
    comment: str

class AssessmentComment(BaseModel):
    code: str
    quality_comment: Optional[str] = None
    general_abilities_comment: Optional[str] = None
    special_abilities_comment: Optional[str] = None
