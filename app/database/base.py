from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

from app.config import settings
from app.models.base import Base

# Opciones específicas para PostgreSQL
connect_args = {}

# Configuración del motor de base de datos
database_url = settings.DATABASE_URL
print(f"Connecting to database: {database_url}")

engine = create_engine(
    database_url,
    connect_args=connect_args,
    # Para desarrollo, es útil tener echo=True para ver las consultas SQL
    echo=settings.DEBUG
)

# Configuración de la sesión
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    """
    Función generadora para obtener una sesión de base de datos.
    
    Yields:
        db: Sesión de SQLAlchemy
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()