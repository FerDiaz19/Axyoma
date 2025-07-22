# -*- coding: utf-8 -*-
"""
Debug específico de la creación de usuarios de planta
"""
import requests
import json
import time

BASE_URL = "http://localhost:8000"
API_URL = f"{BASE_URL}/api"

def debug_creacion_usuario_planta():
    """Debug específico para la creación automática de usuarios de planta"""
    print("👥 === DEBUG: CREACIÓN DE USUARIO DE PLANTA ===")
    
    # Obtener token de admin (usar uno que sabemos que existe)
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
    
    print("🔑 Login exitoso")
    
    # Crear una nueva planta con debug detallado
    timestamp = int(time.time())
    nueva_planta = {
        "nombre": f"Planta Debug {timestamp}",
        "direccion": f"Dirección Debug {timestamp}, Col. Test"
    }
    
    print(f"\n📋 Creando planta: {nueva_planta['nombre']}")
    
    try:
        # Realizar la petición con timeout extendido
        response = requests.post(
            f"{API_URL}/plantas/",
            data=json.dumps(nueva_planta),
            headers=auth_headers,
            timeout=60  # Timeout más largo
        )
        
        print(f"📊 Status: {response.status_code}")
        
        if response.status_code == 201:
            planta_data = response.json()
            
            print(f"✅ Planta creada exitosamente:")
            print(f"   ID: {planta_data.get('planta_id', 'N/A')}")
            print(f"   Nombre: {planta_data.get('nombre', 'N/A')}")
            
            print(f"\n🔍 Verificando credenciales:")
            if 'credenciales_usuario_planta' in planta_data:
                credenciales = planta_data['credenciales_usuario_planta']
                print(f"   ✅ Credenciales generadas:")
                print(f"      Usuario: {credenciales.get('usuario', 'N/A')}")
                print(f"      Password: {credenciales.get('password', 'N/A')}")
                print(f"      Admin Planta ID: {credenciales.get('admin_planta_id', 'N/A')}")
                
                # Probar login con las credenciales
                print(f"\n🧪 Probando login con las credenciales:")
                
                login_planta_data = {
                    'username': credenciales.get('usuario'),
                    'password': credenciales.get('password')
                }
                
                login_planta_response = requests.post(
                    f"{API_URL}/auth/login/",
                    data=json.dumps(login_planta_data),
                    headers={'Content-Type': 'application/json'},
                    timeout=30
                )
                
                print(f"   📊 Status login planta: {login_planta_response.status_code}")
                
                if login_planta_response.status_code == 200:
                    login_result = login_planta_response.json()
                    print(f"   ✅ Login exitoso para usuario de planta")
                    print(f"      Token generado: {login_result.get('token', '')[:20]}...")
                else:
                    print(f"   ❌ Error en login planta: {login_planta_response.text}")
                
            else:
                print(f"   ❌ NO se generaron credenciales automáticas")
                print(f"   📋 Respuesta completa:")
                print(f"      {json.dumps(planta_data, indent=6)}")
            
            # Verificar tabla admin_plantas directamente
            print(f"\n📋 Consultando usuarios de planta:")
            usuarios_planta_response = requests.get(f"{API_URL}/plantas/usuarios_planta/", headers=auth_headers)
            
            print(f"   Status: {usuarios_planta_response.status_code}")
            
            if usuarios_planta_response.status_code == 200:
                usuarios_planta = usuarios_planta_response.json()
                print(f"   📊 Usuarios de planta encontrados: {len(usuarios_planta)}")
                
                for usuario in usuarios_planta:
                    print(f"      - Usuario: {usuario.get('usuario', {}).get('nombre', 'N/A')}")
                    print(f"        Planta: {usuario.get('planta', {}).get('nombre', 'N/A')}")
                    print(f"        Credenciales temporales: {usuario.get('tiene_password_temporal', False)}")
            else:
                print(f"   ❌ Error: {usuarios_planta_response.text}")
                
        elif response.status_code == 400:
            print(f"❌ Error de validación:")
            error_data = response.json()
            print(f"   {json.dumps(error_data, indent=2)}")
            
        else:
            print(f"❌ Error inesperado: {response.status_code}")
            print(f"   Respuesta: {response.text}")
            
    except requests.exceptions.Timeout:
        print(f"⏰ Timeout - La creación está tardando mucho")
        
    except Exception as e:
        print(f"🚨 Error inesperado: {str(e)}")

if __name__ == "__main__":
    debug_creacion_usuario_planta()
