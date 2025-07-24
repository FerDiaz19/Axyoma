@echo off
title AXYOMA - INICIANDO SISTEMA
color 0A

echo ================================================================================
echo                           PROYECTO AXYOMA                          
echo                           INICIO DEL SISTEMA                       
echo ================================================================================
echo.

echo [1/4] Verificando requisitos y directorio actual...
echo Directorio actual: %CD%
dir Backend /b

cd Backend
echo Cambiado a directorio: %CD%
echo Contenido del directorio Backend:
dir /b

echo [1.1/4] Buscando entorno virtual...
set VENV_FOUND=0
set VENV_PATH=

REM Verificar todas las posibles ubicaciones/nombres del entorno virtual
if exist ".venv\Scripts\activate.bat" (
    set VENV_FOUND=1
    set VENV_PATH=.venv
    echo Entorno virtual encontrado en: .venv
)

if %VENV_FOUND%==0 (
    if exist "venv\Scripts\activate.bat" (
        set VENV_FOUND=1
        set VENV_PATH=venv
        echo Entorno virtual encontrado en: venv
    )
)

if %VENV_FOUND%==0 (
    if exist "env\Scripts\activate.bat" (
        set VENV_FOUND=1
        set VENV_PATH=env
        echo Entorno virtual encontrado en: env
    )
)

REM Búsqueda adicional subiendo un nivel
if %VENV_FOUND%==0 (
    if exist "..\venv\Scripts\activate.bat" (
        set VENV_FOUND=1
        set VENV_PATH=..\venv
        echo Entorno virtual encontrado en: ..\venv
    )
)

REM Si todavía no lo encontramos, buscar recursivamente
if %VENV_FOUND%==0 (
    echo Buscando entorno virtual recursivamente...
    for /d %%G in (*) do (
        if exist "%%G\Scripts\activate.bat" (
            set VENV_FOUND=1
            set VENV_PATH=%%G
            echo Entorno virtual encontrado en: %%G
        )
    )
)

REM Verificar si se encontró algún entorno virtual
if %VENV_FOUND%==0 (
    echo X ERROR: Entorno virtual no encontrado
    echo   Directorios buscados:
    echo   - .venv\Scripts\activate.bat
    echo   - venv\Scripts\activate.bat
    echo   - env\Scripts\activate.bat
    echo   - ..\venv\Scripts\activate.bat
    echo   Ejecuta setup.bat primero o crea un entorno virtual manualmente
    pause
    exit /b 1
)

if not exist "requirements.txt" (
    echo X ERROR: requirements.txt no encontrado
    pause
    exit /b 1
)

cd ..\frontend
if not exist "package.json" (
    echo X ERROR: package.json no encontrado
    pause
    exit /b 1
)

if not exist "node_modules" (
    echo X ERROR: node_modules no encontrado
    echo    Ejecuta setup.bat primero
    pause
    exit /b 1
)

cd ..
echo ✓ Requisitos verificados

echo [2/4] Verificando conexión a PostgreSQL...
set PGBIN="C:\Program Files\PostgreSQL\17\bin"
set PGUSER=postgres
set PGPASSWORD=12345678
%PGBIN%\psql -U %PGUSER% -d axyomadb -c "SELECT 1;" >nul 2>&1
if %errorlevel% neq 0 (
    echo X ERROR: No se puede conectar a la base de datos axyomadb
    echo    Verifica que PostgreSQL esté ejecutándose
    echo    Base de datos: axyomadb, Usuario: postgres, Password: 12345678
    echo    Ejecuta reset.bat para crear la base de datos
    pause
    exit /b 1
)
echo ✓ Conexión a PostgreSQL exitosa

echo [3/4] Preparando Backend...
cd Backend
echo Activando entorno virtual desde: %VENV_PATH%\Scripts\activate.bat
call "%VENV_PATH%\Scripts\activate.bat"
if %errorlevel% neq 0 (
    echo X ERROR: No se pudo activar el entorno virtual
    echo   Ruta intentada: %VENV_PATH%\Scripts\activate.bat
    pause
    exit /b 1
)

echo Verificando estructura de base de datos...
python -c "import django,os; os.environ.setdefault('DJANGO_SETTINGS_MODULE','config.settings.local'); django.setup(); from django.db import connection; cursor=connection.cursor(); cursor.execute('SELECT COUNT(*) FROM django_migrations'); row=cursor.fetchone(); print(f'✓ Migraciones verificadas: {row[0]} aplicadas')" 2>nul
if %errorlevel% neq 0 (
    echo X ERROR: No se pudo verificar las migraciones
    echo    Ejecuta reset.bat para inicializar la base de datos
    pause
    exit /b 1
)

echo ✓ Backend preparado

echo [4/4] Iniciando servidores...
echo.

REM Iniciar Backend en segundo plano con monitoreo de errores
echo * Iniciando Backend Django en puerto 8000...
start "AXYOMA Backend" cmd /c "cd /d %~dp0Backend && call %VENV_PATH%\Scripts\activate.bat && python manage.py runserver 8000 || (echo X ERROR AL INICIAR BACKEND && pause)"

REM Esperar un poco para que el backend inicie
echo    Esperando 6 segundos para que el backend inicie...
timeout /t 6 /nobreak >nul

REM Probar si el backend está funcionando
curl -s http://localhost:8000/api/health-check/ >nul 2>&1
if %errorlevel% neq 0 (
    echo ! ADVERTENCIA: El backend puede no estar funcionando correctamente.
    echo    Verifica los mensajes en la ventana del backend.
)

REM Iniciar Frontend en segundo plano con monitoreo de errores
echo * Iniciando Frontend React en puerto 3000...
start "AXYOMA Frontend" cmd /c "cd /d %~dp0frontend && npm start || (echo X ERROR AL INICIAR FRONTEND && pause)"

echo.
echo ================================================================================
echo                           SISTEMA INICIADO                         
echo                                                              
echo  * ACCESOS:                                                 
echo     Frontend React:  http://localhost:3000                  
echo     Backend Django:  http://localhost:8000                  
echo     API REST:        http://localhost:8000/api/             
echo     Admin Django:    http://localhost:8000/admin/           
echo                                                              
echo  * USUARIOS DE PRUEBA:                                     
echo     SuperAdmin:     superadmin / 1234                       
echo     Admin Empresa:  admin_empresa / 1234                    
echo     Admin Planta:   admin_planta / 1234                     
echo                                                              
echo  * PARA DETENER:                                           
echo     Cierra las ventanas "AXYOMA Backend" y "AXYOMA Frontend" 
echo     O usa Ctrl+C en cada ventana                            
echo                                                              
echo  * PARA REINICIAR: ejecutar start.bat de nuevo            
echo ================================================================================
echo.

echo * Verificando acceso a la API...
curl -s http://localhost:8000/api/health-check/
echo.

pause
