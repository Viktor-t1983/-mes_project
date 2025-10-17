import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", "")

    # PlanFix
    PLANFIX_BASE_URL: str = os.getenv("PLANFIX_BASE_URL", "")
    PLANFIX_API_KEY: str = os.getenv("PLANFIX_API_KEY", "")
    PLANFIX_ACCOUNT: str = os.getenv("PLANFIX_ACCOUNT", "")

    # SolidWorks
    SOLIDWORKS_BOM_DIR: str = os.getenv("SOLIDWORKS_BOM_DIR", "./bom_imports")

    # 1C
    ONE_C_BASE_URL: str = os.getenv("ONE_C_BASE_URL", "")
    ONE_C_USER: str = os.getenv("ONE_C_USER", "")          # ← ЕДИНСТВЕННОЕ ИМЯ
    ONE_C_PASSWORD: str = os.getenv("ONE_C_PASSWORD", "")

    # Validation
    def __init__(self, **data):
        super().__init__(**data)
        if not self.DATABASE_URL:
            raise ValueError("DATABASE_URL must be set in .env")

settings = Settings()
