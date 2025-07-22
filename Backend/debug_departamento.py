# -*- coding: utf-8 -*-
"""
Debug específico del problema del departamento
"""
import requests
import json
import time

BASE_URL = "http://localhost:8000"
API_URL = f"{BASE_URL}/api"

def debug_departamento():
    """Debug específico del problema del departamento"""
    print("🔍 === DEBUG: PROBLEMA DEPARTAMENTO ===")
    
    # Obtener token de admin (usar el último creado)
    login_data = {
        'username': 'admin_empresa_1753156918',  # Del último test
        'password': 'AdminPass123!'
    }
    
    headers = {'Content-Type': 'application/json'}
    login_response = requests.post(f"{API_URL}/auth/login/", 
                                 data=json.dumps(login_data), 
                                 headers=headers)
    
    if login_response.status_code != 200:
        print("❌ No se pudo hacer login")
        return
    
    token = login_response.json()['token']
    auth_headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Token {token}'
    }
    
    # 1. Listar plantas disponibles
    print("\n1️⃣ Plantas disponibles:")
    plantas_response = requests.get(f"{API_URL}/plantas/", headers=auth_headers)
    
    if plantas_response.status_code == 200:
        plantas = plantas_response.json()
        print(f"   Plantas encontradas: {len(plantas)}")
        
        if plantas:
            planta = plantas[0]
            planta_id = planta['planta_id']
            print(f"   Planta ID: {planta_id}")
            print(f"   Planta Nombre: {planta['nombre']}")
            
            # 2. Intentar crear departamento
            print(f"\n2️⃣ Intentando crear departamento:")
            
            departamento_data = {
                "nombre": f"Departamento Debug {int(time.time())}",
                "descripcion": "Departamento de prueba para debug",
                "planta": planta_id
            }
            
            print(f"   Datos enviados: {json.dumps(departamento_data, indent=2)}")
            
            depto_response = requests.post(f"{API_URL}/departamentos/", 
                                         data=json.dumps(departamento_data), 
                                         headers=auth_headers)
            
            print(f"   Status: {depto_response.status_code}")
            print(f"   Respuesta: {depto_response.text}")
            
            # 3. Verificar directamente en la base de datos (simulado)
            print(f"\n3️⃣ Verificación de la planta:")
            
            # Hacer un GET específico de esa planta
            planta_detail_response = requests.get(f"{API_URL}/plantas/{planta_id}/", headers=auth_headers)
            print(f"   Status GET planta específica: {planta_detail_response.status_code}")
            
            if planta_detail_response.status_code == 200:
                planta_detail = planta_detail_response.json()
                print(f"   Detalle planta: {json.dumps(planta_detail, indent=2)}")
            else:
                print(f"   Error: {planta_detail_response.text}")
        else:
            print("   ❌ No hay plantas disponibles")
    else:
        print(f"   ❌ Error listando plantas: {plantas_response.text}")

if __name__ == "__main__":
    debug_departamento()
