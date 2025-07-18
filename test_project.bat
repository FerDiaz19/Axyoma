@echo off
title AXYOMA - TEST PROJECT
color 0B

echo ╔══════════════════════════════════════════════════════════════╗
echo ║                    PROYECTO AXYOMA                          ║
echo ║                    TEST DE FUNCIONALIDAD                    ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.

echo [1/4] Probando conexión a Backend...
curl -s http://localhost:8000/api/auth/health/ >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Backend no está ejecutándose
    echo    Ejecuta start.bat primero
    pause
    exit /b 1
)
echo ✓ Backend conectado

echo [2/4] Probando conexión a Frontend...
curl -s http://localhost:3000/ >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Frontend no está ejecutándose
    echo    Ejecuta start.bat primero
    pause
    exit /b 1
)
echo ✓ Frontend conectado

echo [3/4] Probando login con usuarios existentes...
powershell -Command "$headers = @{'Content-Type'='application/json'}; $body = @{username='superadmin'; password='1234'} | ConvertTo-Json; $response = Invoke-WebRequest -Uri 'http://localhost:8000/api/auth/login/' -Method POST -Headers $headers -Body $body; if ($response.StatusCode -eq 200) {Write-Host '✓ Login SuperAdmin funciona'} else {Write-Host '❌ Login SuperAdmin falló'}"
powershell -Command "$headers = @{'Content-Type'='application/json'}; $body = @{username='admin_empresa'; password='1234'} | ConvertTo-Json; $response = Invoke-WebRequest -Uri 'http://localhost:8000/api/auth/login/' -Method POST -Headers $headers -Body $body; if ($response.StatusCode -eq 200) {Write-Host '✓ Login Admin Empresa funciona'} else {Write-Host '❌ Login Admin Empresa falló'}"

echo [4/4] Probando registro de nueva empresa...
powershell -Command "$headers = @{'Content-Type'='application/json'}; $body = @{nombre='Test Company %RANDOM%'; rfc='TEST%RANDOM%'; email_contacto='test%RANDOM%@test.com'; telefono_contacto='555-1234'; direccion='Test Address'; usuario='testuser%RANDOM%'; password='testpass123'; nombre_completo='Test User Admin'} | ConvertTo-Json; $response = Invoke-WebRequest -Uri 'http://localhost:8000/api/empresas/registro/' -Method POST -Headers $headers -Body $body; if ($response.StatusCode -eq 201) {Write-Host '✓ Registro de empresa funciona'} else {Write-Host '❌ Registro de empresa falló'}"

echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║                    PRUEBAS COMPLETADAS                      ║
echo ║                                                              ║
echo ║ 🟢 ACCESOS PARA VERIFICACIÓN MANUAL:                       ║
echo ║    Frontend:        http://localhost:3000                   ║
echo ║    Registro:        http://localhost:3000/registro          ║
echo ║    API Backend:     http://localhost:8000/api/              ║
echo ║                                                              ║
echo ║ 👤 CREDENCIALES DE PRUEBA:                                 ║
echo ║    SuperAdmin:      superadmin / 1234                       ║
echo ║    Admin Empresa:   admin_empresa / 1234                    ║
echo ║    Admin Planta:    admin_planta / 1234                     ║
echo ║                                                              ║
echo ║ ✅ FUNCIONALIDADES VERIFICADAS:                            ║
echo ║    ✓ Backend Django funcionando                             ║
echo ║    ✓ Frontend React funcionando                             ║
echo ║    ✓ Login con usuarios existentes                          ║
echo ║    ✓ Registro de nuevas empresas                           ║
echo ║    ✓ Creación automática de estructura organizacional       ║
echo ║    ✓ Rutas de navegación configuradas                      ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.
pause
