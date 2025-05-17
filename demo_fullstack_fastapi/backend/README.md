# Demo FastAPI con SQLModel con relaciones y validaciones

Este proyecto es una demostración de cómo usar **FastAPI** junto con **SQLModel** para construir una API RESTful con relaciones entre modelos, validaciones y documentación automática. Ahora está configurado para usar PostgreSQL como base de datos y soporta ejecución en contenedores Docker.

## Tecnologías Usadas

- **[FastAPI](https://fastapi.tiangolo.com/)**: Framework para construir APIs rápidas y modernas con Python.
- **[SQLModel](https://sqlmodel.tiangolo.com/)**: Biblioteca para trabajar con bases de datos SQL y modelos Pydantic.
- **[PostgreSQL](https://www.postgresql.org/)**: Base de datos relacional robusta y escalable.
- **[Docker](https://www.docker.com/)**: Plataforma para construir, compartir y ejecutar aplicaciones en contenedores.
- **[Uvicorn](https://www.uvicorn.org/)**: Servidor ASGI para ejecutar la aplicación FastAPI.

## Estructura de Carpetas

```
app/
├── db/
│   ├── database.py       # Configuración de la base de datos y funciones auxiliares
├── models/
│   ├── author.py         # Modelo Author con SQLModel
│   ├── entry.py          # Modelo Entry con SQLModel
├── crud/
│   ├── author.py         # Operaciones CRUD para Author
│   ├── entry.py          # Operaciones CRUD para Entry
├── routes/
│   ├── author.py         # Endpoints relacionados con Author
│   ├── entry.py          # Endpoints relacionados con Entry
├── main.py               # Punto de entrada principal de la aplicación
├── seeder.py             # Script para poblar la base de datos con datos iniciales
├── queries.sql           # Consultas SQL para crear y poblar la base de datos
├── Dockerfile            # Configuración para construir la imagen Docker
├── .env                  # Variables de entorno para configuración de la base de datos
└── README.md             # Documentación del proyecto
```

## Configuración del Proyecto

### Variables de Entorno

El archivo `.env` contiene las credenciales de la base de datos PostgreSQL. Ejemplo:

```properties
DB_USER=postgres
DB_PASSWORD=123456
DB_HOST=localhost
DB_PORT=5432
DB_NAME=postgres
```

### Cómo Ejecutar el Proyecto

#### 1. **Ejecutar Localmente**

1. **Crear un entorno virtual**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # En Windows: venv\Scripts\activate
   ```

2. **Instalar dependencias**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configurar la base de datos**:
   Asegúrate de que PostgreSQL esté instalado y ejecutándose. Crea la base de datos especificada en el archivo `.env`.

4. **Ejecutar el seeder**:
   Si deseas poblar la base de datos con datos iniciales, ejecuta:
   ```bash
   python seeder.py
   ```

5. **Ejecutar la aplicación**:
   ```bash
   python main.py
   ```

6. **Abrir la documentación interactiva**:
   - Swagger UI: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
   - Redoc: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

#### 2. **Ejecutar con Docker**

1. **Construir la imagen Docker**:
   ```bash
   docker build -t fastapi-app .
   ```

2. **Ejecutar el contenedor**:
   ```bash
   docker run -d -p 8000:8000 --env-file .env fastapi-app
   ```

3. **Acceder a la API**:
   - Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)
   - Redoc: [http://localhost:8000/redoc](http://localhost:8000/redoc)

## Consultas SQL

El archivo `queries.sql` contiene las consultas SQL necesarias para crear las tablas, insertar datos y realizar operaciones básicas en la base de datos.

### Ejemplo de Consultas

- Crear tablas:
  ```sql
  CREATE TABLE author (...);
  CREATE TABLE entry (...);
  ```

- Insertar datos:
  ```sql
  INSERT INTO author (name, email) VALUES ('Author One', 'author1@example.com');
  ```

- Consultar entradas por autor:
  ```sql
  SELECT entry.* 
  FROM entry
  JOIN author ON entry.author_id = author.id
  WHERE author.name = 'Author One';
  ```

## Notas Adicionales

- **Validaciones**:
  - El correo del autor (`email`) debe ser único.
  - El título de la entrada (`title`) debe ser único.
- **Relaciones**:
  - Cada entrada está asociada a un autor.
  - Los endpoints devuelven objetos completos con relaciones cargadas.
- **Excepciones**:
  - Manejo global de excepciones para errores inesperados.

---