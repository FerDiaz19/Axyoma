@echo off
echo ===== AXYOMA - SETUP PARA NUEVOS DESARROLLADORES =====
echo.

echo [1/5] Verificando estructura del proyecto...
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

echo [2/5] Verificando PostgreSQL...
psql --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: PostgreSQL no esta instalado o no esta en PATH
    echo.
    echo INSTALAR POSTGRESQL:
    echo 1. Descarga PostgreSQL desde https://www.postgresql.org/download/windows/
    echo 2. Durante la instalacion, configura:
    echo    - Usuario: postgres
    echo    - Password: admin
    echo    - Puerto: 5432
    echo 3. Asegurate de marcar "Add to PATH" durante la instalacion
    echo 4. Despues de instalar, ejecuta este script nuevamente
    pause
    exit /b 1
) else (
    echo ✓ PostgreSQL encontrado
)

echo [3/5] Creando base de datos...
echo Creando base de datos 'axyoma_db'...
psql -U postgres -h localhost -p 5432 -c "DROP DATABASE IF EXISTS axyoma_db;" 2>nul
psql -U postgres -h localhost -p 5432 -c "CREATE DATABASE axyoma_db;" 2>nul
if %errorlevel% neq 0 (
    echo Verificando conexion a PostgreSQL...
    psql -U postgres -h localhost -p 5432 -c "\l" >nul 2>&1
    if %errorlevel% neq 0 (
        echo ERROR: No se puede conectar a PostgreSQL
        echo Verifica que el servicio este ejecutandose y las credenciales sean correctas
        echo Usuario: postgres, Password: admin, Puerto: 5432
        pause
        exit /b 1
    ) else (
        echo ERROR: No se pudo crear la base de datos
        pause
        exit /b 1
    )
) else (
    echo ✓ Base de datos 'axyoma_db' creada exitosamente
)

echo [4/5] Instalando dependencias del Backend...
cd Backend
echo Instalando requirements.txt...
py -m pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ERROR: No se pudieron instalar las dependencias del backend
    echo Asegurate de tener Python 3.8+ instalado
    pause
    exit /b 1
)

echo Ejecutando migraciones de Django...
py manage.py migrate
if %errorlevel% neq 0 (
    echo ERROR: No se pudieron ejecutar las migraciones
    echo Verifica la conexion a PostgreSQL
    pause
    exit /b 1
)

echo [5/5] Instalando dependencias del Frontend...
cd Backend
echo Instalando requirements.txt...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ERROR: No se pudieron instalar las dependencias del backend
    echo Asegurate de tener Python 3.8+ instalado
    pause
    exit /b 1
)

echo [3/4] Instalando dependencias del Frontend...
cd ..\frontend
echo Instalando packages con npm...
npm install
if %errorlevel% neq 0 (
    echo ERROR: No se pudieron instalar las dependencias del frontend
    echo Asegurate de tener Node.js 16+ instalado
    pause
    exit /b 1
)

echo Verificando archivos de configuracion...
cd ..
if not exist "Backend\apps\mock_data.json" (
    echo Creando archivo de datos mock inicial...
    echo {"planes_adicionales":{},"next_plan_id":4,"suscripciones":{},"next_suscripcion_id":1,"pagos":{},"next_pago_id":1,"empresa_suscripcion_map":{},"timestamp":""} > Backend\apps\mock_data.json
)

echo.
echo ===== SETUP COMPLETADO =====
echo.
echo ✅ REQUISITOS VERIFICADOS:
echo    ✓ PostgreSQL configurado (usuario: postgres, password: admin)
echo    ✓ Base de datos 'axyoma_db' creada
echo    ✓ Dependencias del backend instaladas
echo    ✓ Migraciones de Django ejecutadas
echo    ✓ Dependencias del frontend instaladas
echo.
echo 👤 Usuarios de prueba:
echo    SuperAdmin:     superadmin / admin123
echo    Admin Empresa:  admin / admin123
echo    Admin Planta:   planta1 / admin123
echo.
echo 🚀 Para iniciar el sistema usa: start_system.bat
echo.
pause
