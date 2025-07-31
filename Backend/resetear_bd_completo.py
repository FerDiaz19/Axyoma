#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
RESETEO COMPLETO DE LA BASE DE DATOS
===================================
Borra completamente la base de datos y crea una nueva desde cero
"""

import os
import sys
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

def resetear_bd_completo():
    """Resetea completamente la base de datos"""
    print("🔄 RESETEO COMPLETO DE LA BASE DE DATOS")
    print("="*50)
    
    # Configuración de la base de datos
    db_config = {
        'host': 'localhost',
        'port': '5432',
        'user': 'postgres',
        'password': '12345678'
    }
    
    db_name = 'axyoma'
    
    try:
        # 1. Conectar a PostgreSQL (no a la base de datos específica)
        print("🔌 Conectando a PostgreSQL...")
        conn = psycopg2.connect(
            host=db_config['host'],
            port=db_config['port'],
            user=db_config['user'],
            password=db_config['password'],
            database='postgres'  # Conectar a la BD por defecto
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()
        
        # 2. Terminar todas las conexiones activas a la base de datos
        print("🚫 Terminando conexiones activas...")
        cursor.execute(f"""
            SELECT pg_terminate_backend(pid)
            FROM pg_stat_activity
            WHERE datname = '{db_name}' AND pid <> pg_backend_pid()
        """)
        
        # 3. Borrar la base de datos si existe
        print(f"🗑️ Eliminando base de datos '{db_name}'...")
        cursor.execute(f"DROP DATABASE IF EXISTS {db_name}")
        
        # 4. Crear nueva base de datos
        print(f"🆕 Creando nueva base de datos '{db_name}'...")
        cursor.execute(f"CREATE DATABASE {db_name} WITH ENCODING 'UTF8'")
        
        print("✅ Base de datos reseteada completamente!")
        
        cursor.close()
        conn.close()
        
        return True
        
    except Exception as e:
        print(f"❌ Error al resetear BD: {str(e)}")
        return False

def eliminar_migraciones():
    """Elimina todos los archivos de migración excepto __init__.py"""
    print("\n🧹 Eliminando archivos de migración...")
    
    # Directorios de migraciones
    migration_dirs = [
        'apps/users/migrations',
        'apps/subscriptions/migrations',
        'apps/evaluaciones/migrations'
    ]
    
    for migration_dir in migration_dirs:
        if os.path.exists(migration_dir):
            for filename in os.listdir(migration_dir):
                if filename.endswith('.py') and filename != '__init__.py':
                    filepath = os.path.join(migration_dir, filename)
                    try:
                        os.remove(filepath)
                        print(f"   ✅ Eliminado: {filepath}")
                    except Exception as e:
                        print(f"   ❌ Error eliminando {filepath}: {e}")
    
    print("✅ Archivos de migración eliminados!")

def main():
    """Función principal"""
    try:
        # 1. Resetear la base de datos
        if resetear_bd_completo():
            # 2. Eliminar migraciones
            eliminar_migraciones()
            
            print("\n" + "="*50)
            print("🎉 RESETEO COMPLETO EXITOSO")
            print("✅ Base de datos recreada")
            print("✅ Migraciones eliminadas")
            print("\nAhora puedes ejecutar:")
            print("1. python manage.py makemigrations")
            print("2. python manage.py migrate")
            print("3. python implementar_sistema_completo.py")
            print("="*50)
            
            return True
        else:
            return False
            
    except Exception as e:
        print(f"❌ ERROR CRÍTICO: {str(e)}")
        return False

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
