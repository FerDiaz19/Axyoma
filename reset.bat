@echo off
title AXYOMA - RESET BASE DE DATOS
color 0C

echo ╔══════════════════════════════════════════════════════════════╗
echo ║                    PROYECTO AXYOMA                          ║
echo ║                RESET DE BASE DE DATOS                       ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.

echo ⚠️  ADVERTENCIA: Este script eliminará todos los datos!
echo.
set /p confirm="¿Estás seguro de que quieres continuar? (s/N): "
if /i not "%confirm%"=="s" (
    echo Operación cancelada.
    pause
    exit /b 0
)

echo.
echo [1/4] Recreando base de datos...
set PGBIN="C:\Program Files\PostgreSQL\17\bin"
set PGPASSWORD=12345678

%PGBIN%\psql -U postgres -c "DROP DATABASE IF EXISTS axyomadb;"
%PGBIN%\psql -U postgres -c "CREATE DATABASE axyomadb;"
if %errorlevel% neq 0 (
    echo ❌ ERROR: No se pudo recrear la base de datos
    pause
    exit /b 1
)
echo ✓ Base de datos recreada

echo [2/4] Eliminando migraciones...
cd Backend
echo Limpiando migraciones de usuarios...
if exist "apps\users\migrations\*.py" (
    for %%f in (apps\users\migrations\*.py) do (
        if not "%%~nxf"=="__init__.py" (
            del "%%f" 2>nul
        )
    )
)
echo Limpiando migraciones de suscripciones...
if exist "apps\subscriptions\migrations\*.py" (
    for %%f in (apps\subscriptions\migrations\*.py) do (
        if not "%%~nxf"=="__init__.py" (
            del "%%f" 2>nul
        )
    )
)
echo Limpiando migraciones de surveys...
if exist "apps\surveys\migrations\*.py" (
    for %%f in (apps\surveys\migrations\*.py) do (
        if not "%%~nxf"=="__init__.py" (
            del "%%f" 2>nul
        )
    )
)
echo ✓ Migraciones eliminadas

echo [3/4] Creando nuevas migraciones...
call env\Scripts\activate.bat
python manage.py makemigrations
python manage.py migrate
if %errorlevel% neq 0 (
    echo ❌ ERROR: Problemas con migraciones
    pause
    exit /b 1
)
echo ✓ Migraciones aplicadas

echo [4/4] Inicializando datos...
python inicializar_sistema.py
echo ✓ Datos inicializados

echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║                    RESET COMPLETADO                         ║
echo ║                                                              ║
echo ║ ✅ ACCIONES REALIZADAS:                                     ║
echo ║    ✓ Base de datos recreada                                 ║
echo ║    ✓ Migraciones regeneradas                                ║
echo ║    ✓ Datos de prueba inicializados                          ║
echo ║                                                              ║
echo ║ 🚀 SIGUIENTE PASO: ejecutar start.bat                      ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.
pause
