# Eventia Core API 🎯

Plataforma REST API para gestión de eventos y participantes construida con **FastAPI**, **SQLAlchemy** y **Redis**.

## 🏗️ Arquitectura MVC

```
Eventia Core API (MVC)
├── Models          → SQLAlchemy ORM (Event, Participant, Attendance)
├── Controllers     → FastAPI endpoints (HTTP request handlers)
└── Services        → Lógica de negocio (validaciones, reglas, caché)
```

### Capas del Proyecto

| Capa | Responsabilidad | Carpeta |
|------|-----------------|---------|
| **Models** | Entidades de BD | `src/models/` |
| **Controllers** | Rutas HTTP | `src/controllers/` |
| **Services** | Lógica de negocio | `src/services/` |
| **Schemas** | Validación Pydantic | `src/schemas/` |
| **Database** | Conexión ORM | `src/database/` |
| **Cache** | Redis | `src/cache/` |
| **Config** | Configuración app | `src/config/` |
| **Middleware** | Error handling | `src/middleware/` |

## 📋 Requisitos Previos

- Python 3.11+
- MySQL 8.0+
- Redis 7.0+
- pip (Python package manager)

## 🚀 Instalación

### 1. Clonar repositorio
```bash
git clone https://github.com/Arias08426/Eventia-Core-API.git
cd Eventia-Core-API
```

### 2. Crear entorno virtual
```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # Linux/Mac
```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 4. Configurar variables de entorno
```bash
cp .env.example .env
```

Editar `.env` con tus credenciales:
```env
DATABASE_URL=mysql+pymysql://user:password@localhost:3306/eventia
REDIS_URL=redis://localhost:6379
```

### 5. Inicializar base de datos
```bash
python -c "from src.database.connection import init_db; init_db()"
```

## 🏃 Ejecución

### Servidor local
```bash
python -m uvicorn src.main:app --reload
```

API disponible en: http://localhost:8000

### Documentación interactiva
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 📡 Endpoints Principales

### Eventos
| Método | Endpoint | Descripción |
|--------|----------|-------------|
| POST | `/events/` | Crear evento |
| GET | `/events/` | Listar eventos |
| GET | `/events/{id}` | Obtener evento |
| PUT | `/events/{id}` | Actualizar evento |
| DELETE | `/events/{id}` | Eliminar evento |
| GET | `/events/{id}/statistics` | Estadísticas evento |

### Participantes
| Método | Endpoint | Descripción |
|--------|----------|-------------|
| POST | `/participants/` | Crear participante |
| GET | `/participants/` | Listar participantes |
| GET | `/participants/{id}` | Obtener participante |
| PUT | `/participants/{id}` | Actualizar participante |
| DELETE | `/participants/{id}` | Eliminar participante |

### Asistencias
| Método | Endpoint | Descripción |
|--------|----------|-------------|
| POST | `/attendances/` | Registrar asistencia |
| DELETE | `/attendances/{id}` | Cancelar asistencia |
| GET | `/attendances/event/{event_id}` | Participantes evento |
| GET | `/attendances/participant/{participant_id}` | Eventos participante |

