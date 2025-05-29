# tests/test_producto_service.py

import unittest
from unittest.mock import MagicMock, patch
from sqlalchemy.orm import Session

from app.services.producto_service import ProductoService
from app.models.producto import Producto


class TestProductoService(unittest.TestCase):
    
    def setUp(self):
        """Setup for each test"""
        self.mock_db = MagicMock(spec=Session)
        
        # Create service and mock its repository
        self.service = ProductoService(self.mock_db)
        self.service.repository = MagicMock()
    
    @patch('app.services.producto_service.ProductoRepository')
    def test_init_creates_repository(self, mock_repository_class):
        """Test that service properly initializes with repository"""
        service = ProductoService(self.mock_db)
        
        # Verify repository was created with db session
        mock_repository_class.assert_called_once_with(self.mock_db)
        self.assertEqual(service.repository, mock_repository_class.return_value)
    
    def test_obtener_productos_no_filters(self):
        """Test getting all products without filters"""
        # Create mock products
        mock_producto1 = self._create_mock_producto("P001", "Marca A", "Producto 1")
        mock_producto2 = self._create_mock_producto("P002", "Marca B", "Producto 2")
        expected_productos = [mock_producto1, mock_producto2]
        
        # Mock repository method
        self.service.repository.obtener_productos.return_value = expected_productos
        
        # Call service method
        result = self.service.obtener_productos()
        
        # Assertions
        self.service.repository.obtener_productos.assert_called_once_with(None, None, None, None)
        self.assertEqual(result, expected_productos)
        self.assertEqual(len(result), 2)
    
    def test_obtener_productos_with_marca_filter(self):
        """Test getting products filtered by marca"""
        # Create mock product
        mock_producto = self._create_mock_producto("P001", "Marca A", "Producto 1")
        expected_productos = [mock_producto]
        
        # Mock repository method
        self.service.repository.obtener_productos.return_value = expected_productos
        
        # Call service method with marca filter
        result = self.service.obtener_productos(marca="Marca A")
        
        # Assertions
        self.service.repository.obtener_productos.assert_called_once_with("Marca A", None, None, None)
        self.assertEqual(result, expected_productos)
        self.assertEqual(result[0].marca, "Marca A")
    
    def test_obtener_productos_with_multiple_filters(self):
        """Test getting products with multiple filters"""
        # Create mock product
        mock_producto = self._create_mock_producto("P001", "Marca A", "Detergente")
        expected_productos = [mock_producto]
        
        # Mock repository method
        self.service.repository.obtener_productos.return_value = expected_productos
        
        # Call service method with multiple filters
        result = self.service.obtener_productos(
            marca="Marca A", 
            descripcion="Detergente", 
            categoria="limpieza_hogar",
            nombre="Producto"
        )
        
        # Assertions
        self.service.repository.obtener_productos.assert_called_once_with(
            "Marca A", "Detergente", "limpieza_hogar", "Producto"
        )
        self.assertEqual(result, expected_productos)
    
    def test_obtener_productos_empty_result(self):
        """Test when no products match the filters"""
        # Mock repository to return empty list
        self.service.repository.obtener_productos.return_value = []
        
        # Call service method
        result = self.service.obtener_productos(marca="NonExistent")
        
        # Assertions
        self.service.repository.obtener_productos.assert_called_once_with("NonExistent", None, None, None)
        self.assertEqual(result, [])
        self.assertIsInstance(result, list)
    
    def test_obtener_productos_repository_exception(self):
        """Test when repository raises an exception during product search"""
        # Mock repository to raise exception
        self.service.repository.obtener_productos.side_effect = Exception("Database connection error")
        
        # Call service method and expect exception to be propagated
        with self.assertRaises(Exception) as context:
            self.service.obtener_productos()
        
        self.assertEqual(str(context.exception), "Database connection error")
        self.service.repository.obtener_productos.assert_called_once_with(None, None, None, None)
    
    def test_obtener_producto_por_codigo_found(self):
        """Test getting a product by code when it exists"""
        # Create mock product
        mock_producto = self._create_mock_producto("P001", "Marca A", "Producto 1")
        
        # Mock repository method
        self.service.repository.obtener_producto_por_codigo.return_value = mock_producto
        
        # Call service method
        result = self.service.obtener_producto_por_codigo("P001")
        
        # Assertions
        self.service.repository.obtener_producto_por_codigo.assert_called_once_with("P001")
        self.assertEqual(result, mock_producto)
        self.assertEqual(result.codigo, "P001")
    
    def test_obtener_producto_por_codigo_not_found(self):
        """Test getting a product by code when it doesn't exist"""
        # Mock repository to return None
        self.service.repository.obtener_producto_por_codigo.return_value = None
        
        # Call service method
        result = self.service.obtener_producto_por_codigo("NONEXISTENT")
        
        # Assertions
        self.service.repository.obtener_producto_por_codigo.assert_called_once_with("NONEXISTENT")
        self.assertIsNone(result)
    
    def test_obtener_producto_por_codigo_repository_exception(self):
        """Test when repository raises an exception during product lookup"""
        # Mock repository to raise exception
        self.service.repository.obtener_producto_por_codigo.side_effect = Exception("Database error")
        
        # Call service method and expect exception to be propagated
        with self.assertRaises(Exception) as context:
            self.service.obtener_producto_por_codigo("P001")
        
        self.assertEqual(str(context.exception), "Database error")
        self.service.repository.obtener_producto_por_codigo.assert_called_once_with("P001")
    
    def test_obtener_producto_por_codigo_empty_string(self):
        """Test getting a product with empty string code"""
        # Mock repository method
        self.service.repository.obtener_producto_por_codigo.return_value = None
        
        # Call service method with empty string
        result = self.service.obtener_producto_por_codigo("")
        
        # Assertions
        self.service.repository.obtener_producto_por_codigo.assert_called_once_with("")
        self.assertIsNone(result)
    
    def _create_mock_producto(self, codigo: str, marca: str, descripcion: str) -> MagicMock:
        """Helper method to create mock producto objects"""
        mock_producto = MagicMock(spec=Producto)
        mock_producto.codigo = codigo
        mock_producto.marca = marca
        mock_producto.descripcion = descripcion
        mock_producto.precio = 10.50
        mock_producto.categoria = "limpieza_hogar"
        mock_producto.imagen_url = None
        mock_producto.proveedor = "Proveedor Test"
        return mock_producto


if __name__ == '__main__':
    unittest.main()