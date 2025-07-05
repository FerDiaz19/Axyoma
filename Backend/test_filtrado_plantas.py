#!/usr/bin/env python
"""
Script para probar el filtrado de plantas via API
"""
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')
django.setup()

import requests
import json

def test_filtrado_plantas():
    """Probar que cada empresa solo ve sus plantas"""
    print("=== PRUEBA FILTRADO DE PLANTAS VIA API ===\n")
    
    base_url = "http://localhost:8000"
    
    # Usuarios de prueba
    usuarios_test = [
        {
            'username': 'admin_test_empresa',
            'password': 'password123',
            'empresa_esperada': 'Empresa Test Registro',
            'plantas_esperadas': 0
        },
        {
            'username': 'admin_test_limpio', 
            'password': 'test123',
            'empresa_esperada': 'Empresa Test Limpia',
            'plantas_esperadas': 0
        },
        {
            'username': 'axis',
            'password': 'axis',  # Asumir misma contraseña que username
            'empresa_esperada': 'axis',
            'plantas_esperadas': 1
        }
    ]
    
    for usuario_test in usuarios_test:
        print(f"🧪 Probando usuario: {usuario_test['username']}")
        
        # Login
        login_data = {
            'username': usuario_test['username'],
            'password': usuario_test['password']
        }
        
        try:
            login_response = requests.post(f"{base_url}/auth/login/", json=login_data)
            
            if login_response.status_code == 200:
                login_result = login_response.json()
                token = login_result.get('token')
                empresa_nombre = login_result.get('nombre_empresa', 'N/A')
                
                print(f"   ✅ Login exitoso")
                print(f"   📢 Empresa: {empresa_nombre}")
                
                # Verificar empresa
                if empresa_nombre == usuario_test['empresa_esperada']:
                    print(f"   ✅ Empresa correcta")
                else:
                    print(f"   ❌ Empresa incorrecta. Esperada: {usuario_test['empresa_esperada']}")
                
                # Obtener plantas
                headers = {'Authorization': f'Token {token}'}
                plantas_response = requests.get(f"{base_url}/plantas/", headers=headers)
                
                if plantas_response.status_code == 200:
                    plantas = plantas_response.json()
                    print(f"   📋 Plantas obtenidas: {len(plantas)}")
                    
                    # Verificar cantidad esperada
                    if len(plantas) == usuario_test['plantas_esperadas']:
                        print(f"   ✅ Cantidad de plantas correcta")
                    else:
                        print(f"   ❌ Cantidad incorrecta. Esperadas: {usuario_test['plantas_esperadas']}")
                    
                    # Mostrar plantas
                    if plantas:
                        for planta in plantas:
                            print(f"     - {planta['nombre']} (ID: {planta['planta_id']})")
                    else:
                        print(f"     ✅ Sin plantas (correcto para empresa nueva)")
                else:
                    print(f"   ❌ Error obteniendo plantas: {plantas_response.status_code}")
                    
            else:
                print(f"   ❌ Error en login: {login_response.status_code}")
                if login_response.status_code == 401:
                    print(f"   💡 Puede que la contraseña sea incorrecta")
                
        except Exception as e:
            print(f"   ❌ Error durante la prueba: {str(e)}")
        
        print()

def test_creacion_planta():
    """Probar creación de planta con empresa limpia"""
    print("=== PRUEBA CREACIÓN DE PLANTA ===\n")
    
    base_url = "http://localhost:8000"
    
    # Login con empresa limpia
    login_data = {
        'username': 'admin_test_limpio',
        'password': 'test123'
    }
    
    try:
        login_response = requests.post(f"{base_url}/auth/login/", json=login_data)
        
        if login_response.status_code == 200:
            login_result = login_response.json()
            token = login_result.get('token')
            
            headers = {'Authorization': f'Token {token}'}
            
            # Crear planta de prueba
            planta_data = {
                'nombre': 'Planta Test Filtrado',
                'direccion': 'Dir test filtrado 123'
            }
            
            print(f"🏭 Creando planta: {planta_data['nombre']}")
            
            create_response = requests.post(
                f"{base_url}/plantas/", 
                json=planta_data,
                headers=headers
            )
            
            if create_response.status_code == 201:
                planta_creada = create_response.json()
                print(f"   ✅ Planta creada: ID {planta_creada['planta_id']}")
                
                # Verificar que aparece en la lista
                plantas_response = requests.get(f"{base_url}/plantas/", headers=headers)
                if plantas_response.status_code == 200:
                    plantas = plantas_response.json()
                    print(f"   📋 Plantas en lista: {len(plantas)}")
                    
                    if len(plantas) == 1:
                        print(f"   ✅ Filtrado funcionando correctamente")
                    else:
                        print(f"   ❌ Filtrado fallando")
                        
            else:
                print(f"   ❌ Error creando planta: {create_response.status_code}")
                print(f"       Respuesta: {create_response.text}")
                
    except Exception as e:
        print(f"❌ Error durante la prueba: {str(e)}")

if __name__ == "__main__":
    test_filtrado_plantas()
    test_creacion_planta()
