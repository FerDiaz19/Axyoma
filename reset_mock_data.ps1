# Script para reiniciar el sistema mock
# Borra todos los datos guardados y reinicia desde cero

$mockDataFile = "c:\xampp2\htdocs\UTT4B\Axyoma2\Backend\apps\mock_data.json"

Write-Host "=== REINICIANDO SISTEMA MOCK ===" -ForegroundColor Yellow

if (Test-Path $mockDataFile) {
    Remove-Item $mockDataFile -Force
    Write-Host "✅ Archivo de datos mock eliminado: $mockDataFile" -ForegroundColor Green
} else {
    Write-Host "ℹ️ No existe archivo de datos mock" -ForegroundColor Cyan
}

Write-Host ""
Write-Host "🔄 Sistema reiniciado. Los siguientes datos están ahora vacíos:" -ForegroundColor Green
Write-Host "  • Suscripciones: 0" -ForegroundColor White
Write-Host "  • Pagos: 0" -ForegroundColor White
Write-Host "  • Planes adicionales: 0" -ForegroundColor White
Write-Host ""
Write-Host "📋 Planes base disponibles (siempre activos):" -ForegroundColor Green
Write-Host "  • Plan Básico (1 Mes) - $299.00" -ForegroundColor White
Write-Host "  • Plan Profesional (3 Meses) - $799.00" -ForegroundColor White  
Write-Host "  • Plan Anual - $2999.00" -ForegroundColor White
Write-Host ""
Write-Host "🚀 Reinicia el servidor backend para aplicar cambios" -ForegroundColor Yellow
