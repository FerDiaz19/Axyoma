import requests
import json

# Probar login con usuario de planta recién creado
print("=== PROBANDO LOGIN CON USUARIO DE PLANTA ===")
login_data = {
    'username': 'planta_plantanortetest_18@codewavetechnologies.com',
    'password': 'OzifpQFN'
}

response = requests.post('http://localhost:8000/api/auth/login/', json=login_data)
if response.status_code == 200:
    data = response.json()
    print('✅ Login exitoso')
    print('Token:', data.get('token', '')[:20] + '...')
    
    # Obtener datos del usuario con /users/me
    headers = {'Authorization': f'Token {data["token"]}'}
    me_response = requests.get('http://localhost:8000/api/users/me/', headers=headers)
    if me_response.status_code == 200:
        me_data = me_response.json()
        print('\n📋 DATOS COMPLETOS DEL USUARIO (/users/me):')
        print(json.dumps(me_data, indent=2, ensure_ascii=False))
        
        # Verificar específicamente el nivel de usuario
        print(f"\n🔍 VERIFICACIÓN DE NIVEL:")
        print(f"userData?.perfil?.nivel_usuario = '{me_data.get('perfil', {}).get('nivel_usuario')}'")
        print(f"userData?.empresa = {me_data.get('empresa')}")
        print(f"userData?.is_superuser = {me_data.get('is_superuser')}")
        
        # Simular la lógica del Dashboard
        print(f"\n🖥️ LÓGICA DEL DASHBOARD:")
        if me_data.get('is_superuser'):
            print("➡️ Sería dirigido a: SuperAdminDashboard")
        elif me_data.get('perfil', {}).get('nivel_usuario') == 'admin_planta':
            print("➡️ Sería dirigido a: PlantaAdminDashboard ✅")
        elif me_data.get('empresa'):
            print("➡️ Sería dirigido a: EmpresaAdminDashboard")
        else:
            print("➡️ Sería dirigido a: EmpresaAdminDashboard (default)")
            
    else:
        print('❌ Error en /users/me:', me_response.text)
else:
    print('❌ Error en login:', response.text)
