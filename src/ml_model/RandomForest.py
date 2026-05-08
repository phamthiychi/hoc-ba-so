from joblib import load
from src.common.common_setting import settings

LABEL_FIELDS = [
    "Ngôn ngữ",
    "Tính toán",
    "Khoa học",
    "Công nghệ",
    "Tin học",
    "Thẩm mĩ",
    "Thể chất"
]

REVERSE_LEVEL_MAPPING = {
    0: "Không có",
    1: "Chưa đủ cơ sở",
    2: "Đang hình thành",
    3: "Đạt",
    4: "Nổi trội"
}

SUBJECTS = [
    "vietnamese_comment",
    "mathematics_comment",
    "informatics_comment",
    "science_comment",
    "history_and_geography_comment",
    "english_comment",
    "technology_comment",
    "music_comment",
    "arts_comment",
    "civics_comment",
    "physical_education_comment",
    "experiential_activities_comment"
    # "nature_and_society_comment"
]

class StudentSpecialAssessmentRandomForest:
    def __init__(self):
        self.model = load(settings.SRC_ROOT / "ml_model/random_forest_special_assessment.pkl")

    def predict(self, data):
        if data is None:
            return None
        features = self.load_input(data)
        prediction = self.model.predict([features])[0]
        result = []
        for field, level_id in zip(LABEL_FIELDS, prediction):
            result.append({
                "field": field,
                "level": REVERSE_LEVEL_MAPPING[int(level_id)]
            })
        return result

    def load_input(self, data):
        features = []
        for subject in SUBJECTS:
            subject_data = data.get(subject, {})
            confident = subject_data.get("confident", 0)
            level = subject_data.get("level", 0)
            features.append(confident)
            features.append(level)
        return features
