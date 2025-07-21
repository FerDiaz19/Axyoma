import requests
import json

# Login como admin_empresa
login_response = requests.post('http://localhost:8000/api/auth/login/', json={'username':'admin_empresa', 'password':'admin123'})
token = login_response.json().get('token')

if not token:
    print("Error en login")
    exit()

print(f"Token: {token[:20]}...")

# Crear varias plantas
plantas = [
    {'nombre': 'Planta Norte 2', 'direccion': 'Av. Norte 200'},
    {'nombre': 'Planta Centro', 'direccion': 'Av. Centro 300'},
    {'nombre': 'Planta Industrial', 'direccion': 'Zona Industrial 400'}
]

headers = {'Authorization': f'Token {token}', 'Content-Type': 'application/json'}

for planta_data in plantas:
    response = requests.post('http://localhost:8000/api/plantas/', json=planta_data, headers=headers)
    if response.status_code == 201:
        planta = response.json()
        print(f"✅ Planta creada: {planta['nombre']} (ID: {planta['planta_id']})")
    else:
        print(f"❌ Error creando {planta_data['nombre']}: {response.status_code}")

print("\n--- Consultando usuarios de planta ---")
response = requests.get('http://localhost:8000/api/plantas/usuarios_planta/', headers=headers)
data = response.json()
print(f"Total usuarios de planta: {len(data)}")
for usuario in data:
    print(f"• {usuario['usuario']['correo']} -> {usuario['planta']['nombre']}")
