import requests
import json

# Probar login con superadmin y ver respuesta completa
print("=== PROBANDO LOGIN Y /users/me/ CON SUPERADMIN ===")

# 1. Login
login_data = {'username': 'superadmin', 'password': 'admin123'}
response = requests.post('http://localhost:8000/api/auth/login/', json=login_data)

if response.status_code == 200:
    data = response.json()
    print('✅ LOGIN EXITOSO')
    print(f'Token: {data.get("token", "")[:20]}...')
    
    # 2. Obtener /users/me/
    headers = {'Authorization': f'Token {data["token"]}'}
    me_response = requests.get('http://localhost:8000/api/users/me/', headers=headers)
    
    print(f'\n🔍 STATUS /users/me/: {me_response.status_code}')
    
    if me_response.status_code == 200:
        me_data = me_response.json()
        print('✅ /users/me/ EXITOSO')
        print('\n📋 DATOS COMPLETOS:')
        print(json.dumps(me_data, indent=2, ensure_ascii=False))
        
        print(f'\n🎯 VALORES CLAVE:')
        print(f'is_superuser: {me_data.get("is_superuser")}')
        print(f'perfil: {me_data.get("perfil")}')
        print(f'nivel_usuario: {me_data.get("perfil", {}).get("nivel_usuario") if me_data.get("perfil") else "None"}')
        
    else:
        print('❌ ERROR EN /users/me/')
        print(f'Status: {me_response.status_code}')
        print(f'Error: {me_response.text}')
        
else:
    print('❌ ERROR EN LOGIN')
    print(f'Status: {response.status_code}')
    print(f'Error: {response.text}')
