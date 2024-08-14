from dotenv import load_dotenv
from pydantic import BaseSettings

load_dotenv(verbose=True)

class Settings(BaseSettings):
    PROJECT_NAME: str
    DB_ENGINE: str
    DB_NAME: str
    DB_USER: str
    DB_PASS: str
    DB_HOST: str
    DB_PORT: str

settings = Settings()