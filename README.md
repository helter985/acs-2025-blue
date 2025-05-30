# Proyecto Interlimpia
# Documento de Especificación de Pruebas
Versión 1.1
Fecha: 24/04/2025
Preparado para Interlimpia S.A.

## Historial de Revisiones

| Fecha | Descripción | Autor | Comentarios |
|-------|------------|-------|------------|
| 03/04/2025 | Versión 1.0 | F. Caballero, P. Mirazo, F. Lucero, J. Verdini | Borrador Inicial |
| 24/04/2025 | Versión 1.1 | F. Caballero, P. Mirazo, F. Lucero, J. Verdini | Actualización de arquitectura - Separación de sistema administrativo (MVC) de la API |

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
| MVC | Modelo-Vista-Controlador |
| API | Application Programming Interface |

## 2. Requerimientos Específicos

El sistema Interlimpia está dividido en dos componentes principales:
1. **API Pública**: Para consulta de productos por parte de vendedores
2. **Panel de Administración (MVC)**: Para gestión de productos por parte del administrador

Cada componente tendrá roles específicos:

### 2.1 Descripción de Roles

| Rol | Descripción | Componente |
|-----|-------------|------------|
| Administrador | Responsable de actualizar las listas de precios en el sistema. Único usuario con acceso de escritura en el sistema. El encargado de ventas (gerente) tendrá este rol. | Panel de Administración (MVC) |
| Vendedor/Transportista | Usuario final que consulta los precios de los productos a través de la aplicación móvil. Tendrán acceso público de solo lectura a la información de precios. | API Pública |

### 2.2 Features por Rol

| Módulo | Roles Aplicables | Componente | Descripción |
|--------|------------------|------------|-------------|
| Consulta de Precios | VEN | API Pública | Permite buscar y visualizar los precios actualizados de los productos. Los vendedores podrán realizar búsquedas por código, por descripción (parcial) o por marca. |
| Actualización de Listas | ADM | Panel de Administración (MVC) | Permite importar y normalizar las listas de precios desde archivos Excel de los cuatro proveedores (Rey de la limpieza, Mr. Clean, Olimpia, Limpiq). |
| Gestión de Imágenes | ADM | Panel de Administración (MVC) | Permite subir, modificar y eliminar imágenes de productos que serán mostradas en la aplicación. |
| Visualización de Producto | VEN | API Pública | Muestra la información completa del producto (código interno, marca, descripción, precio de venta e imagen). |
| Categorización de Productos | VEN | API Pública | Permite categorizar y filtrar productos por tipo (limpieza del hogar, limpieza industrial). |

### 2.3 User Stories

#### US-01: Búsqueda de productos por código

**Como** vendedor de Interlimpia  
**Quiero** poder buscar productos por su código interno  
**Para** encontrar rápidamente la información actualizada de precios que necesito mostrar a los clientes  

**Criterios de aceptación:**
- El sistema debe permitir ingresar el código interno del producto  
- Al realizar la búsqueda, debe mostrar la información completa del producto:
  - Código  
  - Marca  
  - Descripción  
  - Precio  
  - Imagen  
- Si el código no existe, debe mostrar un mensaje indicando que no se encontraron resultados  
- El tiempo de respuesta debe ser menor a 3 segundos

#### US-02: Actualización de listas de precios

**Como** administrador del sistema  
**Quiero** poder importar y actualizar las listas de precios desde archivos Excel de los proveedores  
**Para** mantener la información de precios actualizada para los vendedores  

**Criterios de aceptación:**
- El sistema debe permitir seleccionar un archivo Excel para importar
- Debe permitir seleccionar el proveedor al que corresponde la lista (Rey de la limpieza, Mr. Clean, Olimpia, Limpiq)
- Debe mostrar una vista previa de los datos antes de confirmar la actualización
- Al confirmar, debe actualizar los precios en el sistema
- Si el formato del archivo no es compatible, debe mostrar un mensaje de error

#### US-03: Subir imagen para un producto existente

**Como** administrador del sistema  
**Quiero** poder subir una imagen para un producto existente  
**Para** que los clientes puedan visualizar el producto en el catálogo

**Criterios de Aceptación:**
1. Acceso desde la sección **"Gestión de Imágenes"**.
2. Búsqueda de productos por **código interno** (ej: `B456`).
3. Soporte para imágenes en formato **JPG/PNG** (<2MB).
4. **Vista previa** de la imagen antes de guardar.
5. **Confirmación** visual al guardar exitosamente.
6. La imagen debe **asociarse persistentemente** al producto.

**Escenarios:**

