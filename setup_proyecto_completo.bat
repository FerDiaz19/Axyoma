@echo off
echo ====================================
echo    CONFIGURACION AXYOMA 2025
echo ====================================
echo.

:: Verificar que estamos en el directorio correcto
if not exist "Backend\manage.py" (
    echo ERROR: No se encuentra manage.py. Ejecute desde la raiz del proyecto.
    pause
    exit /b 1
)

echo [1/7] Verificando PostgreSQL...
psql --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ADVERTENCIA: PostgreSQL no encontrado en PATH.
    echo Asegurese de tener PostgreSQL instalado y configurado.
    echo.
)

echo [2/7] Creando base de datos...
psql -U postgres -c "CREATE DATABASE axyoma;" 2>nul
echo Base de datos 'axyoma' verificada/creada.

echo [3/7] Instalando dependencias del backend...
cd Backend
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ERROR: Fallo instalando dependencias del backend
    pause
    exit /b 1
)

echo [4/7] Ejecutando migraciones...
python manage.py makemigrations
python manage.py makemigrations users
python manage.py migrate
if %errorlevel% neq 0 (
    echo ERROR: Fallo en migraciones de la base de datos
    pause
    exit /b 1
)

echo [5/7] Configurando base de datos adicional...
python setup_database.py

echo [6/7] Insertando datos de prueba...
python manage.py limpiar_datos
python manage.py insertar_datos
python manage.py crear_tokens
if %errorlevel% neq 0 (
    echo ERROR: Fallo insertando datos de prueba
    pause
    exit /b 1
)

echo [6/7] Verificando configuracion...
python manage.py verificar_datos

echo [7/7] Instalando dependencias del frontend...
cd ..\frontend
npm install
if %errorlevel% neq 0 (
    echo ERROR: Fallo instalando dependencias del frontend
    pause
    exit /b 1
)

cd ..
echo.
echo ====================================
echo     CONFIGURACION COMPLETADA
echo ====================================
echo.
echo Para iniciar el proyecto:
echo   Backend:  start-backend.bat
echo   Frontend: start-frontend.bat
echo.
echo Usuarios de prueba:
echo   ed-rubio@axyoma.com / 1234 (SuperAdmin)
echo   juan.perez@codewave.com / 1234 (Admin Empresa)
echo   maria.gomez@codewave.com / 1234 (Admin Planta)
echo.
echo URL Frontend: http://localhost:3000
echo URL Backend API: http://localhost:8000/api/
echo.
pause
