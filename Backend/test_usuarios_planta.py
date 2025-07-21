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
print('Usuarios de planta:', len(data))
for usuario in data:
    print(f"Usuario: {usuario['usuario']['correo']}")
    print(f"Planta: {usuario['planta']['nombre']}")
    print(f"Password temporal: {usuario.get('tiene_password_temporal', 'N/A')}")
    print('---')
