# Practica FastAPI - Weather Report

Este proyecto es una demostración de cómo consumir una API externa del tiempo y generar reportes en diferentes formatos (Excel, CSV, PDF) utilizando **FastAPI**.

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

| Método | Endpoint                  | Descripción                              |
|--------|---------------------------|------------------------------------------|
| GET    | `/weather`                | Obtiene el tiempo de la API externa.     |
| GET    | `/weather/excel`          | Genera un archivo Excel con el tiempo.   |
| GET    | `/weather/csv`            | Genera un archivo CSV con el tiempo.     |
| GET    | `/weather/pdf`            | Genera un archivo PDF con el tiempo.     |

## Estructura del Proyecto

```
practica_weather/
│
├── main.py                     # Archivo principal con los endpoints
├── requirements.txt            # Dependencias del proyecto
├── utils/
│   └── api_weater.py           # Lógica para consumir la API externa
├── views/
│   └── pdf_template.html       # Plantilla HTML para generar el PDF
├── README.md                   # Documentación del proyecto
└── venv/                       # Entorno virtual (excluido en .gitignore)
```

## Notas

- La API externa utilizada es la es la de Open Meteo: [https://api.open-meteo.com/v1/forecast](https://api.open-meteo.com/v1/forecast)
- Asegúrate de que las dependencias del sistema necesarias para **xhtml2pdf** estén instaladas correctamente.
- Si tienes problemas con dependencias, consulta la documentación oficial de cada biblioteca.

