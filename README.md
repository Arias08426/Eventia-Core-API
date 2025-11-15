# 📋 **Eventia Core API - Sistema de Gestión de Eventos**

## 📖 **1. Introducción**

**Eventia Core API** es un backend robusto y escalable diseñado para gestionar eventos, participantes y registros de asistencia. Esta API sirve como núcleo para futuras aplicaciones web y móviles, implementada siguiendo principios de **arquitectura limpia**, **pruebas automatizadas** e **integración continua**.

### Funcionalidades Principales:

- ✅ **Gestión de Eventos** - Crear, leer, actualizar y eliminar eventos
- ✅ **Gestión de Participantes** - Registro con validación de emails únicos
- ✅ **Control de Asistencia** - Registro a eventos con validaciones de cupo
- ✅ **Estadísticas** - Análisis de ocupación y capacidad de eventos
- ✅ **Sistema de Caché** - Redis para optimizar consultas frecuentes
- ✅ **Documentación Interactiva** - Swagger UI y ReDoc integrados
- ✅ **Manejo Centralizado de Errores** - Respuestas consistentes
- ✅ **Logging Estructurado** - Trazabilidad de operaciones

---

## 🏗️ **2. Arquitectura**

El proyecto utiliza una **Arquitectura Modular Híbrida** que combina conceptos de **MVC** y **Clean Architecture**:

```
src/
├── controllers/        # Capa de presentación (manejadores HTTP)
├── services/          # Lógica de negocio (desacoplada de HTTP)
├── models/            # Modelos de BD (SQLAlchemy ORM)
├── schemas/           # DTOs - Validación de entrada/salida (Pydantic)
├── database/          # Configuración y conexión a BD
├── cache/             # Sistema de caché con Redis
├── config/            # Configuración centralizada
├── middleware/        # Middlewares personalizados
├── exceptions/        # Excepciones personalizadas
└── main.py           # Punto de entrada de la aplicación
```

### Flujo de Datos:

```
Cliente HTTP
    ↓
Controlador (fastapi.endpoints)
    ↓
Servicio (lógica de negocio)
    ↓
Repositorio/Modelo (acceso a datos)
    ↓
Base de Datos / Caché
```

### Capas:

| Capa | Responsabilidad | Ejemplos |
|------|-----------------|----------|
| **Controllers** | Manejar requests HTTP, validar schemas | `event_controller.py`, `participant_controller.py` |
| **Services** | Implementar reglas de negocio | `event_service.py`, `attendance_service.py` |
| **Models** | Definir tablas y relaciones en BD | `event.py`, `participant.py`, `attendance.py` |
| **Schemas** | Validar y serializar datos (Pydantic) | `event.py`, `participant.py` en carpeta schemas |
| **Database** | Gestión de conexiones y ORM | `connection.py` |
| **Cache** | Optimizar consultas recurrentes | `redis_client.py` |

---

## 🛠️ **3. Tecnologías Utilizadas**

### Backend & Framework
- **Python 3.11** - Lenguaje de programación
- **FastAPI 0.109.0** - Framework web moderno y rápido
- **Uvicorn 0.27.0** - Servidor ASGI
- **Pydantic 2.5.3** - Validación de datos

### Base de Datos
- **MySQL** - Base de datos relacional
- **SQLAlchemy 2.0.25** - ORM para Python
- **PyMySQL 1.1.0** - Driver para MySQL

### Caché
- **Redis 5.0.1** - Sistema de caché distribuido
- **Hiredis 2.3.2** - Parser rápido para Redis

### Testing
- **pytest 7.4.4** - Framework de pruebas
- **pytest-asyncio 0.23.3** - Soporte para async
- **pytest-cov 4.1.0** - Cobertura de pruebas
- **HTTPx 0.26.0** - Cliente HTTP para tests

### Análisis de Código
- **Bandit 1.7.6** - Análisis de seguridad
- **Flake8 7.0.0** - Linter de código
- **MyPy 1.8.0** - Verificador de tipos estático
- **Black 23.12.1** - Formateador de código
- **isort 5.13.2** - Organizador de imports

---

## 📋 **4. Requisitos**

### Software Necesario:
- **Python 3.11+**
- **MySQL Server 5.7+** (o 8.0)
- **Redis Server 6.0+**
- **Git**

