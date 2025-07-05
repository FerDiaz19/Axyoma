#!/usr/bin/env python
"""
Crear usuario de prueba específico para verificar frontend
"""
import os
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')
django.setup()

from django.contrib.auth.models import User
from apps.users.models import PerfilUsuario, Empresa, Planta

def crear_usuario_prueba():
    print("=== CREANDO USUARIO DE PRUEBA PARA FRONTEND ===")
    
    # Datos del usuario
    username = "admin_frontend_test"
    password = "frontend123"
    
    # Limpiar usuario anterior si existe
    try:
        user_anterior = User.objects.get(username=username)
        print(f"Eliminando usuario anterior: {username}")
        user_anterior.delete()
    except User.DoesNotExist:
        pass
    
    # Crear usuario
    user = User.objects.create_user(
        username=username,
        email='frontend@test.com',
        password=password
    )
    
    # Crear perfil
    perfil = PerfilUsuario.objects.create(
        user=user,
        nombre='Admin',
        apellido_paterno='Frontend',
        apellido_materno='Test',
        correo='frontend@test.com',
        nivel_usuario='admin-empresa'
    )
    
    # Crear empresa
    empresa = Empresa.objects.create(
        nombre='Empresa Frontend Test',
        rfc='FRONTEND123',
        direccion='Dirección Frontend Test',
        email_contacto='frontend@test.com',
        telefono_contacto='555-FRONT',
        administrador=perfil
    )
    
    # Crear 2 plantas para la empresa
    planta1 = Planta.objects.create(
        nombre='Planta Frontend 1',
        direccion='Dirección Planta 1',
        empresa=empresa
    )
    
    planta2 = Planta.objects.create(
        nombre='Planta Frontend 2',
        direccion='Dirección Planta 2',
        empresa=empresa
    )
    
    print(f"✅ Usuario creado: {username}")
    print(f"✅ Password: {password}")
    print(f"✅ Empresa creada: {empresa.nombre} (ID: {empresa.empresa_id})")
    print(f"✅ Plantas creadas:")
    print(f"   - {planta1.nombre} (ID: {planta1.planta_id})")
    print(f"   - {planta2.nombre} (ID: {planta2.planta_id})")
    
    return {
        'username': username,
        'password': password,
        'empresa_id': empresa.empresa_id,
        'plantas': [planta1.planta_id, planta2.planta_id]
    }

def verificar_plantas_backend(username, password):
    print(f"\n=== VERIFICANDO PLANTAS DESDE BACKEND ===")
    import requests
    
    # Login
    login_data = {'username': username, 'password': password}
    response = requests.post('http://127.0.0.1:8000/api/auth/login/', json=login_data)
    
    if response.status_code != 200:
        print(f"❌ Error en login: {response.text}")
        return
    
    token = response.json().get('token')
    print(f"✅ Login exitoso - Token: {token[:20]}...")
    
    # Obtener plantas
    headers = {'Authorization': f'Token {token}'}
    response = requests.get('http://127.0.0.1:8000/api/plantas/', headers=headers)
    
    if response.status_code == 200:
        plantas = response.json()
        print(f"✅ Plantas desde backend: {len(plantas)}")
        for planta in plantas:
            print(f"   - {planta['nombre']} (ID: {planta['planta_id']})")
    else:
        print(f"❌ Error obteniendo plantas: {response.text}")

if __name__ == '__main__':
    # Crear usuario de prueba
    datos = crear_usuario_prueba()
    
    # Verificar desde backend
    verificar_plantas_backend(datos['username'], datos['password'])
    
    print(f"\n🎯 PARA PROBAR EN FRONTEND:")
    print(f"   Username: {datos['username']}")
    print(f"   Password: {datos['password']}")
    print(f"   Deberías ver {len(datos['plantas'])} plantas en el dashboard")
