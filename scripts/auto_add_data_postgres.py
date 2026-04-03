import os
import re
import sys
import json
import shutil
import asyncio
import pandas as pd

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from src.application.core import SystemCore

from src.adapter.api.template.student import StudentCreate
# API
from src.adapter.database.postges_manager import postgres_manager
from src.adapter.database.postgres_repository import (
    PostgresAcademicYearRepository,
    PostgresClassRoomRepository,
    PostgresGradeLevelRepository,
    PostgresStudentRepository,
    PostgresSubjectRepository,
    PostgresTeacherRepository
)
from src.model.postgres.class_room import ClassRoom
from src.model.postgres.student import Student
from src.common.postgres_model_setting import settings

SESSION = postgres_manager.session
CORE = SystemCore(SESSION)
STUDENT_REPO = PostgresStudentRepository(SESSION)
ACADEMIC_YEAR_REPO = PostgresAcademicYearRepository(SESSION)
GRADE_LEVEL_REPO = PostgresGradeLevelRepository(SESSION)
CLASS_ROOM_REPO = PostgresClassRoomRepository(SESSION)
TEACHER_REPO = PostgresTeacherRepository(SESSION)
SUBJECT_REPO = PostgresSubjectRepository(SESSION)

def verify(Value):
    return None if pd.isna(Value) else Value

def extract(pattern, text):
    match = re.search(pattern, text, re.IGNORECASE)
    return match.group(1).strip() if match else None

def create_academic_year_code(academic_year) -> str:
    return f'NH{academic_year.replace(" - ", "")}'

def create_grade_level_code(class_room) -> str:
    return f"MK{settings.WORD2NUM[class_room.split(' ')[0]]:02}"

def create_class_code(class_room, grade_level_code) -> str:
    result = class_room.split(" ")
    return f"{grade_level_code[-3:]}.ML{settings.WORD2SHORTCUT[result[0]]}{result[1]}"

def create_student_code(index, academic_year_code, grade_level_code, class_code) -> str:
    return f"{academic_year_code[2:]}.{grade_level_code[-2:]}.{class_code[-3:]}.{index:03}"

def create_teacher_code(index, subject) -> str:
    return f'{settings.SUBJECT2SHORTCUT[subject]}.GV{index:02}'

