#!/usr/bin/env python
"""
🧪 TEST RÁPIDO DE CORRECCIONES
===========================
"""

import os
import sys
import django

# Configurar Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

django.setup()

def test_carga_datos():
    """Test carga de datos iniciales"""
    print("🔄 Testing carga datos iniciales...")
    
    try:
        from django.contrib.auth.models import User
        from apps.users.models import Empresa, Planta, Departamento, Puesto, Empleado
        
        print("✅ Imports correctos")
        
        # Verificar si existen datos
        print(f"📊 Usuarios: {User.objects.count()}")
        print(f"📊 Empresas: {Empresa.objects.count()}")
        print(f"📊 Empleados: {Empleado.objects.count()}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_empleados_csv():
    """Test CSV empleados"""
    print("🔄 Testing CSV empleados...")
    
    try:
        from django.db import connection
        
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT 
                    e.empleado_id,
                    e.nombre,
                    e.apellido_paterno,
                    p.nombre as puesto_nombre
                FROM empleados e
                LEFT JOIN puestos p ON e.puesto_id = p.puesto_id
                LIMIT 1
            """)
            
            result = cursor.fetchone()
            if result:
                print(f"✅ Query funciona: {result}")
            else:
                print("⚠️ No hay datos de empleados")
        
        return True
        
    except Exception as e:
        print(f"❌ Error en query: {e}")
        return False

if __name__ == "__main__":
    print("🧪 TESTS RÁPIDOS DE CORRECCIONES")
    print("=" * 40)
    
    test1 = test_carga_datos()
    test2 = test_empleados_csv()
    
    if test1 and test2:
        print("🎉 TODAS LAS CORRECCIONES FUNCIONAN")
    else:
        print("⚠️ HAY PROBLEMAS")
