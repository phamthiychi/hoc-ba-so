from pydantic import BaseModel
from typing import Optional

class Comment(BaseModel):
    code: str
    comment: str

class SpecialAbilitiesComment(BaseModel):
    code: str
    vietnamese_comment: Optional[str] = None
    mathematics_comment: Optional[str] = None
    informatics_comment: Optional[str] = None
    science_comment: Optional[str] = None
    history_and_geography_comment: Optional[str] = None
    english_comment: Optional[str] = None
    technology_comment: Optional[str] = None
    music_comment: Optional[str] = None
    arts_comment: Optional[str] = None
    civics_comment: Optional[str] = None
    physical_education_comment: Optional[str] = None
    experiential_activities_comment: Optional[str] = None
    nature_and_society_comment: Optional[str] = None

class AssessmentComment(BaseModel):
    code: str
    quality_comment: Optional[str] = None
    general_abilities_comment: Optional[str] = None
    vietnamese_comment: Optional[str] = None
    mathematics_comment: Optional[str] = None
    informatics_comment: Optional[str] = None
    science_comment: Optional[str] = None
    history_and_geography_comment: Optional[str] = None
    english_comment: Optional[str] = None
    technology_comment: Optional[str] = None
    music_comment: Optional[str] = None
    arts_comment: Optional[str] = None
    civics_comment: Optional[str] = None
    physical_education_comment: Optional[str] = None
    experiential_activities_comment: Optional[str] = None
    nature_and_society_comment: Optional[str] = None

