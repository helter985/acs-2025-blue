import os
from typing import Optional
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

# Cargar variables de entorno desde archivo .env si existe
load_dotenv()


class Settings(BaseSettings):
    """
    Configuración global de la aplicación utilizando Pydantic.
    Permite cargar configuraciones desde variables de entorno.
    """
    APP_NAME: str = "Interlimpia API"
    API_PREFIX: str = "/api/v1"
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"
    
    # Configuración de MySQL
    MYSQL_USER: Optional[str] = None
    MYSQL_PASSWORD: Optional[str] = None
    MYSQL_DATABASE: Optional[str] = None
    MYSQL_PORT: Optional[str] = None
    MYSQL_HOST: str = os.getenv("MYSQL_HOST", "localhost")
    MYSQL_ROOT_PASSWORD: Optional[str] = None
    
    # Configuración de la base de datos
    DATABASE_URL: Optional[str] = None
    
    # Configuración de almacenamiento de imágenes
    STORAGE_URL: str = os.getenv(
        "STORAGE_URL", 
        "https://storage.interlimpia.com"
    )
    
    def __init__(self, **data):
        super().__init__(**data)
        self.DATABASE_URL = self._get_database_url()
    
    def _get_database_url(self) -> str:
        """
        Obtiene la URL de conexión a la base de datos.
        Si DATABASE_URL está definido, lo usa; de lo contrario, construye la URL 
        a partir de los parámetros de MySQL.
        """
        # Verificar si DATABASE_URL ya está definido en variables de entorno
        db_url = os.getenv("DATABASE_URL")
        if db_url:
            return db_url
        
        # Construir URL de conexión a MySQL
        if all([self.MYSQL_USER, self.MYSQL_PASSWORD, self.MYSQL_DATABASE]):
            return f"mysql+pymysql://{self.MYSQL_USER}:{self.MYSQL_PASSWORD}@{self.MYSQL_HOST}:{self.MYSQL_PORT}/{self.MYSQL_DATABASE}"
        
        # URL por defecto para desarrollo
        return "sqlite:///./interlimpia.db"
    
    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "allow"  # Permitir campos adicionales


# Instancia de configuración global
settings = Settings()