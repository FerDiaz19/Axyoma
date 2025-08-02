#!/usr/bin/env python3
import requests
import json

# Login simple
login_data = {'username': 'ferdiaz', 'password': 'fer123'}

print('Haciendo login...')
response = requests.post('http://localhost:8000/api/auth/login/', 
                       json=login_data, timeout=10)

print(f'Status Code: {response.status_code}')
if response.status_code == 200:
    data = response.json()
    print('Login exitoso!')
    print(f'Token: {data.get("token", "N/A")}')
    print(f'Usuario: {data.get("usuario", "N/A")}')
    print(f'Nivel: {data.get("nivel_usuario", "N/A")}')
else:
    print('Error en login')
    print(response.text)
