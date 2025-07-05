@echo off
echo ====================================
echo      INICIANDO BACKEND DJANGO
echo ====================================
echo.

cd Backend

echo Verificando entorno virtual...
if exist "env\Scripts\activate.bat" (
    echo Activando entorno virtual...
    call env\Scripts\activate.bat
) else (
    echo ❌ Error: No se encontro el entorno virtual
    echo Ejecuta setup_proyecto_completo.bat primero
    pause
    exit /b 1
)

echo.
echo Configurando base de datos si es necesario...
python setup_database.py

echo.
echo Iniciando servidor Django en puerto 8000...
echo API disponible en: http://localhost:8000/api/
echo Admin disponible en: http://localhost:8000/admin/
echo.
echo Presiona Ctrl+C para detener el servidor
echo.

python manage.py runserver
