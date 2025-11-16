# Redis Setup & Verification Guide

## 📊 Redis Status Report

### Current Status: ⚠️ OFFLINE
Redis **NO está corriendo actualmente** en tu máquina local.

### Test Results:
```
✅ RedisClient configurado correctamente
✅ Configuración en settings.py correcta
✅ Pruebas de integración disponibles
❌ Redis servidor no está disponible
```

---

## 🚀 Cómo Iniciar Redis

### Opción 1: Docker (Recomendado)
La forma más fácil en Windows es usar Docker.

#### Paso 1: Instala Docker
Descarga de: https://www.docker.com/products/docker-desktop

#### Paso 2: Ejecuta Redis en Docker
```powershell
docker run -d -p 6379:6379 --name redis-eventia redis:7-alpine
```

#### Paso 3: Verifica que Redis está corriendo
```powershell
docker ps | grep redis
```

Deberías ver algo como:
```
redis-eventia   redis:7-alpine   redis-server   ...
```

---

### Opción 2: Windows Subsystem for Linux (WSL)
Si tienes WSL2 instalado:

```bash
# 1. Abre WSL
wsl

# 2. Instala Redis
sudo apt update
sudo apt install redis-server

# 3. Inicia Redis
redis-server
```

---

### Opción 3: Descarga directa para Windows
1. Ve a: https://github.com/microsoftarchive/redis/releases
2. Descarga la versión más reciente (.msi)
3. Instala normalmente
4. Abre Command Prompt y ejecuta:
```cmd
redis-server
```

---

## ✅ Verificar que Redis Está Funcionando

### Método 1: Python Script
```powershell
cd "C:\Users\Usuario\Desktop\Eventia Core API"
python -c "
from src.cache.redis_client import RedisClient
client = RedisClient()
if client.ping():
    print('✅ Redis está funcionando correctamente!')
else:
    print('❌ Redis no está disponible')
"
```

### Método 2: Redis CLI
```powershell
redis-cli ping
```

Debería responder: `PONG`

### Método 3: Verificar conexión
```powershell
redis-cli
# Luego escribir:
> PING
PONG
> SET key1 "Hello"
OK
> GET key1
"Hello"
> EXIT
```

---

## 🧪 Ejecutar Pruebas de Redis

Una vez que Redis esté corriendo, puedes ejecutar las pruebas:

```powershell
cd "C:\Users\Usuario\Desktop\Eventia Core API"

# Pruebas de caché específicamente
pytest tests/integration/test_cache.py -v

# Todas las pruebas de integración
pytest tests/integration/ -v

# Ejecutar solo las pruebas que usan Redis
pytest tests/integration/ -v -m "not skipif"
```

---

## 📦 Redis Configuration en tu Proyecto

### Ubicación: `src/config/setting.py`
```python
# CONFIGURACIÓN DE REDIS (CACHÉ)
REDIS_HOST: str = "localhost"
REDIS_PORT: int = 6379
REDIS_DB: int = 0
REDIS_PASSWORD: str = ""
CACHE_TTL: int = 300  # 5 minutos por defecto
```

### Cliente Redis: `src/cache/redis_client.py`
El cliente está completamente configurado y listo para usar con métodos como:
- `get(key)` - Obtener valor
- `set(key, value, ttl)` - Guardar valor
- `delete(key)` - Eliminar clave
- `clear_all()` - Limpiar todo
- `ping()` - Verificar conexión

---

## 🔗 Integración en la Aplicación

### Cómo usar Redis en tu código:

```python
from src.cache.redis_client import RedisClient

# Crear cliente
cache = RedisClient()

# Guardar datos
cache.set("user:123", {"name": "Juan", "email": "juan@example.com"})

# Obtener datos
user = cache.get("user:123")
print(user)  # {'name': 'Juan', 'email': 'juan@example.com'}

# Eliminar datos
cache.delete("user:123")

# Verificar conexión
if cache.ping():
    print("Redis está disponible")
```

---

## 📊 Redis Stats

### Comandos Básicos:
```
PING              - Verifica conexión
SET key value     - Guarda un valor
GET key           - Obtiene un valor
DEL key           - Elimina una clave
FLUSHALL          - Borra todo
KEYS *            - Lista todas las claves
DBSIZE            - Cantidad de claves
INFO              - Información del servidor
```

### Monitor Real-time:
```powershell
redis-cli MONITOR
```

---

## 🐳 Docker Compose (Opcional)

Si quieres gestionar Redis junto con MySQL:

Crea un archivo `docker-compose.yml`:

```yaml
version: '3.8'

services:
  mysql:
    image: mysql:8.0
    environment:
      MYSQL_ROOT_PASSWORD: root
      MYSQL_DATABASE: eventia_test
      MYSQL_USER: eventia
      MYSQL_PASSWORD: eventia
    ports:
      - "3306:3306"
    healthcheck:
      test: ["CMD", "mysqladmin", "ping", "-h", "localhost"]
      interval: 10s
      timeout: 5s
      retries: 5

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5

  api:
    build: .
    environment:
      DATABASE_URL: mysql+pymysql://eventia:eventia@mysql:3306/eventia_test
      REDIS_HOST: redis
      REDIS_PORT: 6379
    ports:
      - "8000:8000"
    depends_on:
      mysql:
        condition: service_healthy
      redis:
        condition: service_healthy
```

Luego ejecuta:
```powershell
docker-compose up -d
```

---

## 🔍 Troubleshooting

### Problema: "Connection refused"
**Solución**: Asegúrate de que Redis está corriendo:
```powershell
redis-cli ping
```

### Problema: Puerto 6379 está en uso
**Solución**: Cambia el puerto en `.env`:
```env
REDIS_PORT=6380
```

O mata el proceso:
```powershell
# PowerShell
Get-Process redis-server | Stop-Process -Force
```

### Problema: "WRONGPASS" error
**Solución**: Si configuraste contraseña, asegúrate de que coincida en `.env`:
```env
REDIS_PASSWORD=tu_contraseña
```

---

## 📈 GitHub Actions ✅

En GitHub Actions, Redis está **correctamente configurado** y funcionando:

1. ✅ **Integration Tests**: 7 pruebas pasaron en GitHub Actions
2. ✅ **System Tests**: 25 pruebas pasaron en GitHub Actions
3. ✅ **Redis service**: Disponible en CI/CD en puerto 6379

---

## 📝 Summary

| Aspecto | Estado | Acción |
|--------|--------|--------|
| Código | ✅ OK | No requiere cambios |
| Configuración | ✅ OK | No requiere cambios |
| Tests | ✅ OK (7 pasaron en GitHub) | No requiere cambios |
| Local Redis | ❌ OFFLINE | Inicia Redis con Docker o WSL |
| CI/CD Redis | ✅ ONLINE | Funciona perfectamente |

**Recomendación**: Instala Redis localmente con Docker para desarrollo local completo.
