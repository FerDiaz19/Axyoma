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

print("🧪 DEBUGEAR ERROR 400 EN CREACIÓN DE EMPLEADO")
print("=" * 50)

try:
    # 1. Login
    login_response = requests.post(f'{BASE_URL}/auth/login/', json=login_data)
    if login_response.status_code != 200:
        print(f'❌ Error de login: {login_response.text}')
        exit()
    
    token = login_response.json()['token']
    headers = {'Authorization': f'Token {token}'}
    print('✅ Login exitoso')
    
    # 2. Probar diferentes combinaciones de datos para ver qué falla
    
    # Test 1: Datos mínimos
    print('\n🧪 Test 1: Datos mínimos')
    import time
    timestamp = int(time.time())
    empleado_minimo = {
        'nombre': 'Test',
        'apellido_paterno': 'Usuario',
        'email': f'test.minimo.{timestamp}@empresa.com',  # Email único
        'puesto': 119
    }
    response = requests.post(f'{BASE_URL}/empleados/', json=empleado_minimo, headers=headers)
    print(f'Status: {response.status_code}')
    print(f'Response: {response.text[:1000]}...' if len(response.text) > 1000 else response.text)
    
    # Test 2: Con campos opcionales pero vacíos
    print('\n🧪 Test 2: Con campos opcionales vacíos')
    empleado_vacio = {
        'nombre': 'Test2',
        'apellido_paterno': 'Usuario2',
        'apellido_materno': '',
        'email': f'test.vacio.{timestamp}@empresa.com',
        'telefono': '',
        'fecha_ingreso': '',
        'genero': 'Masculino',
        'antiguedad': 0,
        'puesto': 119,
        'departamento': 0,
        'planta': 0
    }
    response = requests.post(f'{BASE_URL}/empleados/', json=empleado_vacio, headers=headers)
    print(f'Status: {response.status_code}')
    print(f'Response: {response.text}')
    
    # Test 3: Con todos los campos llenos
    print('\n🧪 Test 3: Con todos los campos llenos')
    empleado_completo = {
        'nombre': 'Test3',
        'apellido_paterno': 'Usuario3',
        'apellido_materno': 'Apellido',
        'email': f'test.completo.{timestamp}@test.com',
        'telefono': '1234567890',
        'fecha_ingreso': '2025-07-30',
        'genero': 'Femenino',
        'antiguedad': 5,
        'puesto': 119,
        'departamento': 123,
        'planta': 20
    }
    response = requests.post(f'{BASE_URL}/empleados/', json=empleado_completo, headers=headers)
    print(f'Status: {response.status_code}')
    print(f'Response: {response.text}')
    
    # Test 4: Verificar que el puesto existe
    print('\n🧪 Test 4: Verificar puesto ID 119')
    puestos_response = requests.get(f'{BASE_URL}/empleados/puestos_disponibles/', headers=headers)
    if puestos_response.status_code == 200:
        puestos = puestos_response.json()
        puesto_119 = next((p for p in puestos if p['puesto_id'] == 119), None)
        if puesto_119:
            print(f'✅ Puesto 119 encontrado: {puesto_119}')
        else:
            print(f'❌ Puesto 119 NO encontrado')
            print(f'Primeros 3 puestos disponibles: {puestos[:3]}')
    else:
        print(f'❌ Error obteniendo puestos: {puestos_response.text}')
        
except Exception as e:
    print(f'❌ Error: {e}')
    import traceback
    traceback.print_exc()

print("✅ Debug completado")
