#!/usr/bin/env python
"""
Script para verificar la estructura de una planta específica
"""

import os
import sys
import django

# Configurar Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')

django.setup()

from apps.users.models import Planta, Departamento, Puesto

def verificar_planta(planta_id):
    """Verificar la estructura de una planta específica"""
    try:
        print(f"🔍 === VERIFICACIÓN DE PLANTA ID {planta_id} ===")
        
        # Buscar la planta
        planta = Planta.objects.filter(planta_id=planta_id).first()
        if not planta:
            print("❌ Planta no encontrada")
            return
            
        print(f"🏭 Planta: {planta.nombre}")
        print(f"🏢 Empresa: {planta.empresa.nombre}")
        
        # Contar departamentos
        departamentos = Departamento.objects.filter(planta=planta)
        print(f"📁 Departamentos: {departamentos.count()}")
        
        dept_names = {}
        for dept in departamentos:
            if dept.nombre in dept_names:
                dept_names[dept.nombre] += 1
            else:
                dept_names[dept.nombre] = 1
        
        print("📋 Lista de departamentos:")
        for nombre, count in dept_names.items():
            if count > 1:
                print(f"  ⚠️  {nombre}: {count} duplicados")
            else:
                print(f"  ✅ {nombre}")
        
        # Contar puestos
        puestos = Puesto.objects.filter(departamento__planta=planta)
        print(f"💼 Puestos totales: {puestos.count()}")
        
        # Mostrar primeros 10 puestos por departamento
        for dept in departamentos[:5]:
            puestos_dept = Puesto.objects.filter(departamento=dept)
            print(f"\n📁 {dept.nombre} ({puestos_dept.count()} puestos):")
            for puesto in puestos_dept[:3]:
                print(f"    - {puesto.nombre}")
                
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    verificar_planta(41)  # Verificar la planta recién creada
