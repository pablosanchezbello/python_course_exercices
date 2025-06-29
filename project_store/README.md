# Project Store

Proyecto Project Store, proyecto final compuesto de backend y frontend

## Instrucciones de Uso

### 1. Crear un entorno virtual
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

### 2. Compilar proyecto general
```bash
docker compose up --build -d
```

### 3. Ejecutar seeder
```bash
docker exec -it project_store-backend-1 bash
```
```bash
python3 seeder.py
```

### 4. Acceder a los logs del backend
```bash
docker logs project_store-backend-1 -f
```

## Estructura del Proyecto

```
project_store
│
├── backend/                    # Proyecto backend
├── frontend/                   # Proyecto frontend
├── .env                        # Environment configuration file
├── docker-compose.yml          # Docker compose file to build full project
└── README.md                   # Documentación del proyecto
```

## DEMO
![Video demo](https://github.com/pablosanchezbello/python_course_exercices/blob/main/project_store/demo.gif)

