@echo off
title AXYOMA - CONFIGURACIÓN INICIAL
color 0E

echo ================================================================================
echo                           PROYECTO AXYOMA                         
echo                           CONFIGURACIÓN INICIAL                   
echo ================================================================================
echo.

echo [1/7] Verificando requisitos del sistema...

REM Verificar Python
python --version > nul 2>&1
if %errorlevel% neq 0 (
    echo X ERROR: Python no está instalado o no está en el PATH
    echo    Por favor instala Python 3.10 o superior
    pause
    exit /b 1
)

REM Verificar Node.js
node --version > nul 2>&1
if %errorlevel% neq 0 (
    echo X ERROR: Node.js no está instalado o no está en el PATH
    echo    Por favor instala Node.js 16 o superior
    pause
    exit /b 1
)

REM Verificar PostgreSQL
set PGBIN="C:\Program Files\PostgreSQL\17\bin"
%PGBIN%\psql --version > nul 2>&1
if %errorlevel% neq 0 (
    echo X ERROR: PostgreSQL no está instalado o no está en el PATH
    echo    Por favor instala PostgreSQL 12 o superior
    pause
    exit /b 1
)

echo ✓ Requisitos verificados

echo [2/7] Creando entorno virtual de Python...
cd Backend

REM Usar .venv como nombre del entorno virtual
python -m venv .venv
if %errorlevel% neq 0 (
    echo X ERROR: No se pudo crear el entorno virtual
    pause
    exit /b 1
)

call .venv\Scripts\activate.bat
if %errorlevel% neq 0 (
    echo X ERROR: No se pudo activar el entorno virtual
    pause
    exit /b 1
)

echo [3/7] Instalando dependencias de Python...
python -m pip install --upgrade pip
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo X ERROR: No se pudieron instalar las dependencias de Python
    pause
    exit /b 1
)

echo ✓ Backend configurado

echo [3/7] Configurando Base de Datos...
REM Verificar si el script createdb.py existe
if not exist "createdb.py" (
    echo X ERROR: No se encontró el archivo createdb.py
    echo    Creando archivo createdb.py básico...
    
    echo #!/usr/bin/env python > createdb.py
    echo """Script para crear la base de datos PostgreSQL para Axyoma""" >> createdb.py
    echo. >> createdb.py
    echo import sys >> createdb.py
    echo import os >> createdb.py
    echo import subprocess >> createdb.py
    echo. >> createdb.py
    echo def create_database(): >> createdb.py
    echo     """Crear base de datos PostgreSQL""" >> createdb.py
    echo     print("Creando base de datos PostgreSQL 'axyomadb'...") >> createdb.py
    echo. >> createdb.py
    echo     # Parámetros de conexión >> createdb.py
    echo     db_name = "axyomadb" >> createdb.py
    echo     db_user = "postgres" >> createdb.py
    echo     db_password = "12345678" >> createdb.py
    echo     db_host = "localhost" >> createdb.py
    echo     db_port = "5432" >> createdb.py
    echo. >> createdb.py
    echo     # Comando para verificar si la base de datos ya existe >> createdb.py
    echo     check_db_cmd = f'psql -U {db_user} -h {db_host} -p {db_port} -t -c "SELECT 1 FROM pg_database WHERE datname=\'{db_name}\'"' >> createdb.py
    echo. >> createdb.py
    echo     # Comando para crear la base de datos >> createdb.py
    echo     create_db_cmd = f'psql -U {db_user} -h {db_host} -p {db_port} -c "CREATE DATABASE {db_name} ENCODING \'UTF8\' LC_COLLATE \'Spanish_Spain.1252\' LC_CTYPE \'Spanish_Spain.1252\' TEMPLATE template0;"' >> createdb.py
    echo. >> createdb.py
    echo     # Comando para establecer contraseña mediante variable de entorno >> createdb.py
    echo     os.environ['PGPASSWORD'] = db_password >> createdb.py
    echo. >> createdb.py
    echo     try: >> createdb.py
    echo         # Verificar si la base de datos ya existe >> createdb.py
    echo         result = subprocess.run(check_db_cmd, shell=True, capture_output=True, text=True) >> createdb.py
    echo         if '1' in result.stdout.strip(): >> createdb.py
    echo             print(f"Base de datos '{db_name}' ya existe.") >> createdb.py
    echo             return True >> createdb.py
    echo. >> createdb.py
    echo         # Crear la base de datos >> createdb.py
    echo         result = subprocess.run(create_db_cmd, shell=True, capture_output=True, text=True) >> createdb.py
    echo. >> createdb.py
    echo         if result.returncode != 0: >> createdb.py
    echo             print(f"Error al crear la base de datos: {result.stderr}") >> createdb.py
    echo             return False >> createdb.py
    echo. >> createdb.py
    echo         print(f"Base de datos '{db_name}' creada exitosamente.") >> createdb.py
    echo         return True >> createdb.py
    echo. >> createdb.py
    echo     except Exception as e: >> createdb.py
    echo         print(f"Error inesperado: {str(e)}") >> createdb.py
    echo         return False >> createdb.py
    echo     finally: >> createdb.py
    echo         # Limpiar variable de entorno por seguridad >> createdb.py
    echo         if 'PGPASSWORD' in os.environ: >> createdb.py
    echo             del os.environ['PGPASSWORD'] >> createdb.py
    echo. >> createdb.py
    echo if __name__ == "__main__": >> createdb.py
    echo     success = create_database() >> createdb.py
    echo     sys.exit(0 if success else 1) >> createdb.py
)

echo Creando base de datos...
python createdb.py
if %errorlevel% neq 0 (
    echo X ERROR: No se pudo crear la base de datos
    pause
    exit /b 1
)

echo [4/7] Aplicando migraciones...
python manage.py makemigrations
python manage.py migrate
if %errorlevel% neq 0 (
    echo X ERROR: No se pudieron aplicar las migraciones
    pause
    exit /b 1
)

echo [5/7] Creando superusuario...
python -c "import django; django.setup(); from django.contrib.auth.models import User; User.objects.filter(username='superadmin').exists() or User.objects.create_superuser('superadmin', 'superadmin@axyoma.com', '1234')"
if %errorlevel% neq 0 (
    echo X ERROR: No se pudo crear el superusuario
    pause
    exit /b 1
)

echo [6/7] Instalando dependencias de Node.js...
cd ..
cd frontend
npm install
if %errorlevel% neq 0 (
    echo X ERROR: No se pudieron instalar las dependencias de Node.js
    pause
    exit /b 1
)

echo [7/7] Verificando configuración...
cd ..
cd Backend
python manage.py check
if %errorlevel% neq 0 (
    echo X ERROR: La configuración de Django tiene problemas
    pause
    exit /b 1
)

echo.
echo ================================================================================
echo                        CONFIGURACIÓN COMPLETADA                    
echo ================================================================================
echo.
echo El sistema AXYOMA ha sido configurado exitosamente.
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
