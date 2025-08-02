#!/usr/bin/env python
import os
import sys
import django

# Configurar Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'axyoma.settings')
django.setup()

from apps.users.models import Empleado, Empresa, Planta, Departamento, Puesto

def revisar_empleados():
    print("=== EMPRESAS ===")
    empresas = Empresa.objects.all()
    for emp in empresas:
        print(f"ID: {emp.id} - {emp.nombre}")
    
    print("\n=== EMPLEADOS POR EMPRESA ===")
    empleados = Empleado.objects.select_related('empresa', 'planta', 'departamento', 'puesto').all()[:20]
    
    for emp in empleados:
        empresa_nombre = emp.empresa.nombre if emp.empresa else "Sin empresa"
        planta_nombre = emp.planta.nombre if emp.planta else "Sin planta"
        depto_nombre = emp.departamento.nombre if emp.departamento else "Sin depto"
        puesto_nombre = emp.puesto.nombre if emp.puesto else "Sin puesto"
        
        print(f"ID: {emp.id} - {emp.nombre} {emp.apellido}")
        print(f"   Empresa: {empresa_nombre}")
        print(f"   Planta: {planta_nombre}")
        print(f"   Depto: {depto_nombre}")
        print(f"   Puesto: {puesto_nombre}")
        print("   ---")
    
    print(f"\nTotal empleados: {empleados.count()}")
    
    # Revisar empleados de AXIS2 específicamente
    print("\n=== EMPLEADOS DE AXIS2 ===")
    try:
        axis2 = Empresa.objects.get(nombre__icontains="axis")
        empleados_axis2 = Empleado.objects.filter(empresa=axis2)
        print(f"Empresa AXIS2 encontrada: {axis2.nombre} (ID: {axis2.id})")
        print(f"Empleados en AXIS2: {empleados_axis2.count()}")
        
        for emp in empleados_axis2[:10]:
            print(f"  - {emp.nombre} {emp.apellido}")
    except Empresa.DoesNotExist:
        print("No se encontró empresa AXIS2")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    revisar_empleados()
