@echo off
cls
echo ========================================
echo   INSERTANDO DATOS DE PRUEBA
echo ========================================
echo.

cd Backend
echo Verificando dependencias...
pip install -r requirements.txt
echo.
echo Insertando datos de prueba en la base de datos...
python manage.py insertar_datos

echo.
echo ========================================
echo   DATOS INSERTADOS
echo ========================================
echo.
echo CREDENCIALES DE PRUEBA:
echo - ed-rubio@axyoma.com / 1234 (SuperAdmin)
echo - juan.perez@codewave.com / 1234 (Admin Empresa)  
echo - maria.gomez@codewave.com / 1234 (Admin Planta)
echo - carlos.ruiz@codewave.com / 1234 (Admin Planta)
echo.
echo ¡Ahora puedes probar el login!
echo.

pause
