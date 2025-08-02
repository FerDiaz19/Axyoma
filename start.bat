@echo off
echo ==========================================
echo       🚀 AXYOMA - INICIADOR COMPLETO
echo ==========================================
echo.
echo Iniciando Frontend (React) y Backend (Django)...
echo.

:: Verificar que estamos en el directorio correcto
if not exist "Backend\manage.py" (
    echo ❌ Error: No se encuentra manage.py en Backend\
    echo Asegurate de ejecutar este script desde la raiz del proyecto
    pause
    exit /b 1
)

if not exist "frontend\package.json" (
    echo ❌ Error: No se encuentra package.json en frontend\
    echo Asegurate de ejecutar este script desde la raiz del proyecto
    pause
    exit /b 1
)

:: Iniciar Backend (Django) en una nueva ventana
echo 🔧 Iniciando Backend Django en puerto 8000...
start "AXYOMA Backend - Django Server" cmd /k "cd Backend && python manage.py runserver"

:: Esperar un momento para que Django se inicie
timeout /t 3 /nobreak >nul

:: Iniciar Frontend (React) en una nueva ventana
echo ⚛️  Iniciando Frontend React en puerto 3000...
start "AXYOMA Frontend - React Server" cmd /k "cd frontend && npm start"

echo.
echo ==========================================
echo       ✅ SERVIDORES INICIADOS
echo ==========================================
echo.
echo 🔧 Backend Django:  http://localhost:8000
echo ⚛️  Frontend React:  http://localhost:3000
echo.
echo 📝 Los servidores se están ejecutando en ventanas separadas.
echo    Cierra las ventanas de terminal para detener los servidores.
echo.
echo 🌐 Para abrir la aplicación, espera a que React termine de compilar
echo    y luego abre http://localhost:3000 en tu navegador.
echo.
pause
