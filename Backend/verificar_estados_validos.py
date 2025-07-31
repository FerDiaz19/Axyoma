#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import django

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.db import connection

# Intentar insertar diferentes valores para ver cuáles funcionan
valores_estado = ['activa', 'Activa', 'ACTIVA', 'Active', 'vencida', 'Vencida', 'VENCIDA']

print("Probando valores válidos para el campo 'estado':")

cursor = connection.cursor()

for valor in valores_estado:
    try:
        # Probar con una consulta de inserción temporal
        cursor.execute("""
            INSERT INTO suscripciones (empresa, plan, fecha_inicio, fecha_fin, estado, fecha_registro) 
            VALUES (999, 999, '2025-01-01', '2025-12-31', %s, NOW())
        """, [valor])
        cursor.execute("ROLLBACK")  # Deshacer la inserción
        print(f"   ✅ '{valor}' - VÁLIDO")
    except Exception as e:
        print(f"   ❌ '{valor}' - INVÁLIDO: {str(e)}")

cursor.close()
