#!/usr/bin/env python
"""
Script para validar datos de empleados y generar respuesta de API simulada
"""

import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')
django.setup()

from apps.users.models import Empleado
from apps.serializers import EmpleadoSerializer

def test_empleados_serializer():
    print("🔍 PROBANDO SERIALIZER DE EMPLEADOS")
    print("=" * 60)
    
    # Obtener algunos empleados
    empleados = Empleado.objects.all()[:5]
    
    print(f"📊 Total empleados: {Empleado.objects.count()}")
    print(f"📊 Empleados para prueba: {len(empleados)}")
    
    # Serializar empleados
    serializer = EmpleadoSerializer(empleados, many=True)
    data = serializer.data
    
    print("\n👥 DATOS SERIALIZADOS:")
    for i, empleado_data in enumerate(data):
        print(f"\n--- Empleado {i+1} ---")
        print(f"ID: {empleado_data.get('empleado_id')}")
        print(f"Número: {empleado_data.get('numero_empleado')}")
        print(f"Nombre: {empleado_data.get('nombre')} {empleado_data.get('apellido_paterno')}")
        print(f"Email: {empleado_data.get('email')}")
        print(f"Puesto ID: {empleado_data.get('puesto_id')}")
        print(f"Puesto Nombre: '{empleado_data.get('puesto_nombre')}'")
        print(f"Departamento ID: {empleado_data.get('departamento_id')}")
        print(f"Departamento Nombre: '{empleado_data.get('departamento_nombre')}'")
        print(f"Planta ID: {empleado_data.get('planta_id')}")
        print(f"Planta Nombre: '{empleado_data.get('planta_nombre')}'")
        print(f"Empresa ID: {empleado_data.get('empresa_id')}")
        print(f"Empresa Nombre: '{empleado_data.get('empresa_nombre')}'")
    
    # Verificar problemas comunes
    print(f"\n🔍 ANÁLISIS DE DATOS:")
    empleados_sin_puesto_nombre = [e for e in data if not e.get('puesto_nombre')]
    empleados_sin_departamento_nombre = [e for e in data if not e.get('departamento_nombre')]
    empleados_sin_planta_nombre = [e for e in data if not e.get('planta_nombre')]
    empleados_sin_empresa_nombre = [e for e in data if not e.get('empresa_nombre')]
    
    print(f"❌ Sin puesto nombre: {len(empleados_sin_puesto_nombre)}")
    print(f"❌ Sin departamento nombre: {len(empleados_sin_departamento_nombre)}")
    print(f"❌ Sin planta nombre: {len(empleados_sin_planta_nombre)}")
    print(f"❌ Sin empresa nombre: {len(empleados_sin_empresa_nombre)}")
    
    if empleados_sin_puesto_nombre:
        print("\n⚠️ EMPLEADOS SIN PUESTO NOMBRE:")
        for emp in empleados_sin_puesto_nombre:
            print(f"   - {emp.get('nombre')} {emp.get('apellido_paterno')} (ID: {emp.get('empleado_id')})")

if __name__ == "__main__":
    test_empleados_serializer()
