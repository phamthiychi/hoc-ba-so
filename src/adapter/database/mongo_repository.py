from typing import Generic, Optional, Type, TypeVar
from fastapi import HTTPException

from src.interface.data import Repository
from src.model.mongo.contact_infos import ContactInfos
from src.model.mongo.subject_assessments import SubjectAssessments
T = TypeVar("T")

class MongoRepositoryBase(Repository[T], Generic[T]):
    collection_name: str
    model_cls: Type[T]
    field_code: str

    def __init__(self, db):
        self.db = db
        self.col = db[self.collection_name]

    async def get_all(self) -> Optional[list[T]]:
        entities = []
        for doc in self.col.find():
            doc["_id"] = str(doc["_id"])
            entities.append(doc)
        return entities

    async def get(self, code: str) -> Optional[T]:
        doc = self.col.find_one({self.field_code: code})
        return None if not doc else self.model_cls.from_dict(doc)

    async def add(self, create_info: dict) -> Optional[T]:
        entity = self.model_cls(**create_info)
        exist = await self.get(create_info.get(self.field_code))
        if exist:
            return None
        result = self.col.insert_one(entity.to_dict())
        doc = self.col.find_one({"_id": result.inserted_id})
        return self.model_cls.from_dict(doc)

    async def delete(self, code: str) -> bool:
        delete_result = self.col.delete_one({self.field_code: code})
        return delete_result.deleted_count > 0

    async def update(self, update_info: dict) -> Optional[T]:
        update_data = {}
        code = update_info.get(self.field_code)
        update_info.pop(self.field_code, None)
        if "other_info" in update_info.keys():
            update_data = {"other_info": update_info.get("other_info")}
            update_info.pop("other_info", None)
        for key, value in update_info.items():
            if not value:
                continue
            update_data[f"data.{key}"] = value
        update_result = self.col.update_one(
            {self.field_code: code},
            {"$set": update_data}
        )
        if update_result.matched_count == 0:
            return None
        if update_result.modified_count == 0:
            raise HTTPException(
                status_code=400,
                detail="No fields were changed"
            )
        updated_doc = self.col.find_one({self.field_code: code})
        return self.model_cls.from_dict(updated_doc)

class MongoContactInfosRepository(MongoRepositoryBase[ContactInfos]):
    collection_name = "contact_infos"
    model_cls = ContactInfos
    field_code = "student_code"

class MongoSubjectAssessmentsRepository(MongoRepositoryBase[SubjectAssessments]):
    collection_name = "subject_assessments"
    model_cls = SubjectAssessments
    field_code = "student_code"

