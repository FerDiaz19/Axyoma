#!/usr/bin/env python3
"""
Script de prueba para los endpoints del SuperAdmin
"""
import requests
import json

# URL base del API
BASE_URL = "http://127.0.0.1:8000/api"

def test_login():
    """Probar login y obtener token"""
    print("🔐 Probando login...")
    
    # Datos de login (ajustar según tu usuario superadmin)
    login_data = {
        "username": "superadmin@axyoma.com",  # Email como username
        "password": "admin123"                # Contraseña establecida
    }
    
    try:
        response = requests.post(f"{BASE_URL}/auth/login/", json=login_data)
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Login exitoso")
            print(f"   Token: {data.get('token', 'N/A')[:20]}...")
            print(f"   Nivel: {data.get('nivel_usuario', 'N/A')}")
            return data.get('token')
        else:
            print(f"❌ Login fallido: {response.status_code}")
            print(f"   Respuesta: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Error en login: {e}")
        return None

def test_superadmin_endpoints(token):
    """Probar endpoints del SuperAdmin"""
    headers = {
        'Authorization': f'Token {token}',
        'Content-Type': 'application/json'
    }
    
    # 1. Probar estadísticas
    print("\n📊 Probando estadísticas del sistema...")
    try:
        response = requests.get(f"{BASE_URL}/superadmin/estadisticas_sistema/", headers=headers)
        if response.status_code == 200:
            print("✅ Estadísticas obtenidas correctamente")
            data = response.json()
            print(f"   Total empresas: {data.get('total_empresas', 0)}")
            print(f"   Total usuarios: {data.get('total_usuarios', 0)}")
        else:
            print(f"❌ Error obteniendo estadísticas: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # 2. Probar listar empresas
    print("\n🏢 Probando listado de empresas...")
    try:
        response = requests.get(f"{BASE_URL}/superadmin/listar_empresas/", headers=headers)
        if response.status_code == 200:
            print("✅ Empresas listadas correctamente")
            data = response.json()
            empresas = data.get('empresas', [])
            print(f"   Total empresas: {len(empresas)}")
            if empresas:
                primera = empresas[0]
                print(f"   Primera empresa: {primera.get('nombre', 'N/A')}")
        else:
            print(f"❌ Error listando empresas: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # 3. Probar listar usuarios
    print("\n👥 Probando listado de usuarios...")
    try:
        response = requests.get(f"{BASE_URL}/superadmin/listar_usuarios/", headers=headers)
        if response.status_code == 200:
            print("✅ Usuarios listados correctamente")
            data = response.json()
            usuarios = data.get('usuarios', [])
            print(f"   Total usuarios: {len(usuarios)}")
            if usuarios:
                superadmins = [u for u in usuarios if u.get('nivel_usuario') == 'superadmin']
                print(f"   SuperAdmins: {len(superadmins)}")
        else:
            print(f"❌ Error listando usuarios: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # 4. Probar crear usuario SuperAdmin
    print("\n👤 Probando creación de usuario SuperAdmin...")
    nuevo_usuario = {
        "username": "test_superadmin",
        "email": "test@superadmin.com",
        "nombre": "Usuario",
        "apellido_paterno": "Prueba",
        "apellido_materno": "Test",
        "password": "test1234",
        "nivel_usuario": "superadmin"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/superadmin/crear_usuario/", json=nuevo_usuario, headers=headers)
        if response.status_code in [200, 201]:
            print("✅ Usuario SuperAdmin creado correctamente")
            data = response.json()
            print(f"   Usuario creado: {data.get('message', 'N/A')}")
            if 'password_temporal' in data:
                print(f"   Contraseña temporal: {data['password_temporal']}")
        elif response.status_code == 400:
            print("⚠️  Usuario ya existe o datos inválidos")
            print(f"   Respuesta: {response.json()}")
        else:
            print(f"❌ Error creando usuario: {response.status_code}")
            print(f"   Respuesta: {response.text}")
    except Exception as e:
        print(f"❌ Error: {e}")

def main():
    """Función principal"""
    print("🚀 Iniciando pruebas de endpoints SuperAdmin...")
    print("=" * 50)
    
    # 1. Login
    token = test_login()
    
    if not token:
        print("\n❌ No se pudo obtener token. Verifica:")
        print("   1. Que el servidor Django esté corriendo")
        print("   2. Que exista un usuario superadmin")
        print("   3. Que las credenciales sean correctas")
        return
    
    # 2. Probar endpoints
    test_superadmin_endpoints(token)
    
    print("\n" + "=" * 50)
    print("🏁 Pruebas completadas")

if __name__ == "__main__":
    main()
