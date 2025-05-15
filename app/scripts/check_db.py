#!/usr/bin/env python3
"""
Script simple para verificar la conexión a la base de datos directamente.
No depende de importaciones del proyecto.

Uso:
    python scripts/simple_db_check.py
"""

import os
import sys
import logging
import psycopg2
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger("db_check")

def check_postgres_connection():
    """
    Verifica la conexión a la base de datos PostgreSQL.
    """
    # Obtener variables de entorno
    postgres_user = os.getenv("POSTGRES_USER")
    postgres_password = os.getenv("POSTGRES_PASSWORD")
    postgres_db = os.getenv("POSTGRES_DB")
    postgres_host = os.getenv("POSTGRES_HOST", "localhost")
    postgres_port = os.getenv("POSTGRES_PORT", "5432")
    
    database_url = os.getenv("DATABASE_URL")
    
    if database_url:
        logger.info(f"Usando DATABASE_URL: {database_url}")
    else:
        logger.info(f"Conectando a PostgreSQL: {postgres_host}:{postgres_port}/{postgres_db} como {postgres_user}")
    
    try:
        # Conectar a PostgreSQL
        conn = psycopg2.connect(
            host=postgres_host,
            port=postgres_port,
            dbname=postgres_db,
            user=postgres_user,
            password=postgres_password
        )
        
        # Crear cursor
        cursor = conn.cursor()
        
        # Ejecutar consulta simple
        cursor.execute("SELECT 1")
        result = cursor.fetchone()
        
        if result and result[0] == 1:
            logger.info("✅ Conexión exitosa a la base de datos PostgreSQL")
            
            # Verificar tablas existentes
            cursor.execute("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public'
                ORDER BY table_name
            """)
            
            tables = cursor.fetchall()
            logger.info(f"Tablas encontradas ({len(tables)}):")
            for table in tables:
                logger.info(f"  - {table[0]}")
                
                # Verificar columnas de la tabla
                cursor.execute(f"""
                    SELECT column_name, data_type
                    FROM information_schema.columns
                    WHERE table_name = '{table[0]}'
                    ORDER BY ordinal_position
                """)
                
                columns = cursor.fetchall()
                for column in columns:
                    logger.info(f"      * {column[0]} ({column[1]})")
            
            # Verificar versión de Alembic
            try:
                cursor.execute("SELECT version_num FROM alembic_version")
                versions = cursor.fetchall()
                if versions:
                    logger.info(f"Versiones de Alembic: {[v[0] for v in versions]}")
                else:
                    logger.info("No hay versiones de Alembic registradas")
            except psycopg2.errors.UndefinedTable:
                logger.info("La tabla alembic_version no existe")
            
            return True
        else:
            logger.error("❌ La consulta de prueba no devolvió el resultado esperado")
            return False
            
    except Exception as e:
        logger.error(f"❌ Error al conectar a la base de datos: {str(e)}")
        return False
    finally:
        if 'conn' in locals() and conn is not None:
            conn.close()

def main():
    """
    Función principal.
    """
    logger.info("Verificando la conexión a la base de datos PostgreSQL...")
    
    if not check_postgres_connection():
        logger.error("No se pudo conectar a la base de datos PostgreSQL.")
        sys.exit(1)
    
    logger.info("Verificación completada con éxito.")

if __name__ == "__main__":
    main()