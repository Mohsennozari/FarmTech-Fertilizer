# Platform-v3\backend\app\config.py

import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./farmtech.db")
    DEBUG: bool = os.getenv("DEBUG", "True").lower() == "true"
    API_VERSION: str = "3.0.0"
    API_TITLE: str = "FarmTech API"

settings = Settings()