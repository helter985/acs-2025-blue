#!/usr/bin/env python3
"""
Script para forzar la ejecución de las migraciones de Alembic usando conexión directa a la base de datos.
Esto es útil cuando la migración normal de Alembic no funciona correctamente.

Uso:
    python -m scripts.force_migration
"""

import sys
import os
import logging
import glob
from sqlalchemy import create_engine, text

# Agregar la ruta del proyecto al PYTHONPATH
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.config import settings
from app.models.base import Base

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger("force_migration")

def get_migration_version():
    """
    Obtiene la última versión de migración de Alembic.
    """
    try:
        # Obtener lista de archivos de migración
        migration_files = glob.glob(os.path.join("alembic", "versions", "*.py"))
        if not migration_files:
            logger.error("No se encontraron archivos de migración")
            return None
        
        # Ordenar por fecha de modificación (más reciente primero)
        migration_files.sort(key=os.path.getmtime, reverse=True)
        
        # Extraer versión del nombre del archivo (XXXXXXXXXXXX_name.py)
        latest_file = os.path.basename(migration_files[0])
        version = latest_file.split("_")[0]
        
        logger.info(f"Última versión de migración encontrada: {version}")
        return version
    except Exception as e:
        logger.error(f"Error al obtener la versión de migración: {str(e)}")
        return None

def create_alembic_version_table(engine, version):
    """
    Crea la tabla alembic_version y registra la versión actual.
    """
    try:
        with engine.begin() as conn:
            # Verificar si la tabla ya existe
            result = conn.execute(text("SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = 'alembic_version')"))
            table_exists = result.scalar()
            
            if table_exists:
                logger.info("La tabla alembic_version ya existe")
                
                # Actualizamos la versión
                conn.execute(text("DELETE FROM alembic_version"))
                conn.execute(text(f"INSERT INTO alembic_version (version_num) VALUES ('{version}')"))
                logger.info(f"Versión actualizada a: {version}")
            else:
                # Crear la tabla y registrar la versión
                conn.execute(text("CREATE TABLE alembic_version (version_num VARCHAR(32) NOT NULL)"))
                conn.execute(text(f"INSERT INTO alembic_version (version_num) VALUES ('{version}')"))
                logger.info(f"Tabla alembic_version creada con versión: {version}")
                
        return True
    except Exception as e:
        logger.error(f"Error al crear la tabla alembic_version: {str(e)}")
        return False

def force_create_tables(engine):
    """
    Fuerza la creación de todas las tablas desde los modelos SQLAlchemy.
    """
    try:
        # Crear tablas definidas en los modelos
        Base.metadata.create_all(engine)
        logger.info("Tablas creadas desde los modelos SQLAlchemy")
        return True
    except Exception as e:
        logger.error(f"Error al crear tablas: {str(e)}")
        return False

def main():
    """
    Función principal.
    """
    logger.info("Iniciando migración forzada...")
    
    # Crear motor de base de datos
    engine = create_engine(settings.DATABASE_URL, echo=True)
    
    # Obtener la última versión de migración
    version = get_migration_version()
    if not version:
        logger.error("No se pudo obtener la versión de migración")
        sys.exit(1)
    
    # Forzar creación de tablas
    logger.info("Forzando creación de tablas...")
    if not force_create_tables(engine):
        logger.error("Error al crear las tablas")
        sys.exit(1)
    
    # Crear o actualizar la tabla alembic_version
    logger.info("Actualizando la tabla alembic_version...")
    if not create_alembic_version_table(engine, version):
        logger.error("Error al actualizar la tabla alembic_version")
        sys.exit(1)
    
    logger.info("Migración forzada completada con éxito.")

if __name__ == "__main__":
    main()