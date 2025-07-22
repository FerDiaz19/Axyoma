@echo off
title Inicializar Datos Axyoma
color 0A

echo.
echo ==========================================
echo    INICIALIZADOR DE DATOS AXYOMA
echo ==========================================
echo.
echo Este script va a:
echo - Limpiar completamente la base de datos
echo - Crear datos de prueba para Axyoma
echo - Configurar usuarios, plantas, empleados
echo - Preparar suscripciones y evaluaciones
echo.
echo ADVERTENCIA: Esto borrara TODOS los datos existentes
echo.
set /p confirm="¿Continuar? (S/N): "
if /I not "%confirm%"=="S" (
    echo Operacion cancelada.
    pause
    exit /b
)

echo.
echo Iniciando proceso...
echo.

cd /d "%~dp0"

echo Activando entorno virtual...
call env\Scripts\activate.bat

echo.
echo Ejecutando inicializador...
python inicializar_datos_completo.py

echo.
echo ==========================================
echo           PROCESO COMPLETADO
echo ==========================================
echo.
echo El sistema esta listo para usar con:
echo.
echo SUPERADMIN:
echo   Usuario: superadmin
echo   Password: admin123
echo   URL: http://localhost:3000
echo.
echo ADMIN EMPRESA:
echo   Usuario: admin_axyoma  
echo   Password: admin123
echo   URL: http://localhost:3000
echo.
echo Para iniciar los servidores use:
echo   Backend: start_django.bat
echo   Frontend: start_react.bat
echo.
pause
