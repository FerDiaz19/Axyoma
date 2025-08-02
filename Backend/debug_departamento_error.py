#!/usr/bin/env python
"""
Debug específico para el error de conversión de Departamento a int
"""
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')
django.setup()

from apps.serializers import EmpleadoCreateSerializer

def test_empleado_data():
    print("🔍 TESTING EMPLEADO SERIALIZER")
    print("=" * 40)
    
    # Datos similares a los que envía el frontend
    test_data = {
        'nombre': 'Juan',
        'apellido_paterno': 'Pérez',
        'apellido_materno': 'García',
        'email': 'juan.test@empresa.com',
        'telefono': '555-1234',
        'fecha_ingreso': '2025-01-01',
        'genero': 'Masculino',
        'antiguedad': '2',  # String que debería convertirse a int
        'departamento': '1',  # String que debería convertirse a int  
        'puesto': '1'  # String que debería convertirse a int
    }
    
    print(f"📋 Datos de entrada: {test_data}")
    print(f"📊 Tipos de datos:")
    for key, value in test_data.items():
        print(f"   {key}: {type(value).__name__} = {value}")
    
    print("\n🧪 Probando serializer...")
    
    try:
        serializer = EmpleadoCreateSerializer(data=test_data)
        print(f"✅ Serializer creado")
        
        print("\n🔍 Validando datos...")
        if serializer.is_valid():
            print("✅ Datos válidos")
            print(f"📊 Datos validados:")
            for key, value in serializer.validated_data.items():
                print(f"   {key}: {type(value).__name__} = {value}")
                
            print("\n💾 Intentando guardar...")
            empleado = serializer.save()
            print(f"✅ Empleado guardado! ID: {empleado.empleado_id}")
            
            # Limpiar - eliminar empleado de prueba
            empleado.delete()
            print("🧹 Empleado de prueba eliminado")
            
        else:
            print("❌ Datos inválidos")
            print(f"🚫 Errores: {serializer.errors}")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        print(f"🔍 Tipo de error: {type(e).__name__}")
        import traceback
        print(f"📋 Traceback completo:")
        traceback.print_exc()

if __name__ == "__main__":
    test_empleado_data()
