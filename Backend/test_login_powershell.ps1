$uri = "http://localhost:8000/api/auth/login/"
$body = @{
    username = "axis"
    password = "123"
} | ConvertTo-Json

$headers = @{
    "Content-Type" = "application/json"
}

Write-Host "🧪 PROBANDO LOGIN AXIS CON POWERSHELL" -ForegroundColor Cyan
Write-Host "=" * 50

try {
    $response = Invoke-RestMethod -Uri $uri -Method Post -Body $body -Headers $headers -TimeoutSec 10
    
    Write-Host "✅ LOGIN EXITOSO" -ForegroundColor Green
    Write-Host "👤 Usuario: $($response.usuario)" -ForegroundColor Yellow
    Write-Host "🏢 Empresa: $($response.nombre_empresa)" -ForegroundColor Yellow
    Write-Host "🎯 Dashboard: $($response.tipo_dashboard)" -ForegroundColor Yellow
    Write-Host "🔑 Token: $($response.token.Substring(0, 20))..." -ForegroundColor Yellow
    
    if ($response.empresa_suspendida) {
        Write-Host "⚠️ EMPRESA SUSPENDIDA: SI" -ForegroundColor Red
        if ($response.advertencia) {
            Write-Host "📢 Advertencia: $($response.advertencia.mensaje)" -ForegroundColor Red
        }
    } else {
        Write-Host "✅ EMPRESA ACTIVA: SI" -ForegroundColor Green
    }
    
    Write-Host "`n🎉 ¡EL LOGIN FUNCIONA CORRECTAMENTE!" -ForegroundColor Green
    Write-Host "✅ Credenciales confirmadas:" -ForegroundColor Green
    Write-Host "   Usuario: axis" -ForegroundColor White
    Write-Host "   Contraseña: 123" -ForegroundColor White
    
} catch {
    Write-Host "❌ ERROR EN LOGIN:" -ForegroundColor Red
    Write-Host $_.Exception.Message -ForegroundColor Red
    
    if ($_.Exception.Response) {
        $statusCode = $_.Exception.Response.StatusCode.value__
        Write-Host "📊 Status Code: $statusCode" -ForegroundColor Yellow
        
        if ($statusCode -eq 401) {
            Write-Host "🔐 Credenciales inválidas - Verificando..." -ForegroundColor Yellow
        }
    }
}
