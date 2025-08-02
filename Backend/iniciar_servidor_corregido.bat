@echo off
echo ====================================================
echo    SCRIPT DE PRUEBA - AXYOMA ENDPOINTS
echo ====================================================
echo.

cd /d "%~dp0"

echo [1/4] Verificando directorio...
if not exist "manage.py" (
    echo ERROR: No se encuentra manage.py
    echo Cambiando al directorio Backend...
    cd Backend
    if not exist "manage.py" (
        echo ERROR: manage.py no encontrado en Backend/
        pause
        exit /b 1
    )
)

echo [2/4] Aplicando migraciones...
python manage.py migrate --run-syncdb

echo.
echo [3/4] Creando datos de prueba (si no existen)...
python -c "
import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')
django.setup()

from apps.users.models import Empresa, Planta

# Verificar si existe empresa con ID 3
try:
    empresa = Empresa.objects.get(empresa_id=3)
    print(f'✅ Empresa encontrada: {empresa.nombre}')
    
    # Verificar plantas
    plantas = Planta.objects.filter(empresa=empresa)
    print(f'   Plantas: {plantas.count()}')
    
    if plantas.count() == 0:
        print('   Creando planta de prueba...')
        Planta.objects.create(
            nombre='Planta Principal',
            direccion='Dirección de prueba',
            empresa=empresa
        )
        print('   ✅ Planta creada')
    
except Empresa.DoesNotExist:
    print('❌ No existe empresa con ID 3')
    print('   Listando empresas disponibles:')
    for emp in Empresa.objects.all()[:5]:
        print(f'   - ID {emp.empresa_id}: {emp.nombre}')
"

echo.
echo [4/4] Iniciando servidor Django...
echo El servidor se iniciará en http://localhost:8000
echo.
echo ENDPOINTS CORREGIDOS:
echo - /api/plantas/?empresa_id=3
echo - /api/departamentos/?empresa_id=3  
echo - /api/puestos/?empresa_id=3
echo - /api/empleados/?empresa_id=3
echo.
echo Presiona Ctrl+C para detener el servidor
echo.

python manage.py runserver
