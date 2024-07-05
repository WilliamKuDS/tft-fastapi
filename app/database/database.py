from sqlmodel import create_engine
import os
from dotenv import load_dotenv

load_dotenv()

pg_user = os.getenv("POSTGRES_USER", "postgres")
pg_pass = os.getenv("POSTGRES_PASSWORD", "")
pg_server = os.getenv("POSTGRES_SERVER", "127.0.0.1")
pg_port = os.getenv("POSTGRES_PORT", "5432")
pg_db = os.getenv("POSTGRES_DB", "postgres")

#SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
SQLALCHEMY_DATABASE_URL = f"postgresql://{pg_user}:{pg_pass}@{pg_server}:{pg_port}/{pg_db}"
#connect_args = {"check_same_thread": False}

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    echo=True,
#    connect_args=connect_args
)
