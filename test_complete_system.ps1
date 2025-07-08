# Script de prueba completo para el sistema de suscripciones
# Este script prueba el flujo completo: listar planes, crear suscripción, procesar pago

$BASE_URL = "http://localhost:8000"

Write-Host "=== TESTING COMPLETO DEL SISTEMA DE SUSCRIPCIONES ===" -ForegroundColor Green
Write-Host ""

# Función para hacer requests con manejo de errores
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

# 1. Probar endpoint de planes
Write-Host "1. Listando planes disponibles..." -ForegroundColor Yellow
$planes = Invoke-ApiRequest "$BASE_URL/suscripciones/listar_planes/"
if ($planes) {
    Write-Host "✅ Planes obtenidos:" -ForegroundColor Green
    $planes | ConvertTo-Json -Depth 3
} else {
    Write-Host "❌ Error al obtener planes" -ForegroundColor Red
}
Write-Host ""

# 2. Crear una suscripción de prueba
Write-Host "2. Creando suscripción de prueba..." -ForegroundColor Yellow
$suscripcionData = @{
    empresa_id = 1
    plan_id = 1
}
$suscripcion = Invoke-ApiRequest "$BASE_URL/suscripciones/crear_suscripcion/" "POST" $suscripcionData
if ($suscripcion) {
    Write-Host "✅ Suscripción creada:" -ForegroundColor Green
    $suscripcion | ConvertTo-Json -Depth 3
    $suscripcionId = $suscripcion.suscripcion.suscripcion_id
} else {
    Write-Host "❌ Error al crear suscripción" -ForegroundColor Red
    $suscripcionId = $null
}
Write-Host ""

# 3. Procesar pago para la suscripción
if ($suscripcionId) {
    Write-Host "3. Procesando pago para suscripción ID: $suscripcionId..." -ForegroundColor Yellow
    $pagoData = @{
        suscripcion_id = $suscripcionId
        monto_pago = 299.00
        transaccion_id = "TEST-$(Get-Date -Format 'yyyyMMddHHmmss')"
    }
    $pago = Invoke-ApiRequest "$BASE_URL/suscripciones/procesar_pago/" "POST" $pagoData
    if ($pago) {
        Write-Host "✅ Pago procesado:" -ForegroundColor Green
        $pago | ConvertTo-Json -Depth 3
    } else {
        Write-Host "❌ Error al procesar pago" -ForegroundColor Red
    }
} else {
    Write-Host "3. ⚠️ Saltando prueba de pago - no se pudo crear suscripción" -ForegroundColor Yellow
}
Write-Host ""

# 4. Listar suscripciones (debería mostrar la nueva)
Write-Host "4. Listando todas las suscripciones..." -ForegroundColor Yellow
$suscripciones = Invoke-ApiRequest "$BASE_URL/suscripciones/listar_suscripciones/"
if ($suscripciones) {
    Write-Host "✅ Suscripciones obtenidas:" -ForegroundColor Green
    $suscripciones | ConvertTo-Json -Depth 3
} else {
    Write-Host "❌ Error al obtener suscripciones" -ForegroundColor Red
}
Write-Host ""

# 5. Listar pagos (debería mostrar el nuevo)
Write-Host "5. Listando todos los pagos..." -ForegroundColor Yellow
$pagos = Invoke-ApiRequest "$BASE_URL/suscripciones/listar_pagos/"
if ($pagos) {
    Write-Host "✅ Pagos obtenidos:" -ForegroundColor Green
    $pagos | ConvertTo-Json -Depth 3
} else {
    Write-Host "❌ Error al obtener pagos" -ForegroundColor Red
}
Write-Host ""

# 6. Probar información de suscripción de empresa
Write-Host "6. Obteniendo información de suscripción para empresa ID: 1..." -ForegroundColor Yellow
$infoSuscripcion = Invoke-ApiRequest "$BASE_URL/suscripciones/info_suscripcion_empresa/?empresa_id=1"
if ($infoSuscripcion) {
    Write-Host "✅ Información de suscripción obtenida:" -ForegroundColor Green
    $infoSuscripcion | ConvertTo-Json -Depth 3
} else {
    Write-Host "❌ Error al obtener información de suscripción" -ForegroundColor Red
}
Write-Host ""

Write-Host "=== TESTING COMPLETADO ===" -ForegroundColor Green
