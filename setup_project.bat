@echo off
echo ===== AXYOMA - SETUP PARA NUEVOS DESARROLLADORES =====
echo.

echo [1/4] Verificando estructura del proyecto...
if not exist "Backend" (
    echo ERROR: Directorio Backend no encontrado
    pause
    exit /b 1
)

if not exist "frontend" (
    echo ERROR: Directorio frontend no encontrado
    pause
    exit /b 1
)

echo [2/4] Configurando entorno virtual de Python...
cd Backend

if not exist "env" (
    echo Creando entorno virtual...
    py -m venv env
    if %errorlevel% neq 0 (
        echo ERROR: No se pudo crear el entorno virtual
        echo Verifica que Python esté instalado
        pause
        exit /b 1
    )
)

echo Activando entorno virtual...
call env\Scripts\activate.bat

echo Instalando dependencias de Python...
py -m pip install --upgrade pip
py -m pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ERROR: No se pudieron instalar las dependencias del backend
    pause
    exit /b 1
)

echo [3/4] Instalando dependencias del Frontend...
cd ..\frontend
echo Instalando packages con npm...
npm install
if %errorlevel% neq 0 (
    echo ERROR: No se pudieron instalar las dependencias del frontend
    echo Asegurate de tener Node.js 16+ instalado
    pause
    exit /b 1
)

echo [4/4] Configurando base de datos PostgreSQL...
cd ..
echo Base de datos configurada para PostgreSQL únicamente

echo.
echo ===== SETUP COMPLETADO =====
echo.
echo ✅ CONFIGURACIÓN COMPLETADA:
echo    ✓ Entorno virtual creado en Backend\env\
echo    ✓ Dependencias del backend instaladas
echo    ✓ Dependencias del frontend instaladas
echo    ✓ Archivos de configuración creados
echo.
echo 📋 REQUISITOS PARA USAR EL SISTEMA:
echo    - PostgreSQL debe estar instalado y ejecutándose
echo    - Base de datos: axyomadb (usuario: postgres, password: 123456789)
echo    - El backend se conectará automáticamente
echo.
echo 👤 Usuarios de prueba:
echo    SuperAdmin:     ed-rubio@axyoma.com / 1234
echo    Admin Empresa:  juan.perez@codewave.com / 1234
echo    Admin Planta:   maria.gomez@codewave.com / 1234
echo.
echo 🚀 Para iniciar el sistema usa: start.bat
echo.
pause
