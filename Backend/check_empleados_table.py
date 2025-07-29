#!/usr/bin/env python3
import os
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')
django.setup()

from django.db import connection

# Consultar estructura de la tabla empleados
with connection.cursor() as cursor:
    cursor.execute("""
        SELECT column_name, data_type 
        FROM information_schema.columns 
        WHERE table_name = 'empleados'
        ORDER BY ordinal_position
    """)
    columns = cursor.fetchall()
    
    print("Columnas de la tabla empleados:")
    print("-" * 40)
    for column in columns:
        print(f"{column[0]} - {column[1]}")
