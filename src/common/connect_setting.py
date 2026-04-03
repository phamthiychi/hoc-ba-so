import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    MONGO_DB_USERNAME = os.getenv("MONGO_DB_USERNAME")
    MONGO_DB_PASSWORD = os.getenv("MONGO_DB_PASSWORD")
    POSTGRES_DB_PASSWORD = os.getenv("POSTGRES_DB_PASSWORD")
    CHAT_GPT_API_KEY = os.getenv("CHAT_GPT_API_KEY")
    MONGO_DB_URI = f"mongodb+srv://{MONGO_DB_USERNAME}:{MONGO_DB_PASSWORD}@hocbaso-data.wyldsrm.mongodb.net/?appName=HocBaSo-Data"
    POSTGRES_DB_URI = f"postgresql://postgres.kygrdncbipnmyzikossl:{POSTGRES_DB_PASSWORD}@aws-1-ap-southeast-2.pooler.supabase.com:5432/postgres"

    METADATA_MONGO_DB = os.getenv("METADATA_MONGO_DB")
    # ANALYTICS_DB = os.getenv("ANALYTICS_DB")
    # AUDIT_DB = os.getenv("AUDIT_DB")

settings = Settings()