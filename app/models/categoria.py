from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from app.models.base import Base


class Categoria(Base):
    """
    Modelo de Categoría en la base de datos.
    
    Representa una categoría de productos (limpieza_hogar, limpieza_industrial).
    """
    __tablename__ = "categorias"
    
    id = Column(String(36), primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    descripcion = Column(String(255), nullable=True)
    
    # Relación con la tabla productos
    productos = relationship("Producto", back_populates="categoria_rel")