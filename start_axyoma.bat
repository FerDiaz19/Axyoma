@echo off
title Axyoma - Sistema Completo
color 0E

echo.
echo ==========================================
echo           SISTEMA AXYOMA
echo ==========================================
echo.
echo Iniciando servidores Backend y Frontend...
echo.

echo Abriendo servidor Django...
start "Django Server" cmd /k "cd /d %~dp0 && start_django.bat"

timeout /t 3 /nobreak > nul

echo Abriendo servidor React...
start "React Server" cmd /k "cd /d %~dp0 && start_react.bat"

timeout /t 5 /nobreak > nul

echo.
echo Abriendo navegador...
start http://localhost:3000

echo.
echo ==========================================
echo         SERVIDORES INICIADOS
echo ==========================================
echo.
echo Backend (Django): http://localhost:8000
echo Frontend (React): http://localhost:3000
echo.
echo CREDENCIALES:
echo   SuperAdmin: superadmin / admin123
echo   Admin Empresa: admin_axyoma / admin123
echo.
echo Presiona cualquier tecla para cerrar esta ventana
echo (Los servidores seguiran funcionando)
pause > nul
