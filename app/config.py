from dotenv import load_dotenv
import os

load_dotenv()

class Settings:
    MONGO_URI = os.getenv("MONGO_URI")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    DB_NAME = os.getenv("DB_NAME")

settings = Settings()