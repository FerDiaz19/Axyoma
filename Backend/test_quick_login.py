#!/usr/bin/env python
"""
Test rápido de login y registro
"""
import requests
import json

def test_login():
    print("=== PROBANDO LOGIN ===")
    url = 'http://127.0.0.1:8000/api/auth/login/'
    
    # Datos de prueba
    datos = {
        'username': 'admin_empresa_1',
        'password': 'password123'
    }
    
    try:
        response = requests.post(url, json=datos)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            data = response.json()
            return data.get('token')
        
    except Exception as e:
        print(f"Error: {e}")
    
    return None

def test_registro():
    print("\n=== PROBANDO REGISTRO ===")
    url = 'http://127.0.0.1:8000/api/empresas/registro/'
    
    datos = {
        'username': 'test_empresa_nueva',
        'password': 'password123',
        'email': 'test@empresa.com',
        'empresa_nombre': 'Empresa Test Nueva',
        'empresa_ruc': '12345678901'
    }
    
    try:
        response = requests.post(url, json=datos)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")
        
    except Exception as e:
        print(f"Error: {e}")

def test_plantas_con_token(token):
    if not token:
        print("\n⚠ No hay token para probar plantas")
        return
        
    print(f"\n=== PROBANDO PLANTAS CON TOKEN ===")
    url = 'http://127.0.0.1:8000/api/plantas/'
    headers = {'Authorization': f'Token {token}'}
    
    try:
        response = requests.get(url, headers=headers)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    # Verificar servidor
    try:
        response = requests.get('http://127.0.0.1:8000/api/')
        print(f"Servidor API: {response.status_code}")
    except:
        print("❌ Servidor no responde")
        exit(1)
    
    # Probar login
    token = test_login()
    
    # Probar registro
    test_registro()
    
    # Probar plantas si tenemos token
    test_plantas_con_token(token)
