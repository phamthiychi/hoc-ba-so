
import os
import json
import hashlib
import torch
from typing import Dict, List
from sentence_transformers import SentenceTransformer, util
from src.common.common_setting import settings

CACHE_DIR = settings.REPO_ROOT / "cache"
MODEL = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"

class EmbeddingSentence:
    def __init__(self):
        self.model = SentenceTransformer(MODEL)
        self.util = util

    def _flatten_knowledge(self, knowledge_base: Dict[str, List[str]]) -> dict:
        all_indicators = []
        for virtue, indicators in knowledge_base.items():
            for ind in indicators:
                all_indicators.append({
                    "virtue": virtue,
                    "indicator": ind
                })
        return all_indicators

    def _hash_knowledge(self, knowledge_base: Dict[str, List[str]]) -> str:
        data = json.dumps(knowledge_base, ensure_ascii=False, sort_keys=True)
        return hashlib.md5(data.encode("utf-8")).hexdigest()

    def emb_knowledge(self, name: str, knowledge_base: Dict[str, List[str]]) -> dict:
        os.makedirs(CACHE_DIR, exist_ok=True)
        CACHE_FILE = os.path.join(CACHE_DIR, f"{name}_indicator_embeddings.pt")
        META_FILE = os.path.join(CACHE_DIR, f"{name}_indicator_embeddings_meta.json")
        kb_hash = self._hash_knowledge(knowledge_base)
        if os.path.exists(CACHE_FILE) and os.path.exists(META_FILE):
            with open(META_FILE, "r", encoding="utf-8") as f:
                meta = json.load(f)
            if meta.get("kb_hash") == kb_hash and meta.get("model") == MODEL:
                data = torch.load(CACHE_FILE)
                return {
                    "encode": data["encode"],
                    "all_indicators": data["all_indicators"]
                }
        all_indicators = self._flatten_knowledge(knowledge_base)
        indicator_texts = [x["indicator"] for x in all_indicators]
        embeddings = self.model.encode(
            indicator_texts,
            convert_to_tensor=True,
            batch_size=16,
            show_progress_bar=True
        )
        torch.save({
            "encode": embeddings,
            "all_indicators": all_indicators
        }, CACHE_FILE)
        with open(META_FILE, "w", encoding="utf-8") as f:
            json.dump({
                "kb_hash": kb_hash,
                "model": MODEL
            }, f, ensure_ascii=False, indent=2)
        return {
            "encode": embeddings,
            "all_indicators": all_indicators
        }
