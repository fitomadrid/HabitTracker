from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

DB_CONNECTION_URI = os.getenv("DB_CONNECTION_URI", "sqlite:///default_habit_tracker.db")

database_engine = create_engine(DB_CONNECTION_URI, connect_args={"check_same_thread": False})

database_session_scoped = scoped_session(sessionmaker(autocommit=False,
                                                      autoflush=False,
                                                      bind=database_engine))

def get_database_session():
    return database_session_scoped