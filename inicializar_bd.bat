@echo off
echo ======================================================
echo        INICIALIZACION DE BASE DE DATOS AXYOMA
echo ======================================================
echo.

cd Backend

echo Activando entorno virtual...
call env\Scripts\activate.bat

echo.
echo Ejecutando script de inicializacion de base de datos...
python inicializar_bd.py

if %errorlevel% neq 0 (
    echo.
    echo ERROR: La inicializacion de la base de datos fallo.
    pause
    exit /b 1
)

echo.
echo ======================================================
echo    BASE DE DATOS INICIALIZADA CORRECTAMENTE
echo ======================================================
echo.
echo Ahora puedes iniciar el servidor con start.bat
echo.
pause
