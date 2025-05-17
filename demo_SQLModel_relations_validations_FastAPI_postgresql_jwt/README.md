# Demo FastAPI con SQLModel, JWT y PostgreSQL

Este proyecto es una demostración de cómo usar **FastAPI** junto con **SQLModel** para construir una API RESTful con autenticación basada en JWT, relaciones entre modelos, validaciones y documentación automática. Está configurado para usar PostgreSQL como base de datos.

## Tecnologías Usadas

- **[FastAPI](https://fastapi.tiangolo.com/)**: Framework para construir APIs rápidas y modernas con Python.
- **[SQLModel](https://sqlmodel.tiangolo.com/)**: Biblioteca para trabajar con bases de datos SQL y modelos Pydantic.
- **[PostgreSQL](https://www.postgresql.org/)**: Base de datos relacional robusta y escalable.
- **[Uvicorn](https://www.uvicorn.org/)**: Servidor ASGI para ejecutar la aplicación FastAPI.
- **[JWT](https://jwt.io/)**: Autenticación basada en tokens JSON Web Tokens.

## Estructura de Carpetas

```
app/
├── db/
│   ├── database.py       # Configuración de la base de datos y funciones auxiliares
├── models/
│   ├── author.py         # Modelo Author con SQLModel
│   ├── entry.py          # Modelo Entry con SQLModel
│   ├── user.py           # Modelo User con SQLModel
├── crud/
│   ├── author.py         # Operaciones CRUD para Author
│   ├── entry.py          # Operaciones CRUD para Entry
├── routes/
│   ├── author.py         # Endpoints relacionados con Author
│   ├── entry.py          # Endpoints relacionados con Entry
│   ├── auth.py           # Endpoints relacionados con autenticación
├── auth/
│   ├── jwt.py            # Funciones para manejo de JWT y tokens revocados
│   ├── hashing.py        # Funciones para hashear y verificar contraseñas
│   ├── dependencies.py   # Dependencias comunes para autenticación
├── main.py               # Punto de entrada principal de la aplicación
├── seeder.py             # Script para poblar la base de datos con datos iniciales
├── queries.sql           # Consultas SQL para crear y poblar la base de datos
├── revoked_tokens.txt    # Archivo para almacenar tokens revocados
├── .env                  # Variables de entorno para configuración de la base de datos
└── README.md             # Documentación del proyecto
```

## Funcionalidades

### 1. **Autenticación con JWT**
- **Registro de usuarios**: Endpoint `/api/auth/register` para registrar nuevos usuarios.
- **Inicio de sesión**: Endpoint `/api/auth/login` para obtener un token JWT.
- **Cierre de sesión**: Endpoint `/api/auth/logout` para revocar tokens.
- **Protección de rutas**: Uso de JWT para proteger rutas que no sean de tipo `GET`.
- **Manejo de tokens revocados**: Los tokens revocados se almacenan en el archivo `revoked_tokens.txt`.

### 2. **Gestión de Autores**
- **Crear autores**: Endpoint `POST /api/authors/` para crear nuevos autores.
- **Leer autores**: Endpoints `GET /api/authors/` y `GET /api/authors/{id}` para obtener información de autores.
- **Actualizar autores**: Endpoints `PUT /api/authors/{id}` y `PUT /api/authors/name/{name}` para actualizar información de autores.
- **Eliminar autores**: Endpoints `DELETE /api/authors/{id}` y `DELETE /api/authors/name/{name}` para eliminar autores.

### 3. **Gestión de Entries**
- **Crear Entries**: Endpoint `POST /api/entries/` para crear nuevas Entries asociadas a un autor.
- **Leer Entries**: Endpoints `GET /api/entries/`, `GET /api/entries/{id}`, `GET /api/entries/title/{title}` y `GET /api/entries/author/{author_name}` para obtener información de Entries.
- **Actualizar Entries**: Endpoints `PUT /api/entries/{id}` y `PUT /api/entries/title/{title}` para actualizar información de Entries.
- **Eliminar Entries**: Endpoints `DELETE /api/entries/{id}` y `DELETE /api/entries/title/{title}` para eliminar Entries.

### 4. **Base de Datos**
- **PostgreSQL**: Configuración para usar PostgreSQL como base de datos.
- **Migraciones manuales**: Archivo `queries.sql` para crear y poblar la base de datos.
- **Seeder**: Script `seeder.py` para poblar la base de datos con datos iniciales.

### 5. **Documentación Automática**
- **Swagger UI**: Disponible en [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).
- **Redoc**: Disponible en [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc).

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

- Consultar Entries por autor:
  ```sql
  SELECT entry.* 
  FROM entry
  JOIN author ON entry.author_id = author.id
  WHERE author.name = 'Author One';
  ```

## Notas Adicionales

- **Validaciones**:
  - El correo del autor (`email`) debe ser único.
  - El título de la Entry (`title`) debe ser único.
- **Relaciones**:
  - Cada Entry está asociada a un autor.
  - Los endpoints devuelven objetos completos con relaciones cargadas.
- **Excepciones**:
  - Manejo global de excepciones para errores inesperados.

---