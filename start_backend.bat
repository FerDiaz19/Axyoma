@echo off
echo Iniciando Backend de Axyoma...

cd Backend

echo Ejecutando inicializacion del sistema...
python inicializar_sistema.py

echo Iniciando servidor Django...
python manage.py runserver

pause
