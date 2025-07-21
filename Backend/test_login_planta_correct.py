import requests
import json

# Probar login con un usuario de planta
login_data = {
    'username': 'planta_plantaoeste_8@codewavetechnologies.com',
    'password': 'tSv1OxAa'
}

response = requests.post('http://localhost:8000/api/auth/login/', json=login_data)
if response.status_code == 200:
    data = response.json()
    print('Login exitoso')
    print('Token:', data.get('token', '')[:20] + '...')
    
    # Obtener datos del usuario con /users/me
    headers = {'Authorization': f'Token {data["token"]}'}
    me_response = requests.get('http://localhost:8000/api/users/me/', headers=headers)
    if me_response.status_code == 200:
        me_data = me_response.json()
        print('\nDatos del usuario (/users/me):')
        print(json.dumps(me_data, indent=2, ensure_ascii=False))
    else:
        print('Error en /users/me:', me_response.text)
else:
    print('Error en login:', response.text)
