#!/usr/bin/env python3
import requests
import json

# Login
login_data = {'username': 'ferdiaz', 'password': 'fer123'}

print('🔐 Haciendo login...')
try:
    response = requests.post('http://localhost:8000/api/auth/login/', 
                           json=login_data, timeout=5)
    
    if response.status_code == 200:
        data = response.json()
        token = data.get('token')
        print(f'✅ Login exitoso! Token: {token[:20]}...')
        
        # Probar eliminación
        print('\n🗑️ Probando eliminación de planta...')
        headers = {'Authorization': f'Token {token}'}
        
        delete_response = requests.delete('http://localhost:8000/api/plantas/12/', 
                                        headers=headers, timeout=10)
        
        print(f'Status: {delete_response.status_code}')
        if delete_response.status_code == 200:
            print('✅ Planta eliminada exitosamente!')
            print(json.dumps(delete_response.json(), indent=2))
        else:
            print('❌ Error eliminando planta')
            print(delete_response.text[:500])
    else:
        print(f'❌ Error en login: {response.status_code}')
        print(response.text)
        
except Exception as e:
    print(f'❌ Error: {e}')
