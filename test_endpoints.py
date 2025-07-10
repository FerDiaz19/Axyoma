#!/usr/bin/env python3
"""
Script para probar los endpoints del SuperAdmin
"""
import requests
import json

BASE_URL = 'http://127.0.0.1:8000/api'

def test_superadmin_endpoints():
    """Prueba los endpoints del SuperAdmin"""
    
    # Datos de login de SuperAdmin (ajustar según tus datos)
    login_data = {
        'username': 'superadmin',  # Ajustar según tu usuario
        'password': '1234'         # Ajustar según tu contraseña
    }
    
    session = requests.Session()
    
    try:
        # 1. Login
        print("🔐 Probando login...")
        login_response = session.post(f'{BASE_URL}/auth/login/', json=login_data)
        print(f"Login status: {login_response.status_code}")
        
        if login_response.status_code != 200:
            print("❌ Error en login:", login_response.text)
            return
        
        login_result = login_response.json()
        print("✅ Login exitoso")
        
        # 2. Obtener token (si existe)
        headers = {}
        if 'access_token' in login_result:
            headers['Authorization'] = f"Bearer {login_result['access_token']}"
        elif 'token' in login_result:
            headers['Authorization'] = f"Token {login_result['token']}"
        
        # 3. Probar endpoint de estadísticas
        print("\n📊 Probando estadísticas...")
        stats_response = session.get(f'{BASE_URL}/superadmin/estadisticas_sistema/', headers=headers)
        print(f"Estadísticas status: {stats_response.status_code}")
        if stats_response.status_code == 200:
            print("✅ Estadísticas obtenidas exitosamente")
        else:
            print("❌ Error en estadísticas:", stats_response.text[:200])
        
        # 4. Probar endpoint de listar empresas
        print("\n🏢 Probando lista de empresas...")
        empresas_response = session.get(f'{BASE_URL}/superadmin/listar_empresas/', headers=headers)
        print(f"Empresas status: {empresas_response.status_code}")
        if empresas_response.status_code == 200:
            empresas_data = empresas_response.json()
            print(f"✅ {empresas_data.get('total', 0)} empresas encontradas")
        else:
            print("❌ Error en empresas:", empresas_response.text[:200])
        
        # 5. Probar endpoint de listar usuarios
        print("\n👥 Probando lista de usuarios...")
        usuarios_response = session.get(f'{BASE_URL}/superadmin/listar_usuarios/', headers=headers)
        print(f"Usuarios status: {usuarios_response.status_code}")
        if usuarios_response.status_code == 200:
            usuarios_data = usuarios_response.json()
            print(f"✅ {usuarios_data.get('total', 0)} usuarios encontrados")
        else:
            print("❌ Error en usuarios:", usuarios_response.text[:200])
        
        # 6. Probar endpoint de editar empresa (si hay empresas)
        if empresas_response.status_code == 200:
            empresas_data = empresas_response.json()
            if empresas_data.get('empresas'):
                print("\n✏️ Probando edición de empresa...")
                primera_empresa = empresas_data['empresas'][0]
                edit_data = {
                    'empresa_id': primera_empresa['empresa_id'],
                    'nombre': primera_empresa['nombre'] + ' (TEST)',
                    'rfc': primera_empresa['rfc']
                }
                
                edit_response = session.put(f'{BASE_URL}/superadmin/editar_empresa/', 
                                          json=edit_data, headers=headers)
                print(f"Edición empresa status: {edit_response.status_code}")
                if edit_response.status_code == 200:
                    print("✅ Empresa editada exitosamente")
                    
                    # Revertir cambio
                    revert_data = {
                        'empresa_id': primera_empresa['empresa_id'],
                        'nombre': primera_empresa['nombre'],
                        'rfc': primera_empresa['rfc']
                    }
                    session.put(f'{BASE_URL}/superadmin/editar_empresa/', 
                              json=revert_data, headers=headers)
                    print("↩️ Cambio revertido")
                else:
                    print("❌ Error editando empresa:", edit_response.text[:200])
        
        # 7. Probar creación de usuario SuperAdmin
        print("\n👑 Probando creación de usuario SuperAdmin...")
        nuevo_usuario = {
            'username': 'test_superadmin',
            'email': 'test@example.com',
            'nombre': 'Usuario',
            'apellido_paterno': 'Test',
            'apellido_materno': 'SuperAdmin',
            'password': '1234'
        }
        
        crear_response = session.post(f'{BASE_URL}/superadmin/crear_usuario/', 
                                    json=nuevo_usuario, headers=headers)
        print(f"Crear usuario status: {crear_response.status_code}")
        if crear_response.status_code == 201:
            print("✅ Usuario SuperAdmin creado exitosamente")
        else:
            print("❌ Error creando usuario:", crear_response.text[:200])
        
        print("\n🎉 Pruebas completadas!")
        
    except Exception as e:
        print(f"❌ Error durante las pruebas: {e}")

if __name__ == '__main__':
    test_superadmin_endpoints()
