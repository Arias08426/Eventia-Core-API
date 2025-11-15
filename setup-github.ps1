# Script para automatizar la configuración de GitHub Actions
# Ejecuta: .\setup-github.ps1

Write-Host "╔════════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║   Eventia Core API - GitHub Actions Setup                     ║" -ForegroundColor Cyan
Write-Host "╚════════════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

# Paso 1: Verificar Git
Write-Host "📋 Paso 1: Verificando Git..." -ForegroundColor Yellow
$gitVersion = git --version
if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Git instalado: $gitVersion" -ForegroundColor Green
} else {
    Write-Host "❌ Git no está instalado. Instálalo desde: https://git-scm.com" -ForegroundColor Red
    exit 1
}

# Paso 2: Verificar configuración de Git
Write-Host ""
Write-Host "📋 Paso 2: Verificando configuración de Git..." -ForegroundColor Yellow
$gitUser = git config --global user.name
$gitEmail = git config --global user.email

if ($gitUser -and $gitEmail) {
    Write-Host "✅ Git configurado como: $gitUser <$gitEmail>" -ForegroundColor Green
} else {
    Write-Host "⚠️  Git no está completamente configurado." -ForegroundColor Yellow
    Write-Host "Configura tu usuario y email:" -ForegroundColor Gray
    $nombre = Read-Host "Tu nombre"
    $email = Read-Host "Tu email"
    git config --global user.name $nombre
    git config --global user.email $email
    Write-Host "✅ Configuración completada" -ForegroundColor Green
}

# Paso 3: Inicializar repositorio local
Write-Host ""
Write-Host "📋 Paso 3: Configurando repositorio local..." -ForegroundColor Yellow

if (Test-Path ".\.git") {
    Write-Host "✅ Repositorio git ya existe" -ForegroundColor Green
} else {
    Write-Host "Inicializando repositorio git..." -ForegroundColor Gray
    git init
    git add .
    git commit -m "Initial commit: Eventia Core API"
    Write-Host "✅ Repositorio inicializado" -ForegroundColor Green
}

# Paso 4: Agregar remoto
Write-Host ""
Write-Host "📋 Paso 4: Configurando remoto de GitHub..." -ForegroundColor Yellow

$remoteUrl = git remote get-url origin 2>$null
if ($remoteUrl) {
    Write-Host "✅ Remoto ya configurado: $remoteUrl" -ForegroundColor Green
} else {
    Write-Host "Ingresa la URL de tu repositorio en GitHub" -ForegroundColor Gray
    Write-Host "Formato: https://github.com/TU_USUARIO/eventia-core-api.git" -ForegroundColor Gray
    $url = Read-Host "URL del repositorio"
    
    if ($url) {
        git remote add origin $url
        Write-Host "✅ Remoto configurado: $url" -ForegroundColor Green
    } else {
        Write-Host "❌ URL no proporcionada" -ForegroundColor Red
        exit 1
    }
}

# Paso 5: Cambiar rama a main
Write-Host ""
Write-Host "📋 Paso 5: Configurando rama principal..." -ForegroundColor Yellow
git branch -M main
Write-Host "✅ Rama renombrada a 'main'" -ForegroundColor Green

# Paso 6: Hacer push
Write-Host ""
Write-Host "📋 Paso 6: Haciendo push del código..." -ForegroundColor Yellow
Write-Host "Esto puede pedirte autenticación..." -ForegroundColor Gray

git push -u origin main

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Código subido exitosamente" -ForegroundColor Green
} else {
    Write-Host "⚠️  Hubo un error al hacer push" -ForegroundColor Yellow
    Write-Host "Verifica tu URL de repositorio y credenciales" -ForegroundColor Gray
}

# Paso 7: Información final
Write-Host ""
Write-Host "╔════════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║                      ✅ ¡COMPLETADO!                         ║" -ForegroundColor Cyan
Write-Host "╚════════════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""
Write-Host "📝 Próximos pasos:" -ForegroundColor Yellow
Write-Host "1. Abre: https://github.com/TU_USUARIO/eventia-core-api" -ForegroundColor Gray
Write-Host "2. Ve a la pestaña 'Actions'" -ForegroundColor Gray
Write-Host "3. Verás tu workflow ejecutándose" -ForegroundColor Gray
Write-Host ""
Write-Host "📊 Monitores de ejecución:" -ForegroundColor Yellow
Write-Host "  • Code Quality Checks - Formatea y valida código" -ForegroundColor Gray
Write-Host "  • Security Checks - Busca vulnerabilidades" -ForegroundColor Gray
Write-Host "  • Unit Tests - Pruebas unitarias" -ForegroundColor Gray
Write-Host "  • Integration Tests - Pruebas con bases de datos" -ForegroundColor Gray
Write-Host "  • System Tests - Pruebas end-to-end" -ForegroundColor Gray
Write-Host ""
Write-Host "💡 Tip: Lee GITHUB_ACTIONS_SETUP.md para más detalles" -ForegroundColor Cyan
Write-Host ""
