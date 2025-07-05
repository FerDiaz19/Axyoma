@echo off
cls
echo ========================================
echo   RESETEAR Y CONFIGURAR BASE DE DATOS
echo ========================================
echo.

cd Backend

echo Paso 1: Eliminando migraciones anteriores...
del /Q apps\users\migrations\*.py 2>nul
del /Q apps\employees\migrations\*.py 2>nul
del /Q apps\subscriptions\migrations\*.py 2>nul
del /Q apps\surveys\migrations\*.py 2>nul

echo Paso 2: Creando __init__.py en migraciones...
echo # -*- coding: utf-8 -*- > apps\users\migrations\__init__.py
echo # -*- coding: utf-8 -*- > apps\employees\migrations\__init__.py
echo # -*- coding: utf-8 -*- > apps\subscriptions\migrations\__init__.py
echo # -*- coding: utf-8 -*- > apps\surveys\migrations\__init__.py

echo Paso 3: Instalando dependencias...
pip install -r requirements.txt

echo Paso 4: Creando nuevas migraciones...
python manage.py makemigrations users
python manage.py makemigrations employees
python manage.py makemigrations subscriptions  
python manage.py makemigrations surveys

echo Paso 5: Aplicando migraciones...
python manage.py migrate

echo Paso 6: Insertando datos de prueba...
python manage.py insertar_datos

echo.
echo ========================================
echo   CONFIGURACION COMPLETADA
echo ========================================
echo.
echo CREDENCIALES DE PRUEBA:
echo - ed-rubio@axyoma.com / 1234 (SuperAdmin)
echo - juan.perez@codewave.com / 1234 (Admin Empresa)
echo - maria.gomez@codewave.com / 1234 (Admin Planta)
echo - carlos.ruiz@codewave.com / 1234 (Admin Planta)
echo.
echo Ahora ejecuta:
echo - start-backend.bat (en una terminal)
echo - start-frontend.bat (en otra terminal)
echo.

pause
