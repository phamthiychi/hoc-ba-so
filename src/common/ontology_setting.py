import os
from dotenv import load_dotenv

from src.common.common_setting import settings as setting_common

load_dotenv()

class Settings:
    CATEGORY_STUDENT_ASSESSMENT_MAPPING = {
            "Toán học": "Kiến thức",
            "Ngôn ngữ": "Kiến thức",
            "Giao tiếp": "Kỹ năng",
            "Giải quyết vấn đề": "Kỹ năng",
            "Tự học": "Thái độ"
        }
    DIR_SAVE_UNKNOWN_CATEGORY_STUDENT_ASSESSMENT = \
        setting_common.REPO_ROOT / "logs/unknow_category_student_assessment.txt"
    NEO4J_DB_URI = os.getenv("NEO4J_DB_URI")
    NEO4J_DB_USER = os.getenv("NEO4J_DB_USER")
    NEO4J_DB_PASSWORD = os.getenv("NEO4J_DB_PASSWORD")
    NEO4J_DB = os.getenv("NEO4J_DB")

settings = Settings()