#!/usr/bin/env python
import requests
import json

def test_superadmin_login_and_plantas():
    print("🔍 Testing SuperAdmin login and plantas endpoint...")
    
    try:
        # Crear sesión
        session = requests.Session()
        
        # Intentar login con admin
        login_data = {
            'username': 'admin',
            'password': 'admin123'
        }
        
        print("🔐 Intentando login...")
        login_response = session.post('http://localhost:8000/api/auth/login/', json=login_data)
        print(f"📊 Login Status: {login_response.status_code}")
        
        if login_response.status_code == 200:
            login_data_resp = login_response.json()
            print(f"✅ Login exitoso para: {login_data_resp.get('usuario', 'unknown')}")
            print(f"📋 Nivel usuario: {login_data_resp.get('nivel_usuario', 'unknown')}")
            
            # Si el login fue exitoso, probar el endpoint de plantas
            print("🔍 Probando endpoint listar_todas_plantas...")
            plantas_response = session.get('http://localhost:8000/api/superadmin/listar_todas_plantas/')
            print(f"📊 Plantas Status: {plantas_response.status_code}")
            
            if plantas_response.status_code == 200:
                plantas_data = plantas_response.json()
                print(f"✅ SUCCESS! Found {len(plantas_data)} plantas")
                
                # Mostrar información de las primeras plantas
                for i, planta in enumerate(plantas_data[:3]):
                    print(f"  🏭 Planta {i+1}: {planta['nombre']} - {planta['empresa']['nombre']}")
                    
            elif plantas_response.status_code == 500:
                print(f"❌ Error 500 en plantas endpoint")
                print(f"Response: {plantas_response.text}")
            else:
                print(f"❌ Error {plantas_response.status_code}: {plantas_response.text}")
                
        else:
            print(f"❌ Login failed: {login_response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Error: No se pudo conectar al servidor. ¿Está corriendo en localhost:8000?")
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    test_superadmin_login_and_plantas()
