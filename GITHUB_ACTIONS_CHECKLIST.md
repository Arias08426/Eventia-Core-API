# ✅ Checklist Rápido: GitHub Actions

## 🚀 Para Comenzar (5 minutos)

### 1️⃣ Preparar Código Localmente
```powershell
cd "C:\Users\Usuario\Desktop\Eventia Core API"

# Verifica que todo está limpio
git status
```

**Checklist**:
- [ ] No hay archivos sin commitear
- [ ] La rama es `main`

---

### 2️⃣ Crear Repositorio en GitHub
1. Ve a https://github.com/new
2. Nombre: `eventia-core-api`
3. Haz clic en **Create repository**

---

### 3️⃣ Hacer Push del Código
```powershell
# Opción A: Si es primera vez
git remote add origin https://github.com/TU_USUARIO/eventia-core-api.git
git branch -M main
git push -u origin main

# Opción B: Si ya existe remoto
git push origin main
```

**Nota**: Usa un **Personal Access Token** como contraseña (crear en https://github.com/settings/tokens)

---

### 4️⃣ Esperar a que termine

URL para monitorear:
```
https://github.com/TU_USUARIO/eventia-core-api/actions
```

Deberías ver:
```
CI/CD Pipeline 🟡 In progress

├─ Code Quality Checks 🟢 Completed
├─ Security Checks 🟡 In progress
├─ Unit Tests ⚫ Queued
├─ Integration Tests ⚫ Queued
├─ System Tests ⚫ Queued
└─ Final Report ⚫ Queued
```

---

## 🔧 Configuración Avanzada (Opcional)

### Agregar Secrets
```powershell
# En GitHub: Settings → Secrets and variables → Actions

# Ejemplo (si lo necesitas):
CODECOV_TOKEN: tu_token_aqui
```

### Proteger Rama Main
```
En GitHub: Settings → Branches → Add rule

Selecciona:
- ✅ Require status checks to pass
- ✅ Require branches to be up to date
```

---

## 🐛 Si algo falla

### Problema: "Authentication failed"
```powershell
# Solución:
git config --global credential.helper wincred
```

### Problema: "Branch already exists"
```powershell
# Solución:
git push -f origin main  # Fuerza el push (úsalo con cuidado)
```

### Problema: Tests fallan en GitHub Actions
```powershell
# Verifica localmente primero:
pytest tests/ -v

# Si falla localmente, arréglalo
# Si funciona local pero falla en Actions, revisa logs en GitHub
```

---

## 📊 Interpretar Resultados

### ✅ TODO PASÓ
```
✅ Code Quality Checks
✅ Security Checks
✅ Unit Tests
✅ Integration Tests
✅ System Tests
✅ Final Report

→ Puedes hacer merge tranquilo
```

### ⚠️ ALGO FALLÓ
```
❌ Code Quality Checks

→ Abre los logs para ver qué pasó
→ Corrige localmente
→ Haz push de nuevo
```

---

## 🎯 Próximas Ejecuciones

**El workflow se ejecuta automáticamente cuando**:
- Haces `git push` a `main`
- Haces `git push` a `develop`
- Abres un Pull Request a `main` o `develop`

---

## 📝 Archivos Importantes

- **`.github/workflows/ci-cd.yml`** - Configuración del workflow
- **`requirements.txt`** - Dependencias de producción
- **`requirements-dev.txt`** - Dependencias de desarrollo y testing
- **`GITHUB_ACTIONS_SETUP.md`** - Guía detallada
- **`setup-github.ps1`** - Script de configuración automática

---

## 💡 Tips

1. **Ejecutar script automático**:
   ```powershell
   .\setup-github.ps1
   ```

2. **Ver cambios antes de push**:
   ```powershell
   git diff
   ```

3. **Hacer commit rápido**:
   ```powershell
   git add . ; git commit -m "Tu mensaje" ; git push
   ```

4. **Ver historial**:
   ```powershell
   git log --oneline
   ```

---

## 🚨 NO HAGAS ESTO

- ❌ Compartir tokens de acceso
- ❌ Hacer push con `--force` sin estar seguro
- ❌ Commitear archivos de configuración sensibles (.env)
- ❌ Cambiar `ci-cd.yml` sin probar

---

**¿Listo para comenzar? Ejecuta: `.\setup-github.ps1`**

¡Buena suerte! 🚀
