@echo off
echo ===== AXYOMA - CONFIGURACION INICIAL =====

REM Verificar Python
echo [1/7] Verificando Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python no esta instalado o no esta en PATH
    echo Instala Python 3.8+ desde https://python.org
    pause
    exit /b 1
)

REM Verificar Node.js
echo [2/7] Verificando Node.js...
node --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Node.js no esta instalado
    echo Instala Node.js 16+ desde https://nodejs.org
    pause
    exit /b 1
)

REM Configurar Backend
echo [3/7] Configurando entorno virtual Python...
cd Backend
if not exist "env" (
    python -m venv env
    if errorlevel 1 (
        echo ERROR: No se pudo crear el entorno virtual
        pause
        exit /b 1
    )
)

echo [4/7] Activando entorno virtual e instalando dependencias...
call env\Scripts\activate.bat
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: No se pudieron instalar las dependencias de Python
    pause
    exit /b 1
)

echo [5/7] Configurando base de datos...
python manage.py migrate
if errorlevel 1 (
    echo ERROR: No se pudieron aplicar las migraciones
    echo Verifica que PostgreSQL este corriendo y la BD 'axyomadb' exista
    pause
    exit /b 1
)

echo [6/7] Creando datos iniciales...
python create_initial_data.py

echo [7/7] Configurando Frontend...
cd ..\frontend
npm install
if errorlevel 1 (
    echo ERROR: No se pudieron instalar las dependencias de Node.js
    pause
    exit /b 1
)

cd ..
echo.
echo ===== CONFIGURACION COMPLETADA =====
echo.
echo Para iniciar el sistema usa: start.bat
echo.
pause
