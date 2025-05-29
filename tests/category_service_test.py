import unittest
from unittest.mock import MagicMock, patch
from sqlalchemy.orm import Session

from app.services.categoria_service import CategoriaService
from app.models.categoria import Categoria


class TestCategoriaService(unittest.TestCase):
    
    @patch('app.services.categoria_service.CategoriaRepository')
    def setUp(self, mock_repository_class):
        """Setup for each test"""
        self.mock_db = MagicMock(spec=Session)
        
        # Create mock repository instance
        self.mock_repository = MagicMock()
        mock_repository_class.return_value = self.mock_repository
        
        # Create service with mocked repository
        self.service = CategoriaService(self.mock_db)
        
        # Store reference to mock class for assertions
        self.mock_repository_class = mock_repository_class
    
    def test_init_creates_repository(self):
        """Test that service properly initializes with repository"""
        # Verify repository was created with db session
        self.mock_repository_class.assert_called_with(self.mock_db)
        self.assertEqual(self.service.repository, self.mock_repository)
    
    def test_obtener_categorias_success(self):
        """Test successful retrieval of categories"""
        # Create mock categories
        mock_categoria1 = MagicMock(spec=Categoria)
        mock_categoria1.id = 1
        mock_categoria1.nombre = "Limpieza Hogar"
        mock_categoria1.descripcion = "Productos para limpieza del hogar"
        
        mock_categoria2 = MagicMock(spec=Categoria)
        mock_categoria2.id = 2
        mock_categoria2.nombre = "Limpieza Industrial"
        mock_categoria2.descripcion = "Productos para limpieza industrial"
        
        expected_categorias = [mock_categoria1, mock_categoria2]
        
        # Mock repository method
        self.mock_repository.obtener_categorias.return_value = expected_categorias
        
        # Call service method
        result = self.service.obtener_categorias()
        
        # Assertions
        self.mock_repository.obtener_categorias.assert_called_once()
        self.assertEqual(result, expected_categorias)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0].nombre, "Limpieza Hogar")
        self.assertEqual(result[1].nombre, "Limpieza Industrial")
    
    def test_obtener_categorias_empty_list(self):
        """Test when no categories are found"""
        # Mock repository to return empty list
        self.mock_repository.obtener_categorias.return_value = []
        
        # Call service method
        result = self.service.obtener_categorias()
        
        # Assertions
        self.mock_repository.obtener_categorias.assert_called_once()
        self.assertEqual(result, [])
        self.assertIsInstance(result, list)
    
    def test_obtener_categorias_repository_exception(self):
        """Test when repository raises an exception"""
        # Mock repository to raise exception
        self.mock_repository.obtener_categorias.side_effect = Exception("Database error")
        
        # Call service method and expect exception to be propagated
        with self.assertRaises(Exception) as context:
            self.service.obtener_categorias()
        
        self.assertEqual(str(context.exception), "Database error")
        self.mock_repository.obtener_categorias.assert_called_once()


if __name__ == '__main__':
    unittest.main()