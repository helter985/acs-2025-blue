from sqlalchemy import Column, String, Float, ForeignKey
from sqlalchemy.orm import relationship

from app.models.base import Base


class Producto(Base):
    """
    Modelo de Producto en la base de datos.
    
    Representa un producto en el catálogo de Interlimpia.
    """
    __tablename__ = "productos"
    
    codigo = Column(String, primary_key=True, index=True)
    marca = Column(String, nullable=False, index=True)
    descripcion = Column(String, nullable=False, index=True)
    precio = Column(Float, nullable=False)
    categoria = Column(String, ForeignKey("categorias.id"), nullable=False)
    imagen_url = Column(String, nullable=True)
    proveedor = Column(String, nullable=False)
    
    # Relación con la tabla categorías
    categoria_rel = relationship("Categoria", back_populates="productos")