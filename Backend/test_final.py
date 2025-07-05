#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Prueba final del sistema - Julio 2025
Verifica que todo funcione correctamente
"""
import requests
import json

BASE_URL = 'http://localhost:8000/api'

def test_complete_flow():
    print("🚀 PRUEBA COMPLETA DEL SISTEMA AXYOMA")
    print("=" * 50)
    
    # 1. Login y obtener token
    print("\n1️⃣ PROBANDO LOGIN...")
    login_data = {
        'username': 'juan.perez@codewave.com',
        'password': '1234'
    }
    
    response = requests.post(f'{BASE_URL}/auth/login/', json=login_data)
    if response.status_code == 200:
        login_result = response.json()
        token = login_result.get('token')
        print(f"   ✅ Login exitoso")
        print(f"   🔑 Token: {token[:20]}...")
        print(f"   👤 Usuario: {login_result.get('usuario')}")
        print(f"   🏢 Empresa: {login_result.get('nombre_empresa')}")
    else:
        print(f"   ❌ Login falló: {response.status_code}")
        print(f"   📄 Respuesta: {response.text}")
        return
    
    headers = {'Authorization': f'Token {token}'}
    
    # 2. Probar API de plantas
    print("\n2️⃣ PROBANDO API DE PLANTAS...")
    response = requests.get(f'{BASE_URL}/plantas/', headers=headers)
    if response.status_code == 200:
        plantas = response.json()
        print(f"   ✅ GET plantas exitoso: {len(plantas)} plantas")
    else:
        print(f"   ❌ GET plantas falló: {response.status_code}")
    
    # 3. Crear nueva planta
    print("\n3️⃣ PROBANDO CREACIÓN DE PLANTA...")
    planta_data = {
        'nombre': 'Planta Prueba Final',
        'direccion': 'Av. Prueba 123, Test City'
    }
    response = requests.post(f'{BASE_URL}/plantas/', json=planta_data, headers=headers)
    if response.status_code == 201:
        nueva_planta = response.json()
        print(f"   ✅ Planta creada: ID {nueva_planta.get('planta_id')}")
        print(f"   📍 Nombre: {nueva_planta.get('nombre')}")
        print(f"   🏢 Empresa: {nueva_planta.get('empresa_nombre')}")
    else:
        print(f"   ❌ Crear planta falló: {response.status_code}")
        print(f"   📄 Respuesta: {response.text}")
    
    # 4. Probar API de empleados
    print("\n4️⃣ PROBANDO API DE EMPLEADOS...")
    
    # GET empleados
    response = requests.get(f'{BASE_URL}/empleados/', headers=headers)
    if response.status_code == 200:
        empleados = response.json()
        print(f"   ✅ GET empleados exitoso: {len(empleados)} empleados")
    else:
        print(f"   ❌ GET empleados falló: {response.status_code}")
    
    # GET plantas disponibles para empleados
    response = requests.get(f'{BASE_URL}/empleados/plantas_disponibles/', headers=headers)
    if response.status_code == 200:
        plantas_disp = response.json()
        print(f"   ✅ Plantas disponibles: {len(plantas_disp)} plantas")
    else:
        print(f"   ❌ Plantas disponibles falló: {response.status_code}")
    
    # GET departamentos disponibles
    response = requests.get(f'{BASE_URL}/empleados/departamentos_disponibles/', headers=headers)
    if response.status_code == 200:
        deps_disp = response.json()
        print(f"   ✅ Departamentos disponibles: {len(deps_disp)} departamentos")
    else:
        print(f"   ❌ Departamentos disponibles falló: {response.status_code}")
    
    # GET puestos disponibles
    response = requests.get(f'{BASE_URL}/empleados/puestos_disponibles/', headers=headers)
    if response.status_code == 200:
        puestos_disp = response.json()
        print(f"   ✅ Puestos disponibles: {len(puestos_disp)} puestos")
    else:
        print(f"   ❌ Puestos disponibles falló: {response.status_code}")
    
    print("\n🎉 PRUEBA COMPLETA FINALIZADA")
    print("🌐 Accede a http://localhost:3000 para usar el frontend")

if __name__ == '__main__':
    test_complete_flow()
