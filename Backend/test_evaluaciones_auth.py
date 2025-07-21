import requests
import json

# Token obtenido del login
token = "521d57bdd9c57a7d813f145797c89457c1be2e06"

# Probar el endpoint de evaluaciones disponibles con autenticación
url = "http://127.0.0.1:8000/api/users/evaluaciones_disponibles/"

headers = {
    "Authorization": f"Token {token}",
    "Content-Type": "application/json"
}

try:
    response = requests.get(url, headers=headers)
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"¡Éxito! Se encontraron {len(data)} evaluaciones disponibles")
        for i, eval in enumerate(data):
            print(f"{i+1}. {eval.get('titulo', 'Sin título')} - ID: {eval.get('id', 'N/A')}")
    else:
        print(f"Error: {response.text}")
        
except Exception as e:
    print(f"Error al hacer la petición: {e}")
