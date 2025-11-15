# 📋 Guía: Cómo Probar el Proyecto en GitHub Actions

## 🎯 Objetivo

Después de hacer push del código a GitHub, el pipeline de CI/CD se ejecutará automáticamente. Esta guía te muestra cómo monitorear y entender los resultados.

---

## ✅ Paso 1: Hacer Push del Código a GitHub

### 1.1 Si tienes un repositorio remoto configurado:

```bash
git push origin main
```

### 1.2 Si no tienes repositorio remoto todavía:

1. Ve a [GitHub.com](https://github.com) y crea un nuevo repositorio vacío
2. Dale un nombre (ej: `TallerPruebas`)
3. NO inicialices con README (ya lo tenemos)

4. En tu terminal local:

```bash
git remote add origin https://github.com/TU_USUARIO/TallerPruebas.git
git branch -M main
git push -u origin main
```

---

## 🚀 Paso 2: Monitorear la Ejecución

### 2.1 Acceder a GitHub Actions

1. Ve a tu repositorio en GitHub
2. Haz clic en la pestaña **"Actions"** en la parte superior
3. Verás tu workflow ejecutándose en tiempo real

### 2.2 URL Directa

```
https://github.com/TU_USUARIO/TallerPruebas/actions
```

---

## 📊 Paso 3: Entender los Resultados

### 3.1 Vista General del Workflow

Deberías ver algo como esto:

```
✅ Eventia Core API: Todos los 10 requisitos...
├── Code Quality Checks (PASSED) ✅
├── Security Analysis (PASSED) ✅
├── Unit Tests (PASSED) ✅
├── Integration Tests (PASSED) ✅
├── System Tests (PASSED) ✅
└── Generate Report (PASSED) ✅
```

### 3.2 Estados Posibles

| Estado | Significado | Acción |
|--------|-------------|--------|
| 🟢 **Passed** | Todo está bien | Nada que hacer |
| 🟡 **Running** | En progreso | Espera... |
| 🔴 **Failed** | Error encontrado | Ver logs |
| ⚫ **Skipped** | Test saltado | Normal (ej: Redis) |

---

## 🔍 Paso 4: Revisar Logs Detallados

### 4.1 Ver Logs de un Job Específico

1. Haz clic en el workflow que está corriendo
2. En la lista de trabajos, haz clic en uno (ej: "Code Quality Checks")
3. Verás los detalles línea por línea

### 4.2 Logs Más Importantes

#### **Code Quality Checks**
```
✓ Black (formateador)
✓ isort (imports)
✓ Flake8 (linting)
✓ MyPy (type checking)
```

#### **Security Analysis**
```
✓ Bandit (seguridad)
✓ Safety (dependencias)
```

#### **Unit Tests**
```
27 tests PASSED ✅
0 tests FAILED ❌
```

#### **Integration Tests**
```
7 tests SKIPPED (Redis no disponible - esto es esperado)
0 tests FAILED ❌
```

#### **System Tests**
```
26 tests PASSED ✅
0 tests FAILED ❌
```

---

## 🛠️ Paso 5: Solucionar Problemas

### ❌ Si algo falla:

#### **Opción 1: Revisar el Log**
1. Haz clic en el job fallido
2. Lee el error desde el final hacia arriba
3. Busca palabras clave: `Error:`, `FAILED`, `Exception`

#### **Opción 2: Ejecutar Localmente**
```bash
# Simular lo que hace GitHub Actions
pytest tests/ -v
black src/
flake8 src/
mypy src/
bandit -r src/
```

#### **Opción 3: Revisar Variables de Entorno**
En `.github/workflows/ci-cd.yml` busca `env:` para ver qué variables se usan

---

## 📝 Paso 6: Verificar Que Todo Está Configurado

### 6.1 Elementos Necesarios

Verifica que tu repositorio tenga:

- ✅ `.github/workflows/ci-cd.yml` - El pipeline
- ✅ `requirements.txt` - Las dependencias
- ✅ `tests/` - Los tests
- ✅ `src/` - El código fuente
- ✅ `.gitignore` - Para ignorar `.venv`

### 6.2 Comando para Verificar

```bash
git ls-files | grep -E "(ci-cd|requirements|tests|src)"
```

---

## 🎯 Paso 7: Resultados Esperados

### ✅ El Pipeline DEBE mostrar:

```
Workflow: Eventia Core API: Todos los 10 requisitos...
Status: ✅ PASSED

Jobs:
  ✅ Code Quality Checks - 3m 20s
  ✅ Security Analysis - 1m 15s
  ✅ Unit Tests - 2m 10s
  ✅ Integration Tests - 1m 50s
  ✅ System Tests - 4m 30s
  ✅ Generate Report - 30s

Total: 13m 35s
```

---

## 🔐 Paso 8: Configurar Secretos (Opcional)

Si quieres hacer push de la imagen Docker a Docker Hub:

1. Ve a **Settings** → **Secrets and variables** → **Actions**
2. Crea estos secretos:
   - `DOCKER_USERNAME` - Tu usuario de Docker Hub
   - `DOCKER_PASSWORD` - Tu contraseña o token

---

## 📊 Paso 9: Monitorear Commits Posteriores

Cada vez que hagas push:

```bash
# Hacer cambios
git add .
git commit -m "Mejora: descripción"
git push origin main
```

El workflow se ejecutará automáticamente. Verás un indicador ✅ o ❌ al lado del commit.

---

## 🚨 Problemas Comunes

### ❌ "No se encuentra el archivo requirements.txt"
**Solución:** Verifica que existe en la raíz del proyecto
```bash
ls requirements.txt
```

### ❌ "ModuleNotFoundError: No module named 'src'"
**Solución:** Revisa que `conftest.py` tiene la línea de `sys.path`
```python
sys.path.insert(0, str(Path(__file__).parent.parent))
```

### ❌ "Redis is not available"
**Solución:** Es NORMAL. Los tests de Redis tienen `@pytest.mark.skipif` y se saltan automáticamente.

### ❌ "MySQL connection failed"
**Solución:** Revisa que el service `mysql` está corriendo en el workflow:
```yaml
services:
  mysql:
    image: mysql:8.0
    env:
      MYSQL_ROOT_PASSWORD: root
```

---

## ✨ Cosas Que Puedes Hacer

### 1. **Agregar Badge al README**

En tu `README.md`, agrega:

```markdown
[![CI/CD Pipeline](https://github.com/TU_USUARIO/TallerPruebas/actions/workflows/ci-cd.yml/badge.svg)](https://github.com/TU_USUARIO/TallerPruebas/actions)
```

### 2. **Descargar Artifacts**

Si el workflow genera reportes, puedes descargarlos:
1. Haz clic en el workflow completado
2. Desplázate hasta "Artifacts"
3. Descarga el archivo

### 3. **Crear una Rama de Desarrollo**

```bash
git checkout -b develop
git push -u origin develop
```

Luego harás Pull Requests para mergear a `main`

---

## 🎉 Indicador de Éxito

Cuando todo está bien, en GitHub verás:

```
✅ All checks passed
```

Y en tu README o perfil, verás un badge verde:

![image](https://img.shields.io/badge/build-passing-brightgreen)

---

## 📞 Próximos Pasos

1. ✅ Push el código
2. ✅ Espera a que se ejecute el workflow (5-15 min)
3. ✅ Revisa que todos los jobs pasaron
4. ✅ Comparte el link del repositorio

¡Tu proyecto está listo para producción! 🚀

---

**Última actualización:** Noviembre 15, 2025
**Versión:** 1.0