### Salud
| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/health/` | Health check básico |
| GET | `/health/detailed` | Health check detallado |

## 🧪 Testing

### Ejecutar todas las pruebas
```bash
python -m pytest tests/ -v
```

**Resultado**: ✅ 59 passed, 7 skipped (3 tipos de pruebas: unit, integration, system)

### Pruebas unitarias
```bash
python -m pytest tests/unit/ -v
# ✅ 27 tests passed
```

### Pruebas de integración
```bash
python -m pytest tests/integration/ -v
# ✅ 7 tests passed
```

### Pruebas de sistema (E2E)
```bash
python -m pytest tests/system/ -v
# ✅ 25 tests passed
```

### Con cobertura
```bash
python -m pytest tests/ --cov=src --cov-report=html
```

## 🔍 Análisis de Código

### Validación de estilo (Flake8)
```bash
python -m flake8 src/ --max-line-length=100
# ✅ 0 errors
```

### Formateo de código (Black)
```bash
python -m black src/
```

### Ordenar imports (isort)
```bash
python -m isort src/
```

### Análisis de seguridad (Bandit)
```bash
python -m bandit -r src/
```

### Escanear dependencias (Safety)
```bash
python -m safety check
```

### Type checking (MyPy)
```bash
python -m mypy src/
```

## 🐳 Docker Compose (Opcional)

```bash
docker-compose up -d
```

Esto inicia:
- **MySQL 8.0** en puerto 3306
- **Redis 7** en puerto 6379
- **API** en puerto 8000

## 📊 Estructura de Base de Datos

### Eventos (events)
```sql
id          INT PRIMARY KEY AUTO_INCREMENT
name        VARCHAR(200) NOT NULL
description TEXT
location    VARCHAR(300) NOT NULL
date        DATETIME NOT NULL
capacity    INT NOT NULL
created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
updated_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
```

### Participantes (participants)
```sql
id         INT PRIMARY KEY AUTO_INCREMENT
name       VARCHAR(200) NOT NULL
email      VARCHAR(255) UNIQUE NOT NULL
phone      VARCHAR(20)
created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
```

### Asistencias (attendance)
```sql
id             INT PRIMARY KEY AUTO_INCREMENT
event_id       INT NOT NULL FK(events.id)
participant_id INT NOT NULL FK(participants.id)
registered_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
UNIQUE KEY (event_id, participant_id)
```

## 🔐 Validaciones

### Evento
- Nombre: 3-200 caracteres
- Ubicación: 3-300 caracteres
- Fecha: Debe ser futura
- Capacidad: Mayor que 0

### Participante
- Nombre: Requerido
- Email: Único, válido
- Teléfono: Opcional

### Asistencia
- Evento debe existir
- Participante debe existir
- No duplicados (1 asistencia/participante/evento)
- Capacidad disponible en evento

## 🔄 Pipeline CI/CD

GitHub Actions ejecuta automáticamente al hacer push:

1. **Code Quality** - Black, isort, Flake8 (✅ 0 errors)
2. **Security** - Bandit, Safety
3. **Unit Tests** - Pruebas unitarias (✅ 27 passed)
4. **Integration Tests** - Pruebas con BD/Cache (✅ 7 passed)
5. **System Tests** - Pruebas E2E (✅ 25 passed)

Ver: `.github/workflows/ci-cd.yml`

## 📝 Reglas de Negocio

1. Un participante **no puede registrarse dos veces** al mismo evento
2. Cada evento tiene **límite de capacidad** inmutable
3. Los emails de participantes **deben ser únicos**
4. Eliminar evento **elimina todas sus asistencias** (cascade)
5. Eliminar participante **elimina todas sus asistencias** (cascade)

## 🛠️ Troubleshooting

### Conexión a MySQL rechazada
- Verificar credenciales en `.env`
- MySQL debe estar corriendo en puerto 3306
- Base de datos `eventia` debe existir

### Redis no disponible
- Pruebas de integración se skipean automáticamente
- App sigue funcionando sin caché
- Verificar que Redis esté en puerto 6379

### Pruebas fallan
```bash
rm -rf .pytest_cache
python -m pytest tests/ -v -s
```

## 📚 Tecnologías

| Componente | Versión | Propósito |
|-----------|---------|-----------|
| FastAPI | 0.109.0 | Framework web |
| SQLAlchemy | 2.0.25 | ORM |
| Pydantic | 2.5.0 | Validación |
| PyMySQL | 1.1.0 | Driver MySQL |
| Redis | 7.0 | Cache |
| pytest | 7.4.4 | Testing |
| Black | 23.12.1 | Formato |
| Flake8 | 7.0.0 | Linting |
| Bandit | 1.7.6 | Seguridad |

## 🎓 Ejemplo de Uso

```bash
# 1. Crear un evento
curl -X POST http://localhost:8000/events/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Conferencia Python",
    "description": "Charlas sobre Python",
    "location": "Madrid",
    "date": "2024-12-15T14:00:00",
    "capacity": 100
  }'

# 2. Crear participante
curl -X POST http://localhost:8000/participants/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Juan Pérez",
    "email": "juan@example.com",
    "phone": "123456789"
  }'

# 3. Registrar participante a evento
curl -X POST http://localhost:8000/attendances/ \
  -H "Content-Type: application/json" \
  -d '{
    "event_id": 1,
    "participant_id": 1
  }'

# 4. Obtener estadísticas del evento
curl http://localhost:8000/events/1/statistics
```

## 📄 Licencia

Este proyecto está bajo licencia MIT.

---

**Última actualización**: Enero 2024  
**Estado**: ✅ Production Ready  
**Pruebas**: ✅ 59/59 passed  
**Código**: ✅ Flake8 0 errors
