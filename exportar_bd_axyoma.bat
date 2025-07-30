@echo off
REM ===============================================================================
REM                           SISTEMA AXYOMA - INICIALIZACION
REM             Script universal para inicializar AXYOMA en cualquier sistema
REM ===============================================================================
REM Modifica PGUSER y PGPASSWORD según tu configuración

set PGUSER=postgres
set PGPASSWORD=postgres
set PGHOST=localhost
set PGPORT=5432
set DBNAME=axyoma_bd
set OUTPUT=axyoma_bd_export.sql

echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║                    SISTEMA AXYOMA                           ║
echo ║              INICIALIZACION COMPLETA                        ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.

REM 1. Crear la base de datos si no existe
echo 🔧 Verificando/creando base de datos...
psql -U %PGUSER% -h %PGHOST% -p %PGPORT% -c "CREATE DATABASE %DBNAME%;" 2>nul
if %ERRORLEVEL% == 0 (
    echo ✅ Base de datos creada o ya existía
) else (
    echo ⚠️ Base de datos ya existe o hay un problema de conexión
)

REM 2. Aplicar migraciones Django para crear la estructura
echo.
echo 🔄 Aplicando migraciones Django...
cd Backend
call env\Scripts\activate.bat
python manage.py migrate

REM 3. Crear superadmin
echo.
echo 👑 Creando usuario superadmin...
python crear_superadmin.py

REM 4. Ejecutar script de datos iniciales completos (usuarios, empresas, plantas, etc.)
echo.
echo 👥 Creando usuarios de prueba...
python crear_usuarios_prueba.py

echo.
echo 🏢 Creando estructura empresarial completa...
python crear_datos_completos.py

cd ..

echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║                INSTALACION COMPLETADA                       ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.
echo 🎯 SISTEMA LISTO PARA USAR
echo ===============================================
echo 🔑 Credenciales de acceso:
echo    👑 SuperAdmin:    superadmin / 1234
echo    🏢 Admin Empresa: admin_empresa / admin123
echo    🏭 Admin Planta:  admin_planta / admin123
echo.
echo 🌐 URLs de acceso:
echo    Frontend:     http://localhost:3000
echo    Backend API:  http://localhost:8000/api/
echo    Admin Django: http://localhost:8000/admin/
echo.
echo 🛠️ Gestión avanzada:
echo    Ejecuta: cd Backend ^&^& python menu_maestro.py
echo    - Respaldos de BD
echo    - Exportación CSV
echo    - Reseteo completo
echo    - Restauración de datos
echo ===============================================
echo.
pause
