from typing import Optional

class ContactInfos:
    def __init__(
        self,
        student_code: str,
        father_name: str,
        father_job: str,
        father_phone: str,
        father_card_id: str,
        mother_name: str,
        mother_job: str,
        mother_phone: str,
        mother_card_id: str,
        guardian_name: str,
        guardian_job: str,
        guardian_phone: str,
        guardian_card_id: str
    ):
        self.student_code = student_code
        self.data = ContactInfosData(
            father_name=father_name,
            father_job=father_job,
            father_phone=father_phone,
            father_card_id=father_card_id,
            mother_name=mother_name,
            mother_job=mother_job,
            mother_phone=mother_phone,
            mother_card_id=mother_card_id,
            guardian_name=guardian_name,
            guardian_job=guardian_job,
            guardian_phone=guardian_phone,
            guardian_card_id=guardian_card_id
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
        contact_info_data = ContactInfosData.from_dict(data.get("data"))
        return cls(
            student_code=data.get("student_code"),
            father_name=contact_info_data.father_name,
            father_job=contact_info_data.father_job,
            father_phone=contact_info_data.father_phone,
            father_card_id=contact_info_data.father_card_id,
            mother_name=contact_info_data.mother_name,
            mother_job=contact_info_data.mother_job,
            mother_phone=contact_info_data.mother_phone,
            mother_card_id=contact_info_data.mother_card_id,
            guardian_name=contact_info_data.guardian_name,
            guardian_job=contact_info_data.guardian_job,
            guardian_phone=contact_info_data.guardian_phone,
            guardian_card_id=contact_info_data.guardian_card_id
        )

class ContactInfosData:
    def __init__(
        self,
        father_name: str,
        father_job: str,
        father_phone: str,
        father_card_id: str,
        mother_name: str,
        mother_job: str,
        mother_phone: str,
        mother_card_id: str,
        guardian_name: str,
        guardian_job: str,
        guardian_phone: str,
        guardian_card_id: str
    ):
        self.father_name=father_name
        self.father_job=father_job
        self.father_phone=father_phone
        self.father_card_id=father_card_id
        self.mother_name=mother_name
        self.mother_job=mother_job
        self.mother_phone=mother_phone
        self.mother_card_id=mother_card_id
        self.guardian_name=guardian_name
        self.guardian_job=guardian_job
        self.guardian_phone=guardian_phone
        self.guardian_card_id=guardian_card_id
        self._validate()

    def _validate(self):
        pass

    def to_dict(self) -> dict:
        return {
            "father_name": self.father_name,
            "father_job": self.father_job,
            "father_phone": self.father_phone,
            "father_card_id": self.father_card_id,
            "mother_name": self.mother_name,
            "mother_job": self.mother_job,
            "mother_phone": self.mother_phone,
            "mother_card_id": self.mother_card_id,
            "guardian_name": self.guardian_name,
            "guardian_job": self.guardian_job,
            "guardian_phone": self.guardian_phone,
            "guardian_card_id": self.guardian_card_id
        }

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            father_name=data.get("father_name"),
            father_job=data.get("father_job"),
            father_phone=data.get("father_phone"),
            father_card_id=data.get("father_card_id"),
            mother_name=data.get("mother_name"),
            mother_job=data.get("mother_job"),
            mother_phone=data.get("mother_phone"),
            mother_card_id=data.get("mother_card_id"),
            guardian_name=data.get("guardian_name"),
            guardian_job=data.get("guardian_job"),
            guardian_phone=data.get("guardian_phone"),
            guardian_card_id=data.get("guardian_card_id")
        )
