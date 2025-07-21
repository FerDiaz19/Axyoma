import requests

# Login para obtener token
login_data = {'username': 'superadmin', 'password': 'admin123'}
response = requests.post('http://localhost:8000/api/auth/login/', json=login_data)
token = response.json()['token']
headers = {'Authorization': f'Token {token}'}
print(f'Token obtenido: {token[:20]}...')

# Test empresas (debería funcionar)
response = requests.get('http://localhost:8000/api/empresas/', headers=headers)
print(f'Empresas: {response.status_code}')
if response.status_code == 200:
    data = response.json()
    print(f'Datos empresas: {len(data) if data else 0} elementos')

# Test empleados
response = requests.get('http://localhost:8000/api/empleados/', headers=headers)
print(f'Empleados: {response.status_code}')
if response.status_code == 200:
    data = response.json()
    print(f'Datos empleados: {len(data) if data else 0} elementos')

# Test superadmin empresas
response = requests.get('http://localhost:8000/api/superadmin/empresas/', headers=headers)
print(f'SuperAdmin Empresas: {response.status_code}')

# Test suscripciones
response = requests.get('http://localhost:8000/api/suscripciones/', headers=headers)
print(f'Suscripciones: {response.status_code}')

# Test subscriptions
response = requests.get('http://localhost:8000/api/subscriptions/', headers=headers)
print(f'Subscriptions: {response.status_code}')

# Test surveys
response = requests.get('http://localhost:8000/api/surveys/evaluaciones/', headers=headers)
print(f'Surveys Evaluaciones: {response.status_code}')
