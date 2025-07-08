@echo off
REM ============================================================================
REM SETUP BASICO - AXYOMA
REM ============================================================================

echo.
echo ===============================================
echo        SETUP BASICO - AXYOMA
echo ===============================================
echo.
echo Este script ejecutara las migraciones basicas.
echo.
echo Presiona cualquier tecla para continuar...
pause > nul

echo.
echo [INFO] Cambiando al directorio Backend...
cd /d "%~dp0Backend"

if not exist "manage.py" (
    echo [ERROR] No se encontro manage.py en Backend/
    pause
    exit /b 1
)

echo [INFO] Creando migraciones...
python manage.py makemigrations
if errorlevel 1 (
    echo [WARNING] Error en makemigrations, continuando...
)

echo [INFO] Aplicando migraciones...
python manage.py migrate
if errorlevel 1 (
    echo [ERROR] Error en migrate
    pause
    exit /b 1
)

echo [INFO] Configurando suscripciones...
python manage.py crear_planes_ejemplo
if errorlevel 1 (
    echo [WARNING] Error creando planes de ejemplo, continuando...
)

echo.
echo ===============================================
echo        CONFIGURACION COMPLETADA
echo ===============================================
echo.
echo Para iniciar el sistema ejecuta: start_system.bat
echo.
pause
