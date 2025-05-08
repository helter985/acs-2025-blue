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
    
    # Configuración de la base de datos
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL", 
        "sqlite:///./interlimpia.db"
    )
    
    # Configuración de almacenamiento de imágenes
    STORAGE_URL: str = os.getenv(
        "STORAGE_URL", 
        "https://storage.interlimpia.com"
    )
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# Instancia de configuración global
settings = Settings()