def get_data_base_on_profile_type(row, additional_info, profile_type) -> dict:
    if profile_type == "student":
        return StudentCreate(
            academic_year=additional_info.get("academic_year"),
            class_name=verify(row.get("Mã lớp")),
            name=verify(row.get("Họ tên")),
            date_of_birth=pd.to_datetime(row.get("Ngày sinh"),
                                            errors="coerce") \
                             .strftime("%Y-%m-%d") if verify(row.get("Ngày sinh")) else None,
            gender=verify(row.get("Giới tính")),
            ethnicity=verify(row.get("Dân tộc")),
            nationality=verify(row.get("Quốc tịch")),
            card_id=None if pd.isna(row.get("Số CCCD")) else str(row.get("Số CCCD")),
            edu_id=None if pd.isna(row.get("Mã định danh Bộ GD&ĐT")) else str(row.get("Mã định danh Bộ GD&ĐT")),
            status=verify(row.get("Trạng thái HS")),
            phone=None if pd.isna(row.get("Số điện thoại liên hệ")) else f'0{str(row.get("Số điện thoại liên hệ"))}',
            address=verify(row.get("Chỗ ở hiện nay chi tiết")),
            father_name=verify(row.get("Họ tên cha")),
            father_job=verify(row.get("Nghề nghiệp cha")),
            father_card_id=None if pd.isna(row.get("Số CCCD/CMND/DDCN cha")) else str(row.get("Số CCCD/CMND/DDCN cha")).split(".")[0],
            father_phone=None if pd.isna(row.get("Số điện thoại cha")) else f'0{str(row.get("Số điện thoại cha"))}'.split(".")[0],
            mother_name=verify(row.get("Họ tên mẹ")),
            mother_job=verify(row.get("Nghề nghiệp mẹ")),
            mother_card_id=None if pd.isna(row.get("Số CCCD/CMND/DDCN mẹ")) else str(row.get("Số CCCD/CMND/DDCN mẹ")).split(".")[0],
            mother_phone=None if pd.isna(row.get("Số điện thoại mẹ")) else f'0{str(row.get("Số điện thoại mẹ"))}'.split(".")[0],
            guardian_name=verify(row.get("Họ tên người giám hộ")),
            guardian_job=verify(row.get("Nghề nghiệp người giám hộ")),
            guardian_card_id=None if pd.isna(row.get("Số CCCD/CMND/DDCN người giám hộ")) else str(row.get("Số CCCD/CMND/DDCN người giám hộ")).split(".")[0],
            guardian_phone=None if pd.isna(row.get("Số điện thoại người giám hộ")) else f'0{str(row.get("Số điện thoại người giám hộ"))}'.split(".")[0],
            place_of_birth=verify(row.get("Nơi sinh"))
        )
    elif profile_type == "teacher":
        if row.get("Vị trí việc làm") != "Giáo viên":
            return None
        return {
            "name": verify(row.get("Họ tên")),
            "date_of_birth": pd.to_datetime(row.get("Ngày sinh"),
                                            errors="coerce") \
                             .strftime("%Y-%m-%d") if verify(row.get("Ngày sinh")) else None,
            "gender": verify(row.get("Giới tính")),
            "ethnicity": verify(row.get("Dân tộc")),
            "nationality": "Việt Nam",
            "card_id": None if pd.isna(row.get("Số CMTND/TCC")) else str(row.get("Số CMTND/TCC")),
            "edu_id": None if pd.isna(row.get("Mã định danh Bộ GD&ĐT")) else str(row.get("Mã định danh Bộ GD&ĐT")),
            "status": verify(row.get("Trạng thái CB")),
            "phone": None if pd.isna(row.get("Điện thoại")) else f'0{str(row.get("Điện thoại"))}',
            "specialization": verify(row.get("Chuyên ngành chính")),
            "position": verify(row.get("Nhóm chức vụ")),
            "subject": verify(row.get("Môn dạy"))
        }

def preprocessing(file_xls, additional_info, profile_type) -> list:
    df = pd.read_excel(file_xls)
    result = []
    for _, row in df.iterrows():
        data = get_data_base_on_profile_type(row, additional_info, profile_type)
        if data:
            result.append(data)
        # if len(result) > 1:
    return result

async def create_and_update_teacher(teacher_code, info) -> None:
    teacher_repo = {
        "code": teacher_code,
        "name": info.get("name"),
        "date_of_birth":info.get("date_of_birth"),
        "gender": info.get("gender"),
        "ethnicity": info.get("ethnicity"),
        "nationality": info.get("nationality"),
        "card_id": info.get("card_id"),
        "edu_id": info.get("edu_id"),
        "status": info.get("status"),
        "phone": info.get("phone"),
        "specialization": info.get("specialization"),
        "position": info.get("position")
    }
    try:
        result = await TEACHER_REPO.add(teacher_repo)
        if result is None:
            try:
                await TEACHER_REPO.update(teacher_repo)
            except Exception:
                return None
        else:
            return teacher_repo
    except Exception as e:
        print(f"Error {e}")
        return None

async def create_and_update_student(student_code, info) -> None:
    student_record = {
        "code": student_code,
        "name": info.get("name"),
        "date_of_birth":info.get("date_of_birth"),
        "gender": info.get("gender"),
        "ethnicity": info.get("ethnicity"),
        "nationality": info.get("nationality"),
        "card_id": info.get("card_id"),
        "edu_id": info.get("edu_id"),
        "status": info.get("status"),
        "phone": info.get("phone"),
        "address": info.get("address"),
        "father_name": info.get("father_name"),
        "father_job": info.get("father_job"),
        "father_phone": info.get("father_phone"),
        "father_card_id": info.get("father_card_id"),
        "mother_name": info.get("mother_name"),
        "mother_job": info.get("mother_job"),
        "mother_phone": info.get("mother_phone"),
        "mother_card_id": info.get("mother_card_id"),
        "guardian_name": info.get("guardian_name"),
        "guardian_job": info.get("guardian_job"),
        "guardian_phone": info.get("guardian_phone"),
        "guardian_card_id": info.get("guardian_card_id"),
        "place_of_birth": info.get("place_of_birth"),
    }
    try:
        result = await STUDENT_REPO.add(student_record)
        if result is None:
            try:
                await STUDENT_REPO.update(student_record)
            except Exception:
                return None
        else:
            return student_record
    except Exception as e:
        print(f'Error {e}')
        return None

