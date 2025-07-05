@echo off
echo ====================================
echo   CONFIGURACION BASE DE DATOS
echo ====================================
echo.

echo Creando base de datos PostgreSQL...
psql -U postgres -c "CREATE DATABASE axyoma;"

if %errorlevel% equ 0 (
    echo ✅ Base de datos 'axyoma' creada exitosamente
) else (
    echo ⚠️  Base de datos 'axyoma' ya existe o error en creacion
)

echo.
echo Ejecute 'setup_proyecto_completo.bat' para continuar con la configuracion
echo.
pause
