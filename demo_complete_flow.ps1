# Demo completa del sistema de suscripciones con persistencia
# Muestra el flujo completo: reset → crear suscripción → pagar → verificar persistencia

$BASE_URL = "http://localhost:8000"

Write-Host "=== DEMO COMPLETA DEL SISTEMA DE SUSCRIPCIONES ===" -ForegroundColor Green
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

# 0. Mostrar estado inicial
Write-Host "0. Verificando estado inicial..." -ForegroundColor Yellow
$infoInicial = Invoke-ApiRequest "$BASE_URL/suscripciones/info_suscripcion_empresa/?empresa_id=1"
if ($infoInicial) {
    Write-Host "📊 Estado inicial:" -ForegroundColor Cyan
    Write-Host "   • Tiene suscripción: $($infoInicial.tiene_suscripcion)" -ForegroundColor White
    Write-Host "   • Estado: $($infoInicial.estado)" -ForegroundColor White
    Write-Host "   • Requiere pago: $($infoInicial.requiere_pago)" -ForegroundColor White
    if ($infoInicial.mensaje) {
        Write-Host "   • Mensaje: $($infoInicial.mensaje)" -ForegroundColor White
    }
}
Write-Host ""

# 1. Listar planes disponibles
Write-Host "1. Listando planes disponibles..." -ForegroundColor Yellow
$planes = Invoke-ApiRequest "$BASE_URL/suscripciones/listar_planes/"
if ($planes) {
    Write-Host "✅ Planes disponibles:" -ForegroundColor Green
    foreach ($plan in $planes) {
        Write-Host "   • ID: $($plan.plan_id) - $($plan.nombre) - $($plan.precio) MXN ($($plan.duracion) días)" -ForegroundColor White
    }
}
Write-Host ""

# 2. Crear suscripción al Plan Básico
Write-Host "2. Creando suscripción al Plan Básico (ID: 1)..." -ForegroundColor Yellow
$suscripcionData = @{
    empresa_id = 1
    plan_id = 1
}
$suscripcion = Invoke-ApiRequest "$BASE_URL/suscripciones/crear_suscripcion/" "POST" $suscripcionData
if ($suscripcion) {
    Write-Host "✅ Suscripción creada:" -ForegroundColor Green
    $suscripcionId = $suscripcion.suscripcion.suscripcion_id
    Write-Host "   • ID: $suscripcionId" -ForegroundColor White
    Write-Host "   • Estado: $($suscripcion.suscripcion.estado)" -ForegroundColor White
    Write-Host "   • Plan: $($suscripcion.suscripcion.plan_nombre)" -ForegroundColor White
    Write-Host "   • Fecha inicio: $($suscripcion.suscripcion.fecha_inicio)" -ForegroundColor White
    Write-Host "   • Fecha fin: $($suscripcion.suscripcion.fecha_fin)" -ForegroundColor White
} else {
    Write-Host "❌ Error al crear suscripción" -ForegroundColor Red
    exit 1
}
Write-Host ""

# 3. Verificar estado después de crear suscripción
Write-Host "3. Verificando estado después de crear suscripción..." -ForegroundColor Yellow
$infoPostSuscripcion = Invoke-ApiRequest "$BASE_URL/suscripciones/info_suscripcion_empresa/?empresa_id=1"
if ($infoPostSuscripcion) {
    Write-Host "📊 Estado después de crear suscripción:" -ForegroundColor Cyan
    Write-Host "   • Tiene suscripción: $($infoPostSuscripcion.tiene_suscripcion)" -ForegroundColor White
    Write-Host "   • Estado: $($infoPostSuscripcion.estado)" -ForegroundColor White
    Write-Host "   • Requiere pago: $($infoPostSuscripcion.requiere_pago)" -ForegroundColor White
    Write-Host "   • Mensaje: $($infoPostSuscripcion.mensaje)" -ForegroundColor White
}
Write-Host ""

# 4. Procesar pago
Write-Host "4. Procesando pago para suscripción ID: $suscripcionId..." -ForegroundColor Yellow
$pagoData = @{
    suscripcion_id = $suscripcionId
    monto_pago = 299.00
    transaccion_id = "DEMO-$(Get-Date -Format 'yyyyMMddHHmmss')"
}
$pago = Invoke-ApiRequest "$BASE_URL/suscripciones/procesar_pago/" "POST" $pagoData
if ($pago) {
    Write-Host "✅ Pago procesado exitosamente:" -ForegroundColor Green
    Write-Host "   • ID: $($pago.pago.pago_id)" -ForegroundColor White
    Write-Host "   • Monto: $($pago.pago.monto_pago) MXN" -ForegroundColor White
    Write-Host "   • Estado: $($pago.pago.estado_pago)" -ForegroundColor White
    Write-Host "   • Transacción: $($pago.pago.transaccion_id)" -ForegroundColor White
    Write-Host "   • Fecha: $($pago.pago.fecha_pago)" -ForegroundColor White
} else {
    Write-Host "❌ Error al procesar pago" -ForegroundColor Red
    exit 1
}
Write-Host ""

