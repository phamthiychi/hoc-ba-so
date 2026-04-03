import zipfile
import traceback

import pdfplumber
from pathlib import Path
from src.application.utils import Utils
from src.common.common_setting import settings as common_settings
from src.common.postgres_model_setting import settings as postgres_settings
from src.adapter.api.template.student import StudentCreate, StudentUpdate
from src.adapter.api.template.academic_year import AcademicYearCreate
from src.adapter.api.template.semester import SemesterCreate
from src.adapter.api.template.grade_level import GradeLevelCreate, GradeLevelUpdate
from src.adapter.api.template.class_room import ClassRoomCreate, ClassRoomUpdate
from src.adapter.api.template.contact_infos import ContactInfosCreateAndUpate
from src.adapter.api.template.student_records import StudentRecords

from src.adapter.database.postgres_repository import (
    PostgresAcademicYearRepository,
    PostgresClassRoomRepository,
    PostgresGradeLevelRepository,
    PostgresScoreRepository,
    PostgresSemesterRepository,
    PostgresStudentRepository,
    PostgresSubjectRepository,
    PostgresTeacherRepository,
    PostgresLearningResultRepository,
    PostgresTeachingAssignmentRepository
)
from src.adapter.database.mongo_repository import (
    MongoContactInfosRepository,
    MongoSubjectAssessmentsRepository
)
from src.adapter.graph.neo4j_repository import (
    Neo4jStudentSpecialAbilitiesRepository,
    Neo4jStudentQualityRepository,
    Neo4jThingRepository,
    Neo4jStudentGeneralAbilitiesRepository,
    Neo4jStudentRepository,
    Neo4jStudentContactInfosRepository,
    Neo4jStudentSubjectAssessmentsRepository
)

from src.model.mongo.subject_assessments import (
    SubjectAssessments,
    SubjectAssessmentsPoint,
    SubjectAssessmentsLevel
)

