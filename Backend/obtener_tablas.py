#!/usr/bin/env python3
"""
Script para obtener tablas principales de la base de datos
"""
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.db import connection

def obtener_tablas():
    """Obtener lista de tablas principales"""
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public' 
            AND table_type = 'BASE TABLE'
            AND table_name NOT LIKE 'django_%'
            AND table_name NOT LIKE 'auth_%'
            AND table_name NOT LIKE '%token%'
            ORDER BY table_name
        """)
        tablas = cursor.fetchall()
        
    print('📋 TABLAS PRINCIPALES DE LA BASE DE DATOS:')
    for i, tabla in enumerate(tablas, 1):
        print(f'{i:2d}. {tabla[0]}')
    
    return [tabla[0] for tabla in tablas]

if __name__ == "__main__":
    obtener_tablas()
