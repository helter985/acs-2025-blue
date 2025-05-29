# app/dtos/categoria.py

from typing import Optional
from pydantic import BaseModel, Field


class CategoriaBase(BaseModel):
    """
    DTO base para datos de categoría.
    """
    id: int = Field(..., description="Identificador único de la categoría")
    nombre: str = Field(..., description="Nombre de la categoría")
    descripcion: Optional[str] = Field(None, description="Descripción de la categoría")


class CategoriaResponse(CategoriaBase):
    """
    DTO para respuestas de categoría.
    """
    class Config:
        orm_mode = True
