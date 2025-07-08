$uri = "http://localhost:8000/api/auth/login/"
$body = @{
    username = "admin_empresa1"
    password = "password123"
} | ConvertTo-Json

$headers = @{
    "Content-Type" = "application/json"
}

Write-Host "🧪 PROBANDO LOGIN CON POWERSHELL" -ForegroundColor Cyan
Write-Host "=" * 50

try {
    $response = Invoke-RestMethod -Uri $uri -Method Post -Body $body -Headers $headers
    
    Write-Host "✅ LOGIN EXITOSO" -ForegroundColor Green
    Write-Host "📋 Respuesta completa:" -ForegroundColor Yellow
    $response | ConvertTo-Json -Depth 3 | Write-Host
    
    if ($response.empresa_suspendida) {
        Write-Host "⚠️ EMPRESA SUSPENDIDA: SI" -ForegroundColor Red
    } else {
        Write-Host "✅ EMPRESA ACTIVA: SI" -ForegroundColor Green
    }
    
    if ($response.advertencia) {
        Write-Host "⚠️ ADVERTENCIA:" -ForegroundColor Red
        $response.advertencia | ConvertTo-Json | Write-Host
    } else {
        Write-Host "ℹ️ SIN ADVERTENCIAS" -ForegroundColor Blue
    }
    
} catch {
    Write-Host "❌ ERROR EN LOGIN:" -ForegroundColor Red
    Write-Host $_.Exception.Message -ForegroundColor Red
    if ($_.Exception.Response) {
        $stream = $_.Exception.Response.GetResponseStream()
        $reader = New-Object System.IO.StreamReader($stream)
        $responseBody = $reader.ReadToEnd()
        Write-Host "📋 Respuesta del servidor: $responseBody" -ForegroundColor Yellow
    }
}
