# Eventia Core API

Sistema de gestión de eventos RESTful con arquitectura MVC, pruebas automatizadas e integración continua.

## Descripción

API backend para administrar eventos, participantes y registros de asistencia. Construida con FastAPI, SQLAlchemy, MySQL y Redis con pipeline CI/CD en GitHub Actions.

---

## Arquitectura

**Patrón:** MVC (Model-View-Controller)

```
src/
  ├── models/                 # Modelos SQLAlchemy ORM
  │   ├── event.py
  │   ├── participant.py
  │   └── attendance.py
  ├── controllers/            # Controladores FastAPI
  │   ├── event_controller.py
  │   ├── participant_controller.py
  │   ├── attendance_controller.py
  │   └── health_controller.py
  ├── services/               # Lógica de negocio
  │   ├── event_service.py
  │   ├── participant_service.py
  │   └── attendance_service.py
  ├── schemas/                # Validación Pydantic
  │   ├── event.py
  │   ├── participant.py
  │   └── attendance.py
  ├── database/               # Conexión y sesiones
  │   └── connection.py
  ├── cache/                  # Redis client
  │   └── redis_client.py
  ├── config/                 # Configuración
  │   └── setting.py
  ├── exceptions/             # Excepciones personalizadas
  │   └── custom_exceptions.py
  ├── middleware/             # Manejo global de errores
  │   └── error_handler.py
  └── main.py                 # Punto de entrada

tests/
  ├── unit/                   # Pruebas unitarias (27)
  │   ├── test_event_service.py
  │   ├── test_participant_service.py
  │   └── test_attendance_service.py
  ├── integration/            # Pruebas de integración (7)
  │   ├── test_database.py
  │   └── test_cache.py
  └── system/                 # Pruebas E2E (25)
      ├── test_events_api.py
      ├── test_participants_api.py
      └── test_attendance_api.py
```

---

## Stack Tecnológico

| Componente | Tecnología | Versión |
|-----------|-----------|---------|
| Lenguaje | Python | 3.11 |
| Framework | FastAPI | 0.109.0 |
| ORM | SQLAlchemy | 2.0.25 |
| Base de Datos | MySQL | 8.0 |
| Caché | Redis | 7-alpine |
| Validación | Pydantic | 2.5.3 |
| Testing | pytest | 7.4.4 |

---

## Requisitos Previos

- Python 3.11+
- MySQL 8.0 (local o Docker)
- Redis 7+ (Docker recomendado)
- Git

---

## Instalación

### 1. Clonar repositorio

```bash
git clone https://github.com/Arias08426/Eventia-Core-API.git
cd "Eventia Core API"
```

### 2. Crear entorno virtual

```bash
# Windows
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# Linux/Mac
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Instalar dependencias

```bash
# Dependencias de producción
pip install -r requirements.txt

# Dependencias de desarrollo (testing, quality, security)
pip install -r requirements-dev.txt
```

### 4. Configurar variables de entorno

Crear archivo `.env` en la raíz del proyecto:

```env
APP_ENV=development
DATABASE_URL=mysql+pymysql://eventia:eventia@localhost:3306/eventia
REDIS_HOST=localhost
REDIS_PORT=6379
CACHE_TTL=3600
CORS_ORIGINS=["http://localhost:3000","http://localhost:5173"]
```

---

## Ejecución Local

### Opción 1: Con Docker Compose (Recomendado)

```bash
# Levantar API + MySQL + Redis
docker-compose up -d

# Verificar servicios
docker ps

# API: http://localhost:8000
```

### Opción 2: Servicios Locales (Linux/Mac/Windows con XAMPP)

```bash
# Terminal 1: Inicializar base de datos
python -c "from src.database.connection import init_db; init_db()"

# Terminal 2: Ejecutar API
python -m uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

**Acceso:**
- API: http://localhost:8000
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
- Health: http://localhost:8000/health

---

## Pruebas Automatizadas

### Ejecutar todas las pruebas

```bash
pytest -v
```

### Por categoría

```bash
pytest tests/unit/ -v           # Pruebas unitarias (27)
pytest tests/integration/ -v    # Pruebas de integración (7)
pytest tests/system/ -v         # Pruebas E2E (25)
```

### Con cobertura

```bash
pytest --cov=src --cov-report=html
```

**Resultado esperado:** 66 tests pasando

---

## Calidad de Código

```bash
# Formateo con Black
black src/ tests/

# Organizar imports con isort
isort src/ tests/

# Lint con Flake8
flake8 src/ tests/ --max-line-length=100

# Análisis de seguridad con Bandit
bandit -r src/

# Verificar dependencias con Safety
safety check
```

---

## Endpoints Principales

### Eventos
- `POST /events` - Crear evento
- `GET /events` - Listar eventos
- `GET /events/{id}` - Obtener evento
- `PUT /events/{id}` - Actualizar evento
- `DELETE /events/{id}` - Eliminar evento
- `GET /events/{id}/statistics` - Estadísticas (caché)

### Participantes
- `POST /participants` - Registrar participante
- `GET /participants` - Listar participantes
- `GET /participants/{id}` - Obtener participante
- `PUT /participants/{id}` - Actualizar participante
- `DELETE /participants/{id}` - Eliminar participante

### Asistencia
- `POST /attendance` - Registrar asistencia
- `DELETE /attendance/{id}` - Cancelar asistencia
- `GET /attendance/event/{event_id}` - Asistencias por evento
- `GET /attendance/participant/{participant_id}` - Asistencias por participante

### Salud
- `GET /health` - Health check del sistema

---

## Pipeline CI/CD

**GitHub Actions** ejecuta automáticamente en cada push/pull request:

1. **Code Quality** - Black, isort, Flake8
2. **Security Analysis** - Bandit, Safety
3. **Unit Tests** - pytest
4. **Integration Tests** - pytest
5. **System Tests** - pytest

Ver `.github/workflows/ci-cd.yml` para detalles.

---

## Características

✅ Arquitectura MVC limpia  
✅ API RESTful con manejo centralizado de errores  
✅ Base de datos MySQL con SQLAlchemy ORM  
✅ Caché Redis para consultas frecuentes  
✅ 66 pruebas automatizadas  
✅ Análisis de seguridad y calidad  
✅ CI/CD con GitHub Actions  
✅ Docker & Docker Compose  

---

## Notas

- En tests locales se usa SQLite automáticamente
- MySQL es requerida en CI/CD
- Redis es opcional (tests se saltan si no está disponible)
- Middleware centralizado maneja todos los errores
