import torch
import datetime
from typing import get_args
from sentence_transformers import SentenceTransformer, util

from src.common.ontology_setting import settings
from src.model.ontology.student import StudentReport, StudentAssessment

class AssessmentStudentExtractor:
    def __init__(self):
        self.model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
        self.valid_competencies = list(get_args(StudentAssessment.__annotations__['competency']))
        self.comp_embeddings = self.model.encode(self.valid_competencies, convert_to_tensor=True)
        self.category_map = settings.CATEGORY_STUDENT_ASSESSMENT_MAPPING
        self.log_file = settings.DIR_SAVE_UNKNOWN_CATEGORY_STUDENT_ASSESSMENT

    def _log_missing_competency(self, message):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(self.log_file, "w", encoding="utf-8") as f:
            f.write(f"[{timestamp}] Cảnh báo: {message} \n")

    def _get_level(self, sentence: str) -> str:
        sentence_low = sentence.lower()
        if any(kw in sentence_low for kw in ["chưa", "cần", "hạn chế", "yếu", "kém", "hơn"]):
            return "Cần cố gắng"
        if any(kw in sentence_low for kw in ["tốt", "giỏi", "xuất sắc", "tích cực", "thạo"]):
            return "Hoàn thành tốt"
        self._log_missing_competency(f"Không tìm thấy level trong câu {sentence}")
        return "Hoàn thành"

    def _get_category(self, comp):
        if comp in self.category_map:
            return self.category_map[comp]
        else:
            self._log_missing_competency(f"{comp} chưa được phân loại vào category")
            return "Chưa phân loại"

    def analyze(self, student_code: str,
                student_name: str,  student_car_id: str,  student_edu_id: str,
                full_comment: str,
                threshold=0.35) -> StudentReport:
        sentences = [s.strip() for s in full_comment.split('.') if len(s.strip()) > 5]
        results = []
        for sentence in sentences:
            sentence_vec = self.model.encode(sentence, convert_to_tensor=True)
            scores = util.cos_sim(sentence_vec, self.comp_embeddings)[0]
            matched_indices = torch.where(scores > threshold)[0]
            if len(matched_indices) > 0:
                for idx in matched_indices:
                    idx = idx.item()
                    comp = self.valid_competencies[idx]
                    assessment = StudentAssessment(
                        category=self._get_category(comp),
                        competency=comp,
                        level=self._get_level(sentence),
                        evidence=sentence
                    )
                    results.append(assessment)
            score_values = [s.item() for s in scores]
            if all(s > threshold for s in score_values):
                continue
            self._log_missing_competency(f"Với câu {sentence}")
            for name, score in zip(self.valid_competencies, scores):
                score_val = score.item() if hasattr(score, 'item') else score
                if score_val <= threshold:
                    self._log_missing_competency(
                        f"  Low Match - Competency: {name:20} | Score: {score_val:.4f}"
                    )
        return StudentReport(code=student_code,
                             name=student_name,
                             card_id=student_car_id,
                             edu_id=student_edu_id,
                             assessments=results)
