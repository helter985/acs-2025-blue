import unittest
from unittest.mock import patch, MagicMock
from fastapi import status
from httpx import AsyncClient
from app.main import app

class TestProductoEndpoints(unittest.IsolatedAsyncioTestCase):

    async def asyncSetUp(self):
        # Setup previo si es necesario (ej. preparar DB de test)
        pass

    async def asyncTearDown(self):
        # Limpieza si es necesaria
        pass

    async def test_get_productos_ok(self):
        # Mock del servicio para devolver lista de productos simulada
        productos_mock = [
            {
                "codigo": "P001",
                "marca": "MarcaA",
                "descripcion": "Producto de limpieza A",
                "precio": 10.5,
                "categoria": "limpieza_hogar",
                "imagen_url": None,
                "proveedor": "Proveedor1"
            }
        ]

        # Use regular MagicMock instead of AsyncMock since service methods are synchronous
        with patch("app.controllers.producto_controller.get_db") as mock_db, \
             patch("app.controllers.producto_controller.ProductoService") as mock_service_class:
            
            mock_db.return_value = MagicMock()
            mock_service_instance = MagicMock()
            mock_service_instance.obtener_productos.return_value = productos_mock
            mock_service_class.return_value = mock_service_instance

            async with AsyncClient(app=app, base_url="http://test") as ac:
                response = await ac.get("/api/v1/productos")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["codigo"], "P001")

    async def test_get_productos_no_content(self):
        # Mock que devuelve lista vacía
        with patch("app.controllers.producto_controller.get_db") as mock_db, \
             patch("app.controllers.producto_controller.ProductoService") as mock_service_class:
            
            mock_db.return_value = MagicMock()
            mock_service_instance = MagicMock()
            mock_service_instance.obtener_productos.return_value = []
            mock_service_class.return_value = mock_service_instance

            async with AsyncClient(app=app, base_url="http://test") as ac:
                response = await ac.get("/api/v1/productos")

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    async def test_get_productos_with_filters(self):
        # Test with query parameters
        productos_mock = [
            {
                "codigo": "P001",
                "marca": "MarcaA",
                "descripcion": "Producto de limpieza A",
                "precio": 10.5,
                "categoria": "limpieza_hogar",
                "imagen_url": None,
                "proveedor": "Proveedor1"
            }
        ]

        with patch("app.controllers.producto_controller.get_db") as mock_db, \
             patch("app.controllers.producto_controller.ProductoService") as mock_service_class:
            
            mock_db.return_value = MagicMock()
            mock_service_instance = MagicMock()
            mock_service_instance.obtener_productos.return_value = productos_mock
            mock_service_class.return_value = mock_service_instance

            async with AsyncClient(app=app, base_url="http://test") as ac:
                response = await ac.get("/api/v1/productos?marca=MarcaA&categoria=limpieza_hogar")

            # Verify that the service was called with the correct parameters
            # The service is called with positional arguments, not keyword arguments
            mock_service_instance.obtener_productos.assert_called_once_with(
                "MarcaA", None, "limpieza_hogar", None
            )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["codigo"], "P001")

    async def test_get_producto_por_codigo_ok(self):
        producto_mock = {
            "codigo": "P001",
            "marca": "MarcaA",
            "descripcion": "Producto de limpieza A",
            "precio": 10.5,
            "categoria": "limpieza_hogar",
            "imagen_url": None,
            "proveedor": "Proveedor1"
        }

        with patch("app.controllers.producto_controller.get_db") as mock_db, \
             patch("app.controllers.producto_controller.ProductoService") as mock_service_class:
            
            mock_db.return_value = MagicMock()
            mock_service_instance = MagicMock()
            mock_service_instance.obtener_producto_por_codigo.return_value = producto_mock
            mock_service_class.return_value = mock_service_instance

            async with AsyncClient(app=app, base_url="http://test") as ac:
                response = await ac.get("/api/v1/productos/P001")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(data["codigo"], "P001")

    async def test_get_producto_por_codigo_not_found(self):
        with patch("app.controllers.producto_controller.get_db") as mock_db, \
             patch("app.controllers.producto_controller.ProductoService") as mock_service_class:
            
            mock_db.return_value = MagicMock()
            mock_service_instance = MagicMock()
            mock_service_instance.obtener_producto_por_codigo.return_value = None
            mock_service_class.return_value = mock_service_instance

            async with AsyncClient(app=app, base_url="http://test") as ac:
                response = await ac.get("/api/v1/productos/NO_EXISTE")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        data = response.json()
        self.assertIn("detail", data)
        self.assertIn("codigo", data["detail"])
        self.assertEqual(data["detail"]["codigo"], 404)

    async def test_get_productos_error_handling(self):
        with patch("app.controllers.producto_controller.get_db") as mock_db, \
             patch("app.controllers.producto_controller.ProductoService") as mock_service_class:
            
            mock_db.return_value = MagicMock()
            mock_service_instance = MagicMock()
            mock_service_instance.obtener_productos.side_effect = Exception("Error de prueba")
            mock_service_class.return_value = mock_service_instance

            async with AsyncClient(app=app, base_url="http://test") as ac:
                response = await ac.get("/api/v1/productos")

        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        data = response.json()
        self.assertIn("detail", data)
        self.assertIn("codigo", data["detail"])
        self.assertEqual(data["detail"]["codigo"], 500)
        self.assertIn("Error de prueba", data["detail"]["mensaje"])

    async def test_get_producto_por_codigo_error_handling(self):
        with patch("app.controllers.producto_controller.get_db") as mock_db, \
             patch("app.controllers.producto_controller.ProductoService") as mock_service_class:
            
            mock_db.return_value = MagicMock()
            mock_service_instance = MagicMock()
            mock_service_instance.obtener_producto_por_codigo.side_effect = Exception("Database error")
            mock_service_class.return_value = mock_service_instance

            async with AsyncClient(app=app, base_url="http://test") as ac:
                response = await ac.get("/api/v1/productos/P001")

        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        data = response.json()
        self.assertIn("detail", data)
        self.assertIn("codigo", data["detail"])
        self.assertEqual(data["detail"]["codigo"], 500)
        self.assertIn("Database error", data["detail"]["mensaje"])


if __name__ == "__main__":
    unittest.main()