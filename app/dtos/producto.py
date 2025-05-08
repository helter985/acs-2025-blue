from typing import Optional
from pydantic import BaseModel, Field


class ProductoBase(BaseModel):
    """
    DTO base para datos de producto.
    """
    codigo: str = Field(..., description="Código interno único del producto")
    marca: str = Field(..., description="Marca del producto")
    descripcion: str = Field(..., description="Descripción detallada del producto")
    precio: float = Field(..., gt=0, description="Precio de venta actual del producto")
    categoria: str = Field(..., description="Categoría a la que pertenece (limpieza_hogar, limpieza_industrial)")
    imagen_url: Optional[str] = Field(None, description="URL de la imagen del producto")
    proveedor: str = Field(..., description="Proveedor del producto")


class ProductoResponse(ProductoBase):
    """
    DTO para respuestas de producto.
    """
    class Config:
        orm_mode = True


class ProductoQuery(BaseModel):
    """
    DTO para filtros en consultas de productos.
    """
    marca: Optional[str] = Field(None, description="Filtrar por marca")
    descripcion: Optional[str] = Field(None, description="Filtrar por descripción (parcial)")
    categoria: Optional[str] = Field(None, description="Filtrar por categoría")
    nombre: Optional[str] = Field(None, description="Filtrar por nombre (parcial)")