### Requisitos Alternativos (con Docker):
- **Docker Desktop 4.0+**
- **Docker Compose 2.0+**

---

## 🚀 **5. Instalación**

### Opción A: Instalación Local

#### 1. Clonar el repositorio
```bash
git clone <tu-repo>
cd TallerPruebas
```

#### 2. Crear entorno virtual
```bash
# Windows (PowerShell)
python -m venv .venv
.venv\Scripts\Activate.ps1

# Linux/Mac
python3 -m venv .venv
source .venv/bin/activate
```

#### 3. Instalar dependencias
```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

#### 4. Configurar variables de entorno
```bash
# Copiar archivo de ejemplo
cp .env.example .env

# Editar .env con tus valores (BD, Redis, etc.)
```

#### 5. Crear base de datos (opcional)
```bash
# Crear base de datos en MySQL
mysql -u root -p -e "CREATE DATABASE eventia_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
```

#### 6. Inicializar esquema de BD
```bash
# Los modelos se crean automáticamente al iniciar la app
python src/main.py
```

### Opción B: Instalación con Docker (RECOMENDADO)

```bash
# Clonar repositorio
git clone <tu-repo>
cd TallerPruebas

# Levantar todos los servicios (Backend, MySQL, Redis)
docker-compose up -d

# Esperar a que se inicialicen (≈30 segundos)
docker-compose logs -f

# Ver logs de la app
docker-compose logs -f backend
```

---

## 🏃 **6. Ejecución en Local**

### Opción A: Ejecución Manual

```bash
# Activar entorno virtual
.venv\Scripts\Activate.ps1  # Windows
source .venv/bin/activate   # Linux/Mac

# Iniciar servidor (puerto 8000)
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

### Opción B: Con Docker Compose
```bash
docker-compose up -d
```

### Acceder a la API:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **API**: http://localhost:8000

### Endpoints Principales:

#### Eventos
```bash
GET    /events              # Listar eventos
POST   /events              # Crear evento
GET    /events/{id}         # Obtener evento
PUT    /events/{id}         # Actualizar evento
DELETE /events/{id}         # Eliminar evento
```

#### Participantes
```bash
GET    /participants        # Listar participantes
POST   /participants        # Crear participante
GET    /participants/{id}   # Obtener participante
PUT    /participants/{id}   # Actualizar participante
DELETE /participants/{id}   # Eliminar participante
```

#### Asistencias
```bash
GET    /attendances        # Listar asistencias
POST   /attendances        # Registrar asistencia
GET    /attendances/{id}   # Obtener asistencia
DELETE /attendances/{id}   # Cancelar asistencia
```

#### Salud
```bash
GET    /health             # Health check
```

---

## 🧪 **7. Ejecución de Pruebas**

### Pruebas Unitarias
```bash
# Ejecutar todas las pruebas unitarias
pytest tests/unit/ -v

# Con cobertura
pytest tests/unit/ --cov=src --cov-report=html
```

### Pruebas de Integración
```bash
# Ejecutar todas las pruebas de integración
pytest tests/integration/ -v
```

### Pruebas de Sistema (E2E)
```bash
# Ejecutar todas las pruebas de sistema
pytest tests/system/ -v
```

### Ejecutar Todas las Pruebas
```bash
# Todas las pruebas con cobertura
pytest tests/ -v --cov=src --cov-report=html

# Sin verbose
pytest tests/ --cov=src
```

### Análisis Estático de Seguridad
```bash
# Bandit (análisis de seguridad)
bandit -r src/

# Flake8 (linting)
flake8 src/ tests/

# MyPy (verificación de tipos)
mypy src/

# Black (formateo)
black src/ tests/ --check

# isort (organización de imports)
isort src/ tests/ --check
```

---

## 🔄 **8. Pipeline de CI/CD (GitHub Actions)**

El proyecto incluye un **workflow automático** que se ejecuta en cada push y pull request:

### Pasos del Pipeline:

