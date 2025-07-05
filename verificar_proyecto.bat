@echo off
echo ====================================
echo    VERIFICACION PROYECTO AXYOMA
echo ====================================
echo.

echo Verificando estructura del proyecto...
echo.

if not exist "Backend\manage.py" (
    echo ❌ ERROR: Backend\manage.py no encontrado
    goto error
) else (
    echo ✅ Backend\manage.py encontrado
)

if not exist "Backend\requirements.txt" (
    echo ❌ ERROR: Backend\requirements.txt no encontrado
    goto error
) else (
    echo ✅ Backend\requirements.txt encontrado
)

if not exist "frontend\package.json" (
    echo ❌ ERROR: frontend\package.json no encontrado
    goto error
) else (
    echo ✅ frontend\package.json encontrado
)

if not exist "frontend\src\App.tsx" (
    echo ❌ ERROR: frontend\src\App.tsx no encontrado
    goto error
) else (
    echo ✅ frontend\src\App.tsx encontrado
)

if not exist "setup_proyecto_completo.bat" (
    echo ❌ ERROR: setup_proyecto_completo.bat no encontrado
    goto error
) else (
    echo ✅ setup_proyecto_completo.bat encontrado
)

if not exist "start-backend.bat" (
    echo ❌ ERROR: start-backend.bat no encontrado
    goto error
) else (
    echo ✅ start-backend.bat encontrado
)

if not exist "start-frontend.bat" (
    echo ❌ ERROR: start-frontend.bat no encontrado
    goto error
) else (
    echo ✅ start-frontend.bat encontrado
)

if not exist "README.md" (
    echo ❌ ERROR: README.md no encontrado
    goto error
) else (
    echo ✅ README.md encontrado
)

echo.
echo ====================================
echo ✅ PROYECTO VERIFICADO CORRECTAMENTE
echo ====================================
echo.
echo Para configurar el proyecto ejecuta:
echo   setup_proyecto_completo.bat
echo.
echo Para iniciar el sistema:
echo   1. start-backend.bat
echo   2. start-frontend.bat
echo.
goto end

:error
echo.
echo ====================================
echo ❌ ERROR EN LA VERIFICACION
echo ====================================
echo Algunos archivos esenciales faltan.
echo Por favor verifica la estructura del proyecto.
echo.

:end
pause
