import os
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from dotenv import load_dotenv

load_dotenv()

def get_db_connection_uri(default_uri="sqlite:///default_habit_tracker.db"):
    return os.getenv("DB_CONNECTION_URI", default_uri)

def create_database_engine(uri):
    connect_args = {}
    if "sqlite" in uri:
        connect_args["check_same_thread"] = False
    return create_engine(uri, connect_args=connect_args)

def create_scoped_session(engine):
    return scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

def get_database_session():
    return database_session_scoped

DB_CONNECTION_URI = get_db_connection_uri()
database_engine = create_database_engine(DB_CONNECTION_URI)
database_session_scoped = create_scoped_session(database_engine)