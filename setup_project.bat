@echo off
color 0A
title AXYOMA - Configuración del Sistema
echo.
echo =========================================
echo CONFIGURACIÓN DEL SISTEMA AXYOMA
echo =========================================
echo.

setlocal enabledelayedexpansion

echo [1/8] Verificando requisitos del sistema...
echo.

REM Verificar Python
echo Verificando Python...
py --version >nul 2>nul
if %errorlevel% neq 0 (
    echo ERROR: Python no está instalado
    echo Instala Python desde https://www.python.org/downloads/
    pause
    exit /b 1
)
echo OK: Python instalado

REM Verificar Node.js
echo Verificando Node.js...
node --version >nul 2>nul
if %errorlevel% neq 0 (
    echo ERROR: Node.js no está instalado
    echo Instala Node.js desde https://nodejs.org/
    pause
    exit /b 1
)
echo OK: Node.js instalado

REM Verificar PostgreSQL
echo Verificando PostgreSQL...
psql --version >nul 2>nul
if %errorlevel% neq 0 (
    echo ERROR: PostgreSQL no está instalado
    echo Instala PostgreSQL desde https://www.postgresql.org/download/windows/
    pause
    exit /b 1
)
echo OK: PostgreSQL instalado

echo.
echo [2/8] Verificando conectividad a PostgreSQL...
set PGPASSWORD=123456789
echo SELECT 1; | psql -h localhost -U postgres -d postgres >nul 2>nul
if %errorlevel% neq 0 (
    echo ERROR: No se puede conectar a PostgreSQL
    echo Verifica que PostgreSQL esté ejecutándose y que el usuario postgres tenga password: 123456789
    pause
    exit /b 1
)
echo OK: Conexión a PostgreSQL exitosa

echo.
echo [3/8] Verificando/creando base de datos...
echo SELECT 1; | psql -h localhost -U postgres -d axyomadb >nul 2>nul
if %errorlevel% neq 0 (
    echo Base de datos axyomadb no existe, creándola...
    echo CREATE DATABASE axyomadb; | psql -h localhost -U postgres -d postgres >nul 2>nul
    if %errorlevel% neq 0 (
        echo ERROR: No se pudo crear la base de datos
        pause
        exit /b 1
    )
    echo OK: Base de datos axyomadb creada
) else (
    echo OK: Base de datos axyomadb ya existe
)

echo.
echo [4/8] Configurando entorno Python...
cd Backend
if not exist "env" (
    echo Creando entorno virtual...
    py -m venv env
    if %errorlevel% neq 0 (
        echo ERROR: No se pudo crear el entorno virtual
        pause
        exit /b 1
    )
)
echo OK: Entorno virtual listo

echo.
echo [5/8] Instalando dependencias Python...
call env\Scripts\activate.bat
py -m pip install --upgrade pip --quiet
py -m pip install -r requirements.txt --quiet
if %errorlevel% neq 0 (
    echo ERROR: No se pudieron instalar las dependencias de Python
    pause
    exit /b 1
)
echo OK: Dependencias Python instaladas

echo.
echo [6/8] Instalando dependencias Node.js...
cd ..\frontend
npm install --silent
if %errorlevel% neq 0 (
    echo ERROR: No se pudieron instalar las dependencias de Node.js
    pause
    exit /b 1
)
echo OK: Dependencias Node.js instaladas

echo.
echo [7/8] Configurando base de datos...
cd ..\Backend
call env\Scripts\activate.bat
py manage.py makemigrations --verbosity=0
py manage.py migrate --verbosity=0
if %errorlevel% neq 0 (
    echo ERROR: No se pudieron ejecutar las migraciones
    pause
    exit /b 1
)
echo OK: Migraciones ejecutadas

echo.
echo [8/8] Creando datos iniciales...
py create_initial_data.py
if %errorlevel% neq 0 (
    echo ADVERTENCIA: Algunos datos pueden no haberse creado
    echo Esto es normal si ya existen datos previos
) else (
    echo OK: Datos iniciales creados
)

cd ..

echo.
echo =========================================
echo CONFIGURACIÓN COMPLETADA EXITOSAMENTE
echo =========================================
echo.
echo El sistema está listo para usar.
echo.
echo Para iniciar el sistema ejecuta: iniciar_sistema.bat
echo Luego ve a: http://localhost:3000
echo.
echo Usuarios de prueba:
echo   SuperAdmin: ed-rubio@axyoma.com / 1234
echo   Admin Empresa: juan.perez@codewave.com / 1234
echo   Admin Planta: maria.gomez@codewave.com / 1234
echo.
pause