*Escenario 1: Subida exitosa*  
**Dado** que soy un administrador logueado  
**Y** existe el producto con código `B456`  
**Cuando** subo una imagen válida (<2MB, JPG/PNG)  
**Y** confirmo la operación  
**Entonces** el sistema:
- Guarda la imagen  
- Muestra mensaje: _"Imagen asociada correctamente"_  
- Asocia la imagen al producto en consultas posteriores

*Escenario 2: Imagen con tamaño excedido*  
**Dado** que soy un administrador logueado  
**Cuando** intento subir una imagen >2MB  
**Entonces** el sistema:
- Muestra error: _"El tamaño máximo es 2MB"_  
- Cancela el proceso de subida  
- Mantiene el formulario editable

*Escenario 3: Producto no encontrado*  
**Dado** que soy un administrador logueado  
**Cuando** ingreso un código inexistente (ej: `XXX999`)  
**Entonces** el sistema muestra: _"Producto no encontrado"_

**Metadata:**
| Campo | Valor |
|-------------|-----------------|
| **Prioridad** | Media (🟡) |
| **Estimación** | 3 story points |
| **Epic** | Gestión de Catálogo |
| **Dependencias** | US-01 (Alta de productos) |

#### US-04: Filtrado de productos por categoría

**Como** vendedor de Interlimpia  
**Quiero** poder filtrar productos por su categoría (limpieza del hogar o industrial)  
**Para** encontrar más fácilmente los productos que necesito según el tipo de cliente

**Criterios de aceptación:**
- El sistema debe mostrar opciones para filtrar por categoría (limpieza del hogar, limpieza industrial)
- Al seleccionar una categoría, debe mostrar solo los productos correspondientes
- Debe permitir quitar los filtros para ver todos los productos
- El filtrado debe aplicarse junto con otros criterios de búsqueda (código, descripción, marca)

### 2.4 Test Cases

#### TC-01: Búsqueda de producto por código interno válido

**Relacionado con:** US-01  
**Componente:** API Pública  
**Objetivo:** Verificar que la búsqueda por código interno muestra la información correcta del producto  
**Precondiciones:**
- La aplicación está disponible y funcionando  
- Existe un producto con código "A123" en el sistema  

**Pasos:**
1. Abrir la aplicación  
2. Ingresar "A123" en el campo de código interno  
3. Presionar el botón de búsqueda  

**Resultado esperado:**
- Se muestra la información completa del producto con código "A123" incluyendo:  
  - Código interno: A123  
  - Marca del producto  
  - Descripción del producto  
  - Precio de venta actual  
  - Imagen del producto (si está disponible)  
- El tiempo de respuesta es menor a 3 segundos  

**Severidad:** Alta

#### TC-02: Importación de lista de precios con formato correcto

**Relacionado con:** US-02  
**Componente:** Panel de Administración (MVC)  
**Objetivo:** Verificar que el administrador puede importar y actualizar listas de precios desde Excel  
**Precondiciones:**
- El usuario ha iniciado sesión como administrador
- Se dispone de un archivo Excel con formato correcto de lista de precios

**Pasos:**
1. Acceder a la sección "Actualización de Listas"
2. Hacer clic en "Seleccionar archivo" y elegir el archivo Excel preparado
3. Seleccionar el proveedor "Rey de la limpieza" del desplegable
4. Hacer clic en "Importar"
5. Revisar la vista previa de los datos
6. Hacer clic en "Confirmar actualización"

**Resultado esperado:**
- El sistema muestra correctamente la vista previa de los datos del archivo
- Al confirmar, muestra un mensaje de éxito
- Los precios de los productos del proveedor "Rey de la limpieza" se actualizan en el sistema
- Al consultar cualquier producto de este proveedor, se muestra el precio actualizado

**Severidad:** Alta

#### TC-03: Subida de imagen para un producto existente

**Relacionado con:** US-03  
**Componente:** Panel de Administración (MVC)  
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

#### TC-04: Filtrado de productos por categoría

**Relacionado con:** US-04  
**Componente:** API Pública  
**Objetivo:** Verificar que los productos se pueden filtrar correctamente por categoría  
**Precondiciones:**
- La aplicación está disponible y funcionando
- Existen productos categorizados como "limpieza del hogar" y "limpieza industrial" en el sistema

**Pasos:**
1. Abrir la aplicación
2. Seleccionar la categoría "limpieza industrial" del filtro
3. Observar los resultados mostrados
4. Cambiar la selección a "limpieza del hogar"
5. Observar los resultados mostrados
6. Quitar el filtro de categoría
7. Observar los resultados mostrados

