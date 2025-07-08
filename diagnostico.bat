@echo off
echo ===== DIAGNÓSTICO DEL SISTEMA AXYOMA =====
echo.
echo Este script te ayudará a identificar por qué los scripts se cierran
echo.

echo [1/5] Verificando Python...
py --version
if %errorlevel% neq 0 (
    echo ❌ Python NO está disponible
    echo    Instala Python desde https://www.python.org/
    echo    IMPORTANTE: Marca "Add Python to PATH" durante la instalación
) else (
    echo ✅ Python OK
)
echo.

echo [2/5] Verificando Node.js...
node --version
if %errorlevel% neq 0 (
    echo ❌ Node.js NO está disponible
    echo    Instala Node.js desde https://nodejs.org/
) else (
    echo ✅ Node.js OK
)
echo.

echo [3/5] Verificando npm...
npm --version
if %errorlevel% neq 0 (
    echo ❌ npm NO está disponible
    echo    Ejecuta: Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
    echo    O reinstala Node.js
) else (
    echo ✅ npm OK
)
echo.

echo [4/5] Verificando PostgreSQL...
psql --version
if %errorlevel% neq 0 (
    echo ❌ PostgreSQL NO está disponible
    echo    Instala PostgreSQL desde https://www.postgresql.org/
    echo    Password recomendado: 123456789
) else (
    echo ✅ PostgreSQL OK
)
echo.

echo [5/5] Verificando políticas de PowerShell...
powershell -Command "Get-ExecutionPolicy -Scope CurrentUser"
echo.

echo ===== VERIFICA LO SIGUIENTE =====
echo.
echo 🔍 Si algún elemento está marcado con ❌:
echo    1. Instálalo siguiendo las instrucciones
echo    2. Reinicia PowerShell
echo    3. Ejecuta este diagnóstico nuevamente
echo.
echo 🔍 Si todo está ✅ pero los scripts se cierran:
echo    1. Ejecuta PowerShell como Administrador
echo    2. Ejecuta: Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
echo    3. Ejecuta setup_project.bat
echo.
echo 📁 Estructura requerida:
if exist "Backend" (echo ✅ Directorio Backend existe) else (echo ❌ Directorio Backend NO existe)
if exist "frontend" (echo ✅ Directorio frontend existe) else (echo ❌ Directorio frontend NO existe)
if exist "setup_project.bat" (echo ✅ Script setup_project.bat existe) else (echo ❌ Script setup_project.bat NO existe)
if exist "iniciar_sistema.bat" (echo ✅ Script iniciar_sistema.bat existe) else (echo ❌ Script iniciar_sistema.bat NO existe)
echo.

echo ===== PRÓXIMOS PASOS =====
echo.
echo 1️⃣ Si este diagnóstico muestra todo ✅:
echo    Ejecuta: setup_project.bat
echo.
echo 2️⃣ Si setup_project.bat funciona:
echo    Ejecuta: iniciar_sistema.bat
echo.
echo 3️⃣ Si aún hay problemas:
echo    Ejecuta los scripts desde PowerShell manualmente:
echo    .\setup_project.bat
echo.
pause
