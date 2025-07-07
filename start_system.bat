@echo off
echo ===== AXYOMA - SISTEMA COMPLETO =====
echo.

REM Verificar estructura del proyecto
if not exist "Backend" (
    echo ERROR: Directorio Backend no encontrado
    echo Asegurate de estar en la raiz del proyecto Axyoma2
    pause
    exit /b 1
)

if not exist "frontend" (
    echo ERROR: Directorio frontend no encontrado
    echo Asegurate de estar en la raiz del proyecto Axyoma2
    pause
    exit /b 1
)

if not exist "start_backend.bat" (
    echo ERROR: start_backend.bat no encontrado
    echo Los archivos del proyecto estan incompletos
    pause
    exit /b 1
)

if not exist "start_frontend.bat" (
    echo ERROR: start_frontend.bat no encontrado
    echo Los archivos del proyecto estan incompletos
    pause
    exit /b 1
)

REM Verificar requisitos del sistema
echo Verificando requisitos del sistema...

REM Verificar Python
py --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python no esta instalado
    echo Descarga e instala Python 3.8+ desde https://python.org/
    echo Asegurate de marcar "Add Python to PATH" durante la instalacion
    pause
    exit /b 1
) else (
    echo ✓ Python encontrado
)

REM Verificar Node.js
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Node.js no esta instalado
    echo Descarga e instala Node.js 16+ desde https://nodejs.org/
    pause
    exit /b 1
) else (
    echo ✓ Node.js encontrado
)

REM Verificar pip
py -m pip --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: pip no esta disponible
    echo Reinstala Python asegurandote de incluir pip
    pause
    exit /b 1
) else (
    echo ✓ pip encontrado
)

REM Verificar npm
npm --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: npm no esta disponible
    echo Reinstala Node.js desde https://nodejs.org/
    pause
    exit /b 1
) else (
    echo ✓ npm encontrado
)

REM Verificar PostgreSQL
psql --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: PostgreSQL no esta instalado o no esta en PATH
    echo Descarga e instala PostgreSQL desde https://www.postgresql.org/download/windows/
    echo Configura: usuario=postgres, password=admin, puerto=5432
    pause
    exit /b 1
) else (
    echo ✓ PostgreSQL encontrado
)

REM Verificar conexion a base de datos
psql -U postgres -h localhost -p 5432 -d axyoma_db -c "\q" >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: No se puede conectar a la base de datos 'axyoma_db'
    echo Ejecuta setup_project.bat para crear la base de datos
    pause
    exit /b 1
) else (
    echo ✓ Base de datos 'axyoma_db' accesible
)

echo.
echo ===== INICIANDO SISTEMA AXYOMA =====
echo.

echo [1/2] Iniciando Backend (Django)...
echo        Abriendo ventana separada para el backend...
start "AXYOMA Backend - Django" cmd /k "start_backend.bat"

echo [2/2] Esperando 5 segundos antes de iniciar Frontend...
timeout /t 5 /nobreak >nul

echo        Iniciando Frontend (React)...
echo        Abriendo ventana separada para el frontend...
start "AXYOMA Frontend - React" cmd /k "start_frontend.bat"

echo.
echo ===== SISTEMA INICIADO CORRECTAMENTE =====
echo.
echo 🌐 URLs del sistema:
echo    Backend (API):  http://localhost:8000
echo    Frontend (Web): http://localhost:3000
echo.
echo 👤 Usuarios de prueba:
echo    SuperAdmin:     superadmin / admin123
echo    Admin Empresa:  admin / admin123  
echo    Admin Planta:   planta1 / admin123
echo.
echo 📋 Funcionalidades principales:
echo    ✓ Sistema de autenticacion con roles
echo    ✓ Gestion de suscripciones automatizada  
echo    ✓ Dashboard diferenciado por usuario
echo    ✓ CRUD completo de empresas, plantas y empleados
echo    ✓ Una suscripcion activa por empresa
echo    ✓ Admin Planta depende de suscripcion de empresa
echo    ✓ Flujo automatico: crear → pagar → activar
echo    ✓ Base de datos PostgreSQL configurada
echo.
echo 🚀 El sistema se esta ejecutando en dos ventanas separadas:
echo    - Una ventana para el Backend (Django)
echo    - Una ventana para el Frontend (React)
echo.
echo ⚠️  Para DETENER el sistema:
echo    - Cierra ambas ventanas de CMD
echo    - O presiona Ctrl+C en cada ventana
echo.
echo 💡 Si hay problemas:
echo    1. Verifica que los puertos 8000 y 3000 esten libres
echo    2. Ejecuta setup_project.bat si es la primera vez
echo    3. Revisa que Python 3.8+, Node.js 16+ y PostgreSQL esten instalados
echo    4. Verifica que PostgreSQL este ejecutandose (usuario: postgres, password: admin)
echo.
echo El navegador se abrira automaticamente en http://localhost:3000
echo.
pause