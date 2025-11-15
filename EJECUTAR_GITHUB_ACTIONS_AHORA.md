# 🎯 EJECUTAR GITHUB ACTIONS - GUÍA INMEDIATA

## ¿Qué Necesitas Hacer? (Selecciona una opción)

---

## ⚡ OPCIÓN 1: Automática (Recomendado - 2 minutos)

### Paso 1: Crea un Repositorio Vacío en GitHub
1. Abre: https://github.com/new
2. **Repository name**: `eventia-core-api`
3. **Visibility**: Public (o Private, como prefieras)
4. Deja todo lo demás por defecto
5. Haz clic: **Create repository**

### Paso 2: Ejecuta el Script
```powershell
cd "C:\Users\Usuario\Desktop\Eventia Core API"
.\setup-github.ps1
```

El script te preguntará:
- `Tu nombre` → Ingresa tu nombre
- `Tu email` → Ingresa tu email
- `URL del repositorio` → Copia la URL que GitHub te mostró

### Paso 3: ¡Listo!
Ve a: `https://github.com/TU_USUARIO/eventia-core-api/actions`

Verás tu pipeline ejecutándose. ✅

---

## 📋 OPCIÓN 2: Manual (Si prefieres hacer paso a paso)

### Paso 1: Configurar Git
```powershell
cd "C:\Users\Usuario\Desktop\Eventia Core API"

git config --global user.name "Tu Nombre Aquí"
git config --global user.email "tu@email.com"
```

### Paso 2: Crear Repositorio Local
```powershell
git init
git add .
git commit -m "Initial commit: Eventia Core API"
```

### Paso 3: Agregar Remoto
```powershell
# Cambia TU_USUARIO por tu usuario de GitHub
git remote add origin https://github.com/TU_USUARIO/eventia-core-api.git
git branch -M main
```

### Paso 4: Hacer Push
```powershell
git push -u origin main
```

Si te pide contraseña:
- Usuario: tu usuario de GitHub
- Contraseña: crea un **Personal Access Token** en:
  https://github.com/settings/tokens
  - Haz clic: **Generate new token (classic)**
  - Selecciona: **repo**
  - Copia el token y úsalo como contraseña

### Paso 5: ¡Listo!
Ve a: `https://github.com/TU_USUARIO/eventia-core-api/actions`

---

## 🚀 OPCIÓN 3: Solo Push (Si ya tienes todo)

```powershell
cd "C:\Users\Usuario\Desktop\Eventia Core API"
git push origin main
```

---

## ✅ Verificar que Funciona

### ¿Dónde veo el workflow?
```
https://github.com/TU_USUARIO/eventia-core-api/actions
```

### ¿Qué debo ver?
```
CI/CD Pipeline
└── Mostrado el estado: In progress / Running

Los jobs deberían aparecer en orden:
  1. Code Quality Checks (ejecutando o completado)
  2. Security Checks
  3. Unit Tests
  4. Integration Tests
  5. System Tests
  6. Final Report
```

### ¿Cuánto tarda?
- Primera ejecución: **15-20 minutos**
- Ejecuciones siguientes: **10-15 minutos**

---

## 🟢 Si TODO Pasó ✅

```
✅ Code Quality Checks
✅ Security Checks
✅ Unit Tests
✅ Integration Tests
✅ System Tests
✅ Final Report

Pipeline Status: OK ✅
```

**Perfecto. Tu CI/CD está funcionando correctamente.** 🎉

---

## 🔴 Si Algo Falló ❌

### Busca el Job que Falló
1. Haz clic en el job rojo (ej: "Code Quality Checks")
2. Expande las secciones para ver el error
3. Lee el mensaje de error

### Errores Comunes

#### "Code Quality Checks failed"
```powershell
# Formatea el código
black src/ tests/
isort src/ tests/

# Haz push de nuevo
git add . && git commit -m "Format" && git push
```

#### "Unit Tests failed"
```powershell
# Prueba localmente
pytest tests/unit/ -v

# Si pasa aquí pero falla en GitHub, 
# probablemente sea por una variable de entorno
# Lee: GITHUB_ACTIONS_TROUBLESHOOTING.md
```

#### "Integration Tests failed"
```powershell
# Suele ser por MySQL o Redis no disponible
# Normalmente se resuelve solo en el siguiente push

# O intenta:
git add . && git commit -m "Retry tests" && git push
```

---

## 📊 Interpretar Cambios de Estado

| Estado | Significado | Qué Hacer |
|--------|------------|----------|
| 🟡 In Progress | Ejecutándose | Espera |
| 🟢 Completed | Pasó correctamente | Nada |
| 🔴 Failed | Error encontrado | Ve los logs |
| ⚫ Queued | Esperando su turno | Espera |
| ⊘ Skipped | Saltado (normal) | Normal |

---

## 💡 Próximos Pasos

Después que funcione:

### 1. Proteger Rama Main (Opcional)
```
GitHub → Settings → Branches → Add rule
├─ Branch name pattern: main
├─ ✅ Require status checks to pass
└─ ✅ Require branches to be up to date
```

### 2. Ver Reportes de Cobertura (Opcional)
```
GitHub Actions → Último workflow exitoso
→ Descarga "unit-test-results"
→ Abre: htmlcov/index.html
```

### 3. Integrar con Codecov (Opcional)
```
1. Ve a: https://codecov.io
2. Conecta tu repositorio
3. Copia el token
4. En GitHub: Settings → Secrets → CODECOV_TOKEN
```

---

## 🚨 Problemas Frecuentes

### "fatal: not a git repository"
```powershell
cd "C:\Users\Usuario\Desktop\Eventia Core API"
git init
```

### "remote origin already exists"
```powershell
git remote remove origin
git remote add origin https://github.com/TU_USUARIO/eventia-core-api.git
```

### "Authentication failed"
```powershell
# Crea PAT en: https://github.com/settings/tokens
# Usa este token como contraseña
```

### "Branch protection rule"
```powershell
# En GitHub: Settings → Branches → Delete la regla
# O usa rama: git push origin develop
```

---

## 📚 Documentos de Ayuda

Si necesitas más detalles:

| Cuando... | Lee... |
|-----------|--------|
| Entender todo en detalle | `GITHUB_ACTIONS_SETUP.md` |
| Algo no funciona | `GITHUB_ACTIONS_TROUBLESHOOTING.md` |
| Necesito comandos específicos | `GITHUB_ACTIONS_COMMANDS.md` |
| Quiero ver el flujo visual | `GITHUB_ACTIONS_SUMMARY.md` |
| Estoy apurado | `GITHUB_ACTIONS_CHECKLIST.md` |
| Soy nuevo | `START_HERE.md` |

---

## 🎯 Resumen Rápido

```
1. Crea repo vacío en GitHub
   └─ https://github.com/new

2. Ejecuta script o comando push
   └─ .\setup-github.ps1
      o
      git push origin main

3. Abre GitHub Actions
   └─ https://github.com/TU_USUARIO/eventia-core-api/actions

4. Espera ~15 minutos
   └─ Verás los jobs ejecutándose

5. ¡Listo! 🎉
   └─ Tu CI/CD está funcionando
```

---

## ✨ ¡COMIENZA AHORA!

### Opción rápida:
```powershell
.\setup-github.ps1
```

### O manual:
```powershell
git push origin main
```

**Luego ve a:**
```
https://github.com/TU_USUARIO/eventia-core-api/actions
```

---

**¿Dudas?** Lee los documentos de ayuda. ¡Éxito! 🚀
