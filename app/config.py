import os
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
    API_PREFIX: str = "/api"
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"
    
    # Configuración de PostgreSQL
    POSTGRES_USER: str | None = None
    POSTGRES_PASSWORD: str | None = None
    POSTGRES_DB: str | None = None
    POSTGRES_PORT: str | None = None
    POSTGRES_HOST: str = os.getenv("POSTGRES_HOST", "interlimpia_db")
    
    # Configuración de la base de datos
    # Si DATABASE_URL está definido, lo usa; de lo contrario, construye la URL a partir de los parámetros de PostgreSQL
    @property
    def DATABASE_URL(self) -> str:
        db_url = os.getenv("DATABASE_URL")
        if db_url:
            return db_url
        
        # Construir URL de conexión a PostgreSQL
        if all([self.POSTGRES_USER, self.POSTGRES_PASSWORD, self.POSTGRES_DB]):
            return f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        
        # URL por defecto para desarrollo
        return "sqlite:///./interlimpia.db"
    
    # Configuración de almacenamiento de imágenes
    STORAGE_URL: str = os.getenv(
        "STORAGE_URL", 
        "https://storage.interlimpia.com"
    )
    
    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "allow"  # Permitir campos adicionales


# Instancia de configuración global
settings = Settings()