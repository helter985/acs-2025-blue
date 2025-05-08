from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from sqlalchemy.orm import Session

from app.database.base import get_db
from app.dtos.producto import ProductoResponse
from app.dtos.error import ErrorResponse
from app.services.producto_service import ProductoService

# Creación del router para los endpoints de producto
router = APIRouter(prefix="/productos", tags=["Productos"])


@router.get(
    "",
    response_model=List[ProductoResponse],
    responses={
        200: {"description": "Lista de productos encontrados"},
        204: {"description": "No hay productos que coincidan con los filtros"},
        400: {"model": ErrorResponse, "description": "Error en la solicitud"},
        500: {"model": ErrorResponse, "description": "Error interno del servidor"}
    }
)
async def obtener_productos(
    marca: Optional[str] = Query(None, description="Filtrar por marca"),
    descripcion: Optional[str] = Query(None, description="Filtrar por descripción (parcial)"),
    categoria: Optional[str] = Query(None, description="Filtrar por categoría (limpieza_hogar, limpieza_industrial)"),
    nombre: Optional[str] = Query(None, description="Filtrar por nombre (parcial)"),
    db: Session = Depends(get_db)
):
    """
    Obtiene una lista de productos que coinciden con los filtros especificados.
    Si no se proporciona ningún filtro, devuelve todos los productos.
    Si no hay coincidencias, devuelve un código 204 (No Content).
    """
    try:
        service = ProductoService(db)
        productos = service.obtener_productos(marca, descripcion, categoria, nombre)
        
        # Si no hay productos encontrados, devolver 204 No Content
        if not productos:
            return Response(status_code=status.HTTP_204_NO_CONTENT)
        
        return productos
    except Exception as e:
        # En caso de error inesperado, devolver 500 Internal Server Error
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"codigo": 500, "mensaje": f"Error interno del servidor: {str(e)}"}
        )


@router.get(
    "/{codigo}",
    response_model=ProductoResponse,
    responses={
        200: {"description": "Producto encontrado"},
        404: {"model": ErrorResponse, "description": "Producto no encontrado"},
        500: {"model": ErrorResponse, "description": "Error interno del servidor"}
    }
)
async def obtener_producto_por_codigo(
    codigo: str,
    db: Session = Depends(get_db)
):
    """
    Obtiene un producto específico por su código interno.
    Si el producto no existe, devuelve un código 404 (Not Found).
    """
    try:
        service = ProductoService(db)
        producto = service.obtener_producto_por_codigo(codigo)
        
        if not producto:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={"codigo": 404, "mensaje": "Producto no encontrado"}
            )
        
        return producto
    except HTTPException:
        # Re-lanzar las HTTPException que ya han sido creadas
        raise
    except Exception as e:
        # En caso de error inesperado, devolver 500 Internal Server Error
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"codigo": 500, "mensaje": f"Error interno del servidor: {str(e)}"}
        )