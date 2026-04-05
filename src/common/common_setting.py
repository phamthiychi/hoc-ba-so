import os
from dotenv import load_dotenv
import pathlib

load_dotenv()

class Settings:
    current_file_path = pathlib.Path(__file__).resolve()
    REPO_ROOT = current_file_path.parent.parent.parent
    SRC_ROOT = REPO_ROOT / "src"
    API_URL = "http://127.0.0.1:8000"

settings = Settings()