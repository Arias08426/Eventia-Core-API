# 🚀 Guía Completa: Ejecutar GitHub Actions

## 📋 Tabla de Contenidos
1. [Requisitos Previos](#requisitos-previos)
2. [Paso 1: Preparar tu Repositorio Local](#paso-1-preparar-tu-repositorio-local)
3. [Paso 2: Crear Repositorio en GitHub](#paso-2-crear-repositorio-en-github)
4. [Paso 3: Hacer Push del Código](#paso-3-hacer-push-del-código)
5. [Paso 4: Configurar GitHub Secrets (Opcional)](#paso-4-configurar-github-secrets-opcional)
6. [Paso 5: Monitorear la Ejecución](#paso-5-monitorear-la-ejecución)
7. [Solucionar Problemas](#solucionar-problemas)

---

## ✅ Requisitos Previos

Antes de comenzar, asegúrate de tener:

- [ ] **Git instalado** en tu sistema
- [ ] **Cuenta de GitHub** (gratuita)
- [ ] **Acceso a tu repositorio local** (Eventia Core API)
- [ ] **Credenciales de GitHub configuradas** en tu máquina

---

## Paso 1: Preparar tu Repositorio Local

### 1.1 Abre PowerShell y navega a tu proyecto

```powershell
cd "C:\Users\Usuario\Desktop\Eventia Core API"
```

### 1.2 Verifica que tienes Git configurado

```powershell
git config --list
```

Si no está configurado, ejecuta:

```powershell
git config --global user.name "Tu Nombre"
git config --global user.email "tu@email.com"
```

### 1.3 Inicializa el repositorio local (si no lo has hecho)

```powershell
git init
git add .
git commit -m "Initial commit: Eventia Core API"
```

---

## Paso 2: Crear Repositorio en GitHub

### 2.1 Ve a GitHub y crea un nuevo repositorio

1. Abre https://github.com/new
2. Llena los datos:
   - **Repository name**: `eventia-core-api`
   - **Description**: `API de gestión de eventos - Eventia Core`
   - **Visibility**: Selecciona **Public** o **Private**
   - **Initialize repository**: Déjalo vacío (ya tenemos código)

3. Haz clic en **Create repository**

### 2.2 Copia la URL de tu repositorio

Deberías ver algo como:
```
https://github.com/TU_USUARIO/eventia-core-api.git
```

---

## Paso 3: Hacer Push del Código

### 3.1 En PowerShell, ejecuta estos comandos

```powershell
# Agrega el remoto
git remote add origin https://github.com/TU_USUARIO/eventia-core-api.git

# Renombra la rama a main (si es necesario)
git branch -M main

# Hace push del código
git push -u origin main
```

**Nota**: Si te pide credenciales:
- Usa tu usuario de GitHub
- Para la contraseña, crea un **Personal Access Token** (PAT) en GitHub

### 3.2 Crear Personal Access Token (si es necesario)

1. Ve a https://github.com/settings/tokens
2. Haz clic en **Generate new token** → **Generate new token (classic)**
3. Configura:
   - **Token name**: `GitHub Actions`
   - **Expiration**: 90 days
   - **Scopes**: Selecciona `repo` (acceso completo)
4. Haz clic en **Generate token**
5. **Copia el token** (aparece una sola vez)
6. Usa este token como contraseña al hacer push

---

## Paso 4: Configurar GitHub Secrets (Opcional)

Si necesitas configurar secretos para bases de datos en producción:

### 4.1 En GitHub, ve a tu repositorio

1. **Settings** → **Secrets and variables** → **Actions**

### 4.2 Agrega los secretos que necesites

| Nombre | Valor | Uso |
|--------|-------|-----|
| `CODECOV_TOKEN` | Tu token de Codecov | Para reportes de cobertura |
| `DATABASE_URL` | URL de BD en producción | Tests de integración |
| `REDIS_URL` | URL de Redis en producción | Tests de integración |

**Nota**: Para testing, usamos valores hardcodeados que son seguros.

---

## Paso 5: Monitorear la Ejecución

### 5.1 Accede a GitHub Actions

1. Ve a tu repositorio: `https://github.com/TU_USUARIO/eventia-core-api`
2. Haz clic en la pestaña **Actions**

### 5.2 Verás el workflow ejecutándose

Deberías ver:
```
✅ Eventia Core API: Todos los requisitos...
├── Code Quality Checks (en ejecución o completado)
├── Security Checks (en cola)
├── Unit Tests (en cola)
├── Integration Tests (en cola)
├── System Tests (en cola)
└── Final Report (en cola)
```

### 5.3 Interpretar los resultados

| Estado | Significado |
|--------|------------|
| 🟡 **In Progress** | Ejecutándose |
| 🟢 **Completed** | Exitoso ✅ |
| 🔴 **Failed** | Error ❌ |
| ⚫ **Skipped** | Saltado (normal para Redis) |

---

## 🔍 Solucionar Problemas

### Problema: "Failed to authenticate"

**Solución**:
```powershell
git config --global credential.helper wincred
git remote set-url origin https://TU_USUARIO:TU_TOKEN@github.com/TU_USUARIO/eventia-core-api.git
git push -u origin main
```

### Problema: "Everything up-to-date"

**Solución**: Ya subiste el código. Haz cambios y commits nuevos:
```powershell
git add .
git commit -m "Test commit"
git push
```

### Problema: "Branch protection rule"

**Solución**: En GitHub Settings → Branches → Main, desactiva las reglas de protección para testing.

### Problema: Tests fallan en GitHub Actions

**Verificar**:
1. ¿Funcionan localmente?
   ```powershell
   pytest tests/
   ```
2. ¿Están las variables de entorno?
3. ¿Las dependencias están en `requirements.txt`?

---

## 📊 Entender los Jobs

### Job 1: Code Quality Checks ✅
- **Black**: Formatea el código
- **isort**: Ordena imports
- **Flake8**: Busca errores
- **MyPy**: Valida tipos

### Job 2: Security Checks 🔐
- **Bandit**: Busca vulnerabilidades
- **Safety**: Revisa dependencias inseguras

### Job 3-5: Tests 🧪
- **Unit Tests**: Pruebas unitarias
- **Integration Tests**: Pruebas con BD y caché
- **System Tests**: Pruebas end-to-end

### Job 6: Final Report 📋
- Resumen de todos los resultados

---

## 🎯 Próximos Pasos

Una vez que todo funcione:

1. **Protege tu rama main**:
   - Settings → Branches → Add rule
   - Require status checks to pass

2. **Configura Deploy automático** (opcional):
   - Agrega job de deploy a producción

3. **Integra con Codecov**:
   - Registra tu repo en https://codecov.io
   - Copia el token y agrégalo como secret

---

## 📞 Ayuda

Si algo no funciona:

1. Revisa los logs en GitHub Actions
2. Ejecuta los tests localmente: `pytest tests/ -v`
3. Valida la configuración: `git remote -v`

**¡Éxito! 🚀**
