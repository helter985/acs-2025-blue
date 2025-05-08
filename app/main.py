from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import logging
import time

from app.config import settings
from app.controllers.producto_controller import router as producto_router
from app.controllers.categoria_controller import router as categoria_router
from app.dtos.error import ErrorResponse
from app.database.base import Base, engine, SessionLocal

# Configurar logging
logging.basicConfig(
    level=logging.INFO if settings.DEBUG else logging.WARNING,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger("app")

# Inicializar la aplicación FastAPI
app = FastAPI(
    title=settings.APP_NAME,
    description="API para consulta de productos de Interlimpia",
    version="1.0.0"
)

# Configurar CORS para permitir solicitudes desde la aplicación móvil
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especificar los orígenes permitidos
    allow_credentials=True,
    allow_methods=["GET"],  # Solo permitir métodos GET (solo lectura)
    allow_headers=["*"],
)

# Registrar los routers
app.include_router(producto_router, prefix=settings.API_PREFIX)
app.include_router(categoria_router, prefix=settings.API_PREFIX)


# Manejador de excepciones global
@app.exception_handler(Exception)
async def exception_handler(request: Request, exc: Exception):
    """
    Manejador global de excepciones para convertir errores no controlados
    en respuestas JSON con el formato estándar de error.
    """
    logger.error(f"Error no controlado: {str(exc)}", exc_info=exc)
    error_response = ErrorResponse(
        codigo=500,
        mensaje=f"Error interno del servidor: {str(exc)}"
    )
    return JSONResponse(
        status_code=500,
        content=error_response.model_dump()  # model_dump() en lugar de dict() para Pydantic v2
    )


# Ruta de información/salud de la API
@app.get("/", tags=["Info"])
async def root():
    """
    Endpoint de información básica sobre la API.
    """
    return {
        "nombre": settings.APP_NAME,
        "version": "1.0.0",
        "estado": "Operativa",
        "database_url_type": settings.DATABASE_URL.split("://")[0]
    }


# Verificación de conexión a la base de datos
@app.get("/health", tags=["Info"])
async def health_check():
    """
    Endpoint para verificar la salud de la aplicación, 
    incluyendo la conexión a la base de datos.
    """
    start_time = time.time()
    try:
        # Intentar conectar a la base de datos
        db = SessionLocal()
        result = db.execute("SELECT 1").fetchone()
        db.close()
        
        db_connected = result is not None
        response_time = time.time() - start_time
        
        return {
            "status": "healthy" if db_connected else "unhealthy",
            "database_connected": db_connected,
            "response_time_ms": round(response_time * 1000, 2)
        }
    except Exception as e:
        logger.error(f"Error en health check: {str(e)}", exc_info=e)
        return {
            "status": "unhealthy",
            "database_connected": False,
            "error": str(e),
            "response_time_ms": round((time.time() - start_time) * 1000, 2)
        }


# Evento de inicio de la aplicación
@app.on_event("startup")
async def startup_event():
    """
    Evento que se ejecuta al iniciar la aplicación.
    """
    logger.info(f"Iniciando {settings.APP_NAME}")
    logger.info(f"Conectando a la base de datos: {settings.DATABASE_URL.split('@')[-1] if '@' in settings.DATABASE_URL else settings.DATABASE_URL}")
    
    # No creamos tablas aquí para evitar conflictos con Alembic
    # Base.metadata.create_all(bind=engine)


# Evento de cierre de la aplicación
@app.on_event("shutdown")
async def shutdown_event():
    """
    Evento que se ejecuta al cerrar la aplicación.
    """
    logger.info(f"Cerrando {settings.APP_NAME}")


# Iniciar con uvicorn
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=settings.DEBUG)