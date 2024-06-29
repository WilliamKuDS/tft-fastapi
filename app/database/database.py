from sqlmodel import create_engine
import os
from dotenv import load_dotenv

load_dotenv()

postgres_pass = os.getenv("POSTGRES_PASSWORD", None)

#SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
SQLALCHEMY_DATABASE_URL = f"postgresql://tft:{postgres_pass}@192.168.68.120:5433/tft"
#connect_args = {"check_same_thread": False}

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    echo=True,
#    connect_args=connect_args
)
