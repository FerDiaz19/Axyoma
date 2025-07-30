#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import json

BASE_URL = 'http://127.0.0.1:8000/api'

# Login como admin-empresa para simular el contexto del usuario
login_data = {
    'username': 'axis',  # Usuario admin-empresa
    'password': '1234'
}

print("🧪 SIMULANDO CREAR EMPLEADO DESDE PANEL EMPRESA")
print("=" * 50)

try:
    # 1. Login como admin-empresa
    login_response = requests.post(f'{BASE_URL}/auth/login/', json=login_data)
    print(f'Login Status: {login_response.status_code}')
    
    if login_response.status_code != 200:
        print(f'❌ Error de login: {login_response.text}')
        # Probar con superadmin
        print('Probando con superadmin...')
        login_data = {'username': 'superadmin', 'password': '1234'}
        login_response = requests.post(f'{BASE_URL}/auth/login/', json=login_data)
    
    if login_response.status_code != 200:
        print(f'❌ Error de login: {login_response.text}')
        exit()
    
    token = login_response.json()['token']
    headers = {'Authorization': f'Token {token}'}
    print('✅ Login exitoso')
    
    # 2. Intentar crear empleado directamente (simula el POST desde frontend)
    empleado_data = {
        'nombre': 'Test Frontend',
        'apellido_paterno': 'Usuario',
        'apellido_materno': 'Panel',
        'genero': 'Masculino',
        'antiguedad': 0,
        'puesto': 119,  # ID de puesto existente
        'departamento': 36,  # ID de departamento
        'planta': 20  # ID de planta
    }
    
    print(f'📝 Enviando POST a /empleados/ con datos: {empleado_data}')
    
    crear_response = requests.post(f'{BASE_URL}/empleados/', json=empleado_data, headers=headers)
    print(f'Status Code: {crear_response.status_code}')
    print(f'Response Headers: {dict(crear_response.headers)}')
    print(f'Response: {crear_response.text}')
    
    if crear_response.status_code == 201:
        print('✅ Empleado creado exitosamente')
    elif crear_response.status_code == 500:
        print('❌ Error interno del servidor (500)')
        print('Esto coincide con el error reportado por el usuario')
    else:
        print(f'❌ Error: {crear_response.status_code}')
        
except Exception as e:
    print(f'❌ Error de conexión: {e}')
    import traceback
    traceback.print_exc()

print("✅ Prueba completada")
