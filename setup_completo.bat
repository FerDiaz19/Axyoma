@echo off
cls
echo ========================================
echo   CONFIGURAR BASE DE DATOS Y DATOS
echo ========================================
echo.

echo Paso 1: Creando base de datos PostgreSQL...
call crear_base_datos.bat

echo.
echo Paso 2: Instalando dependencias de Python...
cd Backend
pip install -r requirements.txt

echo.
echo Paso 3: Configurando Django y creando migraciones...
python manage.py makemigrations
python manage.py migrate

echo.
echo Paso 4: Insertando datos de prueba...
python manage.py insertar_datos

echo.
echo ========================================
echo   CONFIGURACION COMPLETADA
echo ========================================
echo.
echo ✓ Base de datos creada
echo ✓ Dependencias instaladas
echo ✓ Migraciones aplicadas  
echo ✓ Datos de prueba insertados
echo.
echo CREDENCIALES DE PRUEBA:
echo - ed-rubio@axyoma.com / 1234 (SuperAdmin)
echo - juan.perez@codewave.com / 1234 (Admin Empresa)
echo - maria.gomez@codewave.com / 1234 (Admin Planta)
echo.
echo Ahora puedes ejecutar:
echo - start-backend.bat
echo - start-frontend.bat
echo.

pause
