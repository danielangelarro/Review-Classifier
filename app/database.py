from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

DATABASE_URL_DOCKER = "postgresql://user:password@db/app_db"
DATABASE_URL_LOCAL = "postgresql://postgres:postgres@localhost:5434/app_db"

# Selecciona la URL de la base de datos según una variable de entorno
DATABASE_URL = os.getenv("DATABASE_URL", DATABASE_URL_LOCAL)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()