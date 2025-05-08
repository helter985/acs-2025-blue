from typing import List
from sqlalchemy.orm import Session

from app.models.categoria import Categoria


class CategoriaRepository:
    """
    Repositorio para operaciones con la tabla de categorías.
    Maneja el acceso a datos y las consultas a la base de datos.
    """
    
    def __init__(self, db: Session):
        """
        Inicializa el repositorio con una sesión de base de datos.
        
        Args:
            db: Sesión de SQLAlchemy
        """
        self.db = db
    
    def obtener_categorias(self) -> List[Categoria]:
        """
        Obtiene todas las categorías disponibles.
        
        Returns:
            Lista de todas las categorías
        """
        return self.db.query(Categoria).all()