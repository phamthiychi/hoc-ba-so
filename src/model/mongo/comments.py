from typing import Optional

class Comments:
    def __init__(
        self,
        student_code: str,
        vietnamese_comment: Optional[dict] = None,
        mathematics_comment: Optional[dict] = None,
        informatics_comment: Optional[dict] = None,
        science_comment: Optional[dict] = None,
        history_and_geography_comment: Optional[dict] = None,
        english_comment: Optional[dict] = None,
        technology_comment: Optional[dict] = None,
        music_comment: Optional[dict] = None,
        arts_comment: Optional[dict] = None,
        civics_comment: Optional[dict] = None,
        physical_education_comment: Optional[dict] = None,
        experiential_activities_comment: Optional[dict] = None,
        nature_and_society_comment: Optional[dict] = None
    ):
        self.student_code = student_code
        self.data = CommentsData(
            vietnamese_comment=vietnamese_comment,
            mathematics_comment=mathematics_comment,
            informatics_comment=informatics_comment,
            science_comment=science_comment,
            history_and_geography_comment=history_and_geography_comment,
            english_comment=english_comment,
            technology_comment=technology_comment,
            music_comment=music_comment,
            arts_comment=arts_comment,
            civics_comment=civics_comment,
            physical_education_comment=physical_education_comment,
            experiential_activities_comment=experiential_activities_comment,
            nature_and_society_comment=nature_and_society_comment
        )
        self._validate()

    def _validate(self):
        if not self.student_code:
            raise ValueError("student's code cannot be empty")

    def to_dict(self) -> dict:
        return {
            "student_code": self.student_code,
            "data": self.data.to_dict()
        }

    @classmethod
    def from_dict(cls, data: dict):
        comment_data = CommentsData.from_dict(data.get("data"))
        return cls(
            student_code=data.get("student_code"),
            vietnamese_comment=comment_data.vietnamese_comment,
            mathematics_comment=comment_data.mathematics_comment,
            informatics_comment=comment_data.informatics_comment,
            science_comment=comment_data.science_comment,
            history_and_geography_comment=comment_data.history_and_geography_comment,
            english_comment=comment_data.english_comment,
            technology_comment=comment_data.technology_comment,
            music_comment=comment_data.music_comment,
            arts_comment=comment_data.arts_comment,
            civics_comment=comment_data.civics_comment,
            physical_education_comment=comment_data.physical_education_comment,
            experiential_activities_comment=comment_data.experiential_activities_comment,
            nature_and_society_comment=comment_data.nature_and_society_comment
        )

class CommentsData:
    def __init__(
        self,
        vietnamese_comment: Optional[dict] = None,
        mathematics_comment: Optional[dict] = None,
        informatics_comment: Optional[dict] = None,
        science_comment: Optional[dict] = None,
        history_and_geography_comment: Optional[dict] = None,
        english_comment: Optional[dict] = None,
        technology_comment: Optional[dict] = None,
        music_comment: Optional[dict] = None,
        arts_comment: Optional[dict] = None,
        civics_comment: Optional[dict] = None,
        physical_education_comment: Optional[dict] = None,
        experiential_activities_comment: Optional[dict] = None,
        nature_and_society_comment: Optional[dict] = None
    ):
        self.vietnamese_comment = vietnamese_comment
        self.mathematics_comment = mathematics_comment
        self.informatics_comment = informatics_comment
        self.science_comment = science_comment
        self.history_and_geography_comment = history_and_geography_comment
        self.english_comment = english_comment
        self.technology_comment = technology_comment
        self.music_comment = music_comment
        self.arts_comment = arts_comment
        self.civics_comment = civics_comment
        self.physical_education_comment = physical_education_comment
        self.experiential_activities_comment = experiential_activities_comment
        self.nature_and_society_comment = nature_and_society_comment
        self._validate()

    def _validate(self):
        pass

    def to_dict(self) -> dict:
        return {
            "vietnamese_comment": self.vietnamese_comment,
            "mathematics_comment": self.mathematics_comment,
            "informatics_comment": self.informatics_comment,
            "science_comment": self.science_comment,
            "history_and_geography_comment": self.history_and_geography_comment,
            "english_comment": self.english_comment,
            "technology_comment": self.technology_comment,
            "music_comment": self.music_comment,
            "arts_comment": self.arts_comment,
            "civics_comment": self.civics_comment,
            "physical_education_comment": self.physical_education_comment,
            "experiential_activities_comment": self.experiential_activities_comment,
            "nature_and_society_comment": self.nature_and_society_comment
        }

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            vietnamese_comment=data.get("vietnamese_comment"),
            mathematics_comment=data.get("mathematics_comment"),
            informatics_comment=data.get("informatics_comment"),
            science_comment=data.get("science_comment"),
            history_and_geography_comment=data.get("history_and_geography_comment"),
            english_comment=data.get("english_comment"),
            technology_comment=data.get("technology_comment"),
            music_comment=data.get("music_comment"),
            arts_comment=data.get("arts_comment"),
            civics_comment=data.get("civics_comment"),
            physical_education_comment=data.get("physical_education_comment"),
            experiential_activities_comment=data.get("experiential_activities_comment"),
            nature_and_society_comment=data.get("nature_and_society_comment")
        )