**Resultado esperado:**
- Al seleccionar "limpieza industrial", solo se muestran productos de esta categoría
- Al seleccionar "limpieza del hogar", solo se muestran productos de esta categoría
- Al quitar el filtro, se muestran productos de todas las categorías
- El filtrado se realiza en menos de 3 segundos

**Severidad:** Media

## 3. Detalles Técnicos

### 3.1 Arquitectura

La arquitectura del sistema Interlimpia se divide en dos componentes principales: una API pública para los vendedores y un sistema MVC para el administrador, ambos compartiendo la misma base de datos.

```mermaid
graph TD
    A[Aplicación Móvil para Vendedores] -->|Consultas de solo lectura| B[API RESTful]
    B -->|Datos de productos| A
    B -->|Almacena/Consulta| E[(Base de Datos)]
    
    F[Panel Web de Administración] -->|MVC| G[Backend Admin]
    G -->|Administración de datos| E
    
    subgraph "Frontend"
        A
        F
    end
    
    subgraph "Backend"
        B
        G
    end
    
    subgraph "Datos"
        E
    end
```

**Componentes del sistema:**

1. **API RESTful (Backend):**
   - Proporciona endpoints públicos para consulta de productos
   - Implementa lógica de filtrado y búsqueda
   - Acceso de solo lectura para los vendedores a través de la aplicación móvil
   - Está definida en el contrato de API [openapi-interlimpia.yaml](./openapi-interlimpia.yaml)

2. **Aplicación Móvil (Frontend):**
   - Desarrollada en React Native para Android e iOS
   - Interfaz intuitiva para vendedores/transportistas
   - Funcionalidad de búsqueda y visualización de productos

3. **Panel Web de Administración:**
   - Sistema independiente basado en arquitectura MVC
   - Acceso exclusivo para administradores
   - Interfaz para importar listas de precios y gestionar imágenes

4. **Backend de Administración:**
   - Implementa la lógica de negocio para el panel administrativo
   - Maneja la autenticación y autorización
   - Gestiona la importación y normalización de datos

5. **Base de Datos:**
   - Repositorio central compartido entre la API pública y el sistema administrativo
   - Almacena información de productos, precios y categorías

Esta arquitectura garantiza una clara separación entre el acceso público de vendedores (solo lectura) y las funcionalidades administrativas de actualización de datos.

### 3.2 Definición de API

La API de Interlimpia está diseñada siguiendo las especificaciones OpenAPI 3.0, proporcionando endpoints públicos para la consulta de productos y categorías.

El contrato completo de la API se encuentra en el archivo [openapi-interlimpia.yaml](./openapi-interlimpia.yaml).

**Características de la API:**
- Endpoints públicos para consulta de productos y categorías
- Soporte para filtrado por múltiples criterios
- Manejo específico de códigos de estado (204 para resultados vacíos, 404 para recursos inexistentes)
- Documentación completa de parámetros y respuestas

### 3.3 Detalles de Front-End

Esta sección describe el front-end de la aplicación Interlimpia y lista los campos principales de cada módulo.

#### Aplicación Móvil para Vendedores (React Native)

**Consulta de Precios**
- Código interno (campo de texto)
- Descripción (campo de texto para búsqueda parcial)
- Marca (campo de texto)
- Selector de categoría (desplegable)
- Botón de búsqueda
- Lista de resultados mostrando:
  - Imagen del producto
  - Código interno
  - Marca
  - Descripción
  - Precio de venta actual

#### Panel Web de Administración (MVC)

**Login de Administrador**
- Usuario (campo de texto)
- Contraseña (campo de contraseña)
- Botón de inicio de sesión

**Actualización de Listas**
- Selección de archivo (botón para seleccionar archivo Excel)
- Selección de proveedor (desplegable: Rey de la limpieza, Mr. Clean, Olimpia, Limpiq)
- Botón de importar
- Vista previa de datos importados
- Botón de confirmar actualización

**Gestión de Imágenes**
- Código interno de producto (campo de texto)
- Botón para buscar producto
- Botón para subir imagen
- Vista previa de imagen
- Botón de guardar
- Botón de cancelar

### 3.4 Requerimientos Técnicos

#### Componente: Panel de Administración (MVC)

**Login de Administrador**
T1: Usuario - El campo no debe estar vacío
T2: Contraseña - El campo no debe estar vacío

**Actualización de Listas**
T3: Archivo - Debe seleccionarse un archivo
T4: Archivo - Solo se permiten archivos con extensión .xls o .xlsx
T5: Proveedor - Debe seleccionarse un proveedor de la lista

