@echo off
echo ===== LIMPIEZA DE ARCHIVOS INNECESARIOS =====
echo.

echo Eliminando archivos innecesarios...

REM Eliminar archivos de datos mock si existen
if exist "Backend\apps\mock_data.json" (
    del "Backend\apps\mock_data.json"
    echo ✓ mock_data.json eliminado
)

REM Eliminar archivos .bat duplicados/viejos si existen
if exist "start_system.bat" (
    del "start_system.bat"
    echo ✓ start_system.bat eliminado
)

REM Eliminar scripts Python innecesarios
if exist "Backend\verify_axis.py" (
    del "Backend\verify_axis.py"
    echo ✓ verify_axis.py eliminado
)

if exist "Backend\verificacion_final_axis.py" (
    del "Backend\verificacion_final_axis.py"
    echo ✓ verificacion_final_axis.py eliminado
)

if exist "Backend\SOLUCION_AXIS_LOGIN.py" (
    del "Backend\SOLUCION_AXIS_LOGIN.py"
    echo ✓ SOLUCION_AXIS_LOGIN.py eliminado
)

if exist "Backend\fix_migrations.py" (
    del "Backend\fix_migrations.py"
    echo ✓ fix_migrations.py eliminado
)

if exist "Backend\fix_axis_user.py" (
    del "Backend\fix_axis_user.py"
    echo ✓ fix_axis_user.py eliminado
)

if exist "Backend\diagnose_axis.py" (
    del "Backend\diagnose_axis.py"
    echo ✓ diagnose_axis.py eliminado
)

if exist "Backend\create_users.py" (
    del "Backend\create_users.py"
    echo ✓ create_users.py eliminado
)

if exist "Backend\crear_axis_completo.py" (
    del "Backend\crear_axis_completo.py"
    echo ✓ crear_axis_completo.py eliminado
)

if exist "Backend\create_base_plans.py" (
    del "Backend\create_base_plans.py"
    echo ✓ create_base_plans.py eliminado (integrado en start.bat)
)

if exist "Backend\verificacion_final_postgresql.py" (
    del "Backend\verificacion_final_postgresql.py"
    echo ✓ verificacion_final_postgresql.py eliminado (simplificado)
)

REM Eliminar archivos de test viejos
if exist "Backend\test_login.ps1" (
    del "Backend\test_login.ps1"
    echo ✓ test_login.ps1 eliminado
)

if exist "Backend\test_login_powershell.ps1" (
    del "Backend\test_login_powershell.ps1"  
    echo ✓ test_login_powershell.ps1 eliminado
)

echo.
echo ✅ Limpieza completada
echo.
echo 📝 Archivos que PERMANECEN (esenciales):
echo    - start.bat (único script de inicio - TODO INTEGRADO)
echo    - setup_project.bat (setup para nuevos desarrolladores)
echo    - Backend\manage.py (Django management)
echo    - Backend\setup_inicial.py (configuración usuarios y planes)
echo    - Backend\reset_database.py (reseteo completo de BD)
echo    - Backend\requirements.txt (dependencias)
echo    - Frontend y Backend completos (solo código productivo)
echo.
echo 🎯 El sistema ahora usa SOLO start.bat con todo integrado
echo ⚡ Si hay problemas con migraciones, usar: Backend\reset_database.py
echo.
pause
