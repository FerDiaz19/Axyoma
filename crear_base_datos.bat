@echo off
cls
echo ========================================
echo   CONFIGURACION BASE DE DATOS POSTGRESQL
echo ========================================
echo.

echo Creando base de datos 'axyoma' en PostgreSQL...
echo.

REM Intentar crear la base de datos usando psql
psql -U postgres -h localhost -c "DROP DATABASE IF EXISTS axyoma;"
psql -U postgres -h localhost -c "CREATE DATABASE axyoma WITH ENCODING 'UTF8' LC_COLLATE='C' LC_CTYPE='C' TEMPLATE=template0;"

if %errorlevel% equ 0 (
    echo.
    echo ✓ Base de datos 'axyoma' creada exitosamente
    echo.
    
    REM Verificar la base de datos
    psql -U postgres -h localhost -d axyoma -c "SELECT current_database(), pg_encoding_to_char(encoding) FROM pg_database WHERE datname = current_database();"
    
    echo.
    echo ========================================
    echo   CONFIGURACION COMPLETADA
    echo ========================================
    echo.
    echo Ahora puedes ejecutar: start-backend.bat
    echo.
) else (
    echo.
    echo ✗ Error al crear la base de datos
    echo.
    echo PASOS MANUALES:
    echo 1. Abre pgAdmin o psql
    echo 2. Conectate como usuario 'postgres'
    echo 3. Ejecuta: CREATE DATABASE axyoma WITH ENCODING 'UTF8';
    echo.
)

pause
