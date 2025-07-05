@echo off
echo ========================================
echo    REINICIANDO BACKEND DJANGO
echo ========================================
echo.

cd /d "%~dp0Backend"

echo Activando entorno virtual...
call env\Scripts\activate.bat

echo Iniciando servidor Django...
python manage.py runserver

pause
