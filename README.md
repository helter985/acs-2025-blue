# Proyecto Interlimpia
# Documento de Especificación de Pruebas
Versión 1.0
Fecha: 03/04/2025
Preparado para Interlimpia S.A.

## Historial de Revisiones

| Fecha | Descripción | Autor | Comentarios |
|-------|------------|-------|------------|
| 03/04/2025 | Versión 1.0 | F. Caballero, P. Mirazo, F. Lucero, J. Verdini | Borrador Inicial |

## Aprobación del Documento

La siguiente Especificación de Pruebas ha sido aceptada y aprobada por los siguientes:

| Nombre | Cargo | Fecha |
|--------|-------|-------|
| P. Mirazo | Desarrollador | |
| Ing. Mario Cuevas | Scrum Master | |
| F. Lucero | Desarrollador y Responsable de Pruebas | |
| J. Verdini | Tester y Desarrollador | |
| F. Caballero | QA y Desarrollador | |

## 1. Introducción

### 1.1 Propósito

El propósito de este documento es definir los requerimientos de prueba para la aplicación móvil Interlimpia que será desarrollada para Interlimpia S.A., distribuidora de artículos de limpieza que opera en la Región de Cuyo, Argentina. Este documento será utilizado por todos los interesados en el proyecto, incluyendo el equipo de desarrollo (P. Mirazo, F. Caballero, F. Lucero, J. Verdini) y el equipo de pruebas (F. Caballero como QA y Desarrollador, J. Verdini como Tester y Desarrollador, F. Lucero) bajo la supervisión del Scrum Master (Ing. Mario Cuevas).

### 1.2 Alcance de las Pruebas

#### En Alcance (In Scope):

- **FUNCIONALIDAD:** Se probará toda la funcionalidad relacionada con la consulta de precios, sincronización de datos y visualización de productos. Esto incluye búsquedas por código, por descripción y por marca.
- **USABILIDAD:** Se probará la facilidad de uso de la aplicación, considerando que debe ser intuitiva para usuarios con conocimientos tecnológicos muy básicos, sin necesidad de capacitación previa.
- **COMPATIBILIDAD:** Se verificará la compatibilidad con dispositivos Android 10+ e iOS 10+.
- **UI:** Se probarán todos los elementos de la interfaz de usuario, verificando que cumplen con los requisitos de diseño (paleta de colores sobria similar a Mercado Libre) y son fáciles de entender.

#### Fuera de Alcance (Out of Scope):

- **PERFORMANCE:** No se realizarán pruebas exhaustivas de rendimiento, aunque se verificará que las búsquedas respondan en tiempos menores a 3 segundos.
- **HARDWARE:** No se realizarán pruebas específicas de hardware más allá de la compatibilidad básica con dispositivos móviles.
- **PRUEBAS AUTOMATIZADAS:** No están dentro del alcance para esta fase del proyecto.
- **SEGURIDAD:** No se realizarán pruebas específicas de seguridad ya que la aplicación no maneja datos sensibles y operará de forma pública.
- **PRUEBAS DE FUNCIONALIDAD FUTURA:** La funcionalidad para gestión de pedidos que se implementará en el futuro no será parte de estas pruebas.

### 1.3 Definiciones, Acrónimos y Abreviaturas

| Abreviatura | Palabra |
|-------------|---------|
| ADM | Administrador |
| VEN | Vendedor/Transportista |

## 2. Requerimientos Específicos

La aplicación Interlimpia tendrá 2 roles principales:

1. Administrador (Gerente de Ventas)
2. Vendedor/Transportista (Acceso público)

### 2.1 Descripción de Roles

| Rol | Descripción |
|-----|-------------|
| Administrador | Responsable de actualizar las listas de precios en el sistema. Único usuario con acceso de escritura en el sistema. El encargado de ventas (gerente) tendrá este rol. |
| Vendedor/Transportista | Usuario final que consulta los precios de los productos a través de la aplicación móvil. Tendrán acceso público de solo lectura a la información de precios. |

### 2.2 Features por Rol

| Módulo | Roles Aplicables | Descripción |
|--------|------------------|-------------|
| Consulta de Precios | ADM, VEN | Permite buscar y visualizar los precios actualizados de los productos. Los vendedores podrán realizar búsquedas por código, por descripción (parcial) o por marca. |
| Actualización de Listas | ADM | Permite importar y normalizar las listas de precios desde archivos Excel de los cuatro proveedores (Rey de la limpieza, Mr. Clean, Olimpia, Limpiq). |
| Gestión de Imágenes | ADM | Permite subir, modificar y eliminar imágenes de productos que serán mostradas en la aplicación. |
| Visualización de Producto | ADM, VEN | Muestra la información completa del producto (código interno, marca, descripción, precio de venta e imagen). |
| Categorización de Productos | ADM, VEN | Permite categorizar y filtrar productos por tipo (limpieza del hogar, limpieza industrial). |

