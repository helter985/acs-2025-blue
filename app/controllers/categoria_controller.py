from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.base import get_db
from app.dtos.categoria import CategoriaResponse
from app.dtos.error import ErrorResponse
from app.services.categoria_service import CategoriaService

# Creación del router para los endpoints de categoría
router = APIRouter(prefix="/categorias", tags=["Categorías"])


@router.get(
    "",
    response_model=List[CategoriaResponse],
    responses={
        200: {"description": "Lista de categorías"},
        500: {"model": ErrorResponse, "description": "Error interno del servidor"}
    }
)
async def obtener_categorias(
    db: Session = Depends(get_db)
):
    """
    Obtiene la lista completa de categorías disponibles.
    """
    try:
        service = CategoriaService(db)
        categorias = service.obtener_categorias()
        return categorias
    except Exception as e:
        # En caso de error inesperado, devolver 500 Internal Server Error
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"codigo": 500, "mensaje": f"Error interno del servidor: {str(e)}"}
        )