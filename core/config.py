import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    DB_NAME: str = os.getenv("DB_NAME")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD")
    DB_HOST: str = os.getenv("DB_HOST")
    DB_USER: str = os.getenv("DB_USER")
    DB_PORT: str = os.getenv("DB_PORT")

settings = Settings()