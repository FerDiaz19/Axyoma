@echo off
REM ============================================================================
REM SETUP SISTEMA COMPLETO - AXYOMA
REM ============================================================================
REM Este script configura el sistema Axyoma con todos los datos base necesarios
REM Basado en el esquema SQL original AxyomaDB.sql y adaptado para Django
REM ============================================================================

echo.
echo ===============================================
echo     SETUP SISTEMA COMPLETO - AXYOMA
echo ===============================================
echo.
echo Este script configurara el sistema con:
echo - Usuarios base (SuperAdmin, admin empresa, admin planta)
echo - Empresa demo
echo - Plantas demo  
echo - Departamentos y puestos
echo - Empleados de ejemplo
echo - Relaciones admin-plantas
echo.
echo Presiona cualquier tecla para continuar o Ctrl+C para cancelar...
pause > nul

echo.
echo [INFO] Iniciando configuracion del sistema...
echo.

REM Cambiar al directorio del backend
cd /d "%~dp0Backend"

REM Activar el entorno virtual si existe
if exist "env\Scripts\activate.bat" (
    echo [INFO] Activando entorno virtual...
    call env\Scripts\activate.bat
) else (
    echo [WARNING] No se encontro entorno virtual en env\Scripts\
    echo [INFO] Usando Python del sistema...
)

REM Ejecutar migraciones primero
echo [INFO] Ejecutando migraciones de Django...
python manage.py makemigrations
if errorlevel 1 (
    echo [ERROR] Error en makemigrations
    pause
    exit /b 1
)

python manage.py migrate
if errorlevel 1 (
    echo [ERROR] Error en migrate
    pause
    exit /b 1
)

REM Ejecutar el script de setup
echo [INFO] Ejecutando setup del sistema...
python setup_sistema_completo.py

if errorlevel 1 (
    echo.
    echo [ERROR] Error durante la configuracion del sistema
    echo [INFO] Revisa los mensajes anteriores para mas detalles
    echo.
    pause
    exit /b 1
) else (
    echo.
    echo ===============================================
    echo         CONFIGURACION COMPLETADA
    echo ===============================================
    echo.
    echo El sistema Axyoma ha sido configurado exitosamente.
    echo.
    echo CREDENCIALES DE ACCESO:
    echo.
    echo SuperAdmin:
    echo   Usuario: ed-rubio@axyoma.com
    echo   Contrasena: 1234
    echo.
    echo Admin Empresa:
    echo   Usuario: juan.perez@codewave.com  
    echo   Contrasena: 1234
    echo.
    echo Admin Planta 1 (Tijuana):
    echo   Usuario: maria.gomez@codewave.com
    echo   Contrasena: 1234
    echo.
    echo Admin Planta 2 (Monterrey):
    echo   Usuario: carlos.ruiz@codewave.com
    echo   Contrasena: 1234
    echo.
    echo ===============================================
    echo.
    echo Para iniciar el sistema:
    echo 1. Ejecuta: start-backend.bat
    echo 2. Ejecuta: start-frontend.bat  
    echo 3. Accede a: http://localhost:3000
    echo.
    echo ===============================================
)

echo.
echo Presiona cualquier tecla para salir...
pause > nul
