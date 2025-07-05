#!/usr/bin/env python
"""
Script para probar la creación de departamentos via API HTTP
"""
import requests
import json

# Configuración
BASE_URL = "http://127.0.0.1:8000/api"

def test_departamento_api():
    print("🔍 PRUEBA DE DEPARTAMENTOS VIA API")
    print("="*40)
    
    # 1. Login para obtener token
    print("1. Haciendo login...")
    login_data = {
        "username": "juan.perez@codewave.com",
        "password": "123456"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/auth/login/", json=login_data)
        if response.status_code == 200:
            login_result = response.json()
            token = login_result.get('token')
            print(f"✅ Login exitoso. Token: {token[:10]}...")
        else:
            print(f"❌ Error en login: {response.status_code} - {response.text}")
            return
    except Exception as e:
        print(f"❌ Error conectando: {e}")
        return
    
    # 2. Obtener plantas disponibles
    print("\n2. Obteniendo plantas...")
    headers = {
        'Authorization': f'Token {token}',
        'Content-Type': 'application/json'
    }
    
    try:
        response = requests.get(f"{BASE_URL}/plantas/", headers=headers)
        if response.status_code == 200:
            plantas = response.json()
            if plantas:
                planta_id = plantas[0]['planta_id']
                print(f"✅ Planta encontrada: {plantas[0]['nombre']} (ID: {planta_id})")
            else:
                print("❌ No hay plantas disponibles")
                return
        else:
            print(f"❌ Error obteniendo plantas: {response.status_code} - {response.text}")
            return
    except Exception as e:
        print(f"❌ Error obteniendo plantas: {e}")
        return
    
    # 3. Crear departamento
    print("\n3. Creando departamento...")
    departamento_data = {
        "nombre": "Departamento Test API",
        "descripcion": "Departamento creado via API para pruebas",
        "planta_id": planta_id
    }
    
    print(f"Datos a enviar: {json.dumps(departamento_data, indent=2)}")
    
    try:
        response = requests.post(f"{BASE_URL}/departamentos/", json=departamento_data, headers=headers)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 201:
            result = response.json()
            print(f"✅ Departamento creado exitosamente!")
            print(f"   ID: {result.get('departamento_id')}")
            print(f"   Nombre: {result.get('nombre')}")
            print(f"   Descripción: {result.get('descripcion')}")
        else:
            print(f"❌ Error creando departamento:")
            try:
                error_data = response.json()
                print(f"   Error: {json.dumps(error_data, indent=2)}")
            except:
                print(f"   Error texto: {response.text}")
    except Exception as e:
        print(f"❌ Error en la petición: {e}")

if __name__ == "__main__":
    test_departamento_api()
