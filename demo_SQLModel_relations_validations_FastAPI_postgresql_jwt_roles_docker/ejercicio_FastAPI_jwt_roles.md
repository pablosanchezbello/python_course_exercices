# Ejercicios de Mejora con FastAPI, SQLModel y JWT

Ejercicios prácticos sobre la demo montada con FastAPI, SQLModel y autenticación basada en JWT.

---

## Ejercicio 1: Agregar un Campo de Biografía a los Autores

### Descripción
Añade un nuevo campo `biography` al modelo `Author` para almacenar una breve descripción del autor. Este campo debe ser opcional y permitir un máximo de 500 caracteres.

### Pasos
1. Modifica el modelo `Author` en `models/author.py` para incluir el nuevo campo.
2. Actualiza las migraciones de la base de datos para reflejar este cambio.
3. Asegúrate de que el nuevo campo sea retornado en las respuestas de los endpoints relacionados con autores.
4. Prueba el cambio creando y actualizando autores con el nuevo campo.

---

## Ejercicio 2: Añadir un Endpoint para Cambiar Contraseñas

### Descripción
Crea un nuevo endpoint en `routes/auth.py` que permita a los usuarios cambiar su contraseña. Este endpoint debe estar protegido y requerir que el usuario proporcione su contraseña actual y la nueva.

### Pasos
1. Añade un nuevo método en `auth/dependencies.py` para verificar la contraseña actual del usuario.
2. Crea el endpoint en `routes/auth.py` para manejar la lógica de cambio de contraseña.
3. Asegúrate de que la nueva contraseña sea hasheada antes de guardarla en la base de datos.
4. Prueba el endpoint con diferentes casos (contraseña actual incorrecta, nueva contraseña válida, etc.).

---

## Ejercicio 3: Añadir Roles Personalizados

### Descripción
Añade un nuevo rol llamado `editor` que tenga permisos para crear y actualizar entradas, pero no para eliminarlas.

### Pasos
1. Modifica la lógica de roles en `auth/dependencies.py` para incluir el nuevo rol.
2. Actualiza los endpoints en `routes/entry.py` para permitir que los usuarios con el rol `editor` puedan acceder a las operaciones permitidas.
3. Prueba los cambios creando un usuario con el rol `editor` y verificando sus permisos.

---

## Ejercicio 4: Externalizar la Clave Secreta en un Archivo `.env`

### Descripción
Modifica la aplicación para que la clave secreta utilizada para firmar los tokens JWT se cargue desde un archivo `.env`.

### Pasos
1. Añade una nueva variable `SECRET_KEY` en el archivo `.env`.
2. Modifica `auth/jwt.py` para cargar la clave secreta desde las variables de entorno.
3. Asegúrate de que la aplicación funcione correctamente después del cambio.
4. Prueba generando y verificando tokens JWT con la nueva configuración.

---

## Ejercicio 5: Configurar Tiempo de Expiración Dinámico para los Tokens JWT

### Descripción
Modifica la lógica de generación de tokens JWT para que el tiempo de expiración sea dinámico según el rol del usuario. Por ejemplo:
- `admin`: 60 minutos.
- `editor`: 45 minutos.
- `user`: 30 minutos.

### Pasos
1. Modifica la función `create_access_token` en `auth/jwt.py` para calcular el tiempo de expiración según el rol.
2. Asegúrate de que los tokens generados tengan el tiempo de expiración correcto.
3. Prueba el cambio iniciando sesión con usuarios de diferentes roles y verificando el tiempo de expiración en los tokens.

---

## Ejercicio 6: Implementar Revocación de Tokens

### Descripción
Añade un endpoint para listar los tokens revocados y permite a los administradores revocar manualmente un token específico.

### Pasos
1. Crea un nuevo endpoint en `routes/auth.py` para listar los tokens revocados.
2. Añade un endpoint para revocar manualmente un token, accesible solo para administradores.
3. Asegúrate de que los tokens revocados se almacenen correctamente en el archivo `revoked_tokens.txt`.
4. Prueba los endpoints con diferentes casos.

---

## Ejercicio 7: Añadir Filtros y Paginación a las Entradas

### Descripción
Añade soporte para filtros y paginación en el endpoint de lectura de entradas (`/api/entries`).

### Pasos
1. Modifica el endpoint `read_all` en `routes/entry.py` para aceptar parámetros de consulta (`query params`) como `author_name`, `title` y `page`.
2. Implementa la lógica de paginación utilizando `limit` y `offset`.
3. Prueba los cambios con diferentes combinaciones de filtros y paginación.

---

## Ejercicio 8: Añadir Validación de Contraseñas Fuertes

### Descripción
Implementa una validación para asegurarte de que las contraseñas cumplan con ciertos requisitos de seguridad (por ejemplo, longitud mínima, caracteres especiales, etc.).

### Pasos
1. Modifica la lógica de registro en `routes/auth.py` para incluir la validación de contraseñas.
2. Añade una función de validación en `auth/hashing.py` para verificar los requisitos de seguridad.
3. Prueba el cambio registrando usuarios con contraseñas válidas e inválidas.

---

## Ejercicio 9: Añadir Soporte para Recuperación de Contraseña con Expiración de Token

### Descripción
Modifica el flujo de recuperación de contraseña para que el token de recuperación expire después de un tiempo configurable.

### Pasos
1. Modifica la función `create_access_token` en `auth/jwt.py` para aceptar un tiempo de expiración personalizado.
2. Asegúrate de que el token de recuperación expire correctamente.
3. Prueba el flujo de recuperación de contraseña con tokens válidos y expirados.

---

## Ejercicio 10: Añadir Logs de Auditoría

### Descripción
Añade un sistema de logs para registrar las acciones importantes, como inicio de sesión, cierre de sesión, creación de entradas, etc.

### Pasos
1. Configura un sistema de logs en `main.py` utilizando la biblioteca `logging`.
2. Añade registros en los endpoints clave, como `login`, `logout`, `create_entry`, etc.
3. Asegúrate de que los logs incluyan información relevante, como el usuario y la acción realizada.
4. Prueba los cambios verificando los logs generados.


