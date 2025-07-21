#!/usr/bin/env python3
import requests
import json

# Configuración de la prueba
BASE_URL = "http://127.0.0.1:8000/api"

def test_endpoint(token, endpoint, description):
    url = f"{BASE_URL}{endpoint}"
    headers = {"Authorization": f"Token {token}"}
    
    try:
        response = requests.get(url, headers=headers)
        print(f"\n=== {description} ===")
        print(f"URL: {endpoint}")
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ Funcionando correctamente")
            return response.json()
        else:
            print(f"❌ Error: {response.text}")
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Error de conexión: {e}")
        return None

def main():
    # Primero hacer login
    login_url = f"{BASE_URL}/auth/login/"
    login_data = {"username": "admin_empresa", "password": "admin123"}
    
    response = requests.post(login_url, json=login_data)
    if response.status_code != 200:
        print("❌ No se pudo hacer login")
        return
    
    token = response.json()['token']
    print(f"✅ Login exitoso. Token: {token}")
    
    # Probar endpoints clave
    test_endpoint(token, "/users/me/", "Usuario actual")
    test_endpoint(token, "/users/evaluaciones_disponibles/", "Evaluaciones disponibles")
    test_endpoint(token, "/empresas/", "Lista de empresas")
    test_endpoint(token, "/empleados/", "Lista de empleados")

if __name__ == "__main__":
    main()
