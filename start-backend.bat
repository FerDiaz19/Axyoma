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
    echo ❌ Error: No se encontró el entorno virtual
    echo.
    echo SOLUCION:
    echo 1. Ejecuta: setup_proyecto_completo.bat (configuración completa)
    echo    O
    echo 2. Ejecuta: crear_entorno.bat (solo entorno virtual)
    echo.
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
