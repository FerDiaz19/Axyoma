#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script de prueba para verificar autenticación y creación de plantas
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
            result = response.json()
            print("✅ LOGIN EXITOSO")
            print(f"   Usuario: {result.get('user', {}).get('username', 'N/A')}")
            print(f"   Token: {result.get('token', 'N/A')}")
            print(f"   Nivel: {result.get('perfil', {}).get('nivel_usuario', 'N/A')}")
            return result.get('token')
        else:
            print(f"❌ LOGIN FALLÓ: {response.status_code}")
            print(f"   Respuesta: {response.text}")
            return None
    except Exception as e:
        print(f"❌ ERROR EN LOGIN: {e}")
        return None

def test_plantas_with_token(token):
    """Probar GET plantas con token"""
    url = f'{BASE_URL}/plantas/'
    headers = {'Authorization': f'Token {token}'}
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            plantas = response.json()
            print(f"✅ GET PLANTAS EXITOSO: {len(plantas)} plantas")
            return plantas
        else:
            print(f"❌ GET PLANTAS FALLÓ: {response.status_code}")
            print(f"   Respuesta: {response.text}")
            return []
    except Exception as e:
        print(f"❌ ERROR EN GET PLANTAS: {e}")
        return []

def test_create_planta(token):
    """Probar crear nueva planta"""
    url = f'{BASE_URL}/plantas/'
    headers = {'Authorization': f'Token {token}'}
    data = {
        'nombre': 'Planta Test Token',
        'direccion': 'Dirección de prueba con token'
    }
    
    try:
        response = requests.post(url, json=data, headers=headers)
        if response.status_code == 201:
            planta = response.json()
            print(f"✅ CREAR PLANTA EXITOSO: ID {planta.get('planta_id')}")
            print(f"   Nombre: {planta.get('nombre')}")
            print(f"   Empresa: {planta.get('empresa_nombre')}")
            return planta
        else:
            print(f"❌ CREAR PLANTA FALLÓ: {response.status_code}")
            print(f"   Respuesta: {response.text}")
            return None
    except Exception as e:
        print(f"❌ ERROR EN CREAR PLANTA: {e}")
        return None

if __name__ == '__main__':
    print("🧪 PROBANDO AUTENTICACIÓN Y API")
    print("=" * 50)
    
    # 1. Login
    token = test_login()
    
    if token:
        print("\n📋 PROBANDO API CON TOKEN")
        print("-" * 30)
        
        # 2. GET plantas
        plantas = test_plantas_with_token(token)
        
        # 3. CREATE planta
        nueva_planta = test_create_planta(token)
        
        print("\n📊 RESUMEN FINAL:")
        print(f"   Token obtenido: {'✅ SÍ' if token else '❌ NO'}")
        print(f"   Plantas leídas: {'✅ SÍ' if plantas else '❌ NO'}")
        print(f"   Planta creada: {'✅ SÍ' if nueva_planta else '❌ NO'}")
    else:
        print("\n❌ NO SE PUDO OBTENER TOKEN - ABORTANDO PRUEBAS")
