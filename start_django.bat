@echo off
title Servidor Django - Axyoma
color 0B

echo.
echo ==========================================
echo        INICIANDO SERVIDOR DJANGO
echo ==========================================
echo.

cd /d "%~dp0\Backend"

echo Activando entorno virtual...
call env\Scripts\activate.bat

echo.
echo Iniciando servidor Django en puerto 8000...
echo URL: http://localhost:8000
echo Presiona Ctrl+C para detener
echo.

python manage.py runserver

pause
