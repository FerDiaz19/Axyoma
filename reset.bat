@echo off
title AXYOMA - RESET DEL SISTEMA
color 0C

echo ================================================================================
echo                           PROYECTO AXYOMA                          
echo                           RESET COMPLETO                           
echo ================================================================================
echo.
echo ADVERTENCIA: Este script borrará y reinicializará por completo:
echo   - La base de datos PostgreSQL
echo   - Las migraciones de Django
echo   - Los archivos de caché
echo.
echo Los datos existentes SE PERDERÁN definitivamente.
echo.
set /p CONFIRM=¿Estás seguro de continuar? (S/N): 
if /i "%CONFIRM%" neq "S" exit /b

echo.
echo [1/4] Verificando requisitos y directorio actual...
echo Directorio actual: %CD%

echo Contenido del directorio Backend:
dir Backend /b

cd Backend
echo Cambiado a directorio: %CD%
echo Contenido del directorio Backend:
dir /b

echo [1.1/4] Buscando entorno virtual...
set VENV_FOUND=0
set VENV_PATH=

REM Verificar todas las posibles ubicaciones/nombres del entorno virtual
if exist ".venv\Scripts\activate.bat" (
    set VENV_FOUND=1
    set VENV_PATH=.venv
    echo Entorno virtual encontrado en: .venv
)

if %VENV_FOUND%==0 (
    if exist "venv\Scripts\activate.bat" (
        set VENV_FOUND=1
        set VENV_PATH=venv
        echo Entorno virtual encontrado en: venv
    )
)

if %VENV_FOUND%==0 (
    if exist "env\Scripts\activate.bat" (
        set VENV_FOUND=1
        set VENV_PATH=env
        echo Entorno virtual encontrado en: env
    )
)

REM Búsqueda adicional subiendo un nivel
if %VENV_FOUND%==0 (
    if exist "..\venv\Scripts\activate.bat" (
        set VENV_FOUND=1
        set VENV_PATH=..\venv
        echo Entorno virtual encontrado en: ..\venv
    )
)

REM Si todavía no lo encontramos, buscar recursivamente
if %VENV_FOUND%==0 (
    echo Buscando entorno virtual recursivamente...
    for /d %%G in (*) do (
        if exist "%%G\Scripts\activate.bat" (
            set VENV_FOUND=1
            set VENV_PATH=%%G
            echo Entorno virtual encontrado en: %%G
        )
    )
)

REM Verificar si se encontró algún entorno virtual
if %VENV_FOUND%==0 (
    echo X ERROR: Entorno virtual no encontrado
    echo   Directorios buscados:
    echo   - .venv\Scripts\activate.bat
    echo   - venv\Scripts\activate.bat
    echo   - env\Scripts\activate.bat
    echo   - ..\venv\Scripts\activate.bat
    echo   Ejecuta setup.bat primero o crea un entorno virtual manualmente
    pause
    exit /b 1
)

echo ✓ Entorno virtual verificado en: %VENV_PATH%

echo [2/4] Reiniciando la base de datos PostgreSQL...
echo Activando entorno virtual desde: %VENV_PATH%\Scripts\activate.bat
call "%VENV_PATH%\Scripts\activate.bat"
if %errorlevel% neq 0 (
    echo X ERROR: No se pudo activar el entorno virtual
    echo   Ruta intentada: %VENV_PATH%\Scripts\activate.bat
    pause
    exit /b 1
)

REM Eliminar y recrear la base de datos
set PGBIN="C:\Program Files\PostgreSQL\17\bin"
set PGUSER=postgres
set PGPASSWORD=12345678

echo Eliminando base de datos existente...
%PGBIN%\psql -U %PGUSER% -c "DROP DATABASE IF EXISTS axyomadb;" >nul 2>&1

echo Creando nueva base de datos...
%PGBIN%\psql -U %PGUSER% -c "CREATE DATABASE axyomadb ENCODING 'UTF8' LC_COLLATE 'Spanish_Spain.1252' LC_CTYPE 'Spanish_Spain.1252' TEMPLATE template0;" >nul 2>&1
if %errorlevel% neq 0 (
    echo X ERROR: No se pudo crear la base de datos
    pause
    exit /b 1
)

echo ✓ Base de datos reiniciada

echo [3/4] Limpiando migraciones...
echo Eliminando archivos de migración...
for /d %%d in (apps\*) do (
    if exist "%%d\migrations" (
        cd "%%d\migrations"
        del /q /f *.py >nul 2>&1
        if not exist __init__.py (
            echo # > __init__.py
        )
        cd ..\..\..
    )
)

echo Generando nuevas migraciones...
python manage.py makemigrations
python manage.py migrate
if %errorlevel% neq 0 (
    echo X ERROR: No se pudieron aplicar las migraciones
    pause
    exit /b 1
)

echo ✓ Migraciones reiniciadas

echo [4/4] Creando datos iniciales...
python manage.py createsuperuser --username superadmin --email superadmin@axyoma.com --noinput
python manage.py shell -c "from django.contrib.auth.models import User; u=User.objects.get(username='superadmin'); u.set_password('1234'); u.save()"
if %errorlevel% neq 0 (
    echo X ERROR: No se pudo crear el superusuario
    pause
    exit /b 1
)

REM Intenta importar datos iniciales si existe el script
if exist "init_data.py" (
    echo Importando datos iniciales...
    python init_data.py
) else (
    echo No se encontró script de datos iniciales, omitiendo...
)

echo ✓ Datos iniciales creados

echo.
echo ================================================================================
echo                        RESET COMPLETADO EXITOSAMENTE                
echo ================================================================================
echo.
echo El sistema AXYOMA ha sido reiniciado completamente.
echo.
echo Para iniciar el sistema, ejecuta:
echo.
echo     start.bat
echo.
echo Credenciales de superusuario:
echo     Usuario: superadmin
echo     Contraseña: 1234
echo.
pause