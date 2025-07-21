import requests
import json

# Probar diferentes endpoints
endpoints = [
    "http://127.0.0.1:8000/api/",
    "http://127.0.0.1:8000/api/evaluaciones/",
    "http://127.0.0.1:8000/api/evaluaciones/evaluaciones/"
]

for url in endpoints:
    try:
        print(f"\nProbando: {url}")
        response = requests.get(url)
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            if isinstance(data, list):
                print(f"Se encontraron {len(data)} elementos")
                for i, item in enumerate(data[:3]):  # Solo mostrar los primeros 3
                    print(f"- {item}")
            else:
                print(f"Respuesta: {data}")
        else:
            print(f"Error: {response.text}")
    except Exception as e:
        print(f"Error al hacer la petición: {e}")
