from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

# Cargar variables del archivo .env
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL no está definida en el archivo .env")

# Configuración de SQLAlchemy
engine = create_engine(DATABASE_URL)  # Motor para conectar a la base de datos
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine) # Permite que FastAPI hable con la base de datos, creando sesiones.
Base = declarative_base()  # Base para definir los modelos de las tablas

# Dependencia para obtener la sesión de base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()