import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    NEO4J_DB_URI = os.getenv("NEO4J_DB_URI")
    NEO4J_DB_USER = os.getenv("NEO4J_DB_USER")
    NEO4J_DB_PASSWORD = os.getenv("NEO4J_DB_PASSWORD")
    NEO4J_DB = os.getenv("NEO4J_DB")
    ASSESSMENT2CODE = {
        "Yêu nước": "patriotism",
        "Nhân ái": "compassion",
        "Chăm chỉ": "diligence",
        "Trung thực": "honesty",
        "Trách nhiệm": "responsibility",
        "Tự chủ và tự học": "self_reliance_self_learning",
        "Giao tiếp và hợp tác": "communication_collaboration",
        "Giải quyết vấn đề và sáng tạo": "problem_solving_creativity",
        "Ngôn ngữ": "language",
        "Tính toán": "numeracy",
        "Khoa học": "science",
        "Thẩm mĩ": "aesthetics",
        "Thể chất": "physical_education"
    }
    CODES_IN_ASSESSMENT_TYPE = {
        "Phẩm chất chủ yếu": ["patriotism", "compassion", "diligence", "honesty", "responsibility"],
        "Năng lực chung": ["self_reliance_self_learning", "communication_collaboration", "problem_solving_creativity"],
        "Năng lực đặc thù": ["language", "numeracy", "science", "aesthetics", "physical_education"]
    }

settings = Settings()
