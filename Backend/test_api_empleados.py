#!/usr/bin/env python
"""
Script para probar la API de empleados directamente
"""

import os
import sys
import django
import requests
import json

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')
django.setup()

def test_empleados_api():
    print("🔍 PROBANDO API DE EMPLEADOS")
    print("=" * 60)
    
    # Primero, hacer login para obtener token
    login_data = {
        'username': 'superadmin',
        'password': '1234'
    }
    
    try:
        # Login
        login_response = requests.post('http://localhost:8000/api/usuarios/login/', json=login_data)
        
        if login_response.status_code == 200:
            token = login_response.json().get('token')
            print(f"✅ Login exitoso, token obtenido")
            
            # Headers con token
            headers = {
                'Authorization': f'Token {token}',
                'Content-Type': 'application/json'
            }
            
            # Obtener empleados
            empleados_response = requests.get('http://localhost:8000/api/empleados/', headers=headers)
            
            if empleados_response.status_code == 200:
                empleados_data = empleados_response.json()
                print(f"✅ Empleados obtenidos: {len(empleados_data)} registros")
                
                # Mostrar los primeros 3 empleados con detalle
                print("\n👥 MUESTRA DE DATOS DE API:")
                for i, empleado in enumerate(empleados_data[:3]):
                    print(f"\n--- Empleado {i+1} ---")
                    print(f"ID: {empleado.get('empleado_id')}")
                    print(f"Número: {empleado.get('numero_empleado')}")
                    print(f"Nombre: {empleado.get('nombre')} {empleado.get('apellido_paterno')}")
                    print(f"Email: {empleado.get('email')}")
                    print(f"Puesto ID: {empleado.get('puesto_id')}")
                    print(f"Puesto Nombre: {empleado.get('puesto_nombre')}")
                    print(f"Departamento ID: {empleado.get('departamento_id')}")
                    print(f"Departamento Nombre: {empleado.get('departamento_nombre')}")
                    print(f"Planta ID: {empleado.get('planta_id')}")
                    print(f"Planta Nombre: {empleado.get('planta_nombre')}")
                    print(f"Empresa ID: {empleado.get('empresa_id')}")
                    print(f"Empresa Nombre: {empleado.get('empresa_nombre')}")
                    
                # Verificar si hay algún problema con los nombres
                empleados_sin_puesto = [e for e in empleados_data if not e.get('puesto_nombre')]
                if empleados_sin_puesto:
                    print(f"\n⚠️ EMPLEADOS SIN NOMBRE DE PUESTO: {len(empleados_sin_puesto)}")
                    for emp in empleados_sin_puesto[:3]:
                        print(f"   - {emp.get('nombre')} {emp.get('apellido_paterno')} (ID: {emp.get('empleado_id')})")
                
            else:
                print(f"❌ Error obteniendo empleados: {empleados_response.status_code}")
                print(f"Response: {empleados_response.text}")
                
        else:
            print(f"❌ Error en login: {login_response.status_code}")
            print(f"Response: {login_response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Error de conexión. ¿Está corriendo el servidor Django?")
        print("   Ejecuta: python manage.py runserver")
    except Exception as e:
        print(f"❌ Error inesperado: {e}")

if __name__ == "__main__":
    test_empleados_api()
