@echo off
cls
echo ========================================
echo   INSTALANDO DEPENDENCIAS
echo ========================================
echo.

cd Backend
echo Instalando dependencias de Python...
pip install -r requirements.txt

if %errorlevel% equ 0 (
    echo.
    echo ✓ Dependencias instaladas correctamente
    echo.
    echo Insertando datos de prueba...
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
    echo ¡Ahora puedes probar el login!
) else (
    echo.
    echo ✗ Error al instalar dependencias
    echo Intenta manualmente: pip install -r requirements.txt
)

echo.
pause
