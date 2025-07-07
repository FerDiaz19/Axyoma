@echo off
echo ===== AXYOMA - INICIANDO BACKEND (DJANGO) =====
echo.

REM Verificar que estamos en el directorio correcto
if not exist "Backend" (
    echo ERROR: Directorio Backend no encontrado
    echo Asegurate de ejecutar este archivo desde la raiz del proyecto Axyoma2
    pause
    exit /b 1
)

REM Cambiar al directorio del backend
cd Backend

REM Verificar que existe manage.py
if not exist "manage.py" (
    echo ERROR: manage.py no encontrado en Backend
    echo El proyecto no esta configurado correctamente
    pause
    exit /b 1
)

REM Verificar que existe el entorno virtual
if exist "env\Scripts\activate.bat" (
    echo Activando entorno virtual...
    call env\Scripts\activate.bat
) else (
    echo Usando Python del sistema global...
)

REM Verificar archivo de datos mock
if not exist "apps\mock_data.json" (
    echo Creando archivo de datos mock inicial...
    if not exist "apps" mkdir apps
    echo {"planes_adicionales":{},"next_plan_id":4,"suscripciones":{},"next_suscripcion_id":1,"pagos":{},"next_pago_id":1,"empresa_suscripcion_map":{},"timestamp":""} > apps\mock_data.json
)

REM Verificar conexion a PostgreSQL
echo Verificando conexion a PostgreSQL...
psql -U postgres -h localhost -p 5432 -d axyomadb -c "\q" >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: No se puede conectar a PostgreSQL
    echo.
    echo SOLUCION:
    echo 1. Verifica que PostgreSQL este instalado y ejecutandose
    echo 2. Verifica que la base de datos 'axyomadb' exista
    echo 3. Verifica las credenciales: usuario=postgres, password=123456789
    echo 4. Si es la primera vez, ejecuta setup_project.bat
    pause
    exit /b 1
) else (
    echo ✓ Conexion a PostgreSQL exitosa
)

echo.
echo Verificando dependencias de Python...
py -c "import django" >nul 2>&1
if %errorlevel% neq 0 (
    echo ADVERTENCIA: Django no esta instalado
    echo Instalando dependencias...
    py -m pip install -r requirements.txt
    if %errorlevel% neq 0 (
        echo ERROR: No se pudieron instalar las dependencias
        echo Verifica que Python y pip esten instalados correctamente
        pause
        exit /b 1
    )
)

echo.
echo ===== INICIANDO SERVIDOR DJANGO =====
echo URL: http://localhost:8000
echo API: http://localhost:8000/api/
echo.
echo Endpoints principales:
echo   /api/auth/login/              - Login
echo   /api/suscripciones/           - Gestión de suscripciones
echo   /api/empresas/                - Gestión de empresas
echo   /api/empleados/               - Gestión de empleados
echo.
echo Para detener el servidor presiona Ctrl+C
echo.

REM Iniciar servidor Django
py manage.py runserver

echo.
echo Servidor Django detenido
pause