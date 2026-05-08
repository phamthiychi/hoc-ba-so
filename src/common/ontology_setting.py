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
        "Thể chất": "physical_education",
        "Công nghệ": "technology",
        "Tin học": "informatics"
    }
    LEVEL2CODE = {
        "Đang hình thành": "DEVELOPING",
        "Đạt": "HAS_ACQUIRED",
        "Nổi trội": "OUTSTANDING"
    }
    CODES_IN_ASSESSMENT_TYPE = {
        "Phẩm chất": ["patriotism", "compassion", "diligence", "honesty", "responsibility"],
        "Năng lực chung": ["self_reliance_self_learning", "communication_collaboration", "problem_solving_creativity"],
        "Năng lực đặc thù": ["language", "numeracy", "science", "aesthetics", "physical_education"]
    }
    LEVEL_KEYWORDS = {
    0: [
        "chưa đọc được",
        "chưa viết được",
        "chưa hoàn thành",
        "không hoàn thành",
        "chưa có kỹ năng",
        "không thực hiện được",
        "chưa biết",
        "không có",
        "rất yếu",
        "chưa đạt yêu cầu",
    ],
    1: [
        "còn lúng túng",
        "cần cố gắng",
        "cần rèn thêm",
        "cần tích cực hơn",
        "bước đầu",
        "biết ở mức cơ bản",
        "có tham gia nhưng chưa tốt",
        "đôi khi còn",
        "chưa chủ động",
    ],
    2: [
        "hoàn thành nội dung môn học",
        "hoàn thành nhiệm vụ",
        "thực hiện được",
        "biết thực hiện",
        "đạt yêu cầu",
        "biết vận dụng",
        "có tiến bộ",
        "tham gia tốt",
        "nắm được kiến thức cơ bản",
    ],
    3: [
        "nổi bật",
        "thành thạo",
        "chủ động",
        "sáng tạo",
        "tích cực",
        "thực hiện tốt",
        "vượt yêu cầu",
        "rất tốt",
        "biết hỗ trợ bạn",
        "hoàn thành xuất sắc",
    ],
}

settings = Settings()
