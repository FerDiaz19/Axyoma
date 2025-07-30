@echo off
echo ==========================================
echo 🔄 RESETEAR BD COMPLETA - RAPIDO
echo ==========================================

cd /d "c:\xampp2\htdocs\UTT4B\Axyoma2\Backend"

echo 🗑️ Borrando todas las tablas...
python -c "
import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.db import connection
with connection.cursor() as cursor:
    # Deshabilitar constraints
    cursor.execute('SET session_replication_role = replica;')
    
    # Obtener todas las tablas excepto django
    cursor.execute('''
        SELECT tablename FROM pg_tables 
        WHERE schemaname = 'public' 
        AND tablename NOT LIKE 'django_%%'
        AND tablename NOT LIKE 'auth_%%'
        AND tablename != 'authtoken_token'
    ''')
    
    tablas = [row[0] for row in cursor.fetchall()]
    print(f'Borrando {len(tablas)} tablas...')
    
    for tabla in tablas:
        try:
            cursor.execute(f'TRUNCATE TABLE {tabla} RESTART IDENTITY CASCADE')
            print(f'✅ {tabla}')
        except Exception as e:
            print(f'❌ {tabla}: {e}')
    
    # Rehabilitar constraints
    cursor.execute('SET session_replication_role = DEFAULT;')
    
print('🎉 BD RESETEADA COMPLETAMENTE')
"

echo.
echo ✅ BD LIMPIA - Presiona cualquier tecla para continuar...
pause > nul
