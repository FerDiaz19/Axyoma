@echo off
cls
echo ========================================
echo    CREANDO TABLAS EN BASE DE DATOS
echo ========================================
echo.

cd /d "%~dp0Backend"

echo Activando entorno virtual...
call env\Scripts\activate.bat

echo.
echo 1. Generando migraciones para todas las apps...
python manage.py makemigrations
echo.

echo 2. Generando migraciones especificas por app...
python manage.py makemigrations users
python manage.py makemigrations employees  
python manage.py makemigrations surveys
python manage.py makemigrations subscriptions
echo.

echo 3. Aplicando todas las migraciones...
python manage.py migrate
echo.

echo 4. Verificando que las tablas se crearon...
python manage.py dbshell -c "\dt"

echo.
echo ========================================
echo    MIGRACIONES COMPLETADAS
echo ========================================
echo.
pause
