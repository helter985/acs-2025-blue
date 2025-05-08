from pydantic import BaseModel, Field


class ErrorResponse(BaseModel):
    """
    DTO para respuestas de error.
    
    Utilizado para devolver mensajes de error consistentes
    cuando ocurren excepciones o errores en la API.
    """
    codigo: int = Field(..., description="Código de estado HTTP")
    mensaje: str = Field(..., description="Mensaje descriptivo del error")