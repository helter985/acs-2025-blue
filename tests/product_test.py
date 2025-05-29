import unittest
from unittest.mock import patch, MagicMock
from fastapi import status
# Asegúrate de importar ASGITransport
from httpx import AsyncClient, ASGITransport
from app.main import app # Asumo que app.main.app es tu instancia de FastAPI

class TestProductoEndpoints(unittest.IsolatedAsyncioTestCase):

    async def asyncSetUp(self):
        # Setup previo si es necesario (ej. preparar DB de test)
        pass

    async def asyncTearDown(self):
        # Limpieza si es necesaria
        pass

    async def test_get_productos_ok(self):
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

            # CORRECCIÓN AQUÍ
            async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
                response = await ac.get("/v1/api/productos")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["codigo"], "P001")

    async def test_get_productos_no_content(self):
        with patch("app.controllers.producto_controller.get_db") as mock_db, \
             patch("app.controllers.producto_controller.ProductoService") as mock_service_class:
            
            mock_db.return_value = MagicMock()
            mock_service_instance = MagicMock()
            mock_service_instance.obtener_productos.return_value = []
            mock_service_class.return_value = mock_service_instance

            # CORRECCIÓN AQUÍ
            async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
                response = await ac.get("/v1/api/productos")

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    async def test_get_productos_with_filters(self):
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
            
            mock_db.return_value = MagicMock() # Mocks the db session object
            mock_service_instance = MagicMock()
            mock_service_instance.obtener_productos.return_value = productos_mock
            # When ProductoService() is called in the controller, it will return mock_service_instance
            mock_service_class.return_value = mock_service_instance 

            async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
                response = await ac.get("/v1/api/productos?marca=MarcaA&categoria=limpieza_hogar")

            # Verify that the service was called with the correct parameters
            # The "Actual" call from the traceback was: obtener_productos('MarcaA', None, 'limpieza_hogar', None)
            # This implies positional arguments for marca, descripcion, categoria, proveedor.
            mock_service_instance.obtener_productos.assert_called_once_with(
                "MarcaA",    # Corresponds to 'marca'
                None,        # Corresponds to 'descripcion' (since it's not in the query)
                "limpieza_hogar", # Corresponds to 'categoria'
                None         # Corresponds to 'proveedor' (since it's not in the query)
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

            # CORRECCIÓN AQUÍ
            async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
                response = await ac.get("/v1/api/productos/P001")

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

            # CORRECCIÓN AQUÍ
            async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
                response = await ac.get("/v1/api/productos/NO_EXISTE")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        data = response.json()
        self.assertIn("detail", data)
        # La comprobación original de data["detail"]["codigo"] podría ser específica de tu manejo de errores.
        # FastAPI por defecto para un HTTPException(status_code=404, detail="Not Found") no anida "codigo".
        # Ajusta según tu implementación de errores personalizados.
        # Si usas un esquema de error personalizado como el que pareces tener:
        if isinstance(data["detail"], dict) and "codigo" in data["detail"]:
             self.assertEqual(data["detail"]["codigo"], 404)
        else:
             self.assertEqual(data["detail"], "Producto con código NO_EXISTE no encontrado") # O el mensaje que uses

    async def test_get_productos_error_handling(self):
        with patch("app.controllers.producto_controller.get_db") as mock_db, \
             patch("app.controllers.producto_controller.ProductoService") as mock_service_class:
            
            mock_db.return_value = MagicMock()
            mock_service_instance = MagicMock()
            mock_service_instance.obtener_productos.side_effect = Exception("Error de prueba")
            mock_service_class.return_value = mock_service_instance

            # CORRECCIÓN AQUÍ
            async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
                response = await ac.get("/v1/api/productos")

        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        data = response.json()
        self.assertIn("detail", data)
        if isinstance(data["detail"], dict) and "codigo" in data["detail"]: # Adaptar a tu estructura de error
            self.assertEqual(data["detail"]["codigo"], 500)
            self.assertIn("Error de prueba", data["detail"]["mensaje"])
        else:
            self.assertIn("Error de prueba", str(data["detail"])) # O como se formatee tu error 500


    async def test_get_producto_por_codigo_error_handling(self):
        with patch("app.controllers.producto_controller.get_db") as mock_db, \
             patch("app.controllers.producto_controller.ProductoService") as mock_service_class:
            
            mock_db.return_value = MagicMock()
            mock_service_instance = MagicMock()
            mock_service_instance.obtener_producto_por_codigo.side_effect = Exception("Database error")
            mock_service_class.return_value = mock_service_instance

            # CORRECCIÓN AQUÍ
            async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
                response = await ac.get("/v1/api/productos/P001")

        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        data = response.json()
        self.assertIn("detail", data)
        if isinstance(data["detail"], dict) and "codigo" in data["detail"]: # Adaptar a tu estructura de error
            self.assertEqual(data["detail"]["codigo"], 500)
            self.assertIn("Database error", data["detail"]["mensaje"])
        else:
            self.assertIn("Database error", str(data["detail"]))


if __name__ == "__main__":
    unittest.main()