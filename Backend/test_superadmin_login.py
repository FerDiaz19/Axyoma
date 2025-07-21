import requests
import json

# Probar login con usuarios superadmin
usuarios_test = [
    {'username': 'superadmin', 'password': 'admin123'},
    {'username': 'ernesto', 'password': 'admin123'},
    {'username': 'sistema', 'password': 'admin123'},
]

for creds in usuarios_test:
    print(f"\n=== PROBANDO LOGIN CON {creds['username']} ===")
    
    response = requests.post('http://localhost:8000/api/auth/login/', json=creds)
    if response.status_code == 200:
        data = response.json()
        print(f'✅ Login exitoso para {creds["username"]}')
        print('Token:', data.get('token', '')[:20] + '...')
        
        # Obtener datos del usuario con /users/me
        headers = {'Authorization': f'Token {data["token"]}'}
        me_response = requests.get('http://localhost:8000/api/users/me/', headers=headers)
        if me_response.status_code == 200:
            me_data = me_response.json()
            print('\n📋 DATOS DEL USUARIO (/users/me):')
            print(json.dumps(me_data, indent=2, ensure_ascii=False))
        else:
            print(f'❌ Error en /users/me/: {me_response.status_code} - {me_response.text}')
    else:
        print(f'❌ Error en login para {creds["username"]}: {response.status_code} - {response.text}')
