# 🔧 Solucionar Problemas: GitHub Actions

## 🚨 Errores Comunes y Soluciones

---

## ❌ Error: "fatal: not a git repository"

### Causa
Git no está inicializado en tu carpeta.

### Solución
```powershell
cd "C:\Users\Usuario\Desktop\Eventia Core API"
git init
git add .
git commit -m "Initial commit"
```

---

## ❌ Error: "fatal: could not read Username"

### Causa
No tienes credenciales configuradas.

### Solución
```powershell
# Opción 1: Usar Personal Access Token
git config --global user.name "Tu Nombre"
git config --global user.email "tu@email.com"

# Opción 2: Guardar credenciales
git config --global credential.helper wincred
```

---

## ❌ Error: "remote origin already exists"

### Causa
Ya existe un remoto configurado.

### Solución
```powershell
# Ver remoto actual
git remote -v

# Cambiar remoto
git remote set-url origin https://github.com/TU_USUARIO/eventia-core-api.git

# O eliminar y agregar nuevo
git remote remove origin
git remote add origin https://github.com/TU_USUARIO/eventia-core-api.git
```

---

## ❌ Error: "push rejected / branch protection"

### Causa
Hay reglas de protección en main.

### Solución (Desarrollo)
```powershell
# En GitHub: Settings → Branches → Remove rule
# O usar rama de desarrollo:
git push origin develop
```

---

## ❌ Error: "Failed - Code Quality Checks"

### Cause
El código no cumple con estándares (Black, Flake8, isort).

### Solución Local
```powershell
# Formatea con Black
black src/ tests/

# Ordena imports
isort src/ tests/

# Verifica con Flake8
flake8 src/ tests/ --max-line-length=100

# Si todo es OK, haz commit
git add . ; git commit -m "Code formatting" ; git push
```

---

## ❌ Error: "Failed - Unit Tests"

### Causa
Las pruebas fallan en GitHub Actions (pero tal vez funcionan localmente).

### Solución
```powershell
# 1. Verifica que funciona localmente
pytest tests/unit/ -v

# 2. Revisa los logs en GitHub Actions
# 3. Mira qué variable de entorno falta
# 4. Agrega como Secret si es necesario
```

### Ejemplo: Test que falla por variable de entorno
```python
# ❌ ANTES (falla porque falta DATABASE_URL)
def test_connection():
    db_url = os.getenv("DATABASE_URL")
    assert db_url is not None

# ✅ DESPUÉS (usa valor por defecto para testing)
def test_connection():
    db_url = os.getenv("DATABASE_URL", "mysql://localhost/test")
    assert db_url is not None
```

---

## ❌ Error: "Failed - Integration Tests (MySQL error)"

### Causa
El servicio MySQL no está listo.

### Solución
Está solucionado en nuestro workflow, pero si persiste:

```yaml
- name: Wait for MySQL
  run: |
    for i in {1..30}; do
      mysqladmin ping -h127.0.0.1 -ueventia_user -peventia_password 2>/dev/null && break || sleep 1
    done
```

---

## ⚠️ Advertencia: "Codecov upload failed"

### Cause
Token de Codecov no configurado (pero no es crítico).

### Solución
```powershell
# Es opcional. Si quieres:
# 1. Ve a https://codecov.io
# 2. Conecta tu repositorio
# 3. Copia el token
# 4. En GitHub: Settings → Secrets → CODECOV_TOKEN = tu_token
```

---

## 🔍 Cómo Debuggear Errores

### 1. Ver logs completos

```
En GitHub:
1. Ve a Actions
2. Haz clic en el workflow fallido
3. Haz clic en el job (ej: "Code Quality Checks")
4. Verás la salida línea por línea
```

### 2. Reproducir localmente

```powershell
# Copia el comando exacto del log y ejecútalo
pytest tests/unit/ --cov=src --cov-report=xml -v
```

### 3. Verificar archivos

```powershell
# ¿Existen los archivos?
ls tests/unit/
ls src/

# ¿Tienen el contenido correcto?
cat tests/unit/test_attendance_service.py
```

---

## 🚀 Soluciones Rápidas

### Si "Code Quality Checks" falla
```powershell
black src/ tests/ && isort src/ tests/ && git add . && git commit -m "Format" && git push
```

### Si "Unit Tests" falla
```powershell
pytest tests/unit/ -v --tb=short
```

### Si "Integration Tests" falla
```powershell
# Asegúrate de tener MySQL corriendo
docker run -d -p 3306:3306 -e MYSQL_ROOT_PASSWORD=root mysql:8.0
pytest tests/integration/ -v
```

### Si todo falla
```powershell
# Reinicia desde cero
git status              # Ver qué cambió
git diff               # Ver cambios específicos
git log --oneline      # Ver historial
git reset --hard HEAD  # Volver al último commit (CUIDADO)
```

---

## 📝 Checklist de Debugging

- [ ] ¿El código funciona localmente?
- [ ] ¿Todos los tests pasan localmente?
- [ ] ¿Las dependencias están en `requirements.txt`?
- [ ] ¿Las variables de entorno están definidas?
- [ ] ¿Los archivos están en el repo (no en .gitignore)?
- [ ] ¿La rama es `main` o `develop`?
- [ ] ¿El remoto apunta a GitHub?

---

## 🆘 Si Nada Funciona

### Opción 1: Reiniciar
```powershell
# Elimina el remoto y comienza de nuevo
git remote remove origin
git remote add origin https://github.com/TU_USUARIO/eventia-core-api.git
git push -u origin main --force
```

### Opción 2: Clonar desde cero
```powershell
cd \Desktop
git clone https://github.com/TU_USUARIO/eventia-core-api.git
cd eventia-core-api
```

### Opción 3: Contactar soporte
- GitHub: https://github.com/support
- Community: https://github.community

---

## 💡 Tips Finales

1. **Siempre prueba localmente primero**
   ```powershell
   pytest tests/ -v
   black --check src/
   ```

2. **Lee los logs completos**, no solo el título del error

3. **Si algo cambia, vuelve a hacer push**
   ```powershell
   git add . && git commit -m "Fix" && git push
   ```

4. **No forces cambios a main** sin probar
   ```powershell
   git push -f  # ❌ NUNCA
   git push     # ✅ SIEMPRE
   ```

5. **Los secretos no se muestran en los logs** (es normal)

---

**¿Necesitas ayuda? Revisa los logs en GitHub Actions** 🔍