**Gestión de Imágenes**
T6: Código interno de producto - El campo no debe estar vacío
T7: Código interno de producto - Solo se permiten números y caracteres
T8: Imagen - Debe seleccionarse una imagen
T9: Imagen - Solo se permiten formatos .jpg, .png o .gif
T10: Imagen - El tamaño máximo permitido es de 2MB

#### Componente: API Pública

**Consulta de Precios**
T11: Código interno - Se permiten solo números y caracteres
T12: Descripción - Se permiten caracteres alfanuméricos y espacios
T13: Marca - Se permiten caracteres alfanuméricos y espacios
T14: Categoría - Valor seleccionado de una lista predefinida

### 3.5 Validaciones Funcionales

#### Componente: API Pública

**Consulta de Precios**
F1: Si el código no existe, el sistema muestra un mensaje indicando que no se encontraron resultados
F2: Si hay múltiples resultados por descripción o marca, se muestran todos en una lista
F3: Los precios mostrados deben ser los más actualizados
F4: El tiempo de respuesta para una búsqueda debe ser menor a 3 segundos
F5: Al filtrar por categoría, solo se muestran los productos de esa categoría

#### Componente: Panel de Administración (MVC)

**Actualización de Listas**
F6: Si el formato del archivo no es compatible, el sistema muestra un error
F7: Si hay productos en el archivo que no existen en el sistema, se debe mostrar una opción para agregarlos
F8: El sistema debe normalizar los datos de las distintas fuentes (proveedores) a un formato común

**Gestión de Imágenes**
F9: Si el código interno de producto no existe, el sistema muestra un error
F10: Si la imagen no cumple con los requisitos técnicos, el sistema muestra un error

**Login de Administrador**
F11: Si las credenciales son incorrectas, el sistema muestra un mensaje de error

### 3.6 Interfaces Externas

#### Componente: Aplicación Móvil para Vendedores
**Compatibilidad con Dispositivos**
La aplicación debe funcionar en:
- Dispositivos Android versión 10.0 o superior
- Dispositivos iOS versión 10.0 o superior

**Tecnología de Desarrollo**
- Framework: React Native
- Comunicación con backend: API RESTful

#### Componente: Panel de Administración
**Compatibilidad con Navegadores**
El panel administrativo debe funcionar en:
- Google Chrome (últimas 2 versiones)
- Mozilla Firefox (últimas 2 versiones)
- Safari (últimas 2 versiones)

**Tecnología de Desarrollo**
- Patrón: MVC
- Frontend: React.js
- Backend: Node.js con Express
- Comunicación con base de datos: Directa

### 3.7 Requisitos No Funcionales

#### Componente: Aplicación Móvil para Vendedores

**Usabilidad**
- La aplicación debe ser intuitiva y fácil de usar, permitiendo a los vendedores acceder a la información de precios en menos de 3 toques desde la pantalla principal.
- El diseño debe usar una paleta de colores sobria similar a Mercado Libre, sin colores brillantes.
- La interfaz debe ser tan sencilla que cualquier persona sin experiencia pueda aprender a usarla sin capacitación.

**Rendimiento**
- Las búsquedas deben devolver resultados en menos de 3 segundos.
- La aplicación debe ser capaz de manejar eficientemente un catálogo de aproximadamente 400 productos diferentes.
- Debe soportar consultas frecuentes (cada 10-15 minutos) por parte de 30-40 vendedores simultáneamente.

**Disponibilidad**
- La aplicación estará disponible principalmente durante el horario laboral (8 horas diarias).
- La aplicación requiere conexión a internet para funcionar (100% online).

#### Componente: Panel de Administración

**Usabilidad**
- La interfaz debe ser clara y organizada por secciones.
- Debe proporcionar retroalimentación visible para las acciones realizadas.

**Seguridad**
- Acceso restringido mediante autenticación.
- Sesiones con tiempo de expiración.
- Validación de permisos para todas las operaciones de escritura.

## 4. Casos de Prueba

### 4.1 Componente: Aplicación Móvil para Vendedores

#### Caso de Prueba 1: Búsqueda por Código Interno
**Objetivo:** Verificar que la búsqueda por código interno funciona correctamente.
**Pasos:**
1. Abrir la aplicación móvil
2. Ingresar un código interno válido en el campo correspondiente
3. Presionar el botón de búsqueda
**Resultado Esperado:** Se muestra la información completa del producto incluyendo imagen, código, marca, descripción y precio de venta.

#### Caso de Prueba 2: Búsqueda por Descripción Parcial
**Objetivo:** Verificar que la búsqueda por descripción parcial funciona correctamente.
**Pasos:**
1. Abrir la aplicación móvil
2. Ingresar una palabra clave en el campo de descripción
3. Presionar el botón de búsqueda
**Resultado Esperado:** Se muestra una lista de todos los productos que contienen la palabra clave en su descripción.

