from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.controllers.producto_controller import router as producto_router
from app.controllers.categoria_controller import router as categoria_router
from app.dtos.error import ErrorResponse
from app.database.base import Base, engine

# Crear tablas en la base de datos
Base.metadata.create_all(bind=engine)

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
    error_response = ErrorResponse(
        codigo=500,
        mensaje=f"Error interno del servidor: {str(exc)}"
    )
    return JSONResponse(
        status_code=500,
        content=error_response.dict()
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
        "estado": "Operativa"
    }


# Iniciar con uvicorn
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=settings.DEBUG)