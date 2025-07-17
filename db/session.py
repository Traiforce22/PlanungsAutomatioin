# db/session.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# DB file (SQLite)
DATABASE_URL = "sqlite:///planung.db"

# Engine & Session
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)

# Base class for models
Base = declarative_base()
