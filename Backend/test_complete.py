#!/usr/bin/env python3
import requests
import json

# Configuración de la prueba
BASE_URL = "http://127.0.0.1:8000/api"

def test_complete_flow():
    print("=== PRUEBA COMPLETA DEL SISTEMA ===\n")
    
    # 1. Probar login
    print("1. Probando login...")
    login_url = f"{BASE_URL}/auth/login/"
    login_data = {"username": "admin_empresa", "password": "admin123"}
    
    response = requests.post(login_url, json=login_data)
    if response.status_code == 200:
        data = response.json()
        token = data['token']
        print(f"✅ Login exitoso. Usuario: {data['username']}")
        print(f"   Empresa: {data.get('empresa', {}).get('nombre', 'No asignada')}")
    else:
        print(f"❌ Login falló: {response.text}")
        return
    
    headers = {"Authorization": f"Token {token}"}
    
    # 2. Probar endpoints principales
    endpoints = [
        ("/users/me/", "Usuario actual"),
        ("/users/evaluaciones_disponibles/", "Evaluaciones disponibles"),
        ("/empresas/", "Lista de empresas"),
        ("/empleados/", "Lista de empleados"),
    ]
    
    for endpoint, description in endpoints:
        print(f"\n2. Probando {description}...")
        response = requests.get(f"{BASE_URL}{endpoint}", headers=headers)
        if response.status_code == 200:
            data = response.json()
            if isinstance(data, list):
                print(f"✅ {description}: {len(data)} elementos encontrados")
            else:
                print(f"✅ {description}: Datos obtenidos correctamente")
        else:
            print(f"❌ {description}: Error {response.status_code}")
    
    # 3. Probar logout
    print(f"\n3. Probando logout...")
    logout_url = f"{BASE_URL}/auth/logout/"
    response = requests.post(logout_url, headers=headers)
    if response.status_code == 200:
        print("✅ Logout exitoso")
        
        # Verificar que el token ya no funciona
        print("4. Verificando invalidación de token...")
        response = requests.get(f"{BASE_URL}/users/me/", headers=headers)
        if response.status_code == 401:
            print("✅ Token invalidado correctamente")
        else:
            print("❌ Token aún válido después del logout")
    else:
        print(f"❌ Logout falló: {response.text}")
    
    print("\n=== PRUEBA COMPLETA FINALIZADA ===")

if __name__ == "__main__":
    try:
        test_complete_flow()
    except requests.exceptions.RequestException as e:
        print(f"❌ Error de conexión: {e}")
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
