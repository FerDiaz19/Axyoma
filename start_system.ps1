# Script principal para iniciar el sistema Axyoma
# Sistema de gestión de empleados con suscripciones

Write-Host "=== AXYOMA - SISTEMA DE GESTIÓN DE EMPLEADOS ===" -ForegroundColor Green
Write-Host ""

# Verificar que los directorios existan
if (!(Test-Path "Backend")) {
    Write-Host "❌ Error: Directorio Backend no encontrado" -ForegroundColor Red
    exit 1
}

if (!(Test-Path "frontend")) {
    Write-Host "❌ Error: Directorio frontend no encontrado" -ForegroundColor Red
    exit 1
}

Write-Host "🚀 Iniciando servidor Django (Backend)..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd Backend; python manage.py runserver"

Write-Host "⏳ Esperando 3 segundos para que inicie el backend..." -ForegroundColor Yellow
Start-Sleep -Seconds 3

Write-Host "🚀 Iniciando servidor React (Frontend)..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd frontend; npm start"

Write-Host ""
Write-Host "✅ Sistema iniciado correctamente!" -ForegroundColor Green
Write-Host ""
Write-Host "🌐 URLs del sistema:" -ForegroundColor Cyan
Write-Host "   Backend (API): http://localhost:8000" -ForegroundColor Cyan
Write-Host "   Frontend:      http://localhost:3000" -ForegroundColor Cyan
Write-Host ""
Write-Host "👤 Usuarios de prueba:" -ForegroundColor Cyan
Write-Host "   SuperAdmin:    superadmin / admin123" -ForegroundColor Cyan
Write-Host "   Admin Empresa: admin / admin123" -ForegroundColor Cyan
Write-Host "   Admin Planta:  planta1 / admin123" -ForegroundColor Cyan
Write-Host ""
Write-Host "💡 Para detener el sistema, cierre ambas ventanas de PowerShell" -ForegroundColor Yellow
