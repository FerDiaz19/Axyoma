@echo off
title Limpiar Archivos de Desarrollo
color 0D

echo.
echo ==========================================
echo      LIMPIEZA DE ARCHIVOS DE DESARROLLO
echo ==========================================
echo.
echo Este script eliminará todos los archivos de:
echo - Pruebas (test_*.py)
echo - Debug y correcciones (debug_*.py, fix_*.py)
echo - Verificaciones (verificar_*.py, check_*.py)
echo - Archivos temporales y de desarrollo
echo.
set /p confirm="¿Continuar con la limpieza? (S/N): "
if /I not "%confirm%"=="S" (
    echo Operacion cancelada.
    pause
    exit /b
)

echo.
echo Eliminando archivos...

cd /d "%~dp0\Backend"

REM Eliminar archivos de test
del /q test_*.py 2>nul
del /q test_*.js 2>nul

REM Eliminar archivos de debug y fix
del /q debug_*.py 2>nul
del /q fix_*.py 2>nul

REM Eliminar archivos de verificación y check
del /q verificar_*.py 2>nul
del /q check_*.py 2>nul

REM Eliminar archivos de corrección
del /q corregir_*.py 2>nul

REM Eliminar archivos de creación/mostrar temporales
del /q crear_credenciales.py 2>nul
del /q crear_plantas_test.py 2>nul
del /q create_test_user.py 2>nul
del /q mostrar_*.py 2>nul
del /q asignar_empresa_evaluaciones.py 2>nul

REM Eliminar archivos de inicialización simple y desarrollo
del /q inicializar_simple.py 2>nul
del /q resumen_sistema.py 2>nul

REM Eliminar archivos de texto temporales
del /q output.txt 2>nul
del /q README_DEPURADO.md 2>nul

REM Eliminar directorio Scripts si está vacío o tiene archivos temporales
if exist Scripts\ (
    rmdir /s /q Scripts 2>nul
)

REM Eliminar directorio scripts_utiles si existe
if exist scripts_utiles\ (
    rmdir /s /q scripts_utiles 2>nul
)

REM Limpiar archivos del frontend si los hay
cd ..\frontend
del /q test_*.js 2>nul

echo.
echo ==========================================
echo          LIMPIEZA COMPLETADA
echo ==========================================
echo.
echo Archivos eliminados:
echo - Todos los archivos test_*
echo - Todos los archivos debug_* y fix_*
echo - Todos los archivos verificar_* y check_*
echo - Archivos temporales de desarrollo
echo - Directorios de scripts temporales
echo.
echo El sistema ahora contiene solo los archivos necesarios
echo para producción y el inicializador de datos.
echo.
pause