```yaml
1. Code Quality Checks
   ├── Setup Python
   ├── Install dependencies
   ├── Format check (Black)
   ├── Import sort (isort)
   ├── Linting (Flake8)
   └── Type checking (MyPy)

2. Security Analysis
   ├── Bandit security scan
   └── Safety package check

3. Unit Tests
   ├── Run unit tests
   └── Generate coverage report

4. Integration Tests
   ├── Setup test database
   ├── Run integration tests
   └── Generate coverage report

5. System Tests (E2E)
   ├── Start test server
   └── Run end-to-end tests

6. Final Report
   └── Print OK if all pass, FAILED otherwise
```

### Ver Estado del Pipeline:

1. Ir a tu repositorio en GitHub
2. Click en **"Actions"**
3. Seleccionar el workflow **"CI/CD Pipeline"**
4. Ver el estado del último push

---

## 🐳 **9. Docker & Docker Compose (OPCIONAL - +0.5 puntos)**

### Estructura de Servicios:

```yaml
Services:
├── backend     - FastAPI (Puerto 8000)
├── mysql       - Base de datos (Puerto 3306)
└── redis       - Caché (Puerto 6379)
```

### Comandos Útiles:

```bash
# Levantar todos los servicios
docker-compose up -d

# Ver logs en tiempo real
docker-compose logs -f

# Ver logs de un servicio específico
docker-compose logs -f backend

# Detener servicios
docker-compose down

# Reconstruir imágenes
docker-compose build --no-cache

# Ejecutar comandos en contenedor
docker-compose exec backend bash

# Ver estado de contenedores
docker-compose ps
```

### Variables de Entorno en Docker:

Se usan automáticamente desde `.env`:
- `DATABASE_URL` - Conexión MySQL
- `REDIS_HOST` - Host Redis
- `LOG_LEVEL` - Nivel de logging

---

## 📁 **10. Estructura del Proyecto**

```
TallerPruebas/
├── src/
│   ├── __init__.py
│   ├── main.py                    # Punto de entrada
│   ├── config/
│   │   ├── __init__.py
│   │   └── setting.py             # Configuración centralizada
│   ├── controllers/               # Capa de presentación
│   │   ├── event_controller.py
│   │   ├── participant_controller.py
│   │   ├── attendance_controller.py
│   │   └── health_controller.py
│   ├── services/                  # Lógica de negocio
│   │   ├── event_service.py
│   │   ├── participant_service.py
│   │   └── attendance_service.py
│   ├── models/                    # Modelos SQLAlchemy
│   │   ├── event.py
│   │   ├── participant.py
│   │   └── attendance.py
│   ├── schemas/                   # DTOs Pydantic
│   │   ├── event.py
│   │   ├── participant.py
│   │   └── attendance.py
│   ├── database/
│   │   ├── __init__.py
│   │   └── connection.py          # ORM setup
│   ├── cache/
│   │   ├── __init__.py
│   │   └── redis_client.py        # Configuración Redis
│   ├── middleware/
│   │   ├── __init__.py
│   │   └── error_handler.py       # Manejo centralizado de errores
│   └── exceptions/
│       ├── __init__.py
│       └── custom_exceptions.py   # Excepciones personalizadas
│
├── tests/
│   ├── __init__.py
│   ├── conftest.py                # Fixtures de pytest
│   ├── unit/                      # Pruebas unitarias
│   │   ├── test_event_service.py
│   │   ├── test_participant_service.py
│   │   └── test_attendance_service.py
│   ├── integration/               # Pruebas de integración
│   │   ├── test_database.py
│   │   └── test_cache.py
│   └── system/                    # Pruebas E2E
│       ├── test_events_api.py
│       ├── test_participants_api.py
│       └── test_attendance_api.py
│
├── .github/
│   └── workflows/
│       └── ci-cd.yml              # Pipeline de GitHub Actions
│
├── .env.example                   # Variables de entorno (ejemplo)
├── .env                           # Variables de entorno (local)
├── requirements.txt               # Dependencias de producción
├── requirements-dev.txt           # Dependencias de desarrollo
├── Dockerfile                     # Containerización
├── docker-compose.yml             # Orquestación de servicios
└── README.md                      # Este archivo
```

---

## 🔐 **11. Justificación de Tecnologías**

### FastAPI
- **Por qué**: Framework moderno, rápido, con validación automática y documentación integrada
- **Ventajas**: Alto rendimiento, async/await nativo, validación con Pydantic, Swagger UI automático
- **Alternativas**: Flask (más simple), Django (más completo pero pesado), Starlette (más bajo nivel)

