from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.config import settings

# Crear la base para los modelos ORM
Base = declarative_base()

# Configuración del motor de base de datos
engine = create_engine(settings.DATABASE_URL)

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