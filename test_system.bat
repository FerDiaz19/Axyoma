@echo off
echo ===== AXYOMA - VERIFICACION RAPIDA DEL SISTEMA =====
echo.

echo [1/6] Verificando Python...
py --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python no encontrado
    exit /b 1
) else (
    echo ✅ Python OK
)

echo [2/6] Verificando Node.js...
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Node.js no encontrado
    exit /b 1
) else (
    echo ✅ Node.js OK
)

echo [3/6] Verificando PostgreSQL...
psql --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ PostgreSQL no encontrado
    exit /b 1
) else (
    echo ✅ PostgreSQL OK
)

echo [4/6] Verificando conexion a base de datos...
psql -U postgres -h localhost -p 5432 -d axyoma_db -c "\q" >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ No se puede conectar a 'axyoma_db'
    echo    Ejecuta setup_project.bat para crear la base de datos
    exit /b 1
) else (
    echo ✅ Base de datos accesible
)

echo [5/6] Verificando dependencias del backend...
cd Backend
py -c "import django; print('Django OK')" >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Django no instalado
    echo    Ejecuta: pip install -r requirements.txt
    cd ..
    exit /b 1
) else (
    echo ✅ Django OK
)

echo [6/6] Verificando dependencias del frontend...
cd ..\frontend
if not exist "node_modules" (
    echo ❌ node_modules no encontrado
    echo    Ejecuta: npm install
    cd ..
    exit /b 1
) else (
    echo ✅ Node modules OK
)

cd ..
echo.
echo ===== ✅ SISTEMA LISTO PARA USAR =====
echo.
echo 🚀 Ejecuta: start_system.bat
echo.
pause
