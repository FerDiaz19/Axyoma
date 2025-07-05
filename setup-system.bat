@echo off
cls
echo ========================================
echo    INSTALACION COMPLETA DEL SISTEMA
echo ========================================
echo.

echo 1. Instalando dependencias del backend...
cd /d "%~dp0Backend"
call env\Scripts\activate.bat
pip install -r requirements.txt

echo.
echo 2. Instalando dependencias del frontend...
cd /d "%~dp0frontend"
npm install

echo.
echo 3. Aplicando migraciones...
cd /d "%~dp0Backend"
call env\Scripts\activate.bat
python manage.py makemigrations
python manage.py migrate

echo.
echo ========================================
echo    INSTALACION COMPLETADA
echo ========================================
echo.
echo Para iniciar el sistema completo:
echo   start-system.bat
echo.
echo Para iniciar solo backend:
echo   start-backend.bat
echo.
echo Para iniciar solo frontend:
echo   start-frontend.bat
echo.
pause
