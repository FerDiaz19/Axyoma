@echo off
title Servidor React - Axyoma
color 0C

echo.
echo ==========================================
echo        INICIANDO SERVIDOR REACT
echo ==========================================
echo.

cd /d "%~dp0\frontend"

echo.
echo Iniciando servidor React en puerto 3000...
echo URL: http://localhost:3000
echo Presiona Ctrl+C para detener
echo.

npm start

pause
