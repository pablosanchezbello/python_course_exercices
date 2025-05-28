# Demo FastAPI - Consumo de API Externa y Generación de Reportes

Este proyecto es una demostración de cómo consumir una API externa y generar reportes en diferentes formatos (Excel, CSV, PDF) utilizando **FastAPI**.

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

### 2. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 3. Ejecutar la aplicación
```bash
python main.py
```

### 4. Acceder a la documentación interactiva
- **Swagger UI**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **ReDoc**: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

## Endpoints Disponibles

| Método | Endpoint                  | Descripción                                      |
|--------|---------------------------|--------------------------------------------------|
| GET    | `/rick-and-morty`         | Obtiene los personajes de la API externa.       |
| GET    | `/rick-and-morty/excel`   | Genera un archivo Excel con los personajes.     |
| GET    | `/rick-and-morty/csv`     | Genera un archivo CSV con los personajes.       |
| GET    | `/rick-and-morty/pdf`     | Genera un archivo PDF con los personajes.       |

## Estructura del Proyecto

```
demo_fastAPI_peticion_externa/
│
├── main.py                     # Archivo principal con los endpoints
├── requirements.txt            # Dependencias del proyecto
├── utils/
│   └── api_client.py           # Lógica para consumir la API externa
├── views/
│   └── pdf_template.html       # Plantilla HTML para generar el PDF
├── README.md                   # Documentación del proyecto
└── venv/                       # Entorno virtual (excluido en .gitignore)
```

## Notas

- La API externa utilizada es la [Rick and Morty API](https://rickandmortyapi.com/).
- Asegúrate de que las dependencias del sistema necesarias para **xhtml2pdf** estén instaladas correctamente.
- Si tienes problemas con dependencias, consulta la documentación oficial de cada biblioteca.