class SystemCore:
    def __init__(self, session, db, manager):
        # Postgres database
        self.student_repo = PostgresStudentRepository(session)
        self.teacher_repo = PostgresTeacherRepository(session)
        self.subject_repo = PostgresSubjectRepository(session)
        self.semester_repo = PostgresSemesterRepository(session)
        self.score_repo = PostgresScoreRepository(session)
        self.class_room_repo = PostgresClassRoomRepository(session)
        self.grade_level_repo = PostgresGradeLevelRepository(session)
        self.academic_year_repo = PostgresAcademicYearRepository(session)
        self.learning_result_repo = PostgresLearningResultRepository(session)
        self.teaching_assignment_repo = PostgresTeachingAssignmentRepository(session)
        # Mongo database
        self.contact_infos_repo = MongoContactInfosRepository(db)
        self.subject_assessments_repo = MongoSubjectAssessmentsRepository(db)
        # Neo4j database
        self.thing_repo = Neo4jThingRepository(manager)
        self.student_Q_repo = Neo4jStudentQualityRepository(manager)
        self.student_GA_repo = Neo4jStudentGeneralAbilitiesRepository(manager)
        self.student_SA_repo = Neo4jStudentSpecialAbilitiesRepository(manager)
        self.student_graph_repo = Neo4jStudentRepository(manager)
        self.student_contact_infos_repo = Neo4jStudentContactInfosRepository(manager)
        self.student_subject_assessmets_repo = Neo4jStudentSubjectAssessmentsRepository(manager)
        # Other
        self.utils = Utils()

        # Init default
        self._init_graph()

    def _init_graph(self):
        self.thing_repo.create_relationship(
            from_value="thing",
            to_label="StudentQuality",
            to_id_field="code",
            to_value="student_quality",
            relation_type="HAS_ASSESSMENT",
            relation_props=None
        )
        self.thing_repo.create_relationship(
            from_value="thing",
            to_label="StudentGeneralAbilities",
            to_id_field="code",
            to_value="student_general_abilities",
            relation_type="HAS_ASSESSMENT",
            relation_props=None
        )
        self.thing_repo.create_relationship(
            from_value="thing",
            to_label="StudentSpecialAbilities",
            to_id_field="code",
            to_value="student_special_abilities",
            relation_type="HAS_ASSESSMENT",
            relation_props=None
        )

    async def add_student(self, info: StudentRecords) -> dict:
        if info.file_profiles is not None:
            await self.add_student_profiles(info.academic_year, info.file_profiles.file)
        # if info.file_reports is not None:
        #     await self.add_student_reports(info.file_reports.file)

    async def add_student_reports(self, file,
                                  output_folder=common_settings.SRC_ROOT / "adapter/api/uploads/student_reports"):
        with zipfile.ZipFile(file) as zip_ref:
            zip_ref.extractall(output_folder)
        for pdf_file in Path(output_folder).glob("*.pdf"):
            with pdfplumber.open(pdf_file) as pdf:
                text = ""
                for page in pdf.pages:
                    text += page.extract_text() or ""
            print(text)
            return None

    async def add_student_profiles(self, academic_year, file):
        profiles = self.utils.extract_info_from_student_profile(file)
        for p in profiles:
            try:
                student_code = await self.add_student_postgres(StudentCreate(
                        academic_year=academic_year,
                        class_name=p.get("class_name"),
                        name=p.get("name"),
                        date_of_birth=p.get("date_of_birth"),
                        gender=p.get("gender"),
                        ethnicity=p.get("ethnicity"),
                        nationality=p.get("nationality"),
                        card_id=p.get("card_id"),
                        edu_id=p.get("edu_id"),
                        phone=p.get("phone"),
                        address=p.get("address"),
                        status=p.get("status"),
                        place_of_birth=p.get("place_of_birth")
                ))
                await self.add_contact_info_student_mongo(ContactInfosCreateAndUpate(
                    student_code=student_code,
                    father_name=p.get("father_name"),
                    father_job=p.get("father_job"),
                    father_card_id=p.get("father_card_id"),
                    father_phone=p.get("father_phone"),
                    mother_name=p.get("mother_name"),
                    mother_job=p.get("mother_job"),
                    mother_card_id=p.get("mother_card_id"),
                    mother_phone=p.get("mother_phone"),
                    guardian_name=p.get("guardian_name"),
                    guardian_job=p.get("guardian_job"),
                    guardian_card_id=p.get("guardian_card_id"),
                    guardian_phone=p.get("guardian_phone")
                ))
                await self.add_subject_assessments_student_mongo(student_code)
                await self.add_student_relationship(student_code, p)
            except Exception as e:
                self.utils._log(traceback.format_exc())
                continue

    async def find_student(self, code: str) -> dict:
        return await self.student_repo.get(code)

    async def update_student(self, info: StudentUpdate) -> dict:
        return await self.student_repo.update(info.dict())

    async def add_student_postgres(self, info: StudentCreate) -> str:
        academic_year_code = self.academic_year_repo.create_code(info.academic_year)
        grade_level_code = self.grade_level_repo.create_code(info.class_name)
        class_room_code = self.class_room_repo.create_code(info.class_name, grade_level_code)
        student_entity = info.dict()
        student_entity.pop("academic_year", None)
        student_entity.pop("class_name", None)
        indexs = [0]
        students = await self.student_repo.get_by_code_like(".".join(
            self.student_repo.create_code(academic_year_code, grade_level_code,
                                          class_room_code, 1).split(".")[:-1]))
        if students:
            indexs.extend([int(s.code.split(".")[-1]) for s in students])
        student_entity["code"] = self.student_repo.create_code(academic_year_code, grade_level_code,
                                                               class_room_code, max(indexs) + 1)
        Result = await self.student_repo.add(student_entity)
        if isinstance(Result, tuple) and "Exist" in Result:
            return Result[1].code
        academic_year_entity = await self.academic_year_repo.get(academic_year_code)
        grade_level_entity = await self.grade_level_repo.get(grade_level_code)
        class_room_entity = await self.class_room_repo.get(class_room_code)
        start_year, end_year = info.academic_year.split("-")
        if academic_year_entity is None:
            await self.academic_year_repo.add(AcademicYearCreate(
                code=academic_year_code,
                name=info.academic_year,
                start_date=f"{start_year.strip()}-01-08",
                end_date=f"{end_year.strip()}-05-31"
            ).dict())
            await self.semester_repo.add(SemesterCreate(
                code=self.semester_repo.create_code(academic_year_code, 1),
                name=f"HK01",
                start_date=f"{start_year.strip()}-01-08",
                end_date=f"{end_year.strip()}-12-31"
            ).dict())
            await self.semester_repo.add(SemesterCreate(
                code=self.semester_repo.create_code(academic_year_code, 2),
                name=f"HK02",
                start_date=f"{start_year.strip()}-01-01",
                end_date=f"{end_year.strip()}-05-31"
            ).dict())
        if grade_level_entity is None:
            await self.grade_level_repo.add(GradeLevelCreate(
                code=grade_level_code,
                name=f"Khối {int(grade_level_code.split('MK')[1])}",
                max_students=1
            ).dict())
        else:
            await self.grade_level_repo.update(GradeLevelUpdate(
                code=grade_level_code,
                max_students=grade_level_entity.max_students + 1
            ).dict())
        if class_room_entity is None:
            await self.class_room_repo.add(ClassRoomCreate(
                code=class_room_code,
                name=info.class_name,
                size=1,
                grade_level_code=grade_level_code
            ).dict())
        else:
            await self.class_room_repo.update(ClassRoomUpdate(
                code=class_room_code,
                size=class_room_entity.size + 1
            ).dict())
        return student_entity["code"]

    async def add_contact_info_student_mongo(self, info: ContactInfosCreateAndUpate) -> None:
        if await self.contact_infos_repo.get(info.student_code):
            await self.contact_infos_repo.update(info.dict())
            return
        await self.contact_infos_repo.add(info.dict())

    async def add_subject_assessments_student_mongo(self, student_code):
        class_name = postgres_settings.NUM2WORD[int(student_code.split(".")[1])]
        subject_with_eval = postgres_settings.INIT_SUBJECT_EVAL[class_name]
        data = []
        for subject_name, eval_type in subject_with_eval.items():
            if eval_type == "score":
                data.append(SubjectAssessmentsPoint(
                    subject_name=subject_name
                ).to_dict())
            elif eval_type == "level":
                data.append(SubjectAssessmentsLevel(
                    subject_name=subject_name
                ).to_dict())
        if await self.subject_assessments_repo.get(student_code):
            await self.subject_assessments_repo.update(SubjectAssessments(
                student_code=student_code,
                data=data
            ).to_dict())
            return
        await self.subject_assessments_repo.add(SubjectAssessments(
            student_code=student_code,
            data=data
        ).to_dict())

    async def add_student_relationship(self, student_code, profile):
        self.student_graph_repo.create({
            "code": student_code,
            "name": profile.get("name"),
            "card_id": profile.get("card_id"),
            "edu_id": profile.get("edu_id"),
        })
        student_contact_infos_record = {
                "code": student_code,
                "data": f"{self.utils.flatten_props((await self.contact_infos_repo.get(student_code)).data.to_dict())}"
            }
        if self.student_contact_infos_repo.get_by_id(student_code):
            self.student_contact_infos_repo.update_by_id(student_code, student_contact_infos_record)
        else:
            self.student_contact_infos_repo.create(student_contact_infos_record)
        datas = (await self.subject_assessments_repo.get(student_code)).data
        new_data = [self.utils.flatten_props(data) for data in datas]
        student_subject_assessmets_record = {
            "code": student_code,
            "data": f"{new_data}"
        }
        if self.student_subject_assessmets_repo.get_by_id(student_code):
            self.student_subject_assessmets_repo.update_by_id(student_code, student_subject_assessmets_record)
        else:
            self.student_subject_assessmets_repo.create(student_subject_assessmets_record)
        self.student_graph_repo.create_relationship(
            from_value=student_code,
            to_label="StudentContactInfos",
            to_id_field="code",
            to_value=student_code,
            relation_type="HAVE_CONTACT",
            relation_props=None
        )
        self.student_graph_repo.create_relationship(
            from_value=student_code,
            to_label="StudentSubjectAssessments",
            to_id_field="code",
            to_value=student_code,
            relation_type="HAVE_ASSESSMENT",
            relation_props=None
        )
