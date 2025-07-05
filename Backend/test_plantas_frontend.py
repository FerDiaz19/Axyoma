#!/usr/bin/env python
"""
Test para verificar qué pasa con las plantas en el frontend vs backend
"""
import requests
import json

def test_con_usuario_recien_creado():
    print("=== LOGIN CON USUARIO RECIÉN CREADO ===")
    url_login = 'http://127.0.0.1:8000/api/auth/login/'
    
    datos = {
        'username': 'admin_test_nuevo',
        'password': 'password123'
    }
    
    try:
        response = requests.post(url_login, json=datos)
        if response.status_code == 200:
            data = response.json()
            token = data.get('token')
            print(f"✅ Login exitoso - Token: {token[:20]}...")
            print(f"Empresa ID: {data.get('empresa_id')}")
            print(f"Empresa: {data.get('nombre_empresa')}")
            return token, data.get('empresa_id')
        else:
            print(f"❌ Error login: {response.text}")
            
    except Exception as e:
        print(f"❌ Error: {e}")
    
    return None, None

def test_plantas_endpoint(token):
    print(f"\n=== VERIFICANDO ENDPOINT DE PLANTAS ===")
    url = 'http://127.0.0.1:8000/api/plantas/'
    headers = {'Authorization': f'Token {token}'}
    
    try:
        response = requests.get(url, headers=headers)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            plantas = response.json()
            print(f"✅ Plantas encontradas: {len(plantas)}")
            for planta in plantas:
                print(f"  - {planta.get('nombre')} (ID: {planta.get('planta_id')}, Empresa: {planta.get('empresa_id')})")
            return plantas
        else:
            print("❌ Error obteniendo plantas")
            
    except Exception as e:
        print(f"❌ Error: {e}")
    
    return []

def crear_planta_test(token):
    print(f"\n=== CREANDO PLANTA DE PRUEBA ===")
    url = 'http://127.0.0.1:8000/api/plantas/'
    headers = {'Authorization': f'Token {token}'}
    
    datos = {
        'nombre': 'Planta Test Frontend',
        'direccion': 'Dirección Test 123'
    }
    
    try:
        response = requests.post(url, json=datos, headers=headers)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 201:
            planta = response.json()
            print(f"✅ Planta creada: {planta.get('nombre')} (ID: {planta.get('planta_id')})")
            return planta
        else:
            print("❌ Error creando planta")
            
    except Exception as e:
        print(f"❌ Error: {e}")
    
    return None

if __name__ == '__main__':
    # 1. Login
    token, empresa_id = test_con_usuario_recien_creado()
    
    if not token:
        print("❌ No se pudo obtener token")
        exit(1)
    
    # 2. Ver plantas actuales
    plantas = test_plantas_endpoint(token)
    
    # 3. Crear una planta
    nueva_planta = crear_planta_test(token)
    
    # 4. Ver plantas después de crear
    if nueva_planta:
        print(f"\n=== VERIFICANDO PLANTAS DESPUÉS DE CREAR ===")
        plantas_nuevas = test_plantas_endpoint(token)
        
        if len(plantas_nuevas) > len(plantas):
            print("✅ La nueva planta aparece en el backend")
        else:
            print("❌ La nueva planta NO aparece en el backend")
