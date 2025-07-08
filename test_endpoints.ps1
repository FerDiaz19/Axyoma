# Script de prueba para verificar endpoints de suscripciones
# PowerShell version

Write-Host "=== PROBANDO ENDPOINTS DE SUSCRIPCIONES ===" -ForegroundColor Green

# URL base del API
$BASE_URL = "http://localhost:8000/api"

Write-Host "1. Probando endpoint de planes..." -ForegroundColor Yellow
try {
    $response = Invoke-RestMethod -Uri "$BASE_URL/suscripciones/listar_planes/" -Method GET -ContentType "application/json"
    $response | ConvertTo-Json -Depth 10
} catch {
    Write-Host "Error: $_" -ForegroundColor Red
}

Write-Host "`n2. Probando endpoint de suscripciones..." -ForegroundColor Yellow
try {
    $response = Invoke-RestMethod -Uri "$BASE_URL/suscripciones/listar_suscripciones/" -Method GET -ContentType "application/json"
    $response | ConvertTo-Json -Depth 10
} catch {
    Write-Host "Error: $_" -ForegroundColor Red
}

Write-Host "`n3. Probando endpoint de pagos..." -ForegroundColor Yellow
try {
    $response = Invoke-RestMethod -Uri "$BASE_URL/suscripciones/listar_pagos/" -Method GET -ContentType "application/json"
    $response | ConvertTo-Json -Depth 10
} catch {
    Write-Host "Error: $_" -ForegroundColor Red
}

Write-Host "`n=== FIN DE PRUEBAS ===" -ForegroundColor Green
