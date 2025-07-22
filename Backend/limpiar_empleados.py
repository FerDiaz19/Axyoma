#!/usr/bin/env python
"""
Script para limpiar empleados innecesarios de la BD
"""

import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')
django.setup()

from apps.users.models import Empleado, Puesto
from django.db import transaction
import random

def limpiar_empleados():
    """Limpiar empleados innecesarios, dejando solo algunos por puesto"""
    
    print("🧹 Limpiando empleados innecesarios...")
    
    try:
        print("=== EMPLEADOS ANTES ===")
        print(f"Total empleados: {Empleado.objects.count()}")
        
        # Mostrar distribución por puesto
        puestos = Puesto.objects.all()
        for puesto in puestos:
            empleados_count = Empleado.objects.filter(puesto=puesto).count()
            if empleados_count > 0:
                print(f"- {puesto.nombre}: {empleados_count} empleados")
        
        empleados_eliminados = 0
        
        # Por cada puesto, mantener solo 1-2 empleados máximo
        for puesto in puestos:
            empleados_puesto = list(Empleado.objects.filter(puesto=puesto))
            
            if len(empleados_puesto) > 2:
                # Mantener solo los primeros 2 empleados, eliminar el resto
                empleados_a_mantener = empleados_puesto[:2]
                empleados_a_eliminar = empleados_puesto[2:]
                
                for empleado in empleados_a_eliminar:
                    print(f"❌ Eliminando: {empleado.nombre} {empleado.apellido_paterno} ({puesto.nombre})")
                    empleado.delete()
                    empleados_eliminados += 1
            
            elif len(empleados_puesto) > 1:
                # Si tiene más de 1, mantener solo 1
                empleados_a_eliminar = empleados_puesto[1:]
                
                for empleado in empleados_a_eliminar:
                    print(f"❌ Eliminando: {empleado.nombre} {empleado.apellido_paterno} ({puesto.nombre})")
                    empleado.delete()
                    empleados_eliminados += 1
        
        print(f"\n=== EMPLEADOS DESPUÉS ===")
        print(f"Total empleados: {Empleado.objects.count()}")
        print(f"Empleados eliminados: {empleados_eliminados}")
        
        # Mostrar distribución final
        print("\nDistribución final por puesto:")
        for puesto in puestos:
            empleados_count = Empleado.objects.filter(puesto=puesto).count()
            if empleados_count > 0:
                empleado_nombre = Empleado.objects.filter(puesto=puesto).first()
                print(f"- {puesto.nombre}: {empleados_count} empleado(s) - {empleado_nombre.nombre} {empleado_nombre.apellido_paterno}")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    limpiar_empleados()
