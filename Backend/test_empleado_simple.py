#!/usr/bin/env python
"""
Script simple para verificar si podemos crear un empleado básico
"""
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')
django.setup()

from apps.users.models import Empleado, Puesto

print("🔍 VERIFICACIÓN RÁPIDA DE EMPLEADOS")
print("=" * 40)

# Verificar puestos disponibles
print("📋 Puestos disponibles:")
puestos = Puesto.objects.filter(status=True)[:5]
for puesto in puestos:
    print(f"   - ID {puesto.puesto_id}: {puesto.nombre}")
    print(f"     Departamento: {puesto.departamento.nombre}")
    print(f"     Planta: {puesto.departamento.planta.nombre}")

if puestos.exists():
    primer_puesto = puestos.first()
    print(f"\n💾 Intentando crear empleado con puesto ID {primer_puesto.puesto_id}...")
    
    try:
        # Crear empleado directamente
        empleado = Empleado.objects.create(
            nombre="Test",
            apellido_paterno="Usuario",
            email="test.usuario@test.com",
            puesto=primer_puesto
        )
        print(f"✅ Empleado creado exitosamente!")
        print(f"   ID: {empleado.empleado_id}")
        print(f"   Nombre: {empleado.nombre_completo}")
        
        # Eliminar el empleado de prueba
        empleado.delete()
        print("🗑️ Empleado de prueba eliminado")
        
    except Exception as e:
        print(f"❌ Error creando empleado: {e}")
        import traceback
        traceback.print_exc()
else:
    print("❌ No hay puestos disponibles")
    
print("\n🏁 Verificación completada")
