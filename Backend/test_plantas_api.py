import requests
import json

# Configuración
BASE_URL = "http://localhost:8000"
LOGIN_URL = f"{BASE_URL}/api/auth/login/"
PLANTAS_URL = f"{BASE_URL}/api/plantas/"

# Datos de prueba para login
login_data = {
    "username": "admin",
    "password": "admin123"
}

def test_plantas_api():
    session = requests.Session()
    
    try:
        # 1. Login para obtener token
        print("🔐 Iniciando sesión...")
        login_response = session.post(LOGIN_URL, json=login_data)
        
        if login_response.status_code == 200:
            print("✅ Login exitoso")
            token_data = login_response.json()
            token = token_data.get('token')
            
            # Configurar headers con token
            headers = {
                'Authorization': f'Token {token}',
                'Content-Type': 'application/json'
            }
            
        else:
            print(f"❌ Error en login: {login_response.status_code}")
            print(f"Respuesta: {login_response.text}")
            return
            
        # 2. Obtener plantas existentes
        print("\n📋 Obteniendo plantas...")
        get_response = session.get(PLANTAS_URL, headers=headers)
        
        if get_response.status_code == 200:
            plantas = get_response.json()
            print(f"✅ Plantas obtenidas: {len(plantas)}")
            for planta in plantas:
                print(f"   - {planta.get('nombre')} (ID: {planta.get('planta_id')})")
        else:
            print(f"❌ Error obteniendo plantas: {get_response.status_code}")
            print(f"Respuesta: {get_response.text}")
            
        # 3. Intentar crear una nueva planta
        print("\n➕ Creando nueva planta...")
        nueva_planta_data = {
            "nombre": "Planta de Prueba API",
            "direccion": "Dirección de prueba 123",
            "empresa": 1  # Usando empresa ID 1
        }
        
        create_response = session.post(PLANTAS_URL, headers=headers, json=nueva_planta_data)
        
        if create_response.status_code == 201:
            print("✅ Planta creada exitosamente")
            planta_creada = create_response.json()
            print(f"   - Nombre: {planta_creada.get('nombre')}")
            print(f"   - ID: {planta_creada.get('planta_id')}")
            
            # Si se crearon credenciales, mostrarlas
            if 'credenciales_usuario_planta' in planta_creada:
                creds = planta_creada['credenciales_usuario_planta']
                print(f"   - Usuario planta: {creds.get('usuario')}")
                print(f"   - Password: {creds.get('password')}")
                
        else:
            print(f"❌ Error creando planta: {create_response.status_code}")
            print(f"Respuesta: {create_response.text}")
            
            # Intentar obtener más detalles del error
            try:
                error_detail = create_response.json()
                print(f"Detalles del error: {json.dumps(error_detail, indent=2)}")
            except:
                print("No se pudo parsear el JSON de error")
                
        # 4. Intentar actualizar una planta existente (si hay alguna)
        if plantas:
            print(f"\n✏️ Actualizando planta ID {plantas[0].get('planta_id')}...")
            
            update_data = {
                "nombre": f"{plantas[0].get('nombre')} - ACTUALIZADA",
                "direccion": plantas[0].get('direccion', ''),
                "empresa": plantas[0].get('empresa', 1)
            }
            
            planta_id = plantas[0].get('planta_id')
            update_url = f"{PLANTAS_URL}{planta_id}/"
            update_response = session.put(update_url, headers=headers, json=update_data)
            
            if update_response.status_code == 200:
                print("✅ Planta actualizada exitosamente")
                planta_actualizada = update_response.json()
                print(f"   - Nuevo nombre: {planta_actualizada.get('nombre')}")
            else:
                print(f"❌ Error actualizando planta: {update_response.status_code}")
                print(f"Respuesta: {update_response.text}")
                
                try:
                    error_detail = update_response.json()
                    print(f"Detalles del error: {json.dumps(error_detail, indent=2)}")
                except:
                    print("No se pudo parsear el JSON de error")
    
    except Exception as e:
        print(f"❌ Error general: {str(e)}")

if __name__ == "__main__":
    test_plantas_api()
