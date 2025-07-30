@echo off
echo ===================================================
echo CONFIGURACION AUTOMATICA DEL SISTEMA DE RESPALDOS
echo ===================================================
echo.

cd /d "%~dp0Backend"

echo Verificando Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Error: Python no esta instalado o no esta en PATH
    echo Por favor instalar Python y agregarlo al PATH
    pause
    exit /b 1
)

echo ✅ Python encontrado
echo.

echo Ejecutando configuracion automatica...
python configurar_para_companeros.py

echo.
echo ===================================================
echo Si viste "✅ EL SISTEMA ESTA LISTO PARA USAR"
echo entonces todo funciona correctamente.
echo.
echo Credenciales:
echo Usuario: superadmin
echo Password: 1234
echo ===================================================
echo.
pause
