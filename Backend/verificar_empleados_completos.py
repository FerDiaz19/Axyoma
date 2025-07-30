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

print("🔍 VERIFICANDO EMPLEADOS CON DATOS COMPLETOS")
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
    
    # 2. Obtener empleados
    empleados_response = requests.get(f'{BASE_URL}/empleados/', headers=headers)
    
    if empleados_response.status_code == 200:
        empleados = empleados_response.json()
        print(f'✅ Total empleados: {len(empleados)}')
        
        print(f'\n📋 LISTADO DE EMPLEADOS:')
        print(f'{"ID":<4} {"Nombre":<20} {"Empresa":<20} {"Planta":<20} {"Departamento":<20} {"Puesto":<20}')
        print("-" * 110)
        
        for emp in empleados:
            print(f'{emp.get("empleado_id", "N/A"):<4} '
                  f'{emp.get("nombre", "N/A"):<20} '
                  f'{emp.get("empresa_nombre", "N/A"):<20} '
                  f'{emp.get("planta_nombre", "N/A"):<20} '
                  f'{emp.get("departamento_nombre", "N/A"):<20} '
                  f'{emp.get("puesto_nombre", "N/A"):<20}')
        
        # Buscar empleado recién creado (que debe tener datos completos)
        empleado_reciente = None
        for emp in empleados:
            if emp.get("nombre") == "aaaaa":
                empleado_reciente = emp
                break
                
        if empleado_reciente:
            print(f'\n🎯 EMPLEADO RECIÉN CREADO (aaaaa):')
            print(f'  - Nombre completo: {empleado_reciente.get("nombre")} {empleado_reciente.get("apellido_paterno")} {empleado_reciente.get("apellido_materno", "")}')
            print(f'  - Email: {empleado_reciente.get("email", "N/A")}')
            print(f'  - Empresa: {empleado_reciente.get("empresa_nombre", "N/A")} (ID: {empleado_reciente.get("empresa_id", "N/A")})')
            print(f'  - Planta: {empleado_reciente.get("planta_nombre", "N/A")} (ID: {empleado_reciente.get("planta_id", "N/A")})')
            print(f'  - Departamento: {empleado_reciente.get("departamento_nombre", "N/A")} (ID: {empleado_reciente.get("departamento_id", "N/A")})')
            print(f'  - Puesto: {empleado_reciente.get("puesto_nombre", "N/A")} (ID: {empleado_reciente.get("puesto_id", "N/A")})')
            
            if empleado_reciente.get("planta_nombre") != "N/A":
                print(f'\n✅ El empleado tiene datos de planta, departamento y puesto correctos!')
            else:
                print(f'\n❌ El empleado NO tiene datos de planta, departamento y puesto')
        else:
            print(f'\n⚠️ No se encontró el empleado recién creado')
            
    else:
        print(f'❌ Error obteniendo empleados: {empleados_response.text}')
        
except Exception as e:
    print(f'❌ Error: {e}')
    import traceback
    traceback.print_exc()

print("✅ Verificación completada")
