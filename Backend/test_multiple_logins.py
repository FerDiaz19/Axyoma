#!/usr/bin/env python3
import requests
import json

# Configuración de la prueba
BASE_URL = "http://127.0.0.1:8000/api"

def test_login(username, password):
    url = f"{BASE_URL}/auth/login/"
    data = {
        "username": username,
        "password": password
    }
    
    try:
        response = requests.post(url, json=data)
        print(f"\n=== LOGIN: {username} ===")
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("¡Login exitoso!")
            print(f"Token: {data.get('token')}")
            print(f"Usuario: {data.get('username')}")
            print(f"Email: {data.get('email')}")
            empresa = data.get('empresa')
            if empresa:
                print(f"Empresa: {empresa.get('nombre', 'No nombre')}")
            else:
                print("Empresa: No asignada")
        else:
            print(f"Error: {response.text}")
            
    except requests.exceptions.RequestException as e:
        print(f"Error de conexión: {e}")

if __name__ == "__main__":
    # Probar diferentes usuarios
    test_login("superadmin", "admin123")
    test_login("admin_empresa", "admin123")
    test_login("ernesto", "admin123")
