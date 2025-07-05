@echo off
cls
echo ========================================
echo    APLICANDO MIGRACIONES A POSTGRESQL
echo ========================================
echo.

cd /d "%~dp0Backend"

echo Activando entorno virtual...
call env\Scripts\activate.bat
if %errorlevel% neq 0 (
    echo ERROR: No se pudo activar el entorno virtual
    pause
    exit /b 1
)

echo.
echo 1. Verificando conexion a PostgreSQL...
python -c "import psycopg2; conn = psycopg2.connect(host='localhost', database='axyomadb', user='postgres', password='123456789'); print('✓ Conexion exitosa a PostgreSQL'); conn.close()"
if %errorlevel% neq 0 (
    echo ERROR: No se puede conectar a PostgreSQL
    echo Verifica que PostgreSQL este corriendo y la base de datos 'axyomadb' exista
    pause
    exit /b 1
)

echo.
echo 2. Mostrando estado actual de migraciones...
python manage.py showmigrations

echo.
echo 3. Aplicando migraciones pendientes...
python manage.py migrate --verbosity=2

echo.
echo 4. Verificando tablas creadas...
python manage.py shell -c "
from django.db import connection
cursor = connection.cursor()
cursor.execute(\"SELECT table_name FROM information_schema.tables WHERE table_schema = 'public' AND table_name LIKE '%empresa%' OR table_name LIKE '%empleado%' OR table_name LIKE '%usuario%';\"
)
tables = cursor.fetchall()
print('Tablas encontradas:')
for table in tables:
    print(f'  - {table[0]}')
"

echo.
echo ========================================
echo    MIGRACIONES APLICADAS EXITOSAMENTE
echo ========================================
echo.
pause
