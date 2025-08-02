@echo off
echo Iniciando servidor Django...
echo.
echo Verificando estado de la base de datos...
cd Backend

echo === Ejecutando script de debug ===
python debug_user_empresa.py
echo.

echo === Iniciando servidor Django ===
python manage.py runserver
pause
