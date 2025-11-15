# 🔧 Comandos Útiles: GitHub Actions

## 📍 Localización

Todos los comandos se ejecutan desde:
```powershell
cd "C:\Users\Usuario\Desktop\Eventia Core API"
```

---

## 🚀 Comandos Iniciales

### Inicializar repositorio
```powershell
git init
git config --global user.name "Tu Nombre"
git config --global user.email "tu@email.com"
git add .
git commit -m "Initial commit"
```

### Agregar remoto
```powershell
git remote add origin https://github.com/TU_USUARIO/eventia-core-api.git
```

### Hacer push
```powershell
git branch -M main
git push -u origin main
```

---

## 📤 Comandos de Push

### Push normal (recomendado)
```powershell
git add .
git commit -m "Tu mensaje descriptivo"
git push
```

### Push a rama específica
```powershell
git push origin main
git push origin develop
git push origin feature/mi-rama
```

### Ver remoto configurado
```powershell
git remote -v
```

### Cambiar remoto
```powershell
git remote set-url origin https://github.com/TU_USUARIO/nuevo-repo.git
```

---

## 🔍 Comandos de Verificación

### Ver estado
```powershell
git status
```

### Ver cambios
```powershell
git diff
git diff --staged
```

### Ver historial
```powershell
git log
git log --oneline
git log --oneline -5
```

### Ver ramas
```powershell
git branch
git branch -a
```

---

## 🧪 Comandos de Testing

### Ejecutar todos los tests
```powershell
pytest tests/ -v
pytest tests/ -v --tb=short
```

### Tests específicos
```powershell
# Unit tests
pytest tests/unit/ -v

# Integration tests
pytest tests/integration/ -v

# System tests
pytest tests/system/ -v
```

### Con cobertura
```powershell
pytest tests/ --cov=src --cov-report=html -v
pytest tests/ --cov=src --cov-report=term -v
```

### Un archivo específico
```powershell
pytest tests/unit/test_event_service.py -v
pytest tests/unit/test_event_service.py::test_create_event -v
```

---

## 🎨 Comandos de Código Quality

### Format con Black
```powershell
black src/ tests/
black --check src/ tests/  # Solo verificar
```

### Ordenar imports
```powershell
isort src/ tests/
isort --check-only src/ tests/  # Solo verificar
```

### Linting con Flake8
```powershell
flake8 src/ tests/
flake8 src/ --max-line-length=100
```

### Type checking con MyPy
```powershell
mypy src/
mypy src/ --ignore-missing-imports
```

### Seguridad con Bandit
```powershell
bandit -r src/
bandit -r src/ -f json -o report.json
```

### Vulnerabilidades con Safety
```powershell
safety check
safety check --json
```

---

## 🔐 Comandos de Configuración

### Ver configuración global
```powershell
git config --list
git config --list --global
```

### Configurar usuario
```powershell
git config --global user.name "Tu Nombre"
git config --global user.email "tu@email.com"
```

### Guardar credenciales
```powershell
git config --global credential.helper wincred
```

### Cambiar editor por defecto
```powershell
git config --global core.editor "code"
```

---

## 📊 Comandos de Monitoreo

### Ver estado en GitHub (en la terminal)
```powershell
# En Windows, puedes abrir directamente:
Start-Process "https://github.com/TU_USUARIO/eventia-core-api/actions"
```

### Ver último commit
```powershell
git show
git show --stat
```

### Comparar ramas
```powershell
git log main..develop
git diff main develop
```

---

## 🔄 Comandos Avanzados

### Crear rama nueva
```powershell
git checkout -b feature/nueva-rama
git push -u origin feature/nueva-rama
```

### Cambiar de rama
```powershell
git checkout main
git checkout develop
```

### Merge de rama
```powershell
git checkout main
git merge develop
git push
```

### Deshacer cambios
```powershell
git restore archivo.py        # Deshacer cambios locales
git restore --staged archivo  # Sacar del staging
git reset HEAD~1              # Deshacer último commit
```

### Forzar push (⚠️ CUIDADO)
```powershell
git push -f origin main  # ❌ Úsalo solo si sabes qué haces
```

---

## 📋 Comandos Docker (Opcional)

### Ver si MySQL está corriendo
```powershell
docker ps
```

### Iniciar MySQL para testing
```powershell
docker run -d -p 3306:3306 `
  -e MYSQL_ROOT_PASSWORD=root_password `
  -e MYSQL_DATABASE=eventia_db `
  -e MYSQL_USER=eventia_user `
  -e MYSQL_PASSWORD=eventia_password `
  mysql:8.0
```

### Iniciar Redis
```powershell
docker run -d -p 6379:6379 redis:7-alpine
```

### Parar contenedores
```powershell
docker stop $(docker ps -q)
```

---

## 🆘 Comandos de Emergencia

### Ver qué pasó en el último comando
```powershell
$LASTEXITCODE
```

### Limpiar cache de git
```powershell
git clean -fd
git clean -fX
```

### Resetear a un commit anterior
```powershell
git reset --hard <commit-hash>
```

### Recuperar rama eliminada
```powershell
git reflog
git checkout -b rama-recuperada <commit-hash>
```

---

## ⚡ Atajos Útiles

### Crear alias de comandos
```powershell
# En PowerShell, agrega a tu perfil:
# $PROFILE

function gst { git status }
function gadd { git add @args }
function gcm { git commit -m @args }
function gpush { git push }
function glog { git log --oneline }

# Luego puedes usar:
gst              # en lugar de: git status
gadd .           # en lugar de: git add .
gcm "mensaje"    # en lugar de: git commit -m "mensaje"
```

### Comando rápido: Commit y Push
```powershell
git add . ; git commit -m "Tu mensaje" ; git push
```

---

## 📚 Referencia Rápida

| Tarea | Comando |
|-------|---------|
| Ver estado | `git status` |
| Agregar cambios | `git add .` |
| Hacer commit | `git commit -m "msg"` |
| Hacer push | `git push` |
| Ver historial | `git log --oneline` |
| Crear rama | `git checkout -b rama` |
| Cambiar rama | `git checkout rama` |
| Tests unit | `pytest tests/unit/ -v` |
| Formatear código | `black src/ tests/` |
| Verificar tipos | `mypy src/` |
| Seguridad | `bandit -r src/` |

---

## 🎓 Workflow Típico

```powershell
# 1. Cambiar a rama de desarrollo
git checkout develop

# 2. Hacer cambios en tu código
# ... editas archivos ...

# 3. Ver qué cambió
git status

# 4. Probar localmente
pytest tests/ -v
black src/ tests/

# 5. Agregar cambios
git add .

# 6. Hacer commit
git commit -m "Feature: agregar nueva funcionalidad"

# 7. Hacer push
git push origin develop

# 8. Ver el workflow en GitHub
# https://github.com/TU_USUARIO/eventia-core-api/actions
```

---

**¿Necesitas ejecutar un comando específico? Cópialo y pégalo en PowerShell** 🚀
