#!/usr/bin/env python
"""
Test rápido para crear planta
"""
import requests

def test_crear_planta():
    print("=== TEST CREAR PLANTA ===")
    
    # Login primero
    login_data = {'username': 'admin_frontend_test', 'password': 'frontend123'}
    response = requests.post('http://127.0.0.1:8000/api/auth/login/', json=login_data)
    
    if response.status_code != 200:
        print(f"❌ Error en login: {response.text}")
        return
    
    token = response.json().get('token')
    print(f"✅ Login exitoso - Token: {token[:20]}...")
    
    # Crear planta
    headers = {'Authorization': f'Token {token}'}
    planta_data = {
        'nombre': 'Planta Test API',
        'direccion': 'Dirección Test API'
    }
    
    response = requests.post('http://127.0.0.1:8000/api/plantas/', json=planta_data, headers=headers)
    print(f"Status crear planta: {response.status_code}")
    print(f"Response: {response.text}")
    
    if response.status_code == 201:
        print("✅ Planta creada exitosamente!")
        
        # Verificar que aparece en la lista
        response = requests.get('http://127.0.0.1:8000/api/plantas/', headers=headers)
        if response.status_code == 200:
            plantas = response.json()
            print(f"✅ Plantas actuales: {len(plantas)}")
            for planta in plantas:
                print(f"   - {planta['nombre']} (ID: {planta['planta_id']})")
        else:
            print(f"❌ Error obteniendo plantas: {response.text}")
    else:
        print("❌ Error creando planta")

if __name__ == '__main__':
    test_crear_planta()
