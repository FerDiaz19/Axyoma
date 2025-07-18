@echo off
echo Iniciando Backend de Axyoma...

cd Backend

echo Activando entorno virtual...
call env\Scripts\activate.bat

echo Ejecutando inicializacion del sistema...
python inicializar_sistema.py

echo Iniciando servidor Django...
python manage.py runserver

pause
