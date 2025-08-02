@echo off
echo ==========================================
echo       🌟 AXYOMA - INICIO COMPLETO
echo ==========================================
echo.

:: Verificar que estamos en el directorio correcto
if not exist "Backend\manage.py" (
    echo ❌ Error: No se encuentra manage.py en Backend\
    echo Asegurate de ejecutar este script desde la raiz del proyecto
    pause
    exit /b 1
)

if not exist "frontend\package.json" (
    echo ❌ Error: No se encuentra package.json en frontend\
    echo Asegurate de ejecutar este script desde la raiz del proyecto
    pause
    exit /b 1
)

:: Detener procesos previos (por si acaso)
echo 🧹 Limpiando procesos previos...
taskkill /f /im node.exe 2>nul
taskkill /f /im python.exe 2>nul

:: Esperar un momento
timeout /t 2 /nobreak >nul

echo.
echo 🔧 Iniciando Backend Django...
start "AXYOMA Backend - Django" cmd /k "cd Backend && echo 🔧 Servidor Django iniciando... && python manage.py runserver"

:: Esperar a que Django se inicie
echo ⏳ Esperando a que Django se inicie...
timeout /t 5 /nobreak >nul

echo.
echo ⚛️  Iniciando Frontend React...
start "AXYOMA Frontend - React" cmd /k "cd frontend && echo ⚛️ Servidor React iniciando... && npm start"

:: Esperar a que React compile
echo ⏳ Esperando a que React compile...
timeout /t 15 /nobreak >nul

:: Abrir navegador automáticamente
echo.
echo 🌐 Abriendo navegador...
start http://localhost:3000

echo.
echo ==========================================
echo       ✅ AXYOMA COMPLETAMENTE INICIADO
echo ==========================================
echo.
echo 🔧 Backend Django:    http://localhost:8000
echo ⚛️  Frontend React:    http://localhost:3000  
echo 📊 Admin Django:      http://localhost:8000/admin
echo 📋 API Evaluaciones:  http://localhost:8000/api/evaluaciones/
echo.
echo 💡 RECORDATORIO:
echo    - Django Admin: Crear superusuario con 'python manage.py createsuperuser'
echo    - Los logs aparecen en las ventanas de terminal separadas
echo    - Para detener: Ejecuta stop.bat o cierra las ventanas de terminal
echo.
echo 🎉 ¡Listo para trabajar con AXYOMA!
echo.
pause
