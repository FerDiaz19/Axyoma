#!/usr/bin/env python
"""
Script para debuggear el problema con el POST de empleados
"""
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')
django.setup()

from apps.users.models import Empleado, Puesto, Departamento, Planta, Empresa
from apps.serializers import EmpleadoCreateSerializer

def debug_empleado_creation():
    print("🔍 DEBUGGEANDO CREACIÓN DE EMPLEADOS")
    print("=" * 50)
    
    # Datos de prueba similares a los que envía el frontend
    test_data = {
        'nombre': 'Juan',
        'apellido_paterno': 'Pérez',
        'apellido_materno': 'García',
        'email': 'juan.perez@test.com',
        'telefono': '555-1234',
        'fecha_ingreso': '2025-01-01',
        'genero': 'Masculino',
        'antiguedad': 2,
        'departamento': 1,  # Esto se ignora pero el frontend lo envía
        'puesto': 1  # Este es el importante
    }
    
    print(f"📝 Datos de prueba: {test_data}")
    
    # Verificar que existe el puesto
    try:
        puesto = Puesto.objects.get(puesto_id=1)
        print(f"✅ Puesto encontrado: {puesto.nombre} (ID: {puesto.puesto_id})")
        print(f"   Departamento: {puesto.departamento.nombre}")
        print(f"   Planta: {puesto.departamento.planta.nombre}")
        print(f"   Empresa: {puesto.departamento.planta.empresa.nombre}")
    except Puesto.DoesNotExist:
        print("❌ No existe puesto con ID 1")
        print("🔍 Puestos disponibles:")
        for p in Puesto.objects.all()[:5]:
            print(f"   - ID {p.puesto_id}: {p.nombre} (Depto: {p.departamento.nombre})")
        return
    
    # Probar el serializer
    print("\n🧪 Probando EmpleadoCreateSerializer...")
    try:
        serializer = EmpleadoCreateSerializer(data=test_data)
        if serializer.is_valid():
            print("✅ Datos válidos")
            print(f"📊 Datos validados: {serializer.validated_data}")
            
            # Intentar crear el empleado
            print("\n💾 Intentando crear empleado...")
            empleado = serializer.save()
            print(f"✅ Empleado creado exitosamente!")
            print(f"   ID: {empleado.empleado_id}")
            print(f"   Nombre: {empleado.nombre_completo}")
            print(f"   Email: {empleado.email}")
            print(f"   Puesto: {empleado.puesto.nombre}")
            
        else:
            print("❌ Datos inválidos")
            print(f"🚫 Errores: {serializer.errors}")
            
    except Exception as e:
        print(f"❌ Error en serializer: {e}")
        import traceback
        traceback.print_exc()

def check_database_structure():
    print("\n🏗️ VERIFICANDO ESTRUCTURA DE BD")
    print("=" * 50)
    
    empresas = Empresa.objects.all()
    print(f"📊 Total empresas: {empresas.count()}")
    
    for empresa in empresas[:3]:
        print(f"\n🏢 Empresa: {empresa.nombre} (ID: {empresa.empresa_id})")
        plantas = Planta.objects.filter(empresa=empresa)
        print(f"   🏭 Plantas: {plantas.count()}")
        
        for planta in plantas:
            departamentos = Departamento.objects.filter(planta=planta)
            print(f"     🏢 Planta {planta.nombre}: {departamentos.count()} departamentos")
            
            for depto in departamentos:
                puestos = Puesto.objects.filter(departamento=depto)
                empleados = Empleado.objects.filter(puesto__departamento=depto)
                print(f"       📝 {depto.nombre}: {puestos.count()} puestos, {empleados.count()} empleados")

if __name__ == "__main__":
    check_database_structure()
    debug_empleado_creation()
