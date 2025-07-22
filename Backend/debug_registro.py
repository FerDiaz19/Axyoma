#!/usr/bin/env python3

import requests
import json
import time

# Login como admin
response = requests.post("http://127.0.0.1:8000/api/auth/login/", 
    json={
        'username': 'admin',
        'password': 'admin123'
    },
    headers={'Content-Type': 'application/json'}
)

admin_token = response.json()['token']

# Registrar empresa
timestamp = str(int(time.time()))
empresa_data = {
    'nombre': f'Empresa Debug {timestamp}',
    'rfc': f'EMP{timestamp[:10]}',
    'usuario': f'admin{timestamp}',
    'password': 'TempPass123',
    'nombre_completo': 'Admin Empresa Debug',
    'direccion': f'Av. Debug {timestamp}',
    'email_contacto': f'admin{timestamp}@empresatest.com',
    'telefono_contacto': '5551234567'
}

response = requests.post("http://127.0.0.1:8000/api/empresas/registro/", 
    json=empresa_data,
    headers={'Content-Type': 'application/json'}
)

print(f"Status: {response.status_code}")
print(f"Response completa: {json.dumps(response.json(), indent=2)}")
