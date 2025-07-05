#!/usr/bin/env python
"""
Test comparativo entre los dos componentes
"""
import requests

def test_ambos_componentes():
    print("=== COMPARANDO GESTION PLANTAS VS ESTRUCTURA ===")
    
    # Login
    login_data = {'username': 'admin_frontend_test', 'password': 'frontend123'}
    response = requests.post('http://127.0.0.1:8000/api/auth/login/', json=login_data)
    
    if response.status_code != 200:
        print(f"❌ Error en login: {response.text}")
        return
    
    token = response.json().get('token')
    headers = {'Authorization': f'Token {token}'}
    
    print(f"✅ Login exitoso")
    
    # Probar endpoint de plantas (usado por ambos componentes)
    print("\n1. Testing /api/plantas/ (GestionPlantas Y GestionEstructura)")
    response = requests.get('http://127.0.0.1:8000/api/plantas/', headers=headers)
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        plantas = response.json()
        print(f"   Plantas: {len(plantas)}")
        for planta in plantas:
            print(f"      - {planta['nombre']} (ID: {planta['planta_id']})")
    else:
        print(f"   Error: {response.text}")
    
    # Probar endpoint de departamentos (usado por GestionEstructura)
    print("\n2. Testing /api/departamentos/ (GestionEstructura)")
    response = requests.get('http://127.0.0.1:8000/api/departamentos/', headers=headers)
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        departamentos = response.json()
        print(f"   Departamentos: {len(departamentos)}")
    else:
        print(f"   Error: {response.text}")
    
    # Probar endpoint de usuarios planta (usado por GestionEstructura)
    print("\n3. Testing /api/estructura/usuarios_planta/ (GestionEstructura)")
    response = requests.get('http://127.0.0.1:8000/api/estructura/usuarios_planta/', headers=headers)
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        usuarios = response.json()
        print(f"   Usuarios planta: {len(usuarios)}")
    else:
        print(f"   Error: {response.text}")
    
    print(f"\n🎯 CONCLUSION:")
    print(f"   Si plantas funciona aquí pero no en el frontend GestionEstructura,")
    print(f"   el problema está en el frontend, no en el backend.")

if __name__ == '__main__':
    test_ambos_componentes()
