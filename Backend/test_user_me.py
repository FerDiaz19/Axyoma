#!/usr/bin/env python3
import requests
import json

# Configuración de la prueba
BASE_URL = "http://127.0.0.1:8000/api"
TOKEN = "521d57bdd9c57a7d813f145797c89457c1be2e06"

def test_user_me():
    url = f"{BASE_URL}/users/me/"
    headers = {"Authorization": f"Token {TOKEN}"}
    
    try:
        response = requests.get(url, headers=headers)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("¡Éxito! Información del usuario:")
            print(f"- ID: {data.get('id')}")
            print(f"- Username: {data.get('username')}")
            print(f"- Empresa: {data.get('empresa', {}).get('nombre')}")
            print(f"- Is Staff: {data.get('is_staff')}")
            print(f"- Is Active: {data.get('is_active')}")
        else:
            print(f"Error: {response.text}")
            
    except requests.exceptions.RequestException as e:
        print(f"Error de conexión: {e}")

if __name__ == "__main__":
    test_user_me()
