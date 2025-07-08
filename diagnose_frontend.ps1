# Script para diagnosticar problema de frontend
$BASE_URL = "http://localhost:8000/api"

Write-Host "=== DIAGNÓSTICO DEL PROBLEMA DE FRONTEND ===" -ForegroundColor Green
Write-Host ""

# Función para hacer requests
function Invoke-ApiRequest {
    param($Url, $Method = "GET", $Body = $null)
    try {
        $headers = @{ "Content-Type" = "application/json" }
        if ($Body) {
            $response = Invoke-RestMethod -Uri $Url -Method $Method -Headers $headers -Body ($Body | ConvertTo-Json) -ErrorAction Stop
        } else {
            $response = Invoke-RestMethod -Uri $Url -Method $Method -Headers $headers -ErrorAction Stop
        }
        return $response
    } catch {
        Write-Host "Error: $($_.Exception.Message)" -ForegroundColor Red
        return $null
    }
}

Write-Host "1. Verificando estado actual de empresa 1 (la que usa el frontend)..." -ForegroundColor Yellow
$info = Invoke-ApiRequest "$BASE_URL/suscripciones/info_suscripcion_empresa/?empresa_id=1"
if ($info) {
    Write-Host "✅ Respuesta del backend:" -ForegroundColor Green
    $info | ConvertTo-Json -Depth 3
    Write-Host ""
    
    # Analizar respuesta
    if ($info.tiene_suscripcion -eq $true -and $info.estado -eq "activa") {
        Write-Host "✅ BACKEND CORRECTO: Empresa tiene suscripción activa" -ForegroundColor Green
        Write-Host "   - tiene_suscripcion: $($info.tiene_suscripcion)" -ForegroundColor Green
        Write-Host "   - estado: $($info.estado)" -ForegroundColor Green
        Write-Host "   - dias_restantes: $($info.dias_restantes)" -ForegroundColor Green
        Write-Host ""
        Write-Host "🔍 DIAGNÓSTICO: El backend funciona correctamente" -ForegroundColor Cyan
        Write-Host "❌ PROBLEMA: Debe estar en el frontend" -ForegroundColor Red
        Write-Host ""
        Write-Host "💡 SOLUCIONES A VERIFICAR:" -ForegroundColor Yellow
        Write-Host "   1. ¿El frontend está llamando al endpoint correcto?" -ForegroundColor Yellow
        Write-Host "   2. ¿Hay cache de datos antiguos en localStorage?" -ForegroundColor Yellow
        Write-Host "   3. ¿La lógica del dashboard está evaluando correctamente los datos?" -ForegroundColor Yellow
        Write-Host "   4. ¿Hay errores de CORS o de conexión?" -ForegroundColor Yellow
        
    } else {
        Write-Host "❌ PROBLEMA EN BACKEND: Empresa no tiene suscripción activa" -ForegroundColor Red
        Write-Host "   - tiene_suscripcion: $($info.tiene_suscripcion)" -ForegroundColor Red
        Write-Host "   - estado: $($info.estado)" -ForegroundColor Red
    }
} else {
    Write-Host "❌ ERROR: No se pudo conectar al backend" -ForegroundColor Red
    Write-Host "Verificar que el servidor Django esté corriendo en puerto 8000" -ForegroundColor Red
}

Write-Host ""
Write-Host "2. Verificando datos mock en archivo..." -ForegroundColor Yellow
if (Test-Path "Backend\apps\mock_data.json") {
    $mockData = Get-Content "Backend\apps\mock_data.json" | ConvertFrom-Json
    $empresa1Map = $mockData.empresa_suscripcion_map.'1'
    if ($empresa1Map) {
        $suscripcion = $mockData.suscripciones.$empresa1Map
        Write-Host "✅ Datos mock encontrados para empresa 1:" -ForegroundColor Green
        Write-Host "   - Suscripción ID: $empresa1Map" -ForegroundColor Green
        Write-Host "   - Estado: $($suscripcion.estado)" -ForegroundColor Green
        Write-Host "   - Status: $($suscripcion.status)" -ForegroundColor Green
        Write-Host "   - Plan: $($suscripcion.plan_nombre)" -ForegroundColor Green
        Write-Host "   - Fecha fin: $($suscripcion.fecha_fin)" -ForegroundColor Green
        
        if ($suscripcion.estado -eq "activa" -and $suscripcion.status -eq $true) {
            Write-Host "✅ DATOS MOCK CORRECTOS: La empresa debe aparecer como activa" -ForegroundColor Green
        } else {
            Write-Host "❌ DATOS MOCK INCORRECTOS: La empresa no está activa en los datos" -ForegroundColor Red
        }
    } else {
        Write-Host "❌ Empresa 1 no encontrada en datos mock" -ForegroundColor Red
    }
} else {
    Write-Host "❌ Archivo mock_data.json no encontrado" -ForegroundColor Red
}

Write-Host ""
Write-Host "=== CONCLUSIÓN ===" -ForegroundColor Cyan
Write-Host "Si el backend responde correctamente pero el frontend muestra el botón" -ForegroundColor Cyan
Write-Host "'Activar Suscripción', entonces:" -ForegroundColor Cyan
Write-Host "1. Revisar Console del navegador para errores" -ForegroundColor Cyan
Write-Host "2. Verificar que obtenerSuscripcionActual() funcione en el navegador" -ForegroundColor Cyan
Write-Host "3. Limpiar localStorage del navegador" -ForegroundColor Cyan
Write-Host "4. Refrescar completamente la página" -ForegroundColor Cyan
