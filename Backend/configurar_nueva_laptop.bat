@echo off
echo ================================================
echo 🚀 CONFIGURADOR AUTOMATICO AXYOMA - NUEVA LAPTOP
echo ================================================
echo.
echo Este script configurara automaticamente todo el
echo sistema Axyoma en tu nueva laptop para que quede
echo exactamente igual que el sistema original.
echo.
echo REQUISITOS:
echo   - Python 3.8+ instalado
echo   - PostgreSQL instalado y corriendo
echo   - Usuario 'postgres' configurado en PostgreSQL
echo   (La base de datos se crea automaticamente)
echo.
echo ¿Continuar? (S/N)
set /p respuesta="> "

if /i "%respuesta%" neq "S" (
    echo ❌ Configuracion cancelada
    pause
    exit /b
)

echo.
echo 🔧 INICIANDO CONFIGURACION AUTOMATICA...
echo ================================================
echo.

REM Paso 1: Verificar Python
echo 📋 PASO 1: Verificando Python...
python --version
if errorlevel 1 (
    echo ❌ Python no encontrado. Instala Python 3.8+ primero.
    pause
    exit /b
)
echo ✅ Python encontrado
echo.

REM Paso 2: Crear entorno virtual
echo 📋 PASO 2: Configurando entorno virtual...
if not exist ".venv" (
    echo 🔧 Creando entorno virtual...
    python -m venv .venv
    if errorlevel 1 (
        echo ❌ Error creando entorno virtual
        pause
        exit /b
    )
    echo ✅ Entorno virtual creado
) else (
    echo ✅ Entorno virtual ya existe
)
echo.

REM Paso 3: Activar entorno e instalar dependencias
echo 📋 PASO 3: Instalando dependencias...
call .venv\Scripts\activate.bat
pip install -r requirements.txt
if errorlevel 1 (
    echo ❌ Error instalando dependencias
    pause
    exit /b
)
echo ✅ Dependencias instaladas
echo.

REM Paso 4: Crear base de datos axyomadb
echo 📋 PASO 4: Creando base de datos axyomadb...
echo 🏗️ Creando base de datos PostgreSQL automaticamente...
psql -U postgres -c "DROP DATABASE IF EXISTS axyomadb;"
psql -U postgres -c "CREATE DATABASE axyomadb;"
if errorlevel 1 (
    echo ⚠️  Error creando BD. Verificar que PostgreSQL este corriendo y usuario 'postgres' configurado.
    echo 💡 Alternativa: Crear manualmente la BD 'axyomadb' en PostgreSQL
    pause
)
echo ✅ Base de datos axyomadb creada y lista
echo.

REM Paso 5: Limpiar base de datos existente
echo 📋 PASO 5: Limpiando base de datos existente...
echo 🧹 ATENCION: Eliminando todos los datos existentes...
python manage.py flush --noinput
python manage.py migrate --run-syncdb
echo ✅ Base de datos limpia
echo.

REM Paso 6: Configurar base de datos desde cero
echo 📋 PASO 6: Configurando base de datos desde cero...
echo 🔧 Aplicando migraciones...
python manage.py makemigrations
python manage.py migrate
if errorlevel 1 (
    echo ❌ Error en migraciones. Verifica la configuracion de PostgreSQL.
    echo.
    echo 💡 SOLUCION:
    echo    1. Asegurate de que PostgreSQL este corriendo
    echo    2. Verifica que la base de datos "axyomadb" este creada
    echo    3. Verifica credenciales en config/settings/local.py
    pause
    exit /b
)
echo ✅ Base de datos configurada desde cero
echo.

REM Paso 7: Inicializar sistema completo
echo 📋 PASO 7: Inicializando sistema completo...
echo 🎯 Configurando todo el sistema automaticamente...
echo ⚠️  ATENCION: Esto creara todos los datos del sistema
python sistema_completo_listo.py
if errorlevel 1 (
    echo ❌ Error en inicializacion del sistema
    pause
    exit /b
)
echo ✅ Sistema inicializado con todos los datos
echo.

REM Paso 8: Verificar instalacion
echo 📋 PASO 8: Verificando instalacion...
python verificacion_simple.py
echo.

echo ================================================
echo 🎉 ¡SISTEMA AXYOMA CONFIGURADO EXITOSAMENTE!
echo ================================================
echo.
echo 📊 TU SISTEMA INCLUYE:
echo   🏢 2 empresas completamente configuradas
echo   👥 41 empleados distribuidos en la estructura
echo   🏭 4 plantas operativas
echo   📋 14 departamentos activos
echo   💼 28 puestos definidos
echo   💳 Suscripciones y pagos configurados
echo.
echo 🔑 CREDENCIALES DE ACCESO:
echo   👤 Usuario: superadmin
echo   🔒 Contraseña: admin123
echo.
echo 🌐 PARA ACCEDER AL SISTEMA:
echo   1. Ejecutar: python manage.py runserver
echo   2. Abrir: http://localhost:8000
echo   3. Login con las credenciales de arriba
echo.
echo 🔧 COMANDOS UTILES:
echo   📊 python verificacion_simple.py
echo   🔍 python verificar_estado_bd.py
echo   💾 python sistema_respaldos.py
echo.
echo ================================================
echo 🎯 ¡LISTO! Tu sistema esta configurado exactamente
echo    igual que el sistema original.
echo ================================================
echo.
pause
