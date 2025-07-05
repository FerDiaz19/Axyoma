#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script de prueba para verificar que la API funciona correctamente
"""
import os
import django
import requests
import json

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')
django.setup()

BASE_URL = 'http://localhost:8000/api'

def test_login():
    """Probar login de admin empresa"""
    url = f'{BASE_URL}/auth/login/'
    data = {
        'username': 'juan.perez@codewave.com',
        'password': '1234'
    }
    
    try:
        response = requests.post(url, json=data)
        if response.status_code == 200:
            token_data = response.json()
            print("✅ LOGIN EXITOSO")
            print(f"Token: {token_data.get('token', 'No token')}")
            return token_data.get('token')
        else:
            print(f"❌ LOGIN FALLÓ: {response.status_code}")
            print(f"Respuesta: {response.text}")
            return None
    except Exception as e:
        print(f"❌ ERROR EN LOGIN: {e}")
        return None

def test_plantas_get(token):
    """Probar obtener plantas"""
    url = f'{BASE_URL}/plantas/'
    headers = {'Authorization': f'Token {token}'} if token else {}
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            plantas = response.json()
            print(f"✅ GET PLANTAS EXITOSO: {len(plantas)} plantas encontradas")
            return plantas
        else:
            print(f"❌ GET PLANTAS FALLÓ: {response.status_code}")
            print(f"Respuesta: {response.text}")
            return []
    except Exception as e:
        print(f"❌ ERROR EN GET PLANTAS: {e}")
        return []

def test_plantas_post(token):
    """Probar crear nueva planta"""
    url = f'{BASE_URL}/plantas/'
    headers = {'Authorization': f'Token {token}'} if token else {}
    data = {
        'nombre': 'Planta Test API',
        'direccion': 'Dirección de prueba desde API'
    }
    
    try:
        response = requests.post(url, json=data, headers=headers)
        if response.status_code == 201:
            planta = response.json()
            print(f"✅ POST PLANTA EXITOSO: Creada planta ID {planta.get('planta_id')}")
            return planta
        else:
            print(f"❌ POST PLANTA FALLÓ: {response.status_code}")
            print(f"Respuesta: {response.text}")
            return None
    except Exception as e:
        print(f"❌ ERROR EN POST PLANTA: {e}")
        return None

if __name__ == '__main__':
    print("🧪 PROBANDO API DE PLANTAS")
    print("=" * 50)
    
    # 1. Login
    token = test_login()
    
    # 2. GET plantas
    plantas_antes = test_plantas_get(token)
    
    # 3. POST nueva planta
    nueva_planta = test_plantas_post(token)
    
    # 4. GET plantas después
    plantas_despues = test_plantas_get(token)
    
    print("\n📊 RESUMEN:")
    print(f"Plantas antes: {len(plantas_antes)}")
    print(f"Plantas después: {len(plantas_despues)}")
    print(f"Nueva planta creada: {'✅ SÍ' if nueva_planta else '❌ NO'}")
