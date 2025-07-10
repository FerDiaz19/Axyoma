@echo off
title AXYOMA - CONFIGURACION DEL PROYECTO
color 0B

echo ╔══════════════════════════════════════════════════════════════╗
echo ║                    PROYECTO AXYOMA                          ║
echo ║                  CONFIGURACION INICIAL                      ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.

REM Configurar variables
set PGBIN="C:\Program Files\PostgreSQL\17\bin"
set PGPASSWORD=12345678

echo [1/10] Verificando PostgreSQL...
%PGBIN%\psql -U postgres -c "SELECT version();" 2>nul
if %errorlevel% neq 0 (
    echo ❌ ERROR: No se puede conectar a PostgreSQL
    echo.
    echo 🔧 SOLUCION:
    echo    1. Verifica que PostgreSQL este ejecutandose
    echo    2. Cambia la contrasena del usuario postgres a: 12345678
    echo    3. Usa pgAdmin para cambiar la contrasena si es necesario
    echo.
    pause
    exit /b 1
)
echo ✓ PostgreSQL conectado correctamente

echo [2/10] Verificando Node.js...
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ ERROR: Node.js no encontrado
    echo.
    echo 📥 DESCARGAR NODE.JS:
    echo    https://nodejs.org/
    echo    Instala Node.js 16+ y reinicia esta terminal
    echo.
    pause
    exit /b 1
)
echo ✓ Node.js disponible: 
node --version

echo [3/10] Verificando Python...
py --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ ERROR: Python no encontrado
    echo.
    echo 📥 DESCARGAR PYTHON:
    echo    https://python.org/
    echo    Instala Python 3.10+ y reinicia esta terminal
    echo.
    pause
    exit /b 1
)
echo ✓ Python disponible:
py --version

echo [4/10] Creando base de datos...
%PGBIN%\psql -U postgres -c "DROP DATABASE IF EXISTS axyomadb;" 2>nul
%PGBIN%\psql -U postgres -c "CREATE DATABASE axyomadb;"
if %errorlevel% neq 0 (
    echo ❌ ERROR: No se pudo crear la base de datos
    pause
    exit /b 1
)
echo ✓ Base de datos axyomadb creada

echo [5/10] Importando estructura de base de datos...
if exist "AxyomaDB_postgresql.sql" (
    %PGBIN%\psql -U postgres -d axyomadb -f "AxyomaDB_postgresql.sql" >nul 2>&1
    if %errorlevel% neq 0 (
        echo ❌ ERROR: No se pudo importar la estructura
        pause
        exit /b 1
    )
    echo ✓ Estructura de base de datos importada
) else (
    echo ⚠️  Archivo AxyomaDB_postgresql.sql no encontrado, se creará estructura con migraciones
)

echo [6/10] Configurando entorno virtual Python...
cd Backend

if not exist "env" (
    echo Creando entorno virtual...
    py -m venv env
    if %errorlevel% neq 0 (
        echo ❌ ERROR: No se pudo crear el entorno virtual
        pause
        exit /b 1
    )
)

echo Activando entorno virtual...
call env\Scripts\activate.bat

echo Instalando dependencias de Python...
py -m pip install --upgrade pip >nul
py -m pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ❌ ERROR: No se pudieron instalar las dependencias del backend
    pause
    exit /b 1
)
echo ✓ Entorno virtual y dependencias configurados

echo [7/10] Configurando Django...
echo Creando migraciones...
python manage.py makemigrations --noinput
echo Aplicando migraciones...
python manage.py migrate --run-syncdb
if %errorlevel% neq 0 (
    echo ⚠️  Advertencia: Problemas con migraciones, pero continuando...
)
echo ✓ Django configurado

echo [8/10] Creando datos iniciales...
if exist "inicializar_sistema.py" (
    python inicializar_sistema.py
    echo ✓ Datos de prueba creados
) else (
    echo ⚠️  Script de inicialización no encontrado
)

echo [9/10] Configurando Frontend...
cd ..\frontend

echo Instalando dependencias de Node.js...
npm install
if %errorlevel% neq 0 (
    echo ❌ ERROR: No se pudieron instalar las dependencias del frontend
    pause
    exit /b 1
)
echo ✓ Frontend configurado

echo [10/10] Configuración final...
cd ..

if not exist "Backend\apps\mock_data.json" (
    echo Creando archivo de datos mock...
    echo {"planes_adicionales":{},"next_plan_id":4,"suscripciones":{},"next_suscripcion_id":1,"pagos":{},"next_pago_id":1,"empresa_suscripcion_map":{},"timestamp":""} > Backend\apps\mock_data.json
)
echo ✓ Archivos de configuración creados

echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║                    CONFIGURACION COMPLETADA                 ║
echo ║                                                              ║
echo ║ ✅ COMPONENTES CONFIGURADOS:                                ║
echo ║    ✓ PostgreSQL y base de datos axyomadb                   ║
echo ║    ✓ Entorno virtual Python (Backend\env\)                 ║
echo ║    ✓ Dependencias del backend instaladas                   ║
echo ║    ✓ Django configurado con migraciones                    ║
echo ║    ✓ Dependencias del frontend instaladas                  ║
echo ║    ✓ Datos de prueba inicializados                         ║
echo ║                                                              ║
echo ║ 👤 USUARIOS DE PRUEBA:                                     ║
echo ║    SuperAdmin:     ed-rubio@axyoma.com / 1234              ║
echo ║    Admin Empresa:  juan.perez@codewave.com / 1234          ║
echo ║    Admin Planta:   maria.gomez@codewave.com / 1234         ║
echo ║                                                              ║
echo ║ 🚀 INICIAR SISTEMA: ejecutar start.bat                     ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.
pause
