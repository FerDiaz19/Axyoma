@echo off
REM Script universal para inicializar AXYOMA en cualquier sistema
REM Modifica PGUSER y PGPASSWORD según tu configuración

set PGUSER=postgres
set PGPASSWORD=postgres
set PGHOST=localhost
set PGPORT=5432
set DBNAME=axyoma_bd
set OUTPUT=axyoma_bd_export.sql

REM 1. Crear la base de datos si no existe
psql -U %PGUSER% -h %PGHOST% -p %PGPORT% -c "CREATE DATABASE %DBNAME%;" 2>nul

REM 2. Aplicar migraciones Django para crear la estructura
cd Backend
call env\Scripts\activate.bat
python manage.py migrate

REM 3. Ejecutar script de datos iniciales completos (usuarios, empresas, plantas, etc.)
python crear_usuarios_prueba.py
cd ..

echo Instalación y datos iniciales completos realizados. El sistema está listo para usar.
pause
