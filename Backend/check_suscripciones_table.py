#!/usr/bin/env python3
import os
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')
django.setup()

from django.db import connection

# Consultar estructura de las tablas relacionadas con suscripciones
tables = ['suscripciones_empresa', 'planes', 'empresas']

for table_name in tables:
    print(f"\n=== Tabla: {table_name} ===")
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT column_name, data_type 
            FROM information_schema.columns 
            WHERE table_name = %s
            ORDER BY ordinal_position
        """, [table_name])
        columns = cursor.fetchall()
        
        if columns:
            for column in columns:
                print(f"{column[0]} - {column[1]}")
        else:
            print("No se encontró la tabla")
