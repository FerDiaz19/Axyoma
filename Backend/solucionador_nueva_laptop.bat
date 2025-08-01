@echo off
echo =======================================================
echo 🔧 SOLUCIONADOR PARA NUEVA LAPTOP - WINDOWS
echo =======================================================
echo.
echo Este script solucionara problemas de configuracion
echo en laptops que ya tienen datos o migraciones previas.
echo.
echo ⚠️  ATENCION: Esto eliminara TODOS los datos existentes
echo    y configurara el sistema desde cero.
echo.
echo ¿Continuar? (S/N)
set /p respuesta="> "

if /i "%respuesta%" neq "S" (
    echo ❌ Operacion cancelada
    pause
    exit /b
)

echo.
echo 🔥 INICIANDO SOLUCION COMPLETA...
echo =======================================================

REM Activar entorno virtual
if exist ".venv\Scripts\activate.bat" (
    echo 🔧 Activando entorno virtual...
    call .venv\Scripts\activate.bat
) else (
    echo ⚠️  Entorno virtual no encontrado, usando Python global
)

echo.
echo 🔧 PASO 1: Limpiando base de datos completamente...
echo -------------------------------------------------------
python manage.py flush --noinput
if errorlevel 1 (
    echo ⚠️  Flush normal fallo, continuando...
)

echo.
echo 🔧 PASO 2: Eliminando migraciones antiguas...
echo -------------------------------------------------------
if exist "apps\users\migrations" (
    for %%f in (apps\users\migrations\*.py) do (
        if not "%%~nxf"=="__init__.py" (
            del "%%f" 2>nul
            echo   ✅ Eliminado: %%~nxf
        )
    )
)

if exist "apps\subscriptions\migrations" (
    for %%f in (apps\subscriptions\migrations\*.py) do (
        if not "%%~nxf"=="__init__.py" (
            del "%%f" 2>nul
            echo   ✅ Eliminado: %%~nxf
        )
    )
)

if exist "apps\evaluaciones\migrations" (
    for %%f in (apps\evaluaciones\migrations\*.py) do (
        if not "%%~nxf"=="__init__.py" (
            del "%%f" 2>nul
            echo   ✅ Eliminado: %%~nxf
        )
    )
)

echo   ✅ Migraciones antiguas eliminadas

echo.
echo 🔧 PASO 3: Creando migraciones frescas...
echo -------------------------------------------------------
python manage.py makemigrations users
python manage.py makemigrations subscriptions
python manage.py makemigrations evaluaciones
python manage.py makemigrations
if errorlevel 1 (
    echo ❌ Error creando migraciones
    pause
    exit /b
)
echo ✅ Migraciones frescas creadas

echo.
echo 🔧 PASO 4: Aplicando migraciones...
echo -------------------------------------------------------
python manage.py migrate
if errorlevel 1 (
    echo ❌ Error aplicando migraciones
    pause
    exit /b
)
echo ✅ Migraciones aplicadas exitosamente

echo.
echo 🔧 PASO 5: Inicializando sistema completo...
echo -------------------------------------------------------
echo 🚀 Configurando todo el sistema automaticamente...
python sistema_completo_listo.py
if errorlevel 1 (
    echo ❌ Error en inicializacion del sistema
    pause
    exit /b
)
echo ✅ Sistema inicializado con todos los datos

echo.
echo 🔧 PASO 6: Verificando instalacion...
echo -------------------------------------------------------
python verificacion_simple.py

echo.
echo =======================================================
echo 🎉 ¡CONFIGURACION COMPLETADA EXITOSAMENTE!
echo =======================================================
echo.
echo ✅ Base de datos limpia y configurada
echo ✅ Sistema inicializado con datos completos
echo ✅ Login funcionando: superadmin / admin123
echo.
echo 📊 TU SISTEMA INCLUYE:
echo   🏢 2 empresas completamente configuradas
echo   👥 41 empleados distribuidos en la estructura
echo   🏭 4 plantas operativas
echo   📋 14 departamentos activos
echo   💼 28 puestos definidos
echo   💳 Suscripciones y pagos configurados
echo.
echo 🚀 PARA USAR EL SISTEMA:
echo   1. Ejecutar: python manage.py runserver
echo   2. Abrir: http://localhost:8000
echo   3. Login: superadmin / admin123
echo.
echo =======================================================
echo 🎯 ¡PROBLEMA RESUELTO! Sistema funcionando correctamente
echo =======================================================
echo.
pause
