import requests
import json

# Login como admin_empresa
login_response = requests.post('http://localhost:8000/api/auth/login/', json={'username':'admin_empresa', 'password':'admin123'})
token = login_response.json().get('token')

# Consultar usuarios de planta
headers = {'Authorization': f'Token {token}'}
response = requests.get('http://localhost:8000/api/plantas/usuarios_planta/', headers=headers)

print('Status:', response.status_code)
data = response.json()
print(f'Total usuarios: {len(data)}')
print()

# Mostrar todos los usuarios con credenciales
for i, usuario in enumerate(data, 1):
    print(f"{i}. Planta: {usuario['planta']['nombre']}")
    if usuario.get('credenciales'):
        print(f"   👤 Usuario: {usuario['credenciales']['usuario']}")
        print(f"   🔑 Password: {usuario['credenciales']['password']}")
    print('---')
