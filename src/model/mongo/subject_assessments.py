from typing import List

class SubjectAssessments:
    def __init__(
        self,
        student_code: str,
        data: List[dict] = []
    ):
        self.student_code = student_code
        self.data = data

    def _validate(self):
        pass

    def to_dict(self) -> dict:
        return {
            "student_code": self.student_code,
            "data": self.data
        }

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            student_code=data.get("student_code"),
            data=data.get("data"),
        )

class SubjectAssessmentsLevel:
    def __init__(
        self,
        subject_name: str,
        level: str = None,
        comment: str = None,
    ):
        self.subject_name = subject_name
        self.level = level
        self.comment = comment
        self._validate()

    def _validate(self):
        pass

    def to_dict(self) -> dict:
        return {
            "subject_name": self.subject_name,
            "level": self.level,
            "comment": self.comment
        }

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            subject_name=data.get("subject_name"),
            level=data.get("level"),
            comment=data.get("comment")
        )

class SubjectAssessmentsPoint:
    def __init__(
        self,
        subject_name: str,
        score_point: float = 0.0,
        comment: str = None,
    ):
        self.subject_name = subject_name
        self.score_point = score_point
        self.comment = comment
        self._validate()

    def _validate(self):
        pass

    def to_dict(self) -> dict:
        return {
            "subject_name": self.subject_name,
            "score_point": self.score_point,
            "comment": self.comment
        }

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            subject_name=data.get("subject_name"),
            score_point=data.get("score_point"),
            comment=data.get("comment")
        )
