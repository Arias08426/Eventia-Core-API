# 🐳 Instalación de Docker en Windows

## Paso 1: Descargar Docker Desktop

1. Ve a: **https://www.docker.com/products/docker-desktop**
2. Haz clic en **"Download for Windows"**
3. Se descargará: `Docker Desktop Installer.exe`

---

## Paso 2: Instalar Docker Desktop

1. Abre el archivo descargado: `Docker Desktop Installer.exe`
2. Sigue el asistente de instalación (acepta todos los términos por defecto)
3. **Importante**: Asegúrate de marcar:
   - ✅ "Install required Windows components for WSL 2"
   - ✅ "Add Docker to the PATH"
4. Haz clic en **"Install"**
5. Espera a que termine (puede tomar 5-10 minutos)
6. **Reinicia tu computadora** cuando se te pida

---

## Paso 3: Verificar instalación

Abre PowerShell y ejecuta:

```powershell
docker --version
```

Deberías ver algo como:
```
Docker version 24.0.6, build abc1234
```

---

## Paso 4: Iniciar Docker Desktop

1. Abre el menú Inicio
2. Busca "Docker Desktop"
3. Abrelo (puede tomar unos minutos en iniciarse)
4. Espera a que aparezca el icono en la bandeja de tareas

---

## Paso 5: Instalar Redis con Docker

Una vez que Docker está corriendo, abre PowerShell en tu carpeta del proyecto y ejecuta:

```powershell
docker run -d -p 6379:6379 --name redis-eventia redis:7-alpine
```

Explicación del comando:
- `docker run` - Ejecuta un contenedor
- `-d` - En background (detached mode)
- `-p 6379:6379` - Mapea puerto 6379 del contenedor al puerto 6379 de tu máquina
- `--name redis-eventia` - Nombre del contenedor
- `redis:7-alpine` - Imagen de Redis 7 versión alpine (ligera)

---

## Paso 6: Verificar que Redis está corriendo

```powershell
docker ps
```

Deberías ver:
```
CONTAINER ID   IMAGE              COMMAND                PORTS                    NAMES
abc123def456   redis:7-alpine     "redis-server"         0.0.0.0:6379->6379/tcp  redis-eventia
```

---

## Paso 7: Verificar conexión a Redis

```powershell
redis-cli ping
```

Respuesta esperada:
```
PONG
```

Si sale error de que `redis-cli` no se reconoce, puedes hacerlo desde Python:

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

---

## 📊 Gestionar el Contenedor Redis

### Ver logs del contenedor:
```powershell
docker logs redis-eventia
```

### Detener Redis:
```powershell
docker stop redis-eventia
```

### Iniciar Redis nuevamente:
```powershell
docker start redis-eventia
```

### Eliminar el contenedor (CUIDADO: borra datos):
```powershell
docker rm redis-eventia
```

---

## 🧪 Ejecutar Pruebas con Redis

Una vez que Redis esté corriendo:

```powershell
cd "C:\Users\Usuario\Desktop\Eventia Core API"

# Ejecutar todas las pruebas
pytest -v

# Solo pruebas de caché
pytest tests/integration/test_cache.py -v

# Con reporte de cobertura
pytest --cov=src tests/ -v
```

---

## 🆘 Troubleshooting

### "docker: The term 'docker' is not recognized"
- ✅ Reinicia PowerShell después de instalar Docker
- ✅ Reinicia tu computadora completamente

### "Port 6379 is already in use"
```powershell
# Busca qué está usando el puerto
netstat -ano | findstr :6379

# O simplemente usa otro puerto
docker run -d -p 6380:6379 --name redis-eventia redis:7-alpine
```

### "Cannot connect to Docker daemon"
- ✅ Asegúrate de que Docker Desktop está corriendo
- ✅ Busca el icono de Docker en la bandeja de tareas

---

## 📝 Resumen de Comandos

```powershell
# Instalar Redis
docker run -d -p 6379:6379 --name redis-eventia redis:7-alpine

# Ver contenedores
docker ps

# Ver logs
docker logs redis-eventia

# Detener
docker stop redis-eventia

# Iniciar
docker start redis-eventia

# Verificar conexión
redis-cli ping
python -c "from src.cache.redis_client import RedisClient; print('OK' if RedisClient().ping() else 'FAIL')"
```

---

## ✅ Próximos Pasos

Una vez que Redis está corriendo:
1. Ejecuta `pytest` para verificar que todas las pruebas pasan
2. Ejecuta `python src/main.py` para iniciar la API
3. Redis estará disponible para caché en la aplicación

¡Listo! 🚀
