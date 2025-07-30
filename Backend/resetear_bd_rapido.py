#!/usr/bin/env python
"""
🗑️ RESETEAR BD COMPLETA - RAPIDO
===============================
"""

import os
import sys
import django

# Configurar Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

django.setup()

def main():
    print("🗑️ BORRANDO TODAS LAS TABLAS...")
    
    from django.db import connection
    
    with connection.cursor() as cursor:
        # Deshabilitar constraints
        cursor.execute('SET session_replication_role = replica;')
        
        # Obtener todas las tablas excepto django
        cursor.execute('''
            SELECT tablename FROM pg_tables 
            WHERE schemaname = 'public' 
            AND tablename NOT LIKE 'django_%'
            AND tablename NOT LIKE 'auth_%'
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

if __name__ == "__main__":
    main()
