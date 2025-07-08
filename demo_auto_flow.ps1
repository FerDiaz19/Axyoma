# Demo del flujo automático de suscripciones
# Muestra cómo el sistema debe funcionar automáticamente

$BASE_URL = "http://localhost:8000"

Write-Host "=== DEMO DEL FLUJO AUTOMÁTICO DE SUSCRIPCIONES ===" -ForegroundColor Green
Write-Host "Este script demuestra cómo el sistema debe funcionar automáticamente:" -ForegroundColor Cyan
Write-Host "• Sin suscripción = Estado Suspendido" -ForegroundColor White
Write-Host "• Con pago = Estado Activo automáticamente" -ForegroundColor White
Write-Host "• SuperAdmin ve detalles completos" -ForegroundColor White
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

# 1. Estado inicial (debe mostrar suspendido)
Write-Host "1. 🔍 VERIFICANDO ESTADO INICIAL..." -ForegroundColor Yellow
$estadoInicial = Invoke-ApiRequest "$BASE_URL/suscripciones/info_suscripcion_empresa/?empresa_id=1"
if ($estadoInicial) {
    Write-Host "📊 Estado inicial de Empresa ID 1:" -ForegroundColor Cyan
    Write-Host "   • Tiene suscripción: $($estadoInicial.tiene_suscripcion)" -ForegroundColor $(if($estadoInicial.tiene_suscripcion) { "Green" } else { "Red" })
    Write-Host "   • Estado: $($estadoInicial.estado)" -ForegroundColor $(if($estadoInicial.estado -eq "activa") { "Green" } else { "Yellow" })
    Write-Host "   • Requiere pago: $($estadoInicial.requiere_pago)" -ForegroundColor $(if($estadoInicial.requiere_pago) { "Red" } else { "Green" })
    Write-Host "   • Mensaje: $($estadoInicial.mensaje)" -ForegroundColor White
    
    if ($estadoInicial.requiere_pago) {
        Write-Host "   ✅ CORRECTO: Sin suscripción = Estado suspendido" -ForegroundColor Green
    } else {
        Write-Host "   ❌ PROBLEMA: Debería requerir pago" -ForegroundColor Red
    }
}
Write-Host ""

# 2. Proceso automático de suscripción + pago
Write-Host "2. 🔄 PROCESO AUTOMÁTICO: SUSCRIPCIÓN + PAGO..." -ForegroundColor Yellow

# Crear suscripción
Write-Host "   📝 Creando suscripción..." -ForegroundColor Cyan
$suscripcionData = @{
    empresa_id = 1
    plan_id = 1
}
$suscripcion = Invoke-ApiRequest "$BASE_URL/suscripciones/crear_suscripcion/" "POST" $suscripcionData

if ($suscripcion) {
    $suscripcionId = $suscripcion.suscripcion.suscripcion_id
    Write-Host "   ✅ Suscripción creada (ID: $suscripcionId) - Estado: $($suscripcion.suscripcion.estado)" -ForegroundColor Green
    
    # Procesar pago automáticamente
    Write-Host "   💳 Procesando pago automático..." -ForegroundColor Cyan
    $pagoData = @{
        suscripcion_id = $suscripcionId
        monto_pago = 299.00
        transaccion_id = "AUTO-$(Get-Date -Format 'yyyyMMddHHmmss')"
    }
    $pago = Invoke-ApiRequest "$BASE_URL/suscripciones/procesar_pago/" "POST" $pagoData
    
    if ($pago) {
        Write-Host "   ✅ Pago procesado (ID: $($pago.pago.pago_id)) - Estado: $($pago.pago.estado_pago)" -ForegroundColor Green
    }
}
Write-Host ""

# 3. Verificar estado después del pago (debe estar activo)
Write-Host "3. ✅ VERIFICANDO ESTADO DESPUÉS DEL PAGO..." -ForegroundColor Yellow
$estadoFinal = Invoke-ApiRequest "$BASE_URL/suscripciones/info_suscripcion_empresa/?empresa_id=1"
if ($estadoFinal) {
    Write-Host "📊 Estado final de Empresa ID 1:" -ForegroundColor Cyan
    Write-Host "   • Tiene suscripción: $($estadoFinal.tiene_suscripcion)" -ForegroundColor $(if($estadoFinal.tiene_suscripcion) { "Green" } else { "Red" })
    Write-Host "   • Estado: $($estadoFinal.estado)" -ForegroundColor $(if($estadoFinal.estado -eq "activa") { "Green" } else { "Yellow" })
    Write-Host "   • Requiere pago: $($estadoFinal.requiere_pago)" -ForegroundColor $(if($estadoFinal.requiere_pago) { "Red" } else { "Green" })
    Write-Host "   • Días restantes: $($estadoFinal.dias_restantes)" -ForegroundColor White
    Write-Host "   • Mensaje: $($estadoFinal.mensaje)" -ForegroundColor White
    
    if ($estadoFinal.tiene_suscripcion -and $estadoFinal.estado -eq "activa" -and -not $estadoFinal.requiere_pago) {
        Write-Host "   ✅ PERFECTO: Con pago = Estado activo automáticamente" -ForegroundColor Green
    } else {
        Write-Host "   ❌ PROBLEMA: Estado no se activó automáticamente" -ForegroundColor Red
    }
}
Write-Host ""

