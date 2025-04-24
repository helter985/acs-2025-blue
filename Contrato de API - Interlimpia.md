# Contrato de API - Interlimpia

Este documento define el contrato de API para la aplicación Interlimpia, especificando los endpoints disponibles, parámetros, formatos de request/response y códigos de estado HTTP.

## 1. Especificación OpenAPI

La siguiente es la especificación OpenAPI 3.0.4 del contrato:

```yaml
# Ver archivo openapi-interlimpia.yaml
```

## 2. Resumen de Endpoints

### Endpoints Públicos (Vendedores)

| Método | Endpoint | Descripción | Query Parameters | Status Codes |
|--------|----------|-------------|-----------------|--------------|
| GET | `/productos` | Obtener lista de productos | `marca`, `descripcion`, `categoria`, `nombre` | 200, 204, 400, 500 |
| GET | `/productos/{codigo}` | Obtener producto por código | - | 200, 404, 500 |
| GET | `/categorias` | Obtener lista de categorías | - | 200, 500 |

## 3. Consideraciones sobre los Códigos de Estado

### Casos especiales:

1. **GET `/productos/{codigo}`** - Retorna 404 si el producto no existe:
   - Se utiliza 404 porque se está intentando acceder a un recurso específico que no existe.
   - La URI apunta a UN ARTÍCULO ESPECÍFICO, por lo que si ese artículo no existe, lo apropiado es un 404 (Not Found).

2. **GET `/productos`** con filtros - Retorna 204 si no hay coincidencias:
   - Se utiliza 204 (No Content) porque la colección de productos SÍ EXISTE, pero el filtro aplicado no encontró coincidencias.
   - La URI apunta a una COLECCIÓN que existe, pero está vacía según los filtros proporcionados.

## 4. Formatos de Respuesta

Todas las respuestas se devuelven en formato JSON, con estructuras claramente definidas en los schemas de componentes.

### Ejemplo de respuesta exitosa para GET `/productos/{codigo}`:

```json
{
  "codigo": "A123",
  "marca": "Mr. Clean",
  "descripcion": "Limpiador multiusos con aroma a limón",
  "precio": 1250.50,
  "categoria": "limpieza_hogar",
  "imagen_url": "https://storage.interlimpia.com/productos/A123.jpg",
  "proveedor": "Rey de la limpieza"
}
```

### Ejemplo de respuesta de error:

```json
{
  "codigo": 404,
  "mensaje": "Producto no encontrado"
}
```

## 5. Instrucciones para Implementación

Al implementar esta API, asegúrese de:

1. Validar todos los datos de entrada según los schemas definidos.
2. Aplicar los códigos de estado HTTP apropiados según lo especificado.
3. Implementar correctamente los filtros para la colección de productos.
4. Documentar cualquier cambio o extensión a este contrato.

**Nota:** Las funcionalidades administrativas (importación de listas de precios y gestión de imágenes) se implementarán en una solución separada, no a través de esta API pública.