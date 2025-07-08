#!/usr/bin/env python
"""
Script para resetear completamente la base de datos
"""

import os
import sys
import django
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

def resetear_base_datos():
    """Resetear completamente la base de datos"""
    
    print('🔄 Reseteando base de datos PostgreSQL...')
    
    # Configuración de la base de datos
    DB_CONFIG = {
        'host': 'localhost',
        'port': '5432',
        'user': 'postgres',
        'password': '123456789',
        'database': 'axyomadb'
    }
    
    try:
        # Conectar a PostgreSQL (sin especificar base de datos)
        conn = psycopg2.connect(
            host=DB_CONFIG['host'],
            port=DB_CONFIG['port'],
            user=DB_CONFIG['user'],
            password=DB_CONFIG['password'],
            database='postgres'  # Conectar a la BD por defecto
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()
        
        # Terminar todas las conexiones a la base de datos
        print('🔄 Cerrando conexiones existentes...')
        cursor.execute(f"""
            SELECT pg_terminate_backend(pid)
            FROM pg_stat_activity
            WHERE datname = '{DB_CONFIG['database']}' AND pid <> pg_backend_pid()
        """)
        
        # Eliminar la base de datos si existe
        print('🗑️  Eliminando base de datos existente...')
        cursor.execute(f"DROP DATABASE IF EXISTS {DB_CONFIG['database']}")
        
        # Crear la base de datos nuevamente
        print('🆕 Creando base de datos nueva...')
        cursor.execute(f"CREATE DATABASE {DB_CONFIG['database']}")
        
        cursor.close()
        conn.close()
        
        print('✅ Base de datos reseteada exitosamente')
        return True
        
    except Exception as e:
        print(f'❌ Error reseteando base de datos: {str(e)}')
        return False

def eliminar_migraciones():
    """Eliminar archivos de migraciones"""
    
    print('🔄 Eliminando archivos de migraciones...')
    
    import glob
    import os
    
    # Buscar y eliminar archivos de migraciones
    for app in ['users', 'subscriptions', 'surveys']:
        migrations_path = f'apps/{app}/migrations'
        if os.path.exists(migrations_path):
            migration_files = glob.glob(f'{migrations_path}/0*.py')
            for file in migration_files:
                os.remove(file)
                print(f'   ✓ Eliminado: {file}')
    
    print('✅ Archivos de migraciones eliminados')

if __name__ == '__main__':
    try:
        # Eliminar migraciones
        eliminar_migraciones()
        
        # Resetear base de datos
        if resetear_base_datos():
            print('\n🎯 RESETEO COMPLETO EXITOSO')
            print('   ✅ Base de datos limpia')
            print('   ✅ Migraciones eliminadas')
            print('\n📝 Próximo paso: Ejecutar start.bat')
        else:
            print('\n❌ ERROR EN EL RESETEO')
            sys.exit(1)
            
    except Exception as e:
        print(f'\n❌ ERROR GRAVE: {str(e)}')
        sys.exit(1)