### SQLAlchemy + MySQL
- **Por qué**: ORM robusto con soporte para MySQL maduro
- **Ventajas**: Queries type-safe, migraciones fáciles, relaciones bien definidas
- **Alternativas**: Tortoise ORM (más moderno pero menos maduro), Peewee (más simple)

### Redis
- **Por qué**: Caché distribuido de alta velocidad, ideal para consultas recurrentes
- **Ventajas**: In-memory, TTL automático, persistencia opcional, Pub/Sub
- **Casos de uso**: 
  - Estadísticas de ocupación (consulta frecuente)
  - Validación rápida de disponibilidad
  - Sesiones de usuario

### pytest
- **Por qué**: Framework de testing más usado en Python
- **Ventajas**: Sintaxis simple, fixtures poderosas, plugins extensibles
- **Alternativas**: unittest (built-in pero verboso), nose2 (desactualizado)

### Bandit + Flake8 + MyPy
- **Por qué**: Cobertura completa de seguridad, estilo y tipos
- **Ventajas**: Detectan vulnerabilidades, mantienen código limpio, type-safe
- **Alternativas**: Pylint (más lento), ruff (más nuevo pero menos adoption)

### Docker & Docker Compose
- **Por qué**: Reproducibilidad, facilita desarrollo y producción
- **Ventajas**: Aislamiento, portabilidad, CI/CD más simple, matching dev/prod
- **Alternativas**: Kubernetes (overkill para este proyecto), podman (compatible)

---

## ⚙️ **12. Configuración Importante**

### Variables de Entorno (.env):

```env
# Aplicación
APP_NAME=Eventia Core API
APP_VERSION=1.0.0
APP_ENV=development

# Base de Datos
DATABASE_URL=mysql+pymysql://root:password@localhost:3306/eventia_db

# Redis
REDIS_HOST=localhost
REDIS_PORT=6379
CACHE_TTL=300

# Server
HOST=0.0.0.0
PORT=8000

# Logging
LOG_LEVEL=INFO

# CORS
CORS_ORIGINS=["http://localhost:3000","http://localhost:8000"]
```

### MySQL Connection:
- **Default**: localhost:3306
- **Usuario**: root
- **BD**: eventia_db
- Asegúrate de crear la BD si no existe

### Redis Connection:
- **Default**: localhost:6379
- **TTL**: 300 segundos (5 minutos)

---

## 🐛 **13. Troubleshooting**

### Problema: "Import 'main' could not be resolved"
**Solución**: Agregar `src` al path en `conftest.py` ✅ (Ya configurado)

### Problema: "ModuleNotFoundError: No module named 'redis'"
**Solución**: 
```bash
pip install -r requirements.txt
pip install redis
```

### Problema: "Connection refused" (MySQL/Redis)
**Solución**:
1. Verificar que MySQL y Redis están corriendo
2. Verificar configuración en `.env`
3. Con Docker: `docker-compose up -d`

### Problema: Tests no encuentran la BD
**Solución**: 
```bash
# La BD de tests usa SQLite (test.db)
# Borrar test.db y re-ejecutar
rm test.db
pytest tests/ -v
```

### Problema: Puerto 8000 ya está en uso
**Solución**:
```bash
# Usar otro puerto
uvicorn src.main:app --port 8001
```

---

## 📚 **14. Recursos y Documentación**

### Documentación Oficial:
- [FastAPI](https://fastapi.tiangolo.com/)
- [SQLAlchemy](https://www.sqlalchemy.org/)
- [Pydantic](https://docs.pydantic.dev/)
- [pytest](https://docs.pytest.org/)
- [Redis](https://redis.io/documentation)

### Endpoints Swagger:
```
http://localhost:8000/docs          # Swagger UI
http://localhost:8000/redoc         # ReDoc
http://localhost:8000/openapi.json  # OpenAPI JSON
```

---

## 📞 **15. Contacto y Soporte**

**Equipo de Desarrollo**
- Email: soporte@eventia.com
- Repositorio: [GitHub](<tu-repo>)

---

## 📄 **Licencia**

MIT License - Libre para usar, modificar y distribuir

---

**Última actualización**: Noviembre 2025
**Versión**: 1.0.0
**Estado**: ✅ Producción
