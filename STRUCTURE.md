# 📁 Estructura del Proyecto - Eventia Core API

## Arquitectura: MVC (Model-View-Controller)

```
TallerPruebas/
├── src/                          # Código fuente principal
│   ├── __init__.py
│   ├── main.py                   # Punto de entrada (app FastAPI)
│   │
│   ├── models/                   # 🔹 MODELS - Modelos de datos (SQLAlchemy)
│   │   ├── __init__.py
│   │   ├── event.py              # Modelo de Eventos
│   │   ├── participant.py        # Modelo de Participantes
│   │   └── attendance.py         # Modelo de Asistencias
│   │
│   ├── controllers/              # 🔹 CONTROLLERS - Controladores (endpoints HTTP)
│   │   ├── __init__.py
│   │   ├── event_controller.py       # Endpoints de eventos
│   │   ├── participant_controller.py # Endpoints de participantes
│   │   ├── attendance_controller.py  # Endpoints de asistencias
│   │   └── health_controller.py      # Health check
│   │
│   ├── services/                 # 🔹 SERVICES - Lógica de negocio
│   │   ├── __init__.py
│   │   ├── event_service.py          # Lógica de eventos
│   │   ├── participant_service.py    # Lógica de participantes
│   │   └── attendance_service.py     # Lógica de asistencias
│   │
│   ├── schemas/                  # 📊 Schemas - Validación con Pydantic (DTOs)
│   │   ├── __init__.py
│   │   ├── event.py              # Validación de eventos
│   │   ├── participant.py        # Validación de participantes
│   │   └── attendance.py         # Validación de asistencias
│   │
│   ├── database/                 # 🗄️ Database - Configuración ORM
│   │   ├── __init__.py
│   │   └── connection.py         # Configuración SQLAlchemy, SessionLocal, Base
│   │
│   ├── cache/                    # ⚡ Cache - Sistema de caché con Redis
│   │   ├── __init__.py
│   │   └── redis_client.py       # Cliente Redis
│   │
│   ├── config/                   # ⚙️ Configuration - Configuración de la app
│   │   ├── __init__.py
│   │   └── setting.py            # Configuración centralizada (Pydantic Settings)
│   │
│   ├── exceptions/               # ⚠️ Exceptions - Excepciones personalizadas
│   │   ├── __init__.py
│   │   └── custom_exceptions.py  # Excepciones del negocio
│   │
│   └── middleware/               # 🔧 Middleware - Manejadores personalizados
│       ├── __init__.py
│       └── error_handler.py      # Manejo centralizado de errores
│
├── tests/                        # 🧪 Tests - Suite de pruebas
│   ├── __init__.py
│   ├── conftest.py              # Fixtures y configuración pytest
│   ├── unit/                    # Pruebas unitarias
│   │   ├── __init__.py
│   │   ├── test_event_service.py
│   │   ├── test_participant_service.py
│   │   └── test_attendance_service.py
│   ├── integration/             # Pruebas de integración
│   │   ├── __init__.py
│   │   ├── test_cache.py
│   │   └── test_database.py
│   └── system/                  # Pruebas de sistema (E2E)
│       ├── __init__.py
│       ├── test_events_api.py
│       ├── test_participants_api.py
│       └── test_attendance_api.py
│
├── .github/
│   └── workflows/
│       └── ci-cd.yml            # 🚀 Pipeline de GitHub Actions
│
├── .env                         # Variables de entorno (local)
├── .env.example                 # Plantilla de variables
├── requirements.txt             # Dependencias de producción
├── requirements-dev.txt         # Dependencias de desarrollo
├── Dockerfile                   # 🐳 Containerización del backend
├── docker-compose.yml           # 🐳 Orquestación de servicios
├── README.md                    # 📖 Documentación completa
└── STRUCTURE.md                 # Este archivo
```

## 📊 Desglose por Capas (MVC)

### 1️⃣ MODEL Layer (Modelos)
**Archivos:** `src/models/`
- Define la estructura de datos en la BD
- Usa SQLAlchemy ORM
- No contiene lógica de negocio

### 2️⃣ VIEW Layer (Controladores + Schemas)
**Archivos:** `src/controllers/` + `src/schemas/`
- **Controllers**: Manejan las peticiones HTTP (FastAPI routes)
- **Schemas**: Validan entrada/salida con Pydantic
- Convierten datos HTTP ↔ objetos Python

### 3️⃣ CONTROLLER/SERVICE Layer (Lógica de negocio)
**Archivos:** `src/services/`
- Implementan las reglas de negocio
- Desacoplados de HTTP
- Pueden ser reutilizados desde cualquier lugar

## 🔄 Flujo de Datos

```
Cliente HTTP
    ↓
FastAPI Route (en controller)
    ↓
Schema (Pydantic valida)
    ↓
Service (lógica de negocio)
    ↓
Model (ORM - database access)
    ↓
MySQL / Redis
```

## 🧪 Estrategia de Testing

### Unit Tests (`tests/unit/`)
- Prueban servicios aislados
- Usan mocks
- Rápidas y deterministas

### Integration Tests (`tests/integration/`)
- Prueban servicios + BD real + Redis
- Verifican flujos de datos
- Más lentas pero realistas

### System/E2E Tests (`tests/system/`)
- Prueban endpoints completos HTTP
- Verifican respuestas HTTP
- Prueban casos de uso reales

## ✅ Checklist de Estructura MVC

- ✅ **Models**: Definen esquema de datos
- ✅ **Controllers**: Manejan HTTP
- ✅ **Services**: Contienen lógica
- ✅ **Schemas**: Validan datos
- ✅ **Database**: Configuración ORM
- ✅ **Cache**: Redis integrado
- ✅ **Config**: Centralización de settings
- ✅ **Exceptions**: Errores personalizados
- ✅ **Middleware**: Handlers globales
- ✅ **Tests**: Unitarias + Integración + E2E

## 🚀 Ventajas de esta estructura

1. **Separación de responsabilidades** - Cada carpeta tiene un propósito claro
2. **Fácil de escalar** - Agregar nuevas entidades es repetible
3. **Testeable** - Cada capa puede probarse independientemente
4. **Mantenible** - Cambios localizados, no afectan otras áreas
5. **Profesional** - Sigue convenciones de Django/FastAPI

## 📝 Notas

- Los archivos `__init__.py` permiten imports limpios
- `conftest.py` centraliza fixtures de pytest
- `main.py` es el punto de entrada único
- `docker-compose.yml` orquesta todos los servicios

---

**Última actualización:** Noviembre 2025
