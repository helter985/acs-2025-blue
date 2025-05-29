# tests/category_test.py

import unittest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient

from app.main import app  # Asegúrate de que este path sea correcto

class CategoriaTestCase(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    @patch("app.controllers.categoria_controller.get_db")
    @patch("app.controllers.categoria_controller.CategoriaService")
    def test_obtener_categorias(self, mock_categoria_service, mock_get_db):
        # Mocks necesarios
        mock_session = MagicMock()
        mock_get_db.return_value = mock_session

        # Simular objetos ORM como los que SQLAlchemy devolvería
        mock_categoria1 = MagicMock()
        mock_categoria1.id = 1
        mock_categoria1.nombre = "Tech"
        mock_categoria1.descripcion = None

        mock_categoria2 = MagicMock()
        mock_categoria2.id = 2
        mock_categoria2.nombre = "Hogar"
        mock_categoria2.descripcion = None

        mock_service_instance = MagicMock()
        mock_service_instance.obtener_categorias.return_value = [mock_categoria1, mock_categoria2]
        mock_categoria_service.return_value = mock_service_instance

        # FIXED: Use the correct URL that matches your router configuration
        # Your router has prefix="/categorias" and is included with prefix="/api/v1"
        response = self.client.get("/v1/api/categorias")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [
            {"id": 1, "nombre": "Tech", "descripcion": None},
            {"id": 2, "nombre": "Hogar", "descripcion": None}
        ])

    def test_obtener_categorias_error_handling(self):
        """Test error handling when service raises an exception"""
        with patch("app.controllers.categoria_controller.get_db") as mock_get_db, \
             patch("app.controllers.categoria_controller.CategoriaService") as mock_categoria_service:
            
            mock_session = MagicMock()
            mock_get_db.return_value = mock_session
            
            # Make the service raise an exception
            mock_service_instance = MagicMock()
            mock_service_instance.obtener_categorias.side_effect = Exception("Database error")
            mock_categoria_service.return_value = mock_service_instance
            
            response = self.client.get("/v1/api/categorias")
            
            self.assertEqual(response.status_code, 500)
            response_json = response.json()
            
            # The error response is wrapped in 'detail' due to HTTPException structure
            self.assertIn("detail", response_json)
            detail = response_json["detail"]
            self.assertIn("codigo", detail)
            self.assertIn("mensaje", detail)
            self.assertEqual(detail["codigo"], 500)
            self.assertIn("Database error", detail["mensaje"])

    def test_debug_available_routes(self):
        """Helper test to debug available routes"""
        print("\n=== Available Routes ===")
        for route in app.routes:
            if hasattr(route, 'path'):
                methods = getattr(route, 'methods', set())
                print(f"Path: {route.path}, Methods: {methods}")
        print("========================\n")

if __name__ == '__main__':
    unittest.main()