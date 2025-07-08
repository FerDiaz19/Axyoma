@echo off
echo ===== AXYOMA - INICIANDO FRONTEND (REACT) =====
echo.

REM Verificar que estamos en el directorio correcto
if not exist "frontend" (
    echo ERROR: Directorio frontend no encontrado
    echo Asegurate de ejecutar este archivo desde la raiz del proyecto Axyoma2
    pause
    exit /b 1
)

REM Cambiar al directorio del frontend
cd frontend

REM Verificar que existe package.json
if not exist "package.json" (
    echo ERROR: package.json no encontrado en frontend
    echo El proyecto no esta configurado correctamente
    pause
    exit /b 1
)

REM Verificar que Node.js está instalado
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Node.js no esta instalado
    echo Descarga e instala Node.js 16+ desde https://nodejs.org/
    pause
    exit /b 1
)

REM Verificar que npm está disponible
npm --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: npm no esta disponible
    echo Reinstala Node.js desde https://nodejs.org/
    pause
    exit /b 1
)

echo Verificando dependencias de Node.js...
if not exist "node_modules" (
    echo ADVERTENCIA: node_modules no encontrado
    echo Instalando dependencias...
    npm install
    if %errorlevel% neq 0 (
        echo ERROR: No se pudieron instalar las dependencias
        echo Verifica tu conexion a internet y que npm funcione correctamente
        pause
        exit /b 1
    )
)

REM Verificar que React está instalado
npm list react >nul 2>&1
if %errorlevel% neq 0 (
    echo ADVERTENCIA: React no esta instalado correctamente
    echo Reinstalando dependencias...
    npm install
)

echo.
echo ===== INICIANDO SERVIDOR REACT =====
echo URL: http://localhost:3000
echo.
echo Rutas principales:
echo   /login                        - Página de login
echo   /superadmin                   - Dashboard SuperAdmin
echo   /empresa-admin                - Dashboard Admin Empresa
echo   /planta-admin                 - Dashboard Admin Planta
echo   /plan-selection               - Selección de planes
echo.
echo Usuarios de prueba:
echo   SuperAdmin: superadmin / admin123
echo   Admin Empresa: admin / admin123
echo   Admin Planta: planta1 / admin123
echo.
echo Para detener el servidor presiona Ctrl+C
echo El navegador se abrira automaticamente
echo.

REM Iniciar servidor React
npm start

echo.
echo Servidor React detenido
pause