async def create_and_update_academic_year(academic_year_codes, start_date, end_date) -> None:
    for code in academic_year_codes:
        info = code[2:]
        mark = int(len(info) / 2)
        academic_year_record = {
            "code": code,
            "name": f"{info[:mark]}-{info[mark:]}",
            "start_date": start_date,
            "end_date": end_date,
        }
        result = await ACADEMIC_YEAR_REPO.add(academic_year_record)
        if result is None:
            await ACADEMIC_YEAR_REPO.update(academic_year_record)

async def create_and_update_grade_level(grade_level_codes) -> None:
    for code in grade_level_codes:
        max_students = 0
        class_rooms = [result.to_dict()
                       for result in SESSION.query(ClassRoom) \
                                            .filter(ClassRoom.code.like(f"{code[-3:]}%")).all()]
        max_students += sum([class_room['size'] for class_room in class_rooms])
        grade_level_record = {
            "code": code,
            "name": f"Khối {int(code.split('MK')[1])}",
            "max_students": max_students
        }
        result = await GRADE_LEVEL_REPO.add(grade_level_record)
        if result is None:
            await GRADE_LEVEL_REPO.update(grade_level_record)

async def create_and_update_class_room(class_room_codes, special_program) -> None:
    for code in class_room_codes:
        print(f"ztanloc {code}")
        students = [result.to_dict()
                    for result in SESSION.query(Student) \
                                         .filter(Student.code.like(f"%{code[-3:]}%")).all()]
        class_name = f'{settings.SHORTCUT2WORD[code.split("ML")[1][:2]]} {code.split("ML")[1][2]}'
        class_room_record = {
            "code": code,
            "name": class_name,
            "size": len(students),
            "grade_level_id": create_grade_level_code(class_name),
            "special_program": special_program
        }
        result = await CLASS_ROOM_REPO.add(class_room_record)
        print(f"ztanloc {result}")
        if result is None:
            await CLASS_ROOM_REPO.update(class_room_record)

async def create_and_update_subject(subjects, total_periods_default = 30) -> None:
    for sub in subjects:
        subject_repo = {
            "code": f'MH{settings.SUBJECT2SHORTCUT[sub]}',
            "name": sub,
            "total_periods": total_periods_default
        }
        result = await SUBJECT_REPO.add(subject_repo)
        if result is None:
            await SUBJECT_REPO.update(subject_repo)

async def import_data_from_student_profile(student_profile, additional_info) -> None:
    info_from_student_profile = preprocessing(student_profile, additional_info, "student")
    student_errors = []
    for info in info_from_student_profile:
        result = await CORE.add_student(info)
        if result is None:
            student_errors.append(info)

    if student_errors:
        with open("student_profile_error_portgres.json", "w", encoding="utf-8") as f:
            json.dump(student_errors, f, indent=4, ensure_ascii=False)

async def import_data_from_teacher_profile(teacher_profile) -> None:
    info_from_teacher_profile = preprocessing(teacher_profile, "teacher")
    index = 1
    teacher_error = []
    subjects = set()
    for info in info_from_teacher_profile:
        teacher_code = create_teacher_code(index, info.get("subject"))
        subjects.add(info.get("subject"))
        result = await create_and_update_teacher(teacher_code, info)
        if result is None:
            teacher_error.append(info)
        index = index + 1
    await create_and_update_subject(subjects)
    if teacher_error:
        with open("teacher_profile_error_portgres.json", "w", encoding="utf-8") as f:
            json.dump(teacher_error, f, indent=4, ensure_ascii=False)
