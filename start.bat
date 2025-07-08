@echo off
echo ===== AXYOMA - INICIO COMPLETO =====
echo.

REM Verificar estructura del proyecto
if not exist "Backend" (
    echo ERROR: Directorio Backend no encontrado
    pause
    exit /b 1
)

if not exist "frontend" (
    echo ERROR: Directorio frontend no encontrado
    pause
    exit /b 1
)

REM Verificar Python y Node.js
py --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python no esta instalado
    pause
    exit /b 1
)

node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Node.js no esta instalado
    pause
    exit /b 1
)

REM Verificar entorno virtual
if not exist "Backend\env\Scripts\activate.bat" (
    echo ERROR: Entorno virtual no encontrado
    echo Ejecuta setup_project.bat primero
    pause
    exit /b 1
)

echo ✓ Requisitos verificados
echo.

echo ===== CONFIGURANDO BACKEND =====
cd Backend

echo Activando entorno virtual...
call env\Scripts\activate.bat

echo Ejecutando migraciones...
python manage.py makemigrations >nul 2>&1
python manage.py migrate >nul 2>&1

echo Configurando sistema inicial...
python setup_inicial.py

echo ✓ Backend configurado
cd ..
echo.

echo ===== INICIANDO SERVIDORES =====
echo.
echo [1/2] Iniciando Backend Django en puerto 8000...
start "AXYOMA Backend" cmd /k "cd /d %~dp0Backend && call env\Scripts\activate.bat && python manage.py runserver"

echo [2/2] Esperando 3 segundos e iniciando Frontend React en puerto 3000...
timeout /t 3 /nobreak >nul

cd frontend
start "AXYOMA Frontend" cmd /k "npm start"
cd ..

echo.
echo ===== ✅ SISTEMA AXYOMA INICIADO =====
echo.
echo 🌐 URLs disponibles:
echo    Backend API:  http://localhost:8000/api/
echo    Frontend Web: http://localhost:3000
echo    Admin Django: http://localhost:8000/admin/
echo.
echo 👤 Usuarios y empresa disponibles:
echo    SuperAdmin:     ed-rubio@axyoma.com / 1234
echo    Admin Empresa:  juan.perez@codewave.com / 1234  
echo    Admin Planta:   maria.gomez@codewave.com / 1234
echo    Empresa:        CodeWave Technologies (RFC: CWT240701ABC)
echo    Planta:         Planta Principal
echo.
echo 📊 El sistema está ejecutándose en 2 ventanas separadas:
echo    - Ventana "AXYOMA Backend" (Django)
echo    - Ventana "AXYOMA Frontend" (React)
echo.
echo ⚠️  Para DETENER: Cierra ambas ventanas o presiona Ctrl+C en cada una
echo.
echo 🚀 ¡Listo para usar!
echo.
pause
