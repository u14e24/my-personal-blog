from sqlmodel import SQLModel, create_engine, Session
from sqlalchemy import event, Engine
import sqlite3
from app.models.post import Post
from app.models.post_tag import PostTag
from app.models.tag import Tag
from pathlib import Path

# TODO: Move DATABASE_URL and SECRET_KEY to environment variables (use python-dotenv)

BASE_DIR = Path(__file__).resolve().parent

DATABASE_URL = f"sqlite:///{BASE_DIR}/blog_zsoptij.db"

@event.listens_for(Engine, "connect")
def enable_sqlite_fk(dbapi_connection, connection_record):
    if isinstance(dbapi_connection, sqlite3.Connection):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON;")
        cursor.close()

engine = create_engine(DATABASE_URL, echo=True)

def get_session():
    with Session(engine) as session:
        yield session

def get_engine():
    return engine