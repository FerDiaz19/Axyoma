@echo off
<<<<<<< HEAD
echo ===== AXYOMA - CONFIGURACION INICIAL =====

REM Verificar Python
echo [1/7] Verificando Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python no esta instalado o no esta en PATH
    echo Instala Python 3.8+ desde https://python.org
=======
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
>>>>>>> parent of 27737a2 (emoji cara sonrojada)
    pause
    exit /b 1
)
echo OK: Python instalado

REM Verificar Node.js
<<<<<<< HEAD
echo [2/7] Verificando Node.js...
node --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Node.js no esta instalado
    echo Instala Node.js 16+ desde https://nodejs.org
=======
echo Verificando Node.js...
node --version >nul 2>nul
if %errorlevel% neq 0 (
    echo ERROR: Node.js no está instalado
    echo Instala Node.js desde https://nodejs.org/
>>>>>>> parent of 27737a2 (emoji cara sonrojada)
    pause
    exit /b 1
)
echo OK: Node.js instalado

<<<<<<< HEAD
REM Configurar Backend
echo [3/7] Configurando entorno virtual Python...
=======
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
>>>>>>> parent of 27737a2 (emoji cara sonrojada)
cd Backend
if not exist "env" (
    python -m venv env
    if errorlevel 1 (
        echo ERROR: No se pudo crear el entorno virtual
        pause
        exit /b 1
    )
)
echo OK: Entorno virtual listo

<<<<<<< HEAD
echo [4/7] Activando entorno virtual e instalando dependencias...
call env\Scripts\activate.bat
pip install -r requirements.txt
if errorlevel 1 (
=======
echo.
echo [5/8] Instalando dependencias Python...
call env\Scripts\activate.bat
py -m pip install --upgrade pip --quiet
py -m pip install -r requirements.txt --quiet
if %errorlevel% neq 0 (
>>>>>>> parent of 27737a2 (emoji cara sonrojada)
    echo ERROR: No se pudieron instalar las dependencias de Python
    pause
    exit /b 1
)
echo OK: Dependencias Python instaladas

<<<<<<< HEAD
echo [5/7] Configurando base de datos...
python manage.py migrate
if errorlevel 1 (
    echo ERROR: No se pudieron aplicar las migraciones
    echo Verifica que PostgreSQL este corriendo y la BD 'axyomadb' exista
    pause
    exit /b 1
)

echo [6/7] Creando datos iniciales...
python create_initial_data.py

echo [7/7] Configurando Frontend...
cd ..\frontend
npm install
if errorlevel 1 (
=======
echo.
echo [6/8] Instalando dependencias Node.js...
cd ..\frontend
npm install --silent
if %errorlevel% neq 0 (
>>>>>>> parent of 27737a2 (emoji cara sonrojada)
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
<<<<<<< HEAD
echo.
echo ===== CONFIGURACION COMPLETADA =====
echo.
echo Para iniciar el sistema usa: start.bat
=======

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
>>>>>>> parent of 27737a2 (emoji cara sonrojada)
echo.
pause
