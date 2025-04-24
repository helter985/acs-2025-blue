#### TC-03: Subida de imagen para un producto existente
**Relacionado con:** US-03  
**Objetivo:** Verificar que el administrador puede subir una imagen para un producto  
**Precondiciones:**
- El usuario ha iniciado sesión como administrador
- Existe un producto con código "B456" en el sistema
- Se dispone de una imagen en formato JPG de tamaño menor a 2MB

**Pasos:**
1. Acceder a la sección "Gestión de Imágenes"
2. Ingresar "B456" en el campo de código interno
3. Hacer clic en "Buscar"
4. Hacer clic en "Subir imagen" y seleccionar la imagen preparada
5. Revisar la vista previa de la imagen
6. Hacer clic en "Guardar"

**Resultado esperado:**
- El sistema muestra el producto con código "B456"
- La vista previa de la imagen se muestra correctamente
- Al guardar, muestra un mensaje de éxito
- Al consultar el producto "B456", la imagen aparece junto con la información del producto

**Severidad:** Media