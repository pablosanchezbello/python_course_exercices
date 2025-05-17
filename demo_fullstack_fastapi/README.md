# Fullstack Application: FastAPI + React

Este proyecto es una aplicación fullstack que utiliza **FastAPI** para el backend, **React** para el frontend y **PostgreSQL** como base de datos. La aplicación está dockerizada para facilitar su despliegue y ejecución.

## Tecnologías utilizadas

- **Backend**: FastAPI (Python)
- **Frontend**: React (JavaScript)
- **Base de datos**: PostgreSQL
- **Docker**: Para contenerización y orquestación
- **Docker Compose**: Para levantar todos los servicios con un solo comando

## Estructura del proyecto

```
.
├── backend/          # Código del backend (FastAPI)
│   ├── Dockerfile    # Dockerfile para el backend
│   ├── main.py       # Punto de entrada de la API
│   └── ...           # Otros archivos relacionados con el backend
├── frontend/         # Código del frontend (React)
│   ├── Dockerfile    # Dockerfile para el frontend
│   ├── src/          # Código fuente de React
│   └── ...           # Otros archivos relacionados con el frontend
├── docker-compose.yml # Archivo para orquestar los contenedores
└── README.md         # Documentación del proyecto
```

## Requisitos previos

- Tener instalado **Docker** y **Docker Compose** en tu máquina.

## Cómo ejecutar el proyecto

1. Construye y levanta los contenedores con Docker Compose:
   ```bash
   docker-compose up --build -d
   ```

2. Accede a los servicios:
   - **Frontend**: [http://localhost:3000](http://localhost:3000)  
     El frontend está disponible en esta URL y sirve la aplicación React.
   - **Backend**: [http://localhost:8000](http://localhost:8000)  
     El backend está disponible en esta URL y expone la API REST.
   - **Documentación de la API** (Swagger): [http://localhost:8000/docs](http://localhost:8000/docs)

## Cargar datos iniciales (Seeder)

Para cargar datos iniciales en la base de datos utilizando el seeder, sigue estos pasos:

1. Accede al contenedor del backend:
   ```bash
   docker-compose exec backend bash
   ```

2. Ejecuta el script del seeder:
   ```bash
   python seeder.py
   ```

Esto eliminará las tablas existentes, las recreará y cargará los datos iniciales definidos en el archivo `seeder.py`.

## Servicios

### Backend
El backend está desarrollado con **FastAPI** y expone una API REST para gestionar autores y entradas. Se conecta a una base de datos PostgreSQL para almacenar los datos.

### Frontend
El frontend está desarrollado con **React** y permite interactuar con la API para realizar operaciones CRUD sobre las entradas y autores.

### Base de datos
Se utiliza **PostgreSQL** como base de datos relacional. Los datos se persisten en un volumen Docker para mantenerlos entre reinicios de los contenedores.

## Comandos útiles

- **Detener los contenedores**:
  ```bash
  docker-compose down
  ```

- **Reconstruir los contenedores**:
  ```bash
  docker-compose up --build -d
  ```

- **Ver los logs**:
  ```bash
  docker-compose logs -f
  ```

## Notas

- Asegúrate de que los puertos `3000`, `8000` y `5432` estén libres en tu máquina antes de ejecutar el proyecto.
- Si necesitas cambiar las credenciales de la base de datos, edita el archivo `docker-compose.yml` en la sección del servicio `db`
