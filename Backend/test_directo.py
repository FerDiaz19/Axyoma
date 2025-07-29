#!/usr/bin/env python3
import requests

# Obtener token
print("🔑 Obteniendo token...")
login_response = requests.post('http://127.0.0.1:8000/api/auth/login/', json={
    'username': 'admin', 
    'password': 'admin123'
})

if login_response.status_code != 200:
    print(f"❌ Error al obtener token: {login_response.status_code}")
    print(login_response.text)
    exit(1)

token = login_response.json()['token']
print(f"✅ Token obtenido: {token}")

# Probar endpoint directo
headers = {'Authorization': f'Token {token}'}

# Probar empleados
print("\n📤 Probando exportación empleados...")
export_response = requests.get('http://127.0.0.1:8000/api/admin-bd/directo/exportar/empleados/', headers=headers)

print(f"Status: {export_response.status_code}")
if export_response.status_code == 200:
    print(f"✅ Éxito! Tamaño CSV: {len(export_response.content)} bytes")
    # Mostrar primeras líneas
    lines = export_response.text.split('\n')[:3]
    print("📄 Primeras líneas:")
    for i, line in enumerate(lines):
        if line.strip():
            print(f"   {i+1}: {line}")
else:
    print(f"❌ Error: {export_response.text}")

# Probar suscripciones
print("\n📤 Probando exportación suscripciones...")
export_response = requests.get('http://127.0.0.1:8000/api/admin-bd/directo/exportar/suscripciones/', headers=headers)

print(f"Status: {export_response.status_code}")
if export_response.status_code == 200:
    print(f"✅ Éxito! Tamaño CSV: {len(export_response.content)} bytes")
    # Mostrar primeras líneas
    lines = export_response.text.split('\n')[:3]
    print("📄 Primeras líneas:")
    for i, line in enumerate(lines):
        if line.strip():
            print(f"   {i+1}: {line}")
else:
    print(f"❌ Error: {export_response.text}")
