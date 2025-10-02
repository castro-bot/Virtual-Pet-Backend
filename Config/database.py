from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

# Load variables from the .env file
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL is not defined in the .env file")

# SQLAlchemy configuration
engine = create_engine(DATABASE_URL)  # Engine to connect to the database
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine) # Allows FastAPI to talk to the database by creating sessions.
Base = declarative_base()  # Base for defining table models

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()