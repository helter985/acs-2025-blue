from sqlalchemy import Column, String, Float, ForeignKey
from sqlalchemy.orm import relationship

from app.models.base import Base


class Producto(Base):
    """
    Modelo de Producto en la base de datos.
    
    Representa un producto en el catálogo de Interlimpia.
    """
    __tablename__ = "productos"
    
    codigo = Column(String(50), primary_key=True, index=True)
    marca = Column(String(100), nullable=False, index=True)
    descripcion = Column(String(255), nullable=False, index=True)
    precio = Column(Float, nullable=False)
    categoria = Column(String(36), ForeignKey("categorias.id"), nullable=False)
    imagen_url = Column(String(255), nullable=True)
    proveedor = Column(String(100), nullable=False)
    
    # Relación con la tabla categorías
    categoria_rel = relationship("Categoria", back_populates="productos")