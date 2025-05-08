from typing import List, Optional
from sqlalchemy.orm import Session

from app.models.producto import Producto
from app.repositories.producto_repository import ProductoRepository


class ProductoService:
    """
    Servicio para operaciones relacionadas con productos.
    Implementa la lógica de negocio entre controladores y repositorios.
    """
    
    def __init__(self, db: Session):
        """
        Inicializa el servicio con una sesión de base de datos.
        
        Args:
            db: Sesión de SQLAlchemy
        """
        self.repository = ProductoRepository(db)
    
    def obtener_productos(
        self,
        marca: Optional[str] = None,
        descripcion: Optional[str] = None,
        categoria: Optional[str] = None,
        nombre: Optional[str] = None
    ) -> List[Producto]:
        """
        Obtiene productos aplicando los filtros especificados.
        
        Args:
            marca: Filtro opcional por marca
            descripcion: Filtro opcional por descripción (búsqueda parcial)
            categoria: Filtro opcional por categoría
            nombre: Filtro opcional por nombre (búsqueda parcial)
            
        Returns:
            Lista de productos que coinciden con los filtros
        """
        return self.repository.obtener_productos(marca, descripcion, categoria, nombre)
    
    def obtener_producto_por_codigo(self, codigo: str) -> Optional[Producto]:
        """
        Obtiene un producto específico por su código.
        
        Args:
            codigo: Código interno del producto
            
        Returns:
            Producto encontrado o None si no existe
        """
        return self.repository.obtener_producto_por_codigo(codigo)