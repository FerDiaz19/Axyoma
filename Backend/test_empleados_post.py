#!/usr/bin/env python
"""
Script para verificar y probar los endpoints corregidos
"""
import os
import sys
import requests
import json

# Cambiar al directorio Backend si es necesario
if not os.path.exists('manage.py'):
    if os.path.exists('Backend/manage.py'):
        os.chdir('Backend')
        print("📁 Cambiado al directorio Backend")
    else:
        print("❌ No se encuentra manage.py")
        sys.exit(1)

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')
import django
django.setup()

from apps.users.models import Empresa, Planta, Departamento, Puesto

# Token de autenticación del usuario
TOKEN = 'a5bc8a7c3e2f8b5794d8e0c9a7b6f5e4c3d2a9b8'
BASE_URL = 'http://localhost:8000/api'
EMPRESA_ID = 3

headers = {
    'Authorization': f'Token {TOKEN}',
    'Content-Type': 'application/json'
}

def verificar_datos_bd():
    """Verificar que existan datos básicos en BD"""
    print("🔍 Verificando datos en BD...")
    
    try:
        empresa = Empresa.objects.get(empresa_id=EMPRESA_ID)
        print(f"✅ Empresa: {empresa.nombre}")
        
        plantas = Planta.objects.filter(empresa=empresa)
        print(f"🏭 Plantas: {plantas.count()}")
        
        for planta in plantas:
            departamentos = Departamento.objects.filter(planta=planta)
            print(f"   📋 {planta.nombre}: {departamentos.count()} departamentos")
            
            for dept in departamentos:
                puestos = Puesto.objects.filter(departamento=dept)
                print(f"      💼 {dept.nombre}: {puestos.count()} puestos")
                
        return True
        
    except Empresa.DoesNotExist:
        print(f"❌ No existe empresa con ID {EMPRESA_ID}")
        return False

def crear_datos_prueba():
    """Crear datos de prueba si no existen"""
    print("🔧 Creando datos de prueba...")
    
    try:
        empresa = Empresa.objects.get(empresa_id=EMPRESA_ID)
        
        # Crear planta si no existe
        planta, created = Planta.objects.get_or_create(
            nombre="Planta Principal",
            empresa=empresa,
            defaults={'direccion': 'Dirección de prueba'}
        )
        if created:
            print("✅ Planta creada")
        
        # Crear departamento si no existe
        departamento, created = Departamento.objects.get_or_create(
            nombre="Recursos Humanos",
            planta=planta,
            defaults={'descripcion': 'Departamento de RRHH'}
        )
        if created:
            print("✅ Departamento creado")
        
        # Crear puesto si no existe
        puesto, created = Puesto.objects.get_or_create(
            nombre="Analista de RRHH",
            departamento=departamento,
            defaults={'descripcion': 'Analista de recursos humanos'}
        )
        if created:
            print("✅ Puesto creado")
            
        return True
        
    except Exception as e:
        print(f"❌ Error creando datos: {e}")
        return False

def test_endpoint_post():
    """Probar crear empleado via POST"""
    print("\n🧪 Probando POST de empleado...")
    
    nuevo_empleado = {
        "nombre": "Juan",
        "apellido_paterno": "Pérez",
        "apellido_materno": "García", 
        "email": "juan.perez@test.com",
        "telefono": "555-1234",
        "fecha_ingreso": "2025-01-01",
        "puesto": 1,  # Asumiendo que existe puesto con ID 1
        "genero": "Masculino",
        "antiguedad": 1,
        "departamento": 1,
        "planta": 1
    }
    
    try:
        response = requests.post(f"{BASE_URL}/empleados/", json=nuevo_empleado, headers=headers)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 201:
            print("✅ Empleado creado exitosamente")
            data = response.json()
            print(f"ID: {data.get('empleado_id')}")
            print(f"Nombre: {data.get('nombre')} {data.get('apellido_paterno')}")
            return True
        else:
            print(f"❌ Error: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        return False

def main():
    print("🚀 Verificando correcciones de AXYOMA")
    print("="*50)
    
    # 1. Verificar datos en BD
    if not verificar_datos_bd():
        crear_datos_prueba()
    
    # 2. Probar POST de empleado
    test_endpoint_post()
    
    print("\n✨ Verificación completada")
    print("🌐 Ahora puedes probar el frontend en http://localhost:3000")

if __name__ == "__main__":
    main()
