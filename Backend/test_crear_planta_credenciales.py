import requests
import json

# Primero login como admin empresa
print("=== LOGIN COMO ADMIN EMPRESA ===")
login_data = {
    'username': 'admin_empresa',
    'password': 'admin123'
}

response = requests.post('http://localhost:8000/api/auth/login/', json=login_data)
if response.status_code == 200:
    data = response.json()
    token = data['token']
    print('✅ Login exitoso como admin empresa')
    
    # Crear nueva planta
    print("\n=== CREANDO NUEVA PLANTA ===")
    headers = {'Authorization': f'Token {token}'}
    planta_data = {
        'nombre': 'Planta Norte Test',
        'direccion': 'Av. Norte 123, Ciudad Test'
    }
    
    planta_response = requests.post('http://localhost:8000/api/plantas/', json=planta_data, headers=headers)
    if planta_response.status_code == 201:
        planta_result = planta_response.json()
        print('✅ Planta creada exitosamente!')
        print(f"Planta ID: {planta_result.get('planta_id')}")
        print(f"Nombre: {planta_result.get('nombre')}")
        
        # Verificar si se devolvieron credenciales
        if 'credenciales_usuario_planta' in planta_result:
            creds = planta_result['credenciales_usuario_planta']
            print("\n🔑 CREDENCIALES GENERADAS:")
            print(f"Usuario: {creds['usuario']}")
            print(f"Password: {creds['password']}")
            print(f"Admin Planta ID: {creds['admin_planta_id']}")
            
            # Probar login con las credenciales generadas
            print("\n=== PROBANDO LOGIN CON CREDENCIALES GENERADAS ===")
            login_planta_data = {
                'username': creds['usuario'],
                'password': creds['password']
            }
            
            planta_login_response = requests.post('http://localhost:8000/api/auth/login/', json=login_planta_data)
            if planta_login_response.status_code == 200:
                planta_login_result = planta_login_response.json()
                print('✅ Login exitoso con credenciales de planta!')
                
                # Probar endpoint /users/me/ con el token de planta
                planta_headers = {'Authorization': f'Token {planta_login_result["token"]}'}
                me_response = requests.get('http://localhost:8000/api/users/me/', headers=planta_headers)
                if me_response.status_code == 200:
                    me_data = me_response.json()
                    print("\n👤 DATOS DEL USUARIO DE PLANTA:")
                    print(json.dumps(me_data, indent=2, ensure_ascii=False))
                else:
                    print(f'❌ Error en /users/me/: {me_response.text}')
            else:
                print(f'❌ Error en login de planta: {planta_login_response.text}')
        else:
            print("⚠️ No se devolvieron credenciales en la respuesta")
            print("Respuesta completa:", json.dumps(planta_result, indent=2, ensure_ascii=False))
    else:
        print(f'❌ Error creando planta: {planta_response.text}')
else:
    print(f'❌ Error en login: {response.text}')
