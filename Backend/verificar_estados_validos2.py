#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import django

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.db import connection
from apps.users.models import Empresa
from apps.subscriptions.models import PlanSuscripcion

# Obtener una empresa y plan reales
empresa = Empresa.objects.first()
plan = PlanSuscripcion.objects.first()

if not empresa or not plan:
    print("❌ No hay empresas o planes disponibles")
    sys.exit(1)

print(f"Usando empresa: {empresa.empresa_id}, plan: {plan.plan_id}")

# Valores a probar en minúsculas
valores_estado = ['activa', 'vencida', 'cancelada', 'suspendida']

print("Probando valores válidos para el campo 'estado':")

cursor = connection.cursor()

for valor in valores_estado:
    try:
        cursor.execute("BEGIN")
        cursor.execute("""
            INSERT INTO suscripciones (empresa, plan, fecha_inicio, fecha_fin, estado, fecha_registro) 
            VALUES (%s, %s, '2025-01-01', '2025-12-31', %s, NOW())
        """, [empresa.empresa_id, plan.plan_id, valor])
        cursor.execute("ROLLBACK")
        print(f"   ✅ '{valor}' - VÁLIDO")
    except Exception as e:
        cursor.execute("ROLLBACK")
        print(f"   ❌ '{valor}' - INVÁLIDO: {str(e)}")

cursor.close()
