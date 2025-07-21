#!/usr/bin/env python3
import requests
import json

# Configuración de la prueba
BASE_URL = "http://127.0.0.1:8000/api"
TOKEN = "521d57bdd9c57a7d813f145797c89457c1be2e06"

def test_logout():
    url = f"{BASE_URL}/auth/logout/"
    headers = {"Authorization": f"Token {TOKEN}"}
    
    try:
        response = requests.post(url, headers=headers)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            print("¡Éxito! Logout realizado correctamente")
            print("El token ha sido eliminado del servidor")
        else:
            print(f"Error: {response.text}")
            
    except requests.exceptions.RequestException as e:
        print(f"Error de conexión: {e}")

if __name__ == "__main__":
    test_logout()
