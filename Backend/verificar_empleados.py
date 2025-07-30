#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import json

BASE_URL = 'http://127.0.0.1:8000/api'

# Login para obtener token
login_data = {
    'username': 'superadmin',
    'password': '1234'
}

print("🔍 VERIFICANDO DATOS DE EMPLEADOS")
print("=" * 40)

try:
    # 1. Login
    login_response = requests.post(f'{BASE_URL}/auth/login/', json=login_data)
    if login_response.status_code != 200:
        print(f'❌ Error de login: {login_response.text}')
        exit()
    
    token = login_response.json()['token']
    headers = {'Authorization': f'Token {token}'}
    print('✅ Login exitoso')
    
    # 2. Obtener empleados para ver qué campos se devuelven
    empleados_response = requests.get(f'{BASE_URL}/empleados/', headers=headers)
    print(f'Status Code: {empleados_response.status_code}')
    
    if empleados_response.status_code == 200:
        empleados = empleados_response.json()
        print(f'✅ Total empleados: {len(empleados)}')
        
        if empleados:
            ultimo_empleado = empleados[-1]  # El último empleado (recién creado)
            print(f'\n📄 Datos del último empleado:')
            for key, value in ultimo_empleado.items():
                print(f'  {key}: {value}')
        else:
            print('❌ No hay empleados')
    else:
        print(f'❌ Error: {empleados_response.text}')
        
except Exception as e:
    print(f'❌ Error: {e}')
    import traceback
    traceback.print_exc()

print("✅ Verificación completada")
