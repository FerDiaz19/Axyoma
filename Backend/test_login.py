import requests
import json

# Probar el endpoint de login
url = "http://127.0.0.1:8000/api/auth/login/"

# Datos de prueba
data = {
    "username": "admin_empresa",
    "password": "admin123"
}

try:
    response = requests.post(url, json=data)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")
    
    if response.status_code == 200:
        print("¡Login exitoso!")
        user_data = response.json()
        print(f"Token: {user_data.get('token')}")
        print(f"Usuario: {user_data.get('username')}")
        print(f"Email: {user_data.get('email')}")
    else:
        print("Error en el login")
        
except Exception as e:
    print(f"Error al hacer la petición: {e}")