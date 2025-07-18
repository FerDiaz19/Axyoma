@echo off
echo ===== AXYOMA - INICIO COMPLETO =====

REM Verificar requisitos
echo [?] Verificando requisitos...
cd Backend
if not exist "env" (
    echo ERROR: Entorno virtual no encontrado
    echo Ejecuta setup_project.bat primero
    pause
    exit /b 1
)

if not exist "requirements.txt" (
    echo ERROR: requirements.txt no encontrado
    pause
    exit /b 1
)

cd ..\frontend
if not exist "package.json" (
    echo ERROR: package.json no encontrado
    pause
    exit /b 1
)

if not exist "node_modules" (
    echo ERROR: node_modules no encontrado
    echo Ejecuta setup_project.bat primero
    pause
    exit /b 1
)

cd ..
echo [✓] Requisitos verificados

echo.
echo ===== CONFIGURANDO BACKEND =====
echo Activando entorno virtual...
cd Backend
call env\Scripts\activate.bat

echo Ejecutando migraciones...
python manage.py makemigrations
python manage.py migrate

echo Configurando sistema inicial...
python inicializar_sistema.py

echo [✓] Backend configurado

echo.
echo ===== INICIANDO SERVIDORES =====
echo.

REM Iniciar Backend en segundo plano
echo [1/2] Iniciando Backend Django en puerto 8000...
start cmd /c "cd /d %~dp0Backend && call env\Scripts\activate.bat && python manage.py runserver 8000"

REM Esperar un poco para que el backend inicie
timeout /t 3 /nobreak >nul

REM Iniciar Frontend en segundo plano
echo [2/2] Esperando 3 segundos e iniciando Frontend React en puerto 3000...
start cmd /c "cd /d %~dp0frontend && npm start"

echo.
echo ===== SISTEMA INICIADO =====
echo.
echo [✓] Backend Django: http://localhost:8000
echo [✓] Frontend React: http://localhost:3000
echo.
echo 👤 Usuarios de prueba:
echo    SuperAdmin:     ed-rubio@axyoma.com / 1234
echo    Admin Empresa:  juan.perez@codewave.com / 1234
echo    Admin Planta:   maria.gomez@codewave.com / 1234
echo.
echo [i] Para detener los servidores, cierra las ventanas de terminal
echo [i] O usa Ctrl+C en cada ventana
echo.
pause
