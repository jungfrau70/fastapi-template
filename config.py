import os
import socket
from dotenv import load_dotenv

load_dotenv(dotenv_path=".env")

class Settings:
    TITLE = "Lenz Backend"
    VERSION = "0.0.1"
    DESCRIPTION = """
    this is Lenz Project
    this is not for production
    """
    NAME = "Ian Jung"
    EMAIL= "inhwan.jung@gmail.com"
    
    POSTGRES_USER = os.getenv("POSTGRES_USER")
    POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
    POSTGRES_SERVER = os.getenv("POSTGRES_SERVER", socket.gethostbyname(socket.gethostname()))
    POSTGRES_PORT = os.getenv("POSTGRES_PORT", 5432)
    POSTGRES_DATABASE= os.getenv("POSTGRES_DATABASE", "mydb")
    DATABASE_URL = f"postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DATABASE}"

    SECRET_KEY : str = os.getenv("SECRET_KEY")
    ALGORITHM : str = os.getenv("ALGORITHM")

    TEST_EMAIL = "user1@example.com"
    TEST_NAME = "User1"
    TEST_PASS = "user1"
    TEST_ITEM = "test item"
    TEST_ITEM_DESC = "test item description"

setting = Settings()