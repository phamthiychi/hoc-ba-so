import traceback

from typing import BinaryIO, Optional, Callable, Any, Tuple

from src.application.utils import Utils
from src.adapter.graph.knowledge_base import KnowledgeBase
from src.application.embedding import EmbeddingSentence
from src.common.common_setting import settings as common_settings
from src.common.postgres_model_setting import settings as postgres_settings
from src.common.ontology_setting import settings as ontology_setting
from src.adapter.api.template.student import StudentCreate, StudentUpdate
from src.adapter.api.template.academic_year import AcademicYearCreate
from src.adapter.api.template.semester import SemesterCreate
from src.adapter.api.template.grade_level import GradeLevelCreate, GradeLevelUpdate
from src.adapter.api.template.class_room import ClassRoomCreate, ClassRoomUpdate
from src.adapter.api.template.contact_infos import ContactInfosCreateAndUpate
from src.adapter.api.template.student_records import StudentRecords
from src.adapter.api.template.comment import Comment, SpecialAbilitiesComment

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
    Neo4jStudentSubAssessmentRepository,
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
        self.student_contact_infos_repo = MongoContactInfosRepository(db)
        self.student_subject_assessments_repo = MongoSubjectAssessmentsRepository(db)
        # Neo4j database
        self.graph_thing_repo = Neo4jThingRepository(manager)
        self.graph_student_Q_repo = Neo4jStudentQualityRepository(manager)
        self.graph_student_GA_repo = Neo4jStudentGeneralAbilitiesRepository(manager)
        self.graph_student_SA_repo = Neo4jStudentSpecialAbilitiesRepository(manager)
        self.graph_student_sub_assessment_repo = Neo4jStudentSubAssessmentRepository(manager)
        self.graph_student_repo = Neo4jStudentRepository(manager)
        self.graph_student_contact_infos_repo = Neo4jStudentContactInfosRepository(manager)
        self.graph_student_subject_assessmets_repo = Neo4jStudentSubjectAssessmentsRepository(manager)
        # Embedding
        self.student_assessment_kb = KnowledgeBase().student_assessments.define
        self.embedding_assessment = EmbeddingSentence()
        self.emb_kb = {
            "Phẩm chất": self.embedding_assessment.emb_knowledge(
                knowledge_base=self.student_assessment_kb["Phẩm chất"],
                name="quality"),
            "Năng lực chung": self.embedding_assessment.emb_knowledge(
                knowledge_base=self.student_assessment_kb["Năng lực chung"],
                name="general"),
            "vietnamese": self.embedding_assessment.emb_knowledge(
                knowledge_base={"vietnamese": self.student_assessment_kb["Môn học"]["Tiếng Việt"]},
                name="vietnamese"),
            "mathematics": self.embedding_assessment.emb_knowledge(
                knowledge_base={"mathematics":self.student_assessment_kb["Môn học"]["Toán"]},
                name="mathematics"),
            "informatics": self.embedding_assessment.emb_knowledge(
                knowledge_base={"informatics":self.student_assessment_kb["Môn học"]["Tin học"]},
                name="informatics"),
            "science": self.embedding_assessment.emb_knowledge(
                knowledge_base={"science":self.student_assessment_kb["Môn học"]["Khoa học"]},
                name="science"),
            "history_and_geography": self.embedding_assessment.emb_knowledge(
                knowledge_base={"history_and_geography":self.student_assessment_kb["Môn học"]["Lịch sử và Địa lý"]},
                name="history_and_geography"),
            "english": self.embedding_assessment.emb_knowledge(
                knowledge_base={"english":self.student_assessment_kb["Môn học"]["Tiếng Anh"]},
                name="english"),
            "technology": self.embedding_assessment.emb_knowledge(
                knowledge_base={"technology":self.student_assessment_kb["Môn học"]["Công nghệ"]},
                name="technology"),
            "music": self.embedding_assessment.emb_knowledge(
                knowledge_base={"music":self.student_assessment_kb["Môn học"]["Âm nhạc"]},
                name="music"),
            "arts": self.embedding_assessment.emb_knowledge(
                knowledge_base={"arts":self.student_assessment_kb["Môn học"]["Mĩ thuật"]},
                name="arts"),
            "civics": self.embedding_assessment.emb_knowledge(
                knowledge_base={"civics":self.student_assessment_kb["Môn học"]["Giáo dục công dân"]},
                name="civics"),
            "physical_education": self.embedding_assessment.emb_knowledge(
                knowledge_base={"physical_education":self.student_assessment_kb["Môn học"]["Giáo dục thể chất"]},
                name="physical_education"),
            "experiential_activities": self.embedding_assessment.emb_knowledge(
                knowledge_base={"experiential_activities":self.student_assessment_kb["Môn học"]["Hoạt động trải nghiệm"]},
                name="experiential_activities")
        }
        # Other
        self.utils = Utils()
        self.manage = manager

        # Init default
        self._init_graph()

    ## Export funcs
    async def find_students(self) -> Optional[list]:
        student_infos = await self.student_repo.get_all()
        if student_infos is None:
            return None
        results = []
        for student_info in student_infos:
            results.append(self.find_student(student_info.code))
        return results

    async def find_student(self, code: str) -> Optional[dict]:
        student_info = await self.student_repo.get(code)
        if student_info is None:
            return None
        student_info = student_info.to_dict()
        student_info["contact_infors"] = (await self.student_contact_infos_repo.get(code)).to_dict()
        return student_info

    async def add_student(self, info: StudentRecords) -> list:
        if info.file_profiles is not None:
            self._init_graph()
            return await self.add_student_profiles(info.academic_year, info.file_profiles.file)

    async def update_student(self, info: StudentUpdate) -> list:
        student_info = await self.student_repo.update(info)
        if student_info is None:
            return None
        await self.student_contact_infos_repo.update(ContactInfosCreateAndUpate(
            student_code=student_info.code,
            father_card_id=info.father_card_id,
            father_job=info.father_job,
            father_name=info.father_name,
            father_phone=info.father_phone,
            mother_card_id=info.mother_card_id,
            mother_job=info.mother_job,
            mother_name=info.mother_name,
            mother_phone=info.mother_phone,
            guardian_card_id=info.guardian_card_id,
            guardian_job=info.guardian_job,
            guardian_name=info.guardian_name,
            guardian_phone=info.guardian_phone
        ))
        return self.find_student(student_info.code)

    async def delete_student(self, student_code: str) -> bool:
        is_delete = await self.student_repo.delete(student_code)
        if is_delete == False:
            return False
        try:
            await self.student_contact_infos_repo.delete(student_code)
            await self.student_subject_assessments_repo.delete(student_code)
            self.graph_student_contact_infos_repo.delete_by_id(student_code)
            self.graph_student_subject_assessmets_repo.delete_by_id(student_code)
            self.graph_student_repo.delete_by_id(student_code)
            return True
        except Exception as e:
            self.utils._log(traceback.format_exc())
            return False

    async def find_student_contact_infos(self, student_code: str) -> dict:
        return (await self.student_contact_infos_repo.get(student_code)).to_dict()

    async def find_student_subject_assessmets(self, student_code: str) -> dict:
        return (await self.student_subject_assessments_repo.get(student_code)).to_dict()

    async def add_student_comment_general(self, payload: Comment, type_assessment: str, threshold = 0.5) -> str:
        if await self.find_student(payload.code) is None:
            return None
        self.clear_student_assessment_outstanding(payload.code, type_assessment)
        clauses = self.utils.split_clauses(payload.comment)
        print(clauses)
        clause_embs = self.embedding_assessment.model.encode(clauses, convert_to_tensor=True)
        for i, clause in enumerate(clauses):
            sims = self.embedding_assessment.util.cos_sim(clause_embs[i], self.emb_kb[type_assessment].get("encode"))[0]
            best_idx = sims.argmax().item()
            score = float(sims[best_idx])
            if score <= threshold:
                continue
            indicators = self.emb_kb[type_assessment].get("all_indicators")[best_idx]
            self.create_student_assessment_outstanding(
                student_code=payload.code,
                evidence=clause,
                confident=score,
                name=indicators.get("virtue"),
                indicator=indicators.get("indicator"),
                comment=payload.comment,
                type_assessment=type_assessment
            )
        return payload.code

    async def add_student_comment_special(self, payload: SpecialAbilitiesComment) -> str:
        if await self.find_student(payload.code) is None:
            return None
        self.clear_student_assessment_outstanding(payload.code, "Năng lực đặc thù")
        student_outcome = {"student_code": payload.code}
        for field, comment in payload.model_dump().items():
            if field == "code" or comment == None:
                continue
            key = field.replace('_comment', '')
            student_outcome[key] = self.calc_emb_distance(comment, self.emb_kb[key])
        return student_outcome

    ### ===================================================================================================
    ### Internal funcs
    ### ===================================================================================================

    def _init_graph(self) -> None:
        self.graph_thing_repo.__init__(self.manage)
        self.graph_student_Q_repo.__init__(self.manage)
        self.graph_student_GA_repo.__init__(self.manage)
        self.graph_student_SA_repo.__init__(self.manage)

        self.graph_thing_repo.create_relationship(
            from_value="thing",
            to_label="StudentQuality",
            to_id_field="code",
            to_value="student_quality",
            relation_type="HAS_ASSESSMENT",
            relation_props=None
        )
        self.graph_thing_repo.create_relationship(
            from_value="thing",
            to_label="StudentGeneralAbilities",
            to_id_field="code",
            to_value="student_general_abilities",
            relation_type="HAS_ASSESSMENT",
            relation_props=None
        )
        self.graph_thing_repo.create_relationship(
            from_value="thing",
            to_label="StudentSpecialAbilities",
            to_id_field="code",
            to_value="student_special_abilities",
            relation_type="HAS_ASSESSMENT",
            relation_props=None
        )
        # for type_assessment, data in self.student_assessment_kb.items():
        #     for name in data.keys():
        #         code = ontology_setting.ASSESSMENT2CODE[name]
        #         including_code, callback = self.choose_assessment(type_assessment)
        #         self.graph_student_sub_assessment_repo.create({
        #             "code": code,
        #             "name": name,
        #             "define": " ".join(self.student_assessment_kb[type_assessment][name])
        #         })
        #         callback.create_relationship(
        #             from_value=including_code,
        #             to_label="StudentSubAssessment",
        #             to_id_field="code",
        #             to_value=code,
        #             relation_type="INCLUDING",
        #             relation_props=None
        #         )

    def fill_none(self, value: any, default="Chưa có") -> any:
        return value if value else default

    async def add_student_profiles(self, academic_year: str, file: BinaryIO) -> list:
        error_students = []
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
                        place_of_birth=self.fill_none(p.get("place_of_birth"))
                ))
                await self.add_contact_info_student_mongo(ContactInfosCreateAndUpate(
                    student_code=student_code,
                    student_card_id=p.get("card_id"),
                    student_edu_id=p.get("edu_id"),
                    father_name=self.fill_none(p.get("father_name")),
                    father_job=self.fill_none(p.get("father_job")),
                    father_card_id=self.fill_none(p.get("father_card_id")),
                    father_phone=self.fill_none(p.get("father_phone")),
                    mother_name=self.fill_none(p.get("mother_name")),
                    mother_job=self.fill_none(p.get("mother_job")),
                    mother_card_id=self.fill_none(p.get("mother_card_id")),
                    mother_phone=self.fill_none(p.get("mother_phone")),
                    guardian_name=self.fill_none(p.get("guardian_name")),
                    guardian_job=self.fill_none(p.get("guardian_job")),
                    guardian_card_id=self.fill_none(p.get("guardian_card_id")),
                    guardian_phone=self.fill_none(p.get("guardian_phone"))
                ))
                await self.add_subject_assessments_student_mongo(student_code, p)
                await self.add_student_relationship(student_code, p)
            except Exception as e:
                self.utils._log(traceback.format_exc())
                error_students.append(f'Name: {p.get("name")}, card_id: {p.get("card_id")}')
                continue
        return error_students

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
            await self.student_repo.update(StudentUpdate(
                code=Result[1].code,
                nationality=info.nationality,
                status=info.status,
                phone=info.phone,
                address=info.address
            ).dict())
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
        if await self.student_contact_infos_repo.get(info.student_code):
            await self.student_contact_infos_repo.update(info.dict())
            return None
        await self.student_contact_infos_repo.add(info.dict())

    async def add_subject_assessments_student_mongo(self, student_code: str, profile: dict) -> None:
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
        if await self.student_subject_assessments_repo.get(student_code):
            return None
        await self.student_subject_assessments_repo.add(SubjectAssessments(
            student_code=student_code,
            student_card_id=profile.get("card_id"),
            student_edu_id=profile.get("edu_id"),
            data=data
        ).to_dict())

    async def add_student_relationship(self, student_code: str, profile: dict):
        self.graph_student_repo.create({
            "code": student_code,
            "name": profile.get("name"),
            "card_id": profile.get("card_id"),
            "edu_id": profile.get("edu_id"),
        })
        student_contact_infos_record = {
            "code": student_code,
            "card_id": profile.get("card_id"),
            "edu_id": profile.get("edu_id"),
            "name": "Thông tin liên hệ",
            "url": f"{common_settings.API_URL}/student_contact_infos/{student_code}"
        }
        if self.graph_student_contact_infos_repo.get_by_id(student_code):
            self.graph_student_contact_infos_repo.update_by_id(student_code, student_contact_infos_record)
        else:
            self.graph_student_contact_infos_repo.create(student_contact_infos_record)
        student_subject_assessmets_record = {
            "code": student_code,
            "name": "Đánh giá môn học",
            "card_id": profile.get("card_id"),
            "edu_id": profile.get("edu_id"),
            "url": f"{common_settings.API_URL}/student_subject_assessmets/{student_code}"
        }
        if self.graph_student_subject_assessmets_repo.get_by_id(student_code):
            self.graph_student_subject_assessmets_repo.update_by_id(student_code, student_subject_assessmets_record)
        else:
            self.graph_student_subject_assessmets_repo.create(student_subject_assessmets_record)
        self.graph_student_repo.create_relationship(
            from_value=student_code,
            to_label="StudentContactInfos",
            to_id_field="code",
            to_value=student_code,
            relation_type="HAVE_CONTACT",
            relation_props=None
        )
        self.graph_student_repo.create_relationship(
            from_value=student_code,
            to_label="StudentSubjectAssessments",
            to_id_field="code",
            to_value=student_code,
            relation_type="HAVE_ASSESSMENT",
            relation_props=None
        )
    def create_student_assessment_outstanding(self, student_code: str, evidence: str, confident: float,
                                              name: str, indicator: str, comment: str, type_assessment: str) -> None:
        code = ontology_setting.ASSESSMENT2CODE[name]
        self.graph_student_repo.create_relationship(
            from_value=student_code,
            to_label="StudentSubAssessment",
            to_id_field="code",
            to_value=code,
            relation_type="OUTSTANDING",
            relation_props={
                "including": type_assessment,
                "indicator": indicator,
                "evidence": evidence,
                "full_comment": comment,
                "confident": confident
            }
        )

    def choose_assessment(self, type_assessment: str) -> Tuple[str, Callable[..., Any]]:
        if type_assessment == "Phẩm chất":
            return "student_quality", self.graph_student_Q_repo
        elif type_assessment == "Năng lực chung":
            return "student_general_abilities", self.graph_student_GA_repo
        elif type_assessment == "Năng lực đặc thù":
            return "student_special_abilities", self.graph_student_SA_repo

    def clear_student_assessment_outstanding(self, student_code: str, type_assessment: str) -> None:
        for code in ontology_setting.CODES_IN_ASSESSMENT_TYPE[type_assessment]:
            print(code)
            self.graph_student_repo.delete_relationship(
                from_value=student_code,
                to_label="StudentSubAssessment",
                to_id_field="code",
                to_value=code,
                relation_type="OUTSTANDING"
            )

    def calc_emb_distance(self, comment: str, kb: dict) -> dict:
        clauses = self.utils.split_clauses(comment)
        print(clauses)
        final_score = 0
        final_clause = None
        final_indicators = None
        level = self.get_level(self.utils.normalize_text(comment))
        if level > 0:
            clause_embs = self.embedding_assessment.model.encode(clauses, convert_to_tensor=True)
            for i, clause in enumerate(clauses):
                sims = self.embedding_assessment.util.cos_sim(clause_embs[i], kb.get("encode"))[0]
                best_idx = sims.argmax().item()
                score = float(sims[best_idx])
                if score <= final_score:
                    continue
                indicators = kb.get("all_indicators")[best_idx]
                final_score = score
                final_clause = clause
                final_indicators = indicators

        return {
            "evidence": final_clause,
            "confident": final_score,
            "indicator": final_indicators.get("indicator") if final_indicators else None,
            "level": level,
            "full_comment": comment
        }

    def get_level(self, text: str) -> int:
        if not text:
            return 0
        # Ưu tiên mức thấp trước
        for level in [0, 1, 2, 3]:
            for phrase in ontology_setting.LEVEL_KEYWORDS[level]:
                if phrase in text:
                    return level
        return 1
