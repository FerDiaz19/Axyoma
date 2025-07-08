# Script para simular flujo completo: Sin suscripción -> Crear -> Pagar -> Activar
$BASE_URL = "http://localhost:8000/api"

Write-Host "=== SIMULACIÓN FLUJO COMPLETO DE SUSCRIPCIÓN ===" -ForegroundColor Green
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

# Usaremos empresa ID 5 para este test
$empresaId = 5

Write-Host "PASO 1: Verificando estado inicial de empresa $empresaId..." -ForegroundColor Yellow
$info = Invoke-ApiRequest "$BASE_URL/suscripciones/info_suscripcion_empresa/?empresa_id=$empresaId"
if ($info) {
    Write-Host "Estado inicial:" -ForegroundColor Cyan
    Write-Host "  - Tiene suscripción: $($info.tiene_suscripcion)" -ForegroundColor Cyan
    Write-Host "  - Estado: $($info.estado)" -ForegroundColor Cyan
    Write-Host "  - Requiere pago: $($info.requiere_pago)" -ForegroundColor Cyan
    
    if ($info.tiene_suscripcion -and $info.estado -eq "activa") {
        Write-Host "Empresa ya tiene suscripcion activa. Saltando creacion..." -ForegroundColor Yellow
        exit
    }
}
Write-Host ""

Write-Host "PASO 2: Creando nueva suscripción..." -ForegroundColor Yellow
$suscripcionData = @{
    empresa_id = $empresaId
    plan_id = 1  # Plan básico mensual
}
$suscripcion = Invoke-ApiRequest "$BASE_URL/suscripciones/crear_suscripcion/" "POST" $suscripcionData
if ($suscripcion) {
    Write-Host "✅ Suscripción creada:" -ForegroundColor Green
    $suscripcionId = $suscripcion.suscripcion.suscripcion_id
    Write-Host "  - ID: $suscripcionId" -ForegroundColor Green
    Write-Host "  - Estado: $($suscripcion.suscripcion.estado)" -ForegroundColor Green
    Write-Host "  - Plan: $($suscripcion.suscripcion.plan_nombre)" -ForegroundColor Green
} else {
    Write-Host "❌ Error al crear suscripción" -ForegroundColor Red
    exit
}
Write-Host ""

Write-Host "PASO 3: Verificando estado después de crear suscripción..." -ForegroundColor Yellow
$info = Invoke-ApiRequest "$BASE_URL/suscripciones/info_suscripcion_empresa/?empresa_id=$empresaId"
if ($info) {
    Write-Host "Estado después de crear:" -ForegroundColor Cyan
    Write-Host "  - Tiene suscripción: $($info.tiene_suscripcion)" -ForegroundColor Cyan
    Write-Host "  - Estado: $($info.estado)" -ForegroundColor Cyan
    Write-Host "  - Requiere pago: $($info.requiere_pago)" -ForegroundColor Cyan
    
    if (!$info.tiene_suscripcion -and $info.estado -eq "pendiente_pago") {
        Write-Host "Correcto: Suscripcion pendiente de pago - Frontend debe mostrar boton Activar" -ForegroundColor Green
    }
}
Write-Host ""

Write-Host "PASO 4: Procesando pago..." -ForegroundColor Yellow
$pagoData = @{
    suscripcion_id = $suscripcionId
    monto_pago = 299.00
    transaccion_id = "TEST-" + (Get-Random -Maximum 9999)
}
$pago = Invoke-ApiRequest "$BASE_URL/suscripciones/procesar_pago/" "POST" $pagoData
if ($pago) {
    Write-Host "✅ Pago procesado:" -ForegroundColor Green
    Write-Host "  - ID: $($pago.pago.pago_id)" -ForegroundColor Green
    Write-Host "  - Monto: $($pago.pago.monto_pago)" -ForegroundColor Green
    Write-Host "  - Estado: $($pago.pago.estado_pago)" -ForegroundColor Green
} else {
    Write-Host "❌ Error al procesar pago" -ForegroundColor Red
    exit
}
Write-Host ""

Write-Host "PASO 5: Verificando estado FINAL después del pago..." -ForegroundColor Yellow
$info = Invoke-ApiRequest "$BASE_URL/suscripciones/info_suscripcion_empresa/?empresa_id=$empresaId"
if ($info) {
    Write-Host "Estado FINAL:" -ForegroundColor Cyan
    Write-Host "  - Tiene suscripción: $($info.tiene_suscripcion)" -ForegroundColor Cyan
    Write-Host "  - Estado: $($info.estado)" -ForegroundColor Cyan
    Write-Host "  - Requiere pago: $($info.requiere_pago)" -ForegroundColor Cyan
    Write-Host "  - Días restantes: $($info.dias_restantes)" -ForegroundColor Cyan
    Write-Host "  - Fecha vencimiento: $($info.fecha_vencimiento)" -ForegroundColor Cyan
    
    if ($info.tiene_suscripcion -and $info.estado -eq "activa") {
        Write-Host ""
        Write-Host "EXITO! LA SUSCRIPCION ESTA ACTIVA" -ForegroundColor Green
        Write-Host "Frontend debe mostrar:" -ForegroundColor Green
        Write-Host "  - Badge ACTIVA en header" -ForegroundColor Green
        Write-Host "  - Informacion de suscripcion activa" -ForegroundColor Green
        Write-Host "  - NO mostrar boton Activar Suscripcion" -ForegroundColor Green
        Write-Host "  - Acceso completo a todas las funciones" -ForegroundColor Green
    } else {
        Write-Host ""
        Write-Host "PROBLEMA: La suscripcion no se activo automaticamente" -ForegroundColor Red
        Write-Host "Verificar logica de activacion en el backend" -ForegroundColor Red
    }
}

Write-Host ""
Write-Host "=== TESTING COMPLETADO ===" -ForegroundColor Green