## 3. Detalles Técnicos

### 3.1 Detalles de Front-End

Esta sección describe el front-end de la aplicación Interlimpia y lista los campos principales de cada módulo.

#### Consulta de Precios
- Código interno (campo de texto)
- Descripción (campo de texto para búsqueda parcial)
- Marca (campo de texto)
- Botón de búsqueda
- Lista de resultados mostrando:
  - Imagen del producto
  - Código interno
  - Marca
  - Descripción
  - Precio de venta actual

#### Actualización de Listas (Solo Administrador)
- Selección de archivo (botón para seleccionar archivo Excel)
- Selección de proveedor (desplegable: Rey de la limpieza, Mr. Clean, Olimpia, Limpiq)
- Botón de importar
- Vista previa de datos importados
- Botón de confirmar actualización

#### Gestión de Imágenes (Solo Administrador)
- Código interno de producto (campo de texto)
- Botón para subir imagen
- Vista previa de imagen
- Botón de guardar
- Botón de cancelar

#### Login de Administrador
- Usuario
- Contraseña
- Botón de inicio de sesión

### 3.2 Requerimientos Técnicos

#### Login de Administrador
T1: Usuario - El campo no debe estar vacío
T2: Contraseña - El campo no debe estar vacío

#### Consulta de Precios
T3: Código interno - Se permiten solo números y caracteres
T4: Descripción - Se permiten caracteres alfanuméricos y espacios
T5: Marca - Se permiten caracteres alfanuméricos y espacios

#### Actualización de Listas
T6: Archivo - Debe seleccionarse un archivo
T7: Archivo - Solo se permiten archivos con extensión .xls o .xlsx
T8: Proveedor - Debe seleccionarse un proveedor de la lista

#### Gestión de Imágenes
T9: Código interno de producto - El campo no debe estar vacío
T10: Código interno de producto - Solo se permiten números y caracteres
T11: Imagen - Debe seleccionarse una imagen
T12: Imagen - Solo se permiten formatos .jpg, .png o .gif
T13: Imagen - El tamaño máximo permitido es de 2MB

### 3.3 Validaciones Funcionales

#### Consulta de Precios
F1: Si el código no existe, el sistema muestra un mensaje indicando que no se encontraron resultados
F2: Si hay múltiples resultados por descripción o marca, se muestran todos en una lista
F3: Los precios mostrados deben ser los más actualizados
F4: El tiempo de respuesta para una búsqueda debe ser menor a 3 segundos

#### Actualización de Listas
F5: Si el formato del archivo no es compatible, el sistema muestra un error
F6: Si hay productos en el archivo que no existen en el sistema, se debe mostrar una opción para agregarlos
F7: El sistema debe normalizar los datos de las distintas fuentes (proveedores) a un formato común

#### Gestión de Imágenes
F8: Si el código interno de producto no existe, el sistema muestra un error
F9: Si la imagen no cumple con los requisitos técnicos, el sistema muestra un error

#### Login de Administrador
F10: Si las credenciales son incorrectas, el sistema muestra un mensaje de error

### 3.4 Interfaces Externas

#### Compatibilidad con Dispositivos
La aplicación debe funcionar en:
- Dispositivos Android versión 10.0 o superior
- Dispositivos iOS versión 10.0 o superior

#### Tecnología de Desarrollo
La aplicación se desarrollará utilizando React Native para asegurar la compatibilidad con Android e iOS.

### 3.5 Requisitos No Funcionales

#### Usabilidad
- La aplicación debe ser intuitiva y fácil de usar, permitiendo a los vendedores acceder a la información de precios en menos de 3 toques desde la pantalla principal.
- El diseño debe usar una paleta de colores sobria similar a Mercado Libre, sin colores brillantes.
- La interfaz debe ser tan sencilla que cualquier persona sin experiencia pueda aprender a usarla sin capacitación.

#### Rendimiento
- Las búsquedas deben devolver resultados en menos de 3 segundos.
- La aplicación debe ser capaz de manejar eficientemente un catálogo de aproximadamente 400 productos diferentes.
- Debe soportar consultas frecuentes (cada 10-15 minutos) por parte de 30-40 vendedores simultáneamente.

