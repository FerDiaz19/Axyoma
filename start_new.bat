@echo off
title AXYOMA - INICIANDO SISTEMA
color 0A

echo ╔══════════════════════════════════════════════════════════════╗
echo ║                    PROYECTO AXYOMA                          ║
echo ║                    INICIO DEL SISTEMA                       ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.

echo [1/4] Verificando requisitos...
cd Backend
if not exist "env" (
    echo ❌ ERROR: Entorno virtual no encontrado
    echo    Ejecuta setup.bat primero
    pause
    exit /b 1
)

if not exist "requirements.txt" (
    echo ❌ ERROR: requirements.txt no encontrado
    pause
    exit /b 1
)

cd ..\frontend
if not exist "package.json" (
    echo ❌ ERROR: package.json no encontrado
    pause
    exit /b 1
)

if not exist "node_modules" (
    echo ❌ ERROR: node_modules no encontrado
    echo    Ejecuta setup.bat primero
    pause
    exit /b 1
)

cd ..
echo ✓ Requisitos verificados

echo [2/4] Verificando conexión a PostgreSQL...
set PGPASSWORD=12345678
echo SELECT 1; | "C:\Program Files\PostgreSQL\17\bin\psql" -U postgres -d axyomadb >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ ERROR: No se puede conectar a PostgreSQL
    echo    Verifica que PostgreSQL esté ejecutándose
    echo    Base de datos: axyomadb, Usuario: postgres, Password: 12345678
    pause
    exit /b 1
)
echo ✓ Conexión a PostgreSQL exitosa

echo [3/4] Preparando Backend...
cd Backend
call env\Scripts\activate.bat

echo Verificando estructura de base de datos...
python -c "import django,os; os.environ.setdefault('DJANGO_SETTINGS_MODULE','config.settings.local'); django.setup(); from django.db import connection; cursor=connection.cursor(); cursor.execute('SELECT 1'); print('✓ Django conectado a DB')" 2>nul || echo "⚠️  Advertencia: Problemas de conexión Django-DB"

echo ✓ Backend preparado

echo [4/4] Iniciando servidores...
echo.

REM Iniciar Backend en segundo plano
echo 🚀 Iniciando Backend Django en puerto 8000...
start "AXYOMA Backend" cmd /c "cd /d %~dp0Backend && call env\Scripts\activate.bat && python manage.py runserver 8000"

REM Esperar un poco para que el backend inicie
echo    Esperando 4 segundos para que el backend inicie...
timeout /t 4 /nobreak >nul

REM Iniciar Frontend en segundo plano
echo 🚀 Iniciando Frontend React en puerto 3000...
start "AXYOMA Frontend" cmd /c "cd /d %~dp0frontend && npm start"

echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║                    SISTEMA INICIADO                         ║
echo ║                                                              ║
echo ║ 🌐 ACCESOS:                                                 ║
echo ║    Frontend React:  http://localhost:3000                  ║
echo ║    Backend Django:  http://localhost:8000                  ║
echo ║    API REST:        http://localhost:8000/api/             ║
echo ║    Admin Django:    http://localhost:8000/admin/           ║
echo ║                                                              ║
echo ║ 👤 USUARIOS DE PRUEBA:                                     ║
echo ║    SuperAdmin:     ed-rubio@axyoma.com / 1234              ║
echo ║    Admin Empresa:  juan.perez@codewave.com / 1234          ║
echo ║    Admin Planta:   maria.gomez@codewave.com / 1234         ║
echo ║                                                              ║
echo ║ 🛑 PARA DETENER:                                           ║
echo ║    Cierra las ventanas "AXYOMA Backend" y "AXYOMA Frontend" ║
echo ║    O usa Ctrl+C en cada ventana                            ║
echo ║                                                              ║
echo ║ 🔄 PARA REINICIAR: ejecutar start.bat de nuevo            ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.
pause
