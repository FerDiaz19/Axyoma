#!/usr/bin/env python
"""
Script para probar endpoints de empleados
"""
import requests
import json

BASE_URL = "http://127.0.0.1:8000/api"

def test_empleados_endpoints():
    print("🧪 PRUEBA DE ENDPOINTS DE EMPLEADOS")
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
    
    # Probar endpoints
    endpoints = [
        ('plantas/', 'Plantas'),
        ('departamentos/', 'Departamentos'),
        ('puestos/', 'Puestos'),
        ('empleados/', 'Empleados')
    ]
    
    for endpoint, name in endpoints:
        print(f"\n📡 Probando {name} ({endpoint})...")
        try:
            response = requests.get(f"{BASE_URL}/{endpoint}", headers=headers)
            print(f"   Status: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                print(f"   Items: {len(data)}")
                if data:
                    print(f"   Ejemplo: {json.dumps(data[0], indent=2)}")
            else:
                print(f"   Error: {response.text}")
        except Exception as e:
            print(f"   Exception: {e}")

if __name__ == "__main__":
    test_empleados_endpoints()
