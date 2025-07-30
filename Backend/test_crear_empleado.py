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

print("🧪 PROBANDO CREAR EMPLEADO")
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
    
    # 2. Probar autenticación primero
    test_auth_response = requests.get(f'{BASE_URL}/superadmin/listar_empresas/', headers=headers)
    print(f'Test auth status: {test_auth_response.status_code}')
    if test_auth_response.status_code != 200:
        print(f'❌ Error de autenticación: {test_auth_response.text}')
        print(f'Headers enviados: {headers}')
        exit()
    print('✅ Autenticación funcionando')
    
    # 3. Obtener puestos disponibles
    puestos_response = requests.get(f'{BASE_URL}/empleados/puestos_disponibles/', headers=headers)
    if puestos_response.status_code != 200:
        print(f'❌ Error obteniendo puestos: {puestos_response.text}')
        exit()
    
    puestos = puestos_response.json()
    print(f'✅ Puestos disponibles: {len(puestos)}')
    
    if not puestos:
        print('❌ No hay puestos disponibles para crear empleados')
        exit()
    
    primer_puesto = puestos[0]
    print(f'📍 Usando puesto: {primer_puesto["nombre"]} (ID: {primer_puesto["puesto_id"]})')
    
    # 4. Crear empleado de prueba
    empleado_data = {
        'nombre': 'Juan Carlos',
        'apellido_paterno': 'González',
        'apellido_materno': 'Pérez',
        'email': 'juan.gonzalez@test.com',
        'telefono': '5551234567',
        'fecha_ingreso': '2025-07-30',
        'puesto': primer_puesto['puesto_id']
    }
    
    print(f'📝 Creando empleado: {empleado_data}')
    
    crear_response = requests.post(f'{BASE_URL}/empleados/', json=empleado_data, headers=headers)
    print(f'Status Code: {crear_response.status_code}')
    print(f'Response: {crear_response.text}')
    
    if crear_response.status_code == 201:
        print('✅ Empleado creado exitosamente')
        empleado_creado = crear_response.json()
        print(f'ID del empleado: {empleado_creado.get("empleado_id", "N/A")}')
    else:
        print('❌ Error creando empleado')
        
except Exception as e:
    print(f'❌ Error: {e}')
    import traceback
    traceback.print_exc()

print("✅ Prueba completada")
