from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
import logging

from app.models.base import Base
from app.config import settings

# Configurar logging
logger = logging.getLogger(__name__)

# Opciones específicas para PostgreSQL
connect_args = {}

# Configuración del motor de base de datos
database_url = settings.DATABASE_URL
logger.info(f"Configurando conexión a la base de datos: {database_url}")

try:
    engine = create_engine(
        database_url,
        connect_args=connect_args,
        # Para desarrollo, es útil tener echo=True para ver las consultas SQL
        echo=settings.DEBUG
    )
    
    # Configuración de la sesión
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    
    logger.info("Motor de base de datos inicializado correctamente")
except Exception as e:
    logger.error(f"Error al inicializar el motor de base de datos: {str(e)}")
    # Proporcionar un valor por defecto para que la aplicación no falle al importar
    engine = None
    SessionLocal = sessionmaker()
    raise


def get_db():
    """
    Función generadora para obtener una sesión de base de datos.
    
    Yields:
        db: Sesión de SQLAlchemy
    """
    if engine is None:
        raise RuntimeError("El motor de base de datos no está inicializado correctamente")
    
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()