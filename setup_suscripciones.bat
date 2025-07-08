@echo off
echo ========================================
echo   CONFIGURANDO SUSCRIPCIONES AXYOMA
echo ========================================
echo.

REM Cambiar al directorio Backend
cd /d "%~dp0Backend"

REM Verificar que estamos en el directorio correcto
if not exist "manage.py" (
    echo [ERROR] No se encontro manage.py. Verifica que estas en el directorio correcto.
    pause
    exit /b 1
)

echo [1] Creando migraciones para suscripciones...
python manage.py makemigrations subscriptions
if errorlevel 1 (
    echo [WARNING] Error en makemigrations subscriptions, continuando...
)

echo [2] Aplicando migraciones...
python manage.py migrate
if errorlevel 1 (
    echo [ERROR] Error en migrate
    pause
    exit /b 1
)

echo [3] Creando planes de ejemplo...
python manage.py crear_planes_ejemplo
if errorlevel 1 (
    echo [ERROR] Error creando planes de ejemplo
    pause
    exit /b 1
)

echo.
echo ========================================
echo   CONFIGURACION COMPLETADA
echo ========================================
echo.
echo Los planes de suscripcion han sido creados:
echo - Plan Basico ($299/mes)
echo - Plan Profesional ($599/mes)  
echo - Plan Enterprise ($1299/mes)
echo - Plan Prueba (Gratis)
echo.
pause
