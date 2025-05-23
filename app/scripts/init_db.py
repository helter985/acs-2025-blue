"""
Script para inicializar la base de datos con datos de ejemplo
para la aplicación Interlimpia.

Este script debe ejecutarse después de que las migraciones de Alembic
hayan creado las tablas. Solo carga datos iniciales de categorías y productos.

Uso:
    python -m scripts.init_db
"""

import sys
import os
import logging

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger("init_db")

# Agregar la ruta del proyecto al PYTHONPATH
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from sqlalchemy.orm import Session
from sqlalchemy import inspect

from app.database.base import Base, engine, SessionLocal
from app.models.categoria import Categoria
from app.models.producto import Producto
from app.config import settings

# Verificar la conexión a la base de datos
def check_database_connection():
    """
    Verifica la conexión a la base de datos.
    """
    try:
        # Imprimir información de la base de datos
        logger.info(f"Intentando conectar a: {settings.DATABASE_URL}")
        
        # Intentar conectar
        db = SessionLocal()
        result = db.execute("SELECT 1").fetchone()
        db.close()
        
        if result:
            logger.info("Conexión a la base de datos establecida correctamente")
            return True
        else:
            logger.error("La consulta de prueba no retornó resultados")
            return False
    except Exception as e:
        logger.error(f"Error al conectar a la base de datos: {str(e)}")
        return False

# Verificar si las tablas existen
def check_tables_exist():
    """
    Verifica si las tablas existen en la base de datos.
    """
    inspector = inspect(engine)
    existing_tables = inspector.get_table_names()
    expected_tables = ['categorias', 'productos']
    
    logger.info(f"Tablas encontradas: {existing_tables}")
    
    for table in expected_tables:
        if table not in existing_tables:
            logger.warning(f"La tabla {table} no existe. Ejecute las migraciones de Alembic primero.")
            return False
    
    return True


def init_categorias(db: Session):
    """
    Inicializa las categorías de productos.
    """
    categorias = [
        {
            "id": "limpieza_hogar",
            "nombre": "Limpieza del Hogar",
            "descripcion": "Productos para la limpieza doméstica"
        },
        {
            "id": "limpieza_industrial",
            "nombre": "Limpieza Industrial",
            "descripcion": "Productos para la limpieza de espacios industriales y comerciales"
        }
    ]
    
    for categoria_data in categorias:
        # Verificar si la categoría ya existe
        categoria_existente = db.query(Categoria).filter(
            Categoria.id == categoria_data["id"]
        ).first()
        
        if not categoria_existente:
            # Crear la categoría si no existe
            nueva_categoria = Categoria(
                id=categoria_data["id"],
                nombre=categoria_data["nombre"],
                descripcion=categoria_data["descripcion"]
            )
            db.add(nueva_categoria)
            print(f"Categoría creada: {nueva_categoria.nombre}")
    
    db.commit()


def init_productos(db: Session):
    """
    Inicializa algunos productos de ejemplo.
    """
    productos = [
        {
            "codigo": "A123",
            "marca": "Mr. Clean",
            "descripcion": "Limpiador multiusos con aroma a limón",
            "precio": 1250.50,
            "categoria": "limpieza_hogar",
            "imagen_url": "https://storage.interlimpia.com/productos/A123.jpg",
            "proveedor": "Rey de la limpieza"
        },
        {
            "codigo": "B456",
            "marca": "Olimpia",
            "descripcion": "Desinfectante para pisos de cerámica",
            "precio": 980.75,
            "categoria": "limpieza_hogar",
            "imagen_url": "https://storage.interlimpia.com/productos/B456.jpg",
            "proveedor": "Olimpia"
        },
        {
            "codigo": "C789",
            "marca": "Limpiq",
            "descripcion": "Detergente industrial concentrado",
            "precio": 3450.00,
            "categoria": "limpieza_industrial",
            "imagen_url": "https://storage.interlimpia.com/productos/C789.jpg",
            "proveedor": "Limpiq"
        },
        {
            "codigo": "D012",
            "marca": "Mr. Clean",
            "descripcion": "Desengrasante para cocinas industriales",
            "precio": 2890.25,
            "categoria": "limpieza_industrial",
            "imagen_url": "https://storage.interlimpia.com/productos/D012.jpg",
            "proveedor": "Rey de la limpieza"
        },
        {
            "codigo": "E345",
            "marca": "Olimpia",
            "descripcion": "Jabón líquido para manos antibacterial",
            "precio": 750.00,
            "categoria": "limpieza_hogar",
            "imagen_url": "https://storage.interlimpia.com/productos/E345.jpg",
            "proveedor": "Olimpia"
        }
    ]
    
    for producto_data in productos:
        # Verificar si el producto ya existe
        producto_existente = db.query(Producto).filter(
            Producto.codigo == producto_data["codigo"]
        ).first()
        
        if not producto_existente:
            # Crear el producto si no existe
            nuevo_producto = Producto(
                codigo=producto_data["codigo"],
                marca=producto_data["marca"],
                descripcion=producto_data["descripcion"],
                precio=producto_data["precio"],
                categoria=producto_data["categoria"],
                imagen_url=producto_data["imagen_url"],
                proveedor=producto_data["proveedor"]
            )
            db.add(nuevo_producto)
            print(f"Producto creado: {nuevo_producto.descripcion}")
    
    db.commit()


def main():
    """
    Función principal que inicializa la base de datos.
    """
    print("Creando tablas en la base de datos...")
    Base.metadata.create_all(bind=engine)
    
    # Inicializar datos
    db = SessionLocal()
    try:
        print("Inicializando categorías...")
        init_categorias(db)
        
        print("Inicializando productos de ejemplo...")
        init_productos(db)
        
        print("Base de datos inicializada correctamente.")
    
    except Exception as e:
        print(f"Error al inicializar la base de datos: {str(e)}")
    
    finally:
        db.close()


if __name__ == "__main__":
    main()