#### Disponibilidad
- La aplicación estará disponible principalmente durante el horario laboral (8 horas diarias).
- La aplicación requiere conexión a internet para funcionar (100% online).

### 3.6 Restricciones de Diseño

Los vendedores de Interlimpia S.A. tienen conocimientos tecnológicos muy básicos. Por lo tanto, el sistema debe ser extremadamente intuitivo y fácil de entender, con énfasis en una interfaz limpia y con elementos visuales claros.

## 4. Casos de Prueba

### Caso de Prueba 1: Búsqueda por Código Interno
**Objetivo:** Verificar que la búsqueda por código interno funciona correctamente.
**Pasos:**
1. Abrir la aplicación
2. Ingresar un código interno válido en el campo correspondiente
3. Presionar el botón de búsqueda
**Resultado Esperado:** Se muestra la información completa del producto incluyendo imagen, código, marca, descripción y precio de venta.

### Caso de Prueba 2: Búsqueda por Descripción Parcial
**Objetivo:** Verificar que la búsqueda por descripción parcial funciona correctamente.
**Pasos:**
1. Abrir la aplicación
2. Ingresar una palabra clave en el campo de descripción
3. Presionar el botón de búsqueda
**Resultado Esperado:** Se muestra una lista de todos los productos que contienen la palabra clave en su descripción.

### Caso de Prueba 3: Búsqueda por Marca
**Objetivo:** Verificar que la búsqueda por marca funciona correctamente.
**Pasos:**
1. Abrir la aplicación
2. Ingresar una marca en el campo correspondiente
3. Presionar el botón de búsqueda
**Resultado Esperado:** Se muestra una lista de todos los productos de la marca especificada.

### Caso de Prueba 4: Actualización de Lista de Precios (Administrador)
**Objetivo:** Verificar que el administrador puede actualizar las listas de precios.
**Pasos:**
1. Iniciar sesión como administrador
2. Acceder a la sección de actualización de listas
3. Seleccionar un archivo Excel válido
4. Seleccionar un proveedor
5. Presionar el botón de importar
6. Confirmar la actualización
**Resultado Esperado:** El sistema importa y normaliza los datos, actualizando los precios en la base de datos.

### Caso de Prueba 5: Gestión de Imágenes (Administrador)
**Objetivo:** Verificar que el administrador puede asociar imágenes a los productos.
**Pasos:**
1. Iniciar sesión como administrador
2. Acceder a la sección de gestión de imágenes
3. Ingresar un código interno de producto válido
4. Subir una imagen
5. Guardar los cambios
**Resultado Esperado:** La imagen se asocia correctamente al producto y se muestra en las consultas.

## 5. Proceso de Gestión de Cambios

Los cambios en las especificaciones de prueba, ya sea del equipo de desarrollo, del equipo de pruebas o del cliente, se comunicarán al Scrum Master (Ing. Mario Cuevas).

Cualquier cambio realizado en este documento requerirá la aprobación del desarrollador principal (Pablo Mirazo), el Scrum Master (Ing. Mario Cuevas) y el responsable de pruebas (Facundo Lucero).

Una vez aprobados, los cambios se realizarán en el documento y la nueva versión se distribuirá a todos los interesados.

## 6. Criterios de Aceptación

Para considerar que las pruebas han sido exitosas y que la aplicación está lista para su implementación, se deben cumplir los siguientes criterios:

1. Todas las funcionalidades descritas en el alcance funcionan correctamente.
2. El tiempo de respuesta para las búsquedas es menor a 3 segundos.
3. La aplicación es compatible con los dispositivos Android 10+ e iOS 10+ especificados.
4. La interfaz de usuario es intuitiva y fácil de usar, según evaluación del equipo de pruebas.
5. La actualización de listas de precios por parte del administrador funciona correctamente.

El responsable de aprobar los resultados de las pruebas será Facundo Lucero con el apoyo de Jesús Verdini como tester, quienes deberán verificar que todos los criterios se cumplen antes de dar el visto bueno para la implementación.

## 7. Plan de Soporte y Mantenimiento

El soporte post-implementación será proporcionado por el equipo de desarrollo cuando se detecten fallas o se vayan a realizar actualizaciones del sistema. El responsable del mantenimiento a largo plazo será F. Caballero como QA y Desarrollador.

Las actualizaciones y mejoras se realizarán a medida que surjan nuevos requerimientos por parte de los usuarios o se identifiquen oportunidades de mejora en el sistema.

## Apéndices

No aplicable para este documento.