#### Caso de Prueba 3: Búsqueda por Marca
**Objetivo:** Verificar que la búsqueda por marca funciona correctamente.
**Pasos:**
1. Abrir la aplicación móvil
2. Ingresar una marca en el campo correspondiente
3. Presionar el botón de búsqueda
**Resultado Esperado:** Se muestra una lista de todos los productos de la marca especificada.

#### Caso de Prueba 4: Filtrado por Categoría
**Objetivo:** Verificar que el filtrado por categoría funciona correctamente.
**Pasos:**
1. Abrir la aplicación móvil
2. Seleccionar una categoría del desplegable
3. Observar los resultados mostrados
**Resultado Esperado:** Se muestra una lista de productos que pertenecen a la categoría seleccionada.

### 4.2 Componente: Panel de Administración (MVC)

#### Caso de Prueba 5: Actualización de Lista de Precios
**Objetivo:** Verificar que el administrador puede actualizar las listas de precios.
**Pasos:**
1. Iniciar sesión como administrador en el panel web
2. Acceder a la sección de actualización de listas
3. Seleccionar un archivo Excel válido
4. Seleccionar un proveedor
5. Presionar el botón de importar
6. Confirmar la actualización
**Resultado Esperado:** El sistema importa y normaliza los datos, actualizando los precios en la base de datos.

#### Caso de Prueba 6: Gestión de Imágenes
**Objetivo:** Verificar que el administrador puede asociar imágenes a los productos.
**Pasos:**
1. Iniciar sesión como administrador en el panel web
2. Acceder a la sección de gestión de imágenes
3. Ingresar un código interno de producto válido
4. Subir una imagen
5. Guardar los cambios
**Resultado Esperado:** La imagen se asocia correctamente al producto y se muestra en las consultas.

#### Caso de Prueba 7: Autenticación de Administrador
**Objetivo:** Verificar que solo usuarios autorizados pueden acceder al panel de administración.
**Pasos:**
1. Acceder a la URL del panel de administración
2. Ingresar credenciales correctas
3. Presionar el botón de inicio de sesión
**Resultado Esperado:** El sistema permite el acceso y muestra el panel con las opciones administrativas.

## 5. Proceso de Gestión de Cambios

Los cambios en las especificaciones de prueba, ya sea del equipo de desarrollo, del equipo de pruebas o del cliente, se comunicarán al Scrum Master (Ing. Mario Cuevas).

Cualquier cambio realizado en este documento requerirá la aprobación del desarrollador principal (Pablo Mirazo), el Scrum Master (Ing. Mario Cuevas) y el responsable de pruebas (Facundo Lucero).

Una vez aprobados, los cambios se realizarán en el documento y la nueva versión se distribuirá a todos los interesados.

## 6. Criterios de Aceptación

Para considerar que las pruebas han sido exitosas y que el sistema está listo para su implementación, se deben cumplir los siguientes criterios:

### 6.1 Componente: Aplicación Móvil para Vendedores
1. Todas las funcionalidades de consulta descritas en el alcance funcionan correctamente.
2. El tiempo de respuesta para las búsquedas es menor a 3 segundos.
3. La aplicación es compatible con los dispositivos Android 10+ e iOS 10+ especificados.
4. La interfaz de usuario es intuitiva y fácil de usar, según evaluación del equipo de pruebas.

### 6.2 Componente: Panel de Administración (MVC)
1. La autenticación de administradores funciona correctamente, permitiendo acceso solo a usuarios autorizados.
2. La actualización de listas de precios importa y procesa correctamente los datos.
3. La gestión de imágenes permite subir, visualizar y asociar imágenes a los productos.
4. Los cambios realizados desde el panel administrativo se reflejan correctamente en las consultas realizadas desde la aplicación móvil.

El responsable de aprobar los resultados de las pruebas será Facundo Lucero con el apoyo de Jesús Verdini como tester, quienes deberán verificar que todos los criterios se cumplen antes de dar el visto bueno para la implementación.

## 7. Plan de Soporte y Mantenimiento

El soporte post-implementación será proporcionado por el equipo de desarrollo cuando se detecten fallas o se vayan a realizar actualizaciones del sistema. El responsable del mantenimiento a largo plazo será F. Caballero como QA y Desarrollador.

Las actualizaciones y mejoras se realizarán a medida que surjan nuevos requerimientos por parte de los usuarios o se identifiquen oportunidades de mejora en el sistema.

## Apéndices

No aplicable para este documento.