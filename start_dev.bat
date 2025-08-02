@echo off
echo ==========================================
echo       🛠️  AXYOMA - MODO DESARROLLO
echo ==========================================
echo.
echo Este script prepara el entorno completo de desarrollo
echo.

:: Verificar estructura del proyecto
if not exist "Backend\manage.py" (
    echo ❌ Error: No se encuentra manage.py en Backend\
    pause
    exit /b 1
)

if not exist "frontend\package.json" (
    echo ❌ Error: No se encuentra package.json en frontend\
    pause
    exit /b 1
)

echo 🧹 Limpiando procesos previos...
taskkill /f /im node.exe 2>nul
taskkill /f /im python.exe 2>nul
timeout /t 2 /nobreak >nul

echo.
echo 📦 Verificando dependencias del Frontend...
cd frontend
if not exist "node_modules" (
    echo 📥 Instalando dependencias de React...
    npm install
) else (
    echo ✅ Dependencias de React ya instaladas
)
cd ..

echo.
echo 🗄️  Verificando base de datos...
cd Backend
echo 🔄 Aplicando migraciones...
python manage.py migrate

echo.
echo 📊 Verificando datos de evaluaciones oficiales...
python -c "
import django
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()
from apps.evaluaciones.models_oficiales import EvaluacionOficial
count = EvaluacionOficial.objects.count()
print(f'✅ Evaluaciones oficiales en BD: {count}')
if count == 0:
    print('⚠️  No hay evaluaciones oficiales. Ejecuta cargar_datos_rapido.py')
"

cd ..

echo.
echo 🚀 Iniciando servidores...
echo.

echo 🔧 Iniciando Backend Django...
start "AXYOMA Backend - Django Dev" cmd /k "cd Backend && echo 🔧 Django en modo desarrollo && echo 📍 http://localhost:8000 && python manage.py runserver"

timeout /t 3 /nobreak >nul

echo ⚛️  Iniciando Frontend React...
start "AXYOMA Frontend - React Dev" cmd /k "cd frontend && echo ⚛️ React en modo desarrollo && echo 📍 http://localhost:3000 && npm start"

echo.
echo ⏳ Esperando a que los servidores se inicien...
timeout /t 12 /nobreak >nul

echo 🌐 Abriendo navegador en modo desarrollo...
start http://localhost:3000

echo.
echo ==========================================
echo       ✅ ENTORNO DE DESARROLLO LISTO
echo ==========================================
echo.
echo 🌐 URLs disponibles:
echo    🏠 Frontend:           http://localhost:3000
echo    🔧 Backend API:        http://localhost:8000/api/
echo    📊 Django Admin:       http://localhost:8000/admin/
echo    📋 Evaluaciones API:   http://localhost:8000/api/evaluaciones/
echo    🏥 Evaluaciones NOM:   http://localhost:8000/api/evaluaciones/oficial/
echo.
echo 🛠️  Herramientas útiles:
echo    📝 Logs Django:        Ver ventana "AXYOMA Backend"
echo    📝 Logs React:         Ver ventana "AXYOMA Frontend"  
echo    🗄️  Base de datos:      Usar pgAdmin o scripts Python
echo    🔄 Reiniciar:          Ejecuta este script nuevamente
echo    🛑 Detener:            Ejecuta stop.bat
echo.
echo 💡 Para desarrollo con evaluaciones oficiales:
echo    cd Backend
echo    python mostrar_credenciales.py
echo.
pause
