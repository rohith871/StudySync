from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    PROJECT_NAME: str = "StudySync"
    DATABASE_URL: str = "sqlite+aiosqlite:///./studysync.db"
    CHROMA_PERSIST_DIR: str = "./chroma_db"
    
    GOOGLE_API_KEY: str = ""
    GROK_API_KEY: str = ""

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
