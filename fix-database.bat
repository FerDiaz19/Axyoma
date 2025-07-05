@echo off
echo ========================================
echo    SOLUCIONANDO PROBLEMA DE TABLAS
echo ========================================
echo.

cd /d "%~dp0Backend"

echo Activando entorno virtual...
call env\Scripts\activate.bat

echo.
echo Aplicando migraciones...
python manage.py migrate

echo.
echo ========================================
echo    LISTO - Reinicia el servidor
echo ========================================
pause
