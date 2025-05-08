from typing import List
from sqlalchemy.orm import Session

from app.models.categoria import Categoria
from app.repositories.categoria_repository import CategoriaRepository


class CategoriaService:
    """
    Servicio para operaciones relacionadas con categorías.
    Implementa la lógica de negocio entre controladores y repositorios.
    """
    
    def __init__(self, db: Session):
        """
        Inicializa el servicio con una sesión de base de datos.
        
        Args:
            db: Sesión de SQLAlchemy
        """
        self.repository = CategoriaRepository(db)
    
    def obtener_categorias(self) -> List[Categoria]:
        """
        Obtiene todas las categorías disponibles.
        
        Returns:
            Lista de todas las categorías
        """
        return self.repository.obtener_categorias()