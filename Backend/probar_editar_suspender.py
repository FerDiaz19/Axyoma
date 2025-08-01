#!/usr/bin/env python
"""
Script para probar las funciones de editar y suspender empresas
"""
import os
import django
import sys

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

import requests
import json
from apps.users.models import Empresa

def test_functions():
    print("🔧 Probando funciones de editar y suspender empresas\n")
    
    # URL base del servidor
    BASE_URL = "http://localhost:8000/api/superadmin"
    
    # Obtener token de SuperAdmin
    login_data = {
        'username': 'superadmin',
        'password': '1234'
    }
    
    try:
        login_response = requests.post('http://localhost:8000/api/login/', json=login_data)
        if login_response.status_code == 200:
            token = login_response.json().get('access_token')
            headers = {'Authorization': f'Bearer {token}'}
            print("✅ Login exitoso, token obtenido")
        else:
            print("❌ Error en login:", login_response.text)
            return
    except Exception as e:
        print("❌ Error conectando al servidor:", e)
        return
    
    # Obtener primera empresa para probar
    empresas = Empresa.objects.all()[:2]
    if not empresas:
        print("❌ No hay empresas para probar")
        return
    
    empresa_test = empresas[0]
    print(f"\n📋 Empresa de prueba: {empresa_test.nombre} (ID: {empresa_test.empresa_id})")
    print(f"   Status actual: {empresa_test.status}")
    print(f"   Email: {empresa_test.email_contacto}")
    print(f"   Teléfono: {empresa_test.telefono_contacto}")
    print(f"   Dirección: {empresa_test.direccion}")
    
    # TEST 1: Editar empresa
    print("\n🔧 TEST 1: Editando empresa...")
    edit_data = {
        'empresa_id': empresa_test.empresa_id,
        'nombre': empresa_test.nombre + " (EDITADA)",
        'telefono': '5555555555',
        'correo': 'editado@test.com',
        'direccion': 'Dirección editada 123'
    }
    
    try:
        edit_response = requests.put(f'{BASE_URL}/editar_empresa/', 
                                   json=edit_data, headers=headers)
        print(f"   Response status: {edit_response.status_code}")
        print(f"   Response: {edit_response.text}")
        
        if edit_response.status_code == 200:
            # Verificar cambios en DB
            empresa_test.refresh_from_db()
            print(f"   ✅ Empresa editada exitosamente")
            print(f"   Nuevo nombre: {empresa_test.nombre}")
            print(f"   Nuevo email: {empresa_test.email_contacto}")
            print(f"   Nuevo teléfono: {empresa_test.telefono_contacto}")
        else:
            print(f"   ❌ Error editando empresa")
            
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # TEST 2: Suspender empresa
    print(f"\n⏸️ TEST 2: Suspendiendo empresa...")
    suspend_data = {
        'empresa_id': empresa_test.empresa_id,
        'accion': 'suspender'
    }
    
    try:
        suspend_response = requests.post(f'{BASE_URL}/suspender_empresa/', 
                                       json=suspend_data, headers=headers)
        print(f"   Response status: {suspend_response.status_code}")
        print(f"   Response: {suspend_response.text}")
        
        if suspend_response.status_code == 200:
            # Verificar cambios en DB
            empresa_test.refresh_from_db()
            print(f"   ✅ Empresa suspendida exitosamente")
            print(f"   Nuevo status: {empresa_test.status}")
        else:
            print(f"   ❌ Error suspendiendo empresa")
            
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # TEST 3: Reactivar empresa
    print(f"\n▶️ TEST 3: Reactivando empresa...")
    activate_data = {
        'empresa_id': empresa_test.empresa_id,
        'accion': 'activar'
    }
    
    try:
        activate_response = requests.post(f'{BASE_URL}/suspender_empresa/', 
                                        json=activate_data, headers=headers)
        print(f"   Response status: {activate_response.status_code}")
        print(f"   Response: {activate_response.text}")
        
        if activate_response.status_code == 200:
            # Verificar cambios en DB
            empresa_test.refresh_from_db()
            print(f"   ✅ Empresa reactivada exitosamente")
            print(f"   Nuevo status: {empresa_test.status}")
        else:
            print(f"   ❌ Error reactivando empresa")
            
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    print(f"\n📊 RESUMEN FINAL:")
    empresa_test.refresh_from_db()
    print(f"   Nombre: {empresa_test.nombre}")
    print(f"   Status: {empresa_test.status}")
    print(f"   Email: {empresa_test.email_contacto}")
    print(f"   Teléfono: {empresa_test.telefono_contacto}")
    print(f"   Dirección: {empresa_test.direccion}")

if __name__ == "__main__":
    test_functions()
