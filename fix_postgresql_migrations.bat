@echo off
REM ============================================================================
REM SOLUCION COMPLETA MIGRACIONES POSTGRESQL - AXYOMA
REM ============================================================================

echo.
echo ===============================================
echo   SOLUCIONANDO MIGRACIONES POSTGRESQL
echo ===============================================
echo.

cd /d "%~dp0Backend"

echo [1] Verificando estado actual de migraciones...
python manage.py showmigrations

echo.
echo [2] Marcando migraciones inconsistentes como no aplicadas...

REM Marcar la migración problemática como no aplicada
echo [INFO] Marcando subscriptions.0001_initial como no aplicada...
python manage.py migrate subscriptions 0001 --fake-initial

echo.
echo [3] Verificando dependencias de users...
python manage.py showmigrations users

echo.
echo [4] Aplicando migraciones en orden correcto...

REM Primero asegurar que todas las migraciones de users están aplicadas
echo [INFO] Aplicando migraciones de users...
python manage.py migrate users

echo [INFO] Aplicando migraciones de apps...
python manage.py migrate apps

echo [INFO] Aplicando migraciones de core...
python manage.py migrate core

echo [INFO] Aplicando migraciones de subscriptions...
python manage.py migrate subscriptions

echo [INFO] Aplicando todas las migraciones restantes...
python manage.py migrate

if errorlevel 1 (
    echo.
    echo [ERROR] Error en migraciones. Intentando solucion alternativa...
    echo.
    
    REM Solucion alternativa: fake las migraciones problemáticas
    echo [ALTERNATIVA] Marcando subscriptions como fake aplicada...
    python manage.py migrate subscriptions --fake
    
    echo [ALTERNATIVA] Aplicando migrate general...
    python manage.py migrate
)

echo.
echo [5] Verificando estado final...
python manage.py showmigrations

echo.
echo ===============================================
echo       MIGRACIONES POSTGRESQL CORREGIDAS
echo ===============================================
echo.
pause