# 4. Verificar datos en SuperAdmin
Write-Host "4. 🛠️ VERIFICANDO DATOS EN SUPERADMIN..." -ForegroundColor Yellow

Write-Host "   📋 Suscripciones (para SuperAdmin):" -ForegroundColor Cyan
$suscripciones = Invoke-ApiRequest "$BASE_URL/suscripciones/listar_suscripciones/"
if ($suscripciones -and $suscripciones.Count -gt 0) {
    foreach ($sub in $suscripciones) {
        $diasRestantes = [math]::Ceiling(((Get-Date $sub.fecha_fin) - (Get-Date)).TotalDays)
        $statusIcon = if ($diasRestantes -lt 0) { "❌" } elseif ($diasRestantes -le 7) { "⏰" } else { "✅" }
        
        Write-Host "      $statusIcon ID: $($sub.suscripcion_id) | Empresa: $($sub.empresa_id) | Estado: $($sub.estado) | Días: $diasRestantes" -ForegroundColor White
    }
} else {
    Write-Host "      ⚠️ No hay suscripciones registradas" -ForegroundColor Yellow
}

Write-Host "   💰 Pagos (para SuperAdmin):" -ForegroundColor Cyan
$pagos = Invoke-ApiRequest "$BASE_URL/suscripciones/listar_pagos/"
if ($pagos -and $pagos.Count -gt 0) {
    foreach ($p in $pagos) {
        $statusIcon = if ($p.estado_pago -eq "completado") { "✅" } elseif ($p.estado_pago -eq "pendiente") { "⏳" } else { "❌" }
        
        Write-Host "      $statusIcon ID: $($p.pago_id) | Monto: $($p.monto_pago) | Estado: $($p.estado_pago) | Fecha: $($p.fecha_pago)" -ForegroundColor White
    }
} else {
    Write-Host "      ⚠️ No hay pagos registrados" -ForegroundColor Yellow
}
Write-Host ""

# 5. Resumen y próximos pasos
Write-Host "=== 📊 RESUMEN DEL FLUJO AUTOMÁTICO ===" -ForegroundColor Green

$funcionaCorrectamente = $estadoFinal.tiene_suscripcion -and $estadoFinal.estado -eq "activa" -and -not $estadoFinal.requiere_pago

if ($funcionaCorrectamente) {
    Write-Host "🎉 ¡FLUJO AUTOMÁTICO FUNCIONANDO PERFECTAMENTE!" -ForegroundColor Green
    Write-Host ""
    Write-Host "✅ Estado inicial: Suspendido (sin suscripción)" -ForegroundColor Green
    Write-Host "✅ Después del pago: Activo automáticamente" -ForegroundColor Green
    Write-Host "✅ SuperAdmin: Ve datos actualizados" -ForegroundColor Green
    Write-Host ""
    Write-Host "🌐 PRUEBA EN EL FRONTEND:" -ForegroundColor Cyan
    Write-Host "1. Dashboard empresarial debe mostrar: '✅ ACTIVA (X días)'" -ForegroundColor White
    Write-Host "2. NO debe aparecer botón 'Activar Suscripción'" -ForegroundColor White
    Write-Host "3. Sección 'Reportes' debe estar disponible" -ForegroundColor White
    Write-Host "4. SuperAdmin debe mostrar suscripción activa con días restantes" -ForegroundColor White
    
} else {
    Write-Host "⚠️ FLUJO AUTOMÁTICO NECESITA AJUSTES" -ForegroundColor Yellow
    Write-Host ""
    if (-not $estadoFinal.tiene_suscripcion) {
        Write-Host "❌ Problema: No detecta la suscripción como activa" -ForegroundColor Red
    }
    if ($estadoFinal.requiere_pago) {
        Write-Host "❌ Problema: Sigue requiriendo pago después de procesar" -ForegroundColor Red
    }
    if ($estadoFinal.estado -ne "activa") {
        Write-Host "❌ Problema: Estado no es 'activa' después del pago" -ForegroundColor Red
    }
}

Write-Host ""
Write-Host "📁 ARCHIVOS DE PERSISTENCIA:" -ForegroundColor Cyan
$mockFile = "c:\xampp2\htdocs\UTT4B\Axyoma2\Backend\apps\mock_data.json"
if (Test-Path $mockFile) {
    $size = (Get-Item $mockFile).Length
    Write-Host "✅ mock_data.json existe ($size bytes) - Datos persisten entre reinicios" -ForegroundColor Green
} else {
    Write-Host "⚠️ mock_data.json no existe - Datos se perderán al reiniciar servidor" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "🔄 Para reiniciar la demo: .\reset_mock_data.ps1" -ForegroundColor Gray