# 5. Verificar estado final
Write-Host "5. Verificando estado final después del pago..." -ForegroundColor Yellow
$infoFinal = Invoke-ApiRequest "$BASE_URL/suscripciones/info_suscripcion_empresa/?empresa_id=1"
if ($infoFinal) {
    Write-Host "📊 Estado final:" -ForegroundColor Cyan
    Write-Host "   • Tiene suscripción: $($infoFinal.tiene_suscripcion)" -ForegroundColor White
    Write-Host "   • Estado: $($infoFinal.estado)" -ForegroundColor White
    Write-Host "   • Requiere pago: $($infoFinal.requiere_pago)" -ForegroundColor White
    Write-Host "   • Mensaje: $($infoFinal.mensaje)" -ForegroundColor White
    
    if ($infoFinal.dias_restantes) {
        Write-Host "   • Días restantes: $($infoFinal.dias_restantes)" -ForegroundColor White
    }
    if ($infoFinal.fecha_vencimiento) {
        Write-Host "   • Fecha vencimiento: $($infoFinal.fecha_vencimiento)" -ForegroundColor White
    }
}
Write-Host ""

# 6. Verificar persistencia en endpoints
Write-Host "6. Verificando persistencia en todos los endpoints..." -ForegroundColor Yellow

Write-Host "   📋 Suscripciones registradas:" -ForegroundColor Cyan
$suscripciones = Invoke-ApiRequest "$BASE_URL/suscripciones/listar_suscripciones/"
if ($suscripciones -and $suscripciones.Count -gt 0) {
    foreach ($sub in $suscripciones) {
        Write-Host "      • ID: $($sub.suscripcion_id) - Empresa: $($sub.empresa_id) - Estado: $($sub.estado)" -ForegroundColor White
    }
} else {
    Write-Host "      ⚠️ No hay suscripciones registradas" -ForegroundColor Yellow
}

Write-Host "   💰 Pagos registrados:" -ForegroundColor Cyan
$pagos = Invoke-ApiRequest "$BASE_URL/suscripciones/listar_pagos/"
if ($pagos -and $pagos.Count -gt 0) {
    foreach ($p in $pagos) {
        Write-Host "      • ID: $($p.pago_id) - Monto: $($p.monto_pago) - Estado: $($p.estado_pago)" -ForegroundColor White
    }
} else {
    Write-Host "      ⚠️ No hay pagos registrados" -ForegroundColor Yellow
}
Write-Host ""

# 7. Resumen
Write-Host "=== RESUMEN DE LA DEMO ===" -ForegroundColor Green
if ($infoFinal.tiene_suscripcion -eq $true -and $infoFinal.estado -eq "activa") {
    Write-Host "✅ ÉXITO: El sistema funciona correctamente" -ForegroundColor Green
    Write-Host "   • Suscripción creada y activada" -ForegroundColor White
    Write-Host "   • Pago procesado exitosamente" -ForegroundColor White
    Write-Host "   • Estado persistente entre endpoints" -ForegroundColor White
    Write-Host "   • Dashboard empresarial debe mostrar 'Suscripción Activa'" -ForegroundColor White
} else {
    Write-Host "❌ PROBLEMA: El sistema no está funcionando como esperado" -ForegroundColor Red
    Write-Host "   • Revisar logs del servidor" -ForegroundColor White
    Write-Host "   • Verificar persistencia de datos" -ForegroundColor White
}
Write-Host ""
Write-Host "🌐 Prueba en el frontend:" -ForegroundColor Cyan
Write-Host "   1. Ir al dashboard empresarial" -ForegroundColor White
Write-Host "   2. Debe mostrar 'Suscripción activa' en lugar de avisos de pago" -ForegroundColor White
Write-Host "   3. La sección 'Reportes' debe estar disponible" -ForegroundColor White
Write-Host "   4. SuperAdmin debe ver la nueva suscripción y pago" -ForegroundColor White
