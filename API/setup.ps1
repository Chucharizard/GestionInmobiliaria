# Script de instalacion y configuracion rapida
# Ejecutar en PowerShell desde la carpeta API/

Write-Host "🏗️  Configurando proyecto API - Sistema de Gestion Inmobiliaria" -ForegroundColor Green
Write-Host ""

# Verificar Python
Write-Host "📦 Verificando Python..." -ForegroundColor Cyan
$pythonVersion = python --version 2>&1
if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ $pythonVersion encontrado" -ForegroundColor Green
} else {
    Write-Host "❌ Python no encontrado. Por favor instala Python 3.11+" -ForegroundColor Red
    exit 1
}

# Crear entorno virtual
Write-Host ""
Write-Host "🔧 Creando entorno virtual..." -ForegroundColor Cyan
python -m venv venv

# Activar entorno virtual
Write-Host "✅ Entorno virtual creado" -ForegroundColor Green
Write-Host ""
Write-Host "🔌 Activando entorno virtual..." -ForegroundColor Cyan
.\venv\Scripts\Activate.ps1

# Instalar dependencias
Write-Host ""
Write-Host "📥 Instalando dependencias..." -ForegroundColor Cyan
pip install --upgrade pip
pip install -r requirements.txt

Write-Host ""
Write-Host "✅ Dependencias instaladas correctamente" -ForegroundColor Green

# Verificar archivo .env
Write-Host ""
Write-Host "🔍 Verificando archivo .env..." -ForegroundColor Cyan
if (Test-Path .env) {
    Write-Host "✅ Archivo .env encontrado" -ForegroundColor Green
} else {
    Write-Host "⚠️  Archivo .env no encontrado" -ForegroundColor Yellow
    Write-Host "📝 Copiando .env.example a .env..." -ForegroundColor Cyan
    Copy-Item .env.example .env
    Write-Host "✅ Archivo .env creado" -ForegroundColor Green
    Write-Host ""
    Write-Host "⚠️  IMPORTANTE: Edita el archivo .env con tus credenciales de Supabase" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "=" * 70 -ForegroundColor Cyan
Write-Host "✨ ¡Configuracion completada!" -ForegroundColor Green
Write-Host "=" * 70 -ForegroundColor Cyan
Write-Host ""
Write-Host "📝 Proximos pasos:" -ForegroundColor Cyan
Write-Host "   1. Edita el archivo .env con tus credenciales de Supabase"
Write-Host "   2. Ejecuta: python -m uvicorn app.main:app --reload"
Write-Host "   3. Abre: http://localhost:8000/docs"
Write-Host ""
Write-Host "🚀 Para iniciar el servidor ahora, ejecuta:" -ForegroundColor Green
Write-Host "   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000" -ForegroundColor Yellow
Write-Host ""
