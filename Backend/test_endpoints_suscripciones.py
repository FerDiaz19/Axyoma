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

print("🔍 PROBANDO ENDPOINTS DE SUSCRIPCIONES Y PAGOS")
print("=" * 50)

try:
    login_response = requests.post(f'{BASE_URL}/auth/login/', json=login_data)
    print(f'Login Status: {login_response.status_code}')
    print(f'Login Response: {login_response.text}')
    
    if login_response.status_code == 200:
        response_data = login_response.json()
        # Verificar qué campos tiene la respuesta
        print(f'Response keys: {list(response_data.keys())}')
        
        if 'access' in response_data:
            token = response_data['access']
        elif 'token' in response_data:
            token = response_data['token']
        else:
            print(f'❌ No se encontró token en la respuesta')
            exit()
            
        headers = {'Authorization': f'Bearer {token}'}
        
        print('✅ Token obtenido exitosamente')
        print()
        
        # 1. Probar endpoint de planes
        print("1. Probando /suscripciones/listar_planes/")
        planes_response = requests.get(f'{BASE_URL}/suscripciones/listar_planes/', headers=headers)
        print(f'   Status: {planes_response.status_code}')
        if planes_response.status_code == 200:
            planes = planes_response.json()
            print(f'   ✅ Total planes: {len(planes)}')
            if planes:
                print(f'   Ejemplo: {planes[0]}')
        else:
            print(f'   ❌ Error: {planes_response.text}')
        print()
        
        # 2. Probar endpoint de suscripciones
        print("2. Probando /suscripciones/listar_suscripciones/")
        suscripciones_response = requests.get(f'{BASE_URL}/suscripciones/listar_suscripciones/', headers=headers)
        print(f'   Status: {suscripciones_response.status_code}')
        if suscripciones_response.status_code == 200:
            suscripciones = suscripciones_response.json()
            print(f'   ✅ Total suscripciones: {len(suscripciones)}')
            if suscripciones:
                print(f'   Ejemplo: {suscripciones[0]}')
        else:
            print(f'   ❌ Error: {suscripciones_response.text}')
        print()
        
        # 3. Probar endpoint de pagos
        print("3. Probando /suscripciones/listar_pagos/")
        pagos_response = requests.get(f'{BASE_URL}/suscripciones/listar_pagos/', headers=headers)
        print(f'   Status: {pagos_response.status_code}')
        if pagos_response.status_code == 200:
            pagos = pagos_response.json()
            print(f'   ✅ Total pagos: {len(pagos)}')
            if pagos:
                print(f'   Ejemplo: {pagos[0]}')
        else:
            print(f'   ❌ Error: {pagos_response.text}')
        print()
            
    else:
        print(f'❌ Error de login: {login_response.text}')
        
except Exception as e:
    print(f'❌ Error de conexión: {e}')
    import traceback
    traceback.print_exc()

print("✅ Prueba completada")
