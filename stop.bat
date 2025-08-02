@echo off
echo ==========================================
echo       🛑 AXYOMA - DETENER SERVIDORES
echo ==========================================
echo.
echo Deteniendo servidores Frontend y Backend...
echo.

:: Detener procesos de Node.js (React)
echo 🔴 Deteniendo React (Node.js)...
taskkill /f /im node.exe 2>nul
if %errorlevel% equ 0 (
    echo ✅ React detenido
) else (
    echo ⚠️  No se encontraron procesos de React ejecutándose
)

:: Detener procesos de Python (Django)
echo 🔴 Deteniendo Django (Python)...
taskkill /f /im python.exe 2>nul
if %errorlevel% equ 0 (
    echo ✅ Django detenido
) else (
    echo ⚠️  No se encontraron procesos de Django ejecutándose
)

:: Opcional: Detener procesos específicos por puerto
echo.
echo 🔍 Verificando puertos 3000 y 8000...

:: Verificar puerto 3000 (React)
for /f "tokens=5" %%i in ('netstat -ano ^| findstr :3000') do (
    echo 🔴 Deteniendo proceso en puerto 3000 (PID: %%i)
    taskkill /f /pid %%i 2>nul
)

:: Verificar puerto 8000 (Django)
for /f "tokens=5" %%i in ('netstat -ano ^| findstr :8000') do (
    echo 🔴 Deteniendo proceso en puerto 8000 (PID: %%i)
    taskkill /f /pid %%i 2>nul
)

echo.
echo ==========================================
echo       ✅ SERVIDORES DETENIDOS
echo ==========================================
echo.
echo Los puertos 3000 y 8000 están ahora disponibles.
echo.
pause
