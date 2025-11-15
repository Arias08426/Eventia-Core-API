# setup.ps1 - Script de configuración completo
Write-Host "🚀 Configurando proyecto Eventia..." -ForegroundColor Cyan

# Verificar que estamos en el directorio correcto
if (-not (Test-Path "src")) {
    Write-Host "❌ Error: No estás en el directorio del proyecto" -ForegroundColor Red
    Write-Host "   Ejecuta: cd eventia-core-api" -ForegroundColor Yellow
    exit 1
}

# Crear requirements.txt
Write-Host "`n📝 Creando requirements.txt..." -ForegroundColor Blue
@"
# Framework
fastapi==0.109.0
uvicorn[standard]==0.27.0
pydantic==2.5.3
pydantic-settings==2.1.0

# Database
sqlalchemy==2.0.25
alembic==1.13.1
asyncpg==0.29.0
psycopg2-binary==2.9.9

# Cache
redis==5.0.1

# Utils
python-dotenv==1.0.0
python-multipart==0.0.6
"@ | Out-File -FilePath "requirements.txt" -Encoding UTF8

# Crear requirements-dev.txt
Write-Host "📝 Creando requirements-dev.txt..." -ForegroundColor Blue
@"
# Testing
pytest==7.4.4
pytest-asyncio==0.23.3
pytest-cov==4.1.0
pytest-mock==3.12.0
httpx==0.26.0

# Linting and formatting
black==23.12.1
flake8==7.0.0
isort==5.13.2
mypy==1.8.0

# Security
bandit==1.7.6
safety==3.0.1

# Pre-commit
pre-commit==3.6.0

# Types
types-redis==4.6.0.20240106
"@ | Out-File -FilePath "requirements-dev.txt" -Encoding UTF8

# Crear __init__.py en todos los directorios
Write-Host "`n📁 Creando archivos __init__.py..." -ForegroundColor Blue
$directories = @(
    "src",
    "src/config",
    "src/database",
    "src/cache",
    "src/models",
    "src/schemas",
    "src/services",
    "src/controllers",
    "src/exceptions",
    "src/middleware",
    "tests",
    "tests/unit",
    "tests/integration"
)

foreach ($dir in $directories) {
    if (Test-Path $dir) {
        New-Item -Path "$dir/__init__.py" -ItemType File -Force | Out-Null
    }
}

# Crear configuración de VS Code
Write-Host "`n⚙️ Configurando VS Code..." -ForegroundColor Blue
if (-not (Test-Path ".vscode")) {
    New-Item -Path ".vscode" -ItemType Directory | Out-Null
}

@"
{
  "python.analysis.extraPaths": ["./src"],
  "python.autoComplete.extraPaths": ["./src"],
  "python.analysis.diagnosticSeverityOverrides": {
    "reportMissingImports": "warning"
  },
  "python.analysis.ignore": [".github/workflows"],
  "terminal.integrated.env.windows": {
    "PYTHONPATH": "`${workspaceFolder}/src;`${env:PYTHONPATH}"
  }
}
"@ | Out-File -FilePath ".vscode/settings.json" -Encoding UTF8

# Actualizar pip
Write-Host "`n📦 Actualizando pip..." -ForegroundColor Blue
python -m pip install --upgrade pip --quiet

# Instalar dependencias
Write-Host "`n📦 Instalando dependencias de producción..." -ForegroundColor Blue
pip install -r requirements.txt --quiet

Write-Host "📦 Instalando dependencias de desarrollo..." -ForegroundColor Blue
pip install -r requirements-dev.txt --quiet

# Instalar pre-commit hooks
Write-Host "`n🔨 Instalando pre-commit hooks..." -ForegroundColor Blue
pre-commit install 2>$null

Write-Host "`n✅ ¡Configuración completada!" -ForegroundColor Green
Write-Host "`nPróximos pasos:" -ForegroundColor Cyan
Write-Host "  1. Recarga VS Code: Ctrl+Shift+P -> 'Developer: Reload Window'" -ForegroundColor White
Write-Host "  2. Selecciona el intérprete: Ctrl+Shift+P -> 'Python: Select Interpreter' -> .venv" -ForegroundColor White
Write-Host "  3. Ejecuta: make test" -ForegroundColor White