from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import or_

from app.models.producto import Producto


class ProductoRepository:
    """
    Repositorio para operaciones con la tabla de productos.
    Maneja el acceso a datos y las consultas a la base de datos.
    """
    
    def __init__(self, db: Session):
        """
        Inicializa el repositorio con una sesión de base de datos.
        
        Args:
            db: Sesión de SQLAlchemy
        """
        self.db = db
    
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
        query = self.db.query(Producto)
        
        # Aplicar filtros si están presentes
        if marca:
            query = query.filter(Producto.marca.ilike(f"%{marca}%"))
            
        if descripcion:
            query = query.filter(Producto.descripcion.ilike(f"%{descripcion}%"))
            
        if categoria:
            query = query.filter(Producto.categoria == categoria)
            
        if nombre:
            # Nombre puede estar en la descripción o en la marca
            query = query.filter(
                or_(
                    Producto.descripcion.ilike(f"%{nombre}%"),
                    Producto.marca.ilike(f"%{nombre}%")
                )
            )
        
        return query.all()
    
    def obtener_producto_por_codigo(self, codigo: str) -> Optional[Producto]:
        """
        Obtiene un producto específico por su código.
        
        Args:
            codigo: Código interno del producto
            
        Returns:
            Producto encontrado o None si no existe
        """
        return self.db.query(Producto).filter(Producto.codigo == codigo).first()