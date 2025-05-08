# API Interlimpia

API para la consulta de productos de Interlimpia, desarrollada con FastAPI y SQLAlchemy.

## Descripción

Esta API proporciona endpoints públicos para la consulta de productos y categorías para la aplicación móvil de Interlimpia. Permite a los vendedores/transportistas consultar precios y detalles de productos mediante búsquedas por código, descripción, marca y categoría.

## Estructura del Proyecto

```
interlimpia-api/
│
├── alembic/               # Configuración de migraciones
├── app/
│   ├── controllers/       # Controladores (endpoints de la API)
│   ├── database/          # Configuración de la base de datos
│   ├── dtos/              # Data Transfer Objects (validación y serialización)
│   ├── models/            # Modelos ORM
│   ├── repositories/      # Capa de acceso a datos
│   ├── services/          # Lógica de negocio
│   ├── config.py          # Configuración global de la aplicación
│   └── main.py            # Punto de entrada principal
│
├── scripts/               # Scripts utilidades
├── tests/                 # Pruebas automatizadas
│
├── .env                   # Variables de entorno (no incluido en el repositorio)
├── .env.example           # Ejemplo de variables de entorno
├── alembic.ini            # Configuración de Alembic
├── requirements.txt       # Dependencias del proyecto
└── README.md              # Este archivo
```

## Instalación

1. Clonar el repositorio

```bash
git clone https://github.com/interlimpia/interlimpia-api.git
cd interlimpia-api
```

2. Crear y activar un entorno virtual

```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

3. Instalar dependencias

```bash
pip install -r requirements.txt
```

4. Crear un archivo `.env` basado en `.env.example`

```bash
cp .env.example .env
# Editar el archivo .env con los valores adecuados
```

5. Inicializar la base de datos

```bash
python -m scripts.init_db
```

## Ejecución

Para iniciar el servidor de desarrollo:

```bash
uvicorn app.main:app --reload
```

La API estará disponible en [http://localhost:8000](http://localhost:8000).

La documentación de la API estará disponible en:
- [http://localhost:8000/docs](http://localhost:8000/docs) (Swagger UI)
- [http://localhost:8000/redoc](http://localhost:8000/redoc) (ReDoc)

## Migraciones de Base de Datos

Para crear una nueva migración:

```bash
alembic revision --autogenerate -m "descripción de los cambios"
```

Para aplicar migraciones pendientes:

```bash
alembic upgrade head
```

## Endpoints Disponibles

### Públicos (Vendedores)

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/api/productos` | Obtener lista de productos |
| GET | `/api/productos/{codigo}` | Obtener producto por código |
| GET | `/api/categorias` | Obtener lista de categorías |

## Pruebas

Para ejecutar las pruebas automatizadas:

```bash
pytest
```

## Tecnologías Utilizadas

- [FastAPI](https://fastapi.tiangolo.com/)
- [SQLAlchemy](https://www.sqlalchemy.org/)
- [Pydantic](https://pydantic-docs.helpmanual.io/)
- [Alembic](https://alembic.sqlalchemy.org/)
- [Pytest](https://docs.pytest.org/)

## Licencia

Propietario - Interlimpia S.A.