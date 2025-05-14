import os
import sys
from logging.config import fileConfig
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from sqlalchemy import text
from alembic import context

# Agregar directorio raíz al path para poder importar los módulos
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Importar los modelos y configuraciones
from app.models.base import Base  # Importar el modelo Base
from app.models import Producto, Categoria  # Importar los modelos
from app.config import settings  # Importar configuración

# Este es el objeto de configuración de Alembic, que proporciona
# acceso a los valores dentro del archivo .ini en uso.
config = context.config

# Sobreescribir la URL de la base de datos desde settings
db_url = settings.DATABASE_URL
print(f"Using database URL: {db_url}")
config.set_main_option("sqlalchemy.url", db_url)

# Interpretar el archivo de configuración para el logging de Python.
# Esta línea básicamente configura los loggers.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Agregar el objeto MetaData de tu modelo aquí
# para soporte de 'autogenerate'
target_metadata = Base.metadata  # Asumiendo que Base se importó desde tus modelos

# Otros valores de la configuración, definidos por las necesidades de env.py,
# pueden ser adquiridos:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.

def run_migrations_offline() -> None:
    """Ejecutar migraciones en modo 'offline'.

    Esto configura el contexto con solo una URL
    y no un Engine, aunque un Engine también es aceptable
    aquí. Al omitir la creación del Engine,
    ni siquiera necesitamos que un DBAPI esté disponible.

    Las llamadas a context.execute() aquí emiten la cadena dada a la
    salida del script.
    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Ejecutar migraciones en modo 'online'.

    En este escenario necesitamos crear un Engine
    y asociar una conexión con el contexto.
    """
    # Verificar que la URL sea válida
    if not db_url:
        raise ValueError("DATABASE_URL no está configurado correctamente")
    
    # Obtener configuración para sobrescribir opciones específicas de MySQL
    configuration = config.get_section(config.config_ini_section, {})
    
    # Establecer opciones específicas para MySQL si es necesario
    if 'mysql' in db_url:
        # Configurar innodb_strict_mode para evitar problemas con claves demasiado largas
        configuration["sqlalchemy.url"] = f"{db_url}?charset=utf8mb4"
    
    # Configurar el engine y conectar
    connectable = engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        # Probar la conexión
        try:
            # Adaptar consulta de prueba para MySQL
            if 'mysql' in db_url:
                connection.execute(text("SELECT 1"))
            else:
                connection.execute(text("SELECT 1"))
            print("Conexión a la base de datos exitosa")
        except Exception as e:
            print(f"Error al conectar a la base de datos: {str(e)}")
            raise
        
        # Configurar el contexto de migración con opciones específicas para MySQL
        context_opts = {
            "connection": connection,
            "target_metadata": target_metadata
        }
        
        # Agregar opciónes específicas para MySQL si es necesario
        if 'mysql' in db_url:
            context_opts["render_as_batch"] = True
            # Especificar comparación por defecto para cadenas
            context_opts["compare_type"] = True
        
        context.configure(**context_opts)

        with context.begin_transaction():
            context.run_migrations()


# Determinar si estamos en modo offline o online
if context.is_offline_mode():
    print("Ejecutando migraciones en modo offline")
    run_migrations_offline()
else:
    print("Ejecutando migraciones en modo online")
    run_migrations_online()