#!/usr/bin/env python
"""
Script para probar la creación de un empleado completo
"""
import requests
import json

BASE_URL = "http://127.0.0.1:8000/api"

def test_empleado_creation():
    print("👷 PRUEBA DE CREACIÓN DE EMPLEADO")
    print("="*50)
    
    # Login
    login_data = {
        "username": "juan.perez@codewave.com",
        "password": "123456"
    }
    
    response = requests.post(f"{BASE_URL}/auth/login/", json=login_data)
    if response.status_code != 200:
        print(f"❌ Error en login: {response.status_code}")
        return
    
    token = response.json().get('token')
    headers = {
        'Authorization': f'Token {token}',
        'Content-Type': 'application/json'
    }
    
    # Obtener datos necesarios
    plantas = requests.get(f"{BASE_URL}/plantas/", headers=headers).json()
    departamentos = requests.get(f"{BASE_URL}/departamentos/", headers=headers).json()
    puestos = requests.get(f"{BASE_URL}/puestos/", headers=headers).json()
    
    if not plantas or not departamentos or not puestos:
        print("❌ No hay datos suficientes para crear empleado")
        return
    
    planta = plantas[0]
    # Buscar un departamento de esta planta
    departamento = next((d for d in departamentos if d['planta_id'] == planta['planta_id']), None)
    if not departamento:
        print("❌ No hay departamentos para la planta seleccionada")
        return
    
    # Buscar un puesto de este departamento
    puesto = next((p for p in puestos if p['departamento_id'] == departamento['departamento_id']), None)
    if not puesto:
        print("❌ No hay puestos para el departamento seleccionado")
        return
    
    print(f"✅ Datos seleccionados:")
    print(f"   Planta: {planta['nombre']} (ID: {planta['planta_id']})")
    print(f"   Departamento: {departamento['nombre']} (ID: {departamento['departamento_id']})")
    print(f"   Puesto: {puesto['nombre']} (ID: {puesto['puesto_id']})")
    
    # Crear empleado
    import time
    timestamp = int(time.time())
    empleado_data = {
        "nombre": f"Empleado Test {timestamp}",
        "apellido_paterno": "Apellido",
        "apellido_materno": "Materno",
        "genero": "Masculino",
        "antiguedad": 2,
        "puesto": puesto['puesto_id'],
        "departamento": departamento['departamento_id'],
        "planta": planta['planta_id']
    }
    
    print(f"\n🔨 Creando empleado...")
    print(f"Datos: {json.dumps(empleado_data, indent=2)}")
    
    response = requests.post(f"{BASE_URL}/empleados/", json=empleado_data, headers=headers)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.text}")
    
    if response.status_code == 201:
        empleado = response.json()
        print(f"✅ Empleado creado exitosamente!")
        print(f"   ID: {empleado.get('empleado_id')}")
        print(f"   Nombre: {empleado.get('nombre')} {empleado.get('apellido_paterno')}")
    else:
        print(f"❌ Error creando empleado:")
        try:
            error_data = response.json()
            print(f"   Error: {json.dumps(error_data, indent=2)}")
        except:
            print(f"   Error texto: {response.text}")

if __name__ == "__main__":
    test_empleado_creation()
