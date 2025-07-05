#!/usr/bin/env python
"""
Script completo para diagnosticar problemas de servidor y rutas
"""
import requests
import json
import time

def test_servidor_basico():
    """Prueba que el servidor Django esté corriendo"""
    print("=" * 50)
    print("1. VERIFICANDO SERVIDOR DJANGO")
    print("=" * 50)
    
    try:
        response = requests.get('http://127.0.0.1:8000/', timeout=5)
        print(f"✓ Servidor responde: {response.status_code}")
        return True
    except requests.exceptions.ConnectionError:
        print("✗ ERROR: No se puede conectar al servidor Django")
        print("  Asegúrate de que 'python manage.py runserver' esté ejecutándose")
        return False
    except Exception as e:
        print(f"✗ ERROR inesperado: {e}")
        return False

def test_rutas_api():
    """Prueba las rutas principales de la API"""
    print("\n" + "=" * 50)
    print("2. VERIFICANDO RUTAS DE LA API")
    print("=" * 50)
    
    rutas = [
        'http://127.0.0.1:8000/api/',
        'http://127.0.0.1:8000/api/auth/',
        'http://127.0.0.1:8000/api/auth/login/',
        'http://127.0.0.1:8000/api/auth/register/',
        'http://127.0.0.1:8000/api/plantas/',
        'http://127.0.0.1:8000/api/departamentos/',
    ]
    
    for ruta in rutas:
        try:
            response = requests.get(ruta, timeout=5)
            print(f"✓ {ruta} → {response.status_code}")
        except Exception as e:
            print(f"✗ {ruta} → ERROR: {e}")

def test_login_usuario_existente():
    """Prueba login con usuario conocido"""
    print("\n" + "=" * 50)
    print("3. PROBANDO LOGIN CON USUARIO EXISTENTE")
    print("=" * 50)
    
    url_login = 'http://127.0.0.1:8000/api/auth/login/'
    
    # Datos de prueba - agregamos el usuario que creamos
    usuarios_prueba = [
        {'username': 'admin_frontend_test', 'password': 'frontend123'},
        {'username': 'admin_test_nuevo', 'password': 'password123'},
        {'username': 'admin_empresa_1', 'password': 'password123'},
        {'username': 'admin', 'password': 'admin'},
    ]
    
    for datos in usuarios_prueba:
        print(f"\nProbando login con: {datos['username']}")
        try:
            response = requests.post(url_login, json=datos, timeout=5)
            print(f"  Status: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                print(f"  ✓ Login exitoso!")
                print(f"  Token: {result.get('token', 'No token')[:20]}...")
                print(f"  Usuario: {result.get('user', {}).get('username', 'No username')}")
                return result.get('token')
            else:
                print(f"  ✗ Error: {response.text}")
                
        except Exception as e:
            print(f"  ✗ ERROR: {e}")
    
    return None

def test_registro_empresa():
    """Prueba registro de nueva empresa"""
    print("\n" + "=" * 50)
    print("4. PROBANDO REGISTRO DE EMPRESA")
    print("=" * 50)
    
    # URL CORRECTA para registro
    url_registro = 'http://127.0.0.1:8000/api/empresas/registro/'
    
    # Campos CORRECTOS según el serializer
    datos_empresa = {
        'nombre': f'Empresa Test {int(time.time())}',
        'rfc': f'RFC{int(time.time())}',
        'direccion': f'Dirección Test {int(time.time())}',
        'email_contacto': f'test{int(time.time())}@empresa.com',
        'telefono_contacto': '555-1234',
        'usuario': f'admin_test_{int(time.time())}',
        'password': 'password123',
        'nombre_completo': f'Admin Test {int(time.time())}'
    }
    
    print(f"Datos de registro: {json.dumps(datos_empresa, indent=2)}")
    
    try:
        response = requests.post(url_registro, json=datos_empresa, timeout=10)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 201:
            result = response.json()
            print("✓ Registro exitoso!")
            print(f"Usuario creado: {result.get('user', {}).get('username')}")
            print(f"Empresa creada: {result.get('empresa', {}).get('nombre')}")
            return True
        else:
            print(f"✗ Error en registro: {response.text}")
            
    except Exception as e:
        print(f"✗ ERROR: {e}")
    
    return False

def test_con_token(token):
    """Prueba endpoints que requieren autenticación"""
    if not token:
        print("\n⚠ No hay token disponible, saltando pruebas autenticadas")
        return
        
    print("\n" + "=" * 50)
    print("5. PROBANDO ENDPOINTS CON AUTENTICACIÓN")
    print("=" * 50)
    
    headers = {'Authorization': f'Token {token}'}
    
    endpoints = [
        'http://127.0.0.1:8000/api/plantas/',
        'http://127.0.0.1:8000/api/departamentos/',
        'http://127.0.0.1:8000/api/puestos/',
        'http://127.0.0.1:8000/api/empleados/',
        'http://127.0.0.1:8000/api/usuarios-planta/',
    ]
    
    for endpoint in endpoints:
        try:
            response = requests.get(endpoint, headers=headers, timeout=5)
            print(f"✓ {endpoint} → {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                if isinstance(data, list):
                    print(f"  Elementos encontrados: {len(data)}")
                    
        except Exception as e:
            print(f"✗ {endpoint} → ERROR: {e}")

def main():
    print("DIAGNÓSTICO COMPLETO DEL SERVIDOR Y API")
    print("=" * 60)
    
    # Esperar un poco para que el servidor arranque
    print("Esperando 3 segundos para que el servidor arranque...")
    time.sleep(3)
    
    # 1. Verificar servidor
    if not test_servidor_basico():
        print("\n⚠ ADVERTENCIA: El servidor no está respondiendo.")
        print("   Ejecuta: python manage.py runserver")
        return
    
    # 2. Verificar rutas
    test_rutas_api()
    
    # 3. Probar login
    token = test_login_usuario_existente()
    
    # 4. Probar registro
    test_registro_empresa()
    
    # 5. Probar endpoints autenticados
    test_con_token(token)
    
    print("\n" + "=" * 60)
    print("DIAGNÓSTICO COMPLETADO")
    print("=" * 60)

if __name__ == '__main__':
    main()
