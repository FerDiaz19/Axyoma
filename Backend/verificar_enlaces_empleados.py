#!/usr/bin/env python
"""
Script para verificar que los empleados están correctamente enlazados
"""

import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')
django.setup()

from apps.users.models import Empleado, Puesto, Departamento, Planta, Empresa

def verificar_enlaces_empleados():
    print("🔍 VERIFICANDO ENLACES DE EMPLEADOS")
    print("=" * 60)
    
    # Obtener algunos empleados para verificar
    empleados = Empleado.objects.all()[:10]
    
    print(f"📊 Total empleados en BD: {Empleado.objects.count()}")
    print("\n👥 MUESTRA DE EMPLEADOS (primeros 10):")
    print("-" * 100)
    
    for empleado in empleados:
        try:
            # Verificar relaciones
            puesto = empleado.puesto
            departamento = puesto.departamento
            planta = departamento.planta
            empresa = planta.empresa
            
            print(f"👤 {empleado.nombre} {empleado.apellido_paterno}")
            print(f"   📧 Email: {empleado.email}")
            print(f"   💼 Puesto: {puesto.nombre}")
            print(f"   📋 Departamento: {departamento.nombre}")
            print(f"   🏭 Planta: {planta.nombre}")
            print(f"   🏢 Empresa: {empresa.nombre}")
            print(f"   📅 Fecha ingreso: {empleado.fecha_ingreso}")
            print("-" * 100)
            
        except Exception as e:
            print(f"❌ Error con empleado {empleado.nombre}: {e}")
            print("-" * 100)
    
    # Verificar estadísticas por planta
    print(f"\n📈 ESTADÍSTICAS POR PLANTA:")
    plantas = Planta.objects.all()
    
    for planta in plantas:
        total_empleados = Empleado.objects.filter(puesto__departamento__planta=planta).count()
        print(f"🏭 {planta.nombre}: {total_empleados} empleados")
        
        # Mostrar por departamento
        departamentos = Departamento.objects.filter(planta=planta)
        for dept in departamentos:
            empleados_dept = Empleado.objects.filter(puesto__departamento=dept).count()
            if empleados_dept > 0:
                print(f"   📋 {dept.nombre}: {empleados_dept} empleados")

if __name__ == "__main__":
    verificar_enlaces_empleados()
