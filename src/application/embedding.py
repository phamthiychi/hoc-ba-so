
from typing import Dict, List
from sentence_transformers import SentenceTransformer, util

MODEL = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"

class EmbeddingSentence:
    def __init__(self):
        self.model = SentenceTransformer(MODEL)
        self.util = util

    def emb_knowledge(self, knowledge_base: Dict[str, List[str]]) -> dict:
        all_indicators = []
        for virtue, indicators in knowledge_base.items():
            for ind in indicators:
                all_indicators.append({
                    "virtue": virtue,
                    "indicator": ind
                })

        indicator_texts = [x["indicator"] for x in all_indicators]
        return {
            "encode": self.model.encode(indicator_texts, convert_to_tensor=True),
            "all_indicators": all_indicators
        }
