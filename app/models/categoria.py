from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from app.database.base import Base


class Categoria(Base):
    """
    Modelo de Categoría en la base de datos.
    
    Representa una categoría de productos (limpieza_hogar, limpieza_industrial).
    """
    __tablename__ = "categorias"
    
    id = Column(String, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    descripcion = Column(String, nullable=True)
    
    # Relación con la tabla productos
    productos = relationship("Producto", back_populates="categoria_rel")