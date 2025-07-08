# Script para probar el flujo de suscripción completo
$BASE_URL = "http://localhost:8000/api"

Write-Host "=== TESTING SUBSCRIPTION FLOW ===" -ForegroundColor Green
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

# 1. Verificar información actual de la empresa 1
Write-Host "1. Verificando estado actual de empresa 1..." -ForegroundColor Yellow
$info = Invoke-ApiRequest "$BASE_URL/suscripciones/info_suscripcion_empresa/?empresa_id=1"
if ($info) {
    Write-Host "✅ Estado actual:" -ForegroundColor Green
    $info | ConvertTo-Json -Depth 3
    Write-Host ""
    
    if ($info.tiene_suscripcion -and $info.estado -eq "activa") {
        Write-Host "✅ LA EMPRESA TIENE SUSCRIPCIÓN ACTIVA - NO DEBE MOSTRAR BOTÓN 'ACTIVAR'" -ForegroundColor Green
        Write-Host "   - Días restantes: $($info.dias_restantes)" -ForegroundColor Green
        Write-Host "   - Fecha vencimiento: $($info.fecha_vencimiento)" -ForegroundColor Green
        Write-Host "   - Plan: $($info.suscripcion.plan_nombre)" -ForegroundColor Green
    } else {
        Write-Host "⚠️ LA EMPRESA NO TIENE SUSCRIPCIÓN ACTIVA - DEBE MOSTRAR BOTÓN 'ACTIVAR'" -ForegroundColor Yellow
        Write-Host "   - Estado: $($info.estado)" -ForegroundColor Yellow
        Write-Host "   - Requiere pago: $($info.requiere_pago)" -ForegroundColor Yellow
    }
} else {
    Write-Host "❌ Error al obtener información" -ForegroundColor Red
}

Write-Host ""
Write-Host "=== RESULTADO ESPERADO ===" -ForegroundColor Cyan
Write-Host "El frontend debe detectar que tiene_suscripcion=true y estado='activa'" -ForegroundColor Cyan
Write-Host "Por lo tanto NO debe mostrar el botón 'Activar Suscripción'" -ForegroundColor Cyan
Write-Host "Y SÍ debe mostrar información de suscripción activa" -ForegroundColor Cyan
