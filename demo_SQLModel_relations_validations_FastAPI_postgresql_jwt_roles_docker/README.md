# Demo FastAPI con SQLModel con relaciones, validaciones y autenticación basada en roles

Este proyecto es una demostración de cómo usar **FastAPI** junto con **SQLModel** para construir una API RESTful con relaciones entre modelos, validaciones, autenticación basada en JWT y control de acceso por roles. Está configurado para usar PostgreSQL como base de datos.

## Tecnologías Usadas

- **[FastAPI](https://fastapi.tiangolo.com/)**: Framework para construir APIs rápidas y modernas con Python.
- **[SQLModel](https://sqlmodel.tiangolo.com/)**: Biblioteca para trabajar con bases de datos SQL y modelos Pydantic.
- **[PostgreSQL](https://www.postgresql.org/)**: Base de datos relacional robusta y escalable.
- **[Uvicorn](https://www.uvicorn.org/)**: Servidor ASGI para ejecutar la aplicación FastAPI.
- **[Python-JOSE](https://python-jose.readthedocs.io/)**: Biblioteca para manejar JWT.
- **[Bcrypt](https://pypi.org/project/bcrypt/)**: Biblioteca para hashear y verificar contraseñas.
- **[Jinja2](https://jinja.palletsprojects.com/)**: Motor de plantillas para renderizar vistas HTML.

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
│   ├── jwt.py            # Funciones para manejo de JWT
│   ├── hashing.py        # Funciones para hashear y verificar contraseñas
│   ├── dependencies.py   # Dependencias para autenticación y roles
├── templates/            # Plantillas HTML para vistas SSR
│   ├── forgot_password.html
├── main.py               # Punto de entrada principal de la aplicación
├── seeder.py             # Script para poblar la base de datos con datos iniciales
├── queries.sql           # Consultas SQL para crear y poblar la base de datos
├── .env                  # Variables de entorno para configuración local y Docker
├── Dockerfile            # Archivo Docker para construir la imagen de la aplicación
├── docker-compose.yml    # Archivo Docker Compose para orquestar los servicios
└── README.md             # Documentación del proyecto
```

## Configuración del Proyecto

### Variables de Entorno

El proyecto utiliza un único archivo `.env` para configuraciones tanto locales como en Docker. 

Ejemplo de `.env`:
```properties
# Configuración común
DB_USER=postgres
DB_PASSWORD=123456
DB_PORT=5432
DB_NAME=postgres
SECRET_KEY=your_secret_key
REFRESH_SECRET_KEY=your_refresh_secret_key

# Configuración local
DB_HOST=localhost

# Configuración para Docker (sobrescribir en docker-compose.yml)
# DB_HOST=db
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

#### 2. **Ejecución con Docker**

### Requisitos

- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)

### Pasos para Ejecutar

1. **Construir y levantar los servicios**:
   ```bash
   docker-compose up --build -d
   ```

2. **Acceder a la aplicación**:
   - Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)
   - Redoc: [http://localhost:8000/redoc](http://localhost:8000/redoc)

3. **Parar los servicios**:
   ```bash
   docker-compose down
   ```

### Cómo Ejecutar el Seeder

Si deseas poblar la base de datos con datos iniciales, puedes ejecutar el script `seeder.py` de las siguientes maneras:

#### Localmente

1. Asegúrate de que la base de datos esté configurada y en ejecución.
2. Ejecuta el siguiente comando:
   ```bash
   python seeder.py
   ```

#### Con Docker

1. Asegúrate de que los servicios estén levantados con Docker Compose:
   ```bash
   docker-compose up -d
   ```

2. Ejecuta el seeder dentro del contenedor de la aplicación:
   ```bash
   docker-compose exec app python seeder.py
   ```

Esto poblará la base de datos con los datos iniciales definidos en el script `seeder.py`.

### Notas

- Los datos de la base de datos se almacenan en un volumen llamado `postgres_data`, por lo que no se perderán al reiniciar los contenedores.
- Puedes modificar las variables de entorno en el archivo `.env` según sea necesario.

## Funcionalidades

### Sistema de Roles y Autenticación con JWT

Este proyecto incluye un sistema de autenticación basado en JWT (JSON Web Tokens) y roles (`admin` y `user`). A continuación, se explica cómo usarlo:

#### Roles

- **Admin**: Puede realizar todas las operaciones (`GET`, `POST`, `PUT`, `DELETE`) en todos los endpoints.
- **User**: Puede realizar operaciones `GET` en todos los endpoints protegidos.

#### Protección de Rutas

- Todas las rutas `GET` de los módulos `author` y `entry` están protegidas con JWT. Tanto los usuarios con rol `user` como `admin` pueden acceder a estas rutas.
- Las rutas `POST`, `PUT` y `DELETE` están restringidas únicamente a usuarios con rol `admin`.

#### Registro de Usuarios

Para registrar un nuevo usuario, utiliza el endpoint `/api/auth/register`. Este endpoint espera un objeto JSON con los campos `username`, `email`, `password` y opcionalmente `role` (por defecto es `user`).

#### Inicio de Sesión

Para iniciar sesión y obtener un token JWT, utiliza el endpoint `/api/auth/login`. Este endpoint espera los campos `username` y `password`.

#### Renovación de Tokens

El endpoint `/api/auth/refresh` permite obtener un nuevo `access_token` utilizando un `refresh_token` válido.

#### Cierre de Sesión

El endpoint `/api/auth/logout` permite cerrar sesión y revocar el token de acceso. Los tokens revocados se almacenan en un archivo llamado `revoked_tokens.txt` para evitar su reutilización. Este archivo se encuentra en la raíz del proyecto y se carga al iniciar la aplicación.

---

### Recuperación de Contraseña

El proyecto incluye un flujo para la recuperación de contraseñas:

1. **Solicitar recuperación**:
   - Endpoint: `/api/auth/forgot-password`
   - Método: `POST`
   - Envía un token de recuperación al cliente.

2. **Restablecer contraseña**:
   - Endpoint: `/api/auth/reset-password`
   - Método: `POST`
   - Permite al usuario establecer una nueva contraseña utilizando el token de recuperación.

---

### Operaciones CRUD

#### Autores (`/api/authors`)

- **Crear Autor**: Solo accesible para `admin`.
- **Leer Autores**: Accesible para todos los usuarios autenticados.
- **Actualizar Autor**: Solo accesible para `admin`.
- **Eliminar Autor**: Solo accesible para `admin`.

#### Entradas (`/api/entries`)

- **Crear Entrada**: Solo accesible para `admin`.
- **Leer Entradas**: Accesible para todos los usuarios autenticados.
- **Actualizar Entrada**: Solo accesible para `admin`.
- **Eliminar Entrada**: Solo accesible para `admin`.

---

### Consultas SQL

El archivo `queries.sql` contiene las consultas SQL necesarias para crear las tablas, insertar datos y realizar operaciones básicas en la base de datos.

---

### Notas Adicionales

- **Validaciones**:
  - El correo del autor (`email`) debe ser único.
  - El título de la entrada (`title`) debe ser único.
- **Relaciones**:
  - Cada entrada está asociada a un autor.
  - Los endpoints devuelven objetos completos con relaciones cargadas.
- **Excepciones**:
  - Manejo global de excepciones para errores inesperados.

---