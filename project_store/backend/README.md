# Backend for Project Store

El proyecto backend es la API para el proyecto Project Store, proyecto final utilizando **FastAPI**

## Tecnologías Usadas

- **Python 3.10+**
- **FastAPI**: Framework para construir APIs rápidas y modernas.
- **httpx**: Cliente HTTP asíncrono para consumir APIs externas.
- **pandas**: Biblioteca para manipulación y análisis de datos.
- **xlsxwriter**: Motor para generar archivos Excel.
- **xhtml2pdf**: Biblioteca para convertir HTML a PDF.
- **Jinja2**: Motor de plantillas para generar HTML dinámico.
- **Uvicorn**: Servidor ASGI para ejecutar la aplicación.

## Instrucciones de Uso

### 1. Crear un entorno virtual
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

### 2. Compilar proyecto general (desde directorio padre al actual)
```bash
docker compose up --build -d
```

### 3. Acceder a los logs del backend
```bash
docker logs project_store-backend-1 -f
```

### 4. Acceder a la documentación interactiva
- **Swagger UI**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **ReDoc**: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

## Endpoints Disponibles

| Endpoint                              | Descripción                                          |
|---------------------------------------|------------------------------------------------------|
| `/api/auth/*`                         | Endpoints de Authentication.                         |
| `/api/users/*`                        | Endpoints de gestión de usuarios.                    |
| `/api/orders/*`                       | Endpoints de gestión de orders.                      |
| `/api/orders/{order_id}/projects/*`   | Endpoints de gestión de los productos de una orden.  |
| `/api/products/*`                     | Endpoints para obtener datos de productos            |
| `/api/exports/*`                      | Endpoints de exportación de datos de ordenes         |
| `/api/stats/*`                        | Endpoints de estadísticas                            |


## Estructura del Proyecto

```
project_store/backend/
│
├── main.py                     # Archivo principal con los endpoints
├── requirements.txt            # Dependencias del proyecto
├── utils/
│   └── api_dummy_prodcuts.py   # Lógica para consumir la API externa
├── views/
│   └── pdf_template.html       # Plantilla HTML para generar el PDF
├── README.md                   # Documentación del proyecto
└── venv/                       # Entorno virtual (excluido en .gitignore)
```

## Notas

- La API externa utilizada es la es la de Dummy Products: [https://dummyjson.com/products](https://dummyjson.com/products)
- Asegúrate de que las dependencias del sistema necesarias para **xhtml2pdf** estén instaladas correctamente.
- Si tienes problemas con dependencias, consulta la documentación oficial de cada biblioteca.

