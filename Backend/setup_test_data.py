#!/usr/bin/env python
import os
import sys
import django

# Setup Django
sys.path.insert(0, 'c:/xampp2/htdocs/UTT4B/Axyoma2/Backend')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')
django.setup()

from django.contrib.auth.models import User
from apps.users.models import PerfilUsuario, Empresa, Planta, AdminPlanta
from django.contrib.auth import authenticate

print("=== CREANDO DATOS DE PRUEBA ===")

try:
    # Limpiar datos de prueba anteriores
    print("Limpiando datos anteriores...")
    User.objects.filter(username__in=[
        'ed-rubio@axyoma.com',
        'juan.perez@codewave.com', 
        'maria.gomez@codewave.com',
        'carlos.ruiz@codewave.com'
    ]).delete()
    
    # Crear usuarios principales
    print("Creando usuarios...")
    user1 = User.objects.create_user(
        username='ed-rubio@axyoma.com',
        email='ed-rubio@axyoma.com',
        password='1234'
    )
    user2 = User.objects.create_user(
        username='juan.perez@codewave.com', 
        email='juan.perez@codewave.com',
        password='1234'
    )
    user3 = User.objects.create_user(
        username='maria.gomez@codewave.com',
        email='maria.gomez@codewave.com', 
        password='1234'
    )
    print(f"Usuarios creados: {User.objects.filter(username__contains='@').count()}")
    
    # Crear perfiles
    print("Creando perfiles...")
    perfil1 = PerfilUsuario.objects.create(
        user=user1,
        nombre='Ed',
        apellido_paterno='Rubio',
        correo='ed-rubio@axyoma.com',
        nivel_usuario='superadmin'
    )
    print(f"Perfil superadmin creado: {perfil1}")
    
    perfil2 = PerfilUsuario.objects.create(
        user=user2,
        nombre='Juan',
        apellido_paterno='Perez', 
        correo='juan.perez@codewave.com',
        nivel_usuario='admin-empresa'
    )
    print(f"Perfil admin-empresa creado: {perfil2}")
    
    perfil3 = PerfilUsuario.objects.create(
        user=user3,
        nombre='Maria',
        apellido_paterno='Gomez',
        correo='maria.gomez@codewave.com', 
        nivel_usuario='admin-planta',
        admin_empresa=perfil2
    )
    print(f"Perfil admin-planta creado: {perfil3}")
    
    # Crear empresa
    print("Creando empresa...")
    empresa = Empresa.objects.create(
        nombre='CodeWave Solutions',
        rfc='CWS123456ABC',
        direccion='Av. Tecnología 123',
        administrador=perfil2
    )
    print(f"Empresa creada: {empresa}")
    
    # Crear planta
    print("Creando planta...")
    planta = Planta.objects.create(
        nombre='Oficina Principal',
        direccion='Av. Tecnología 123',
        empresa=empresa
    )
    print(f"Planta creada: {planta}")
    
    # Asignar admin a planta
    print("Asignando admin a planta...")
    admin_planta = AdminPlanta.objects.create(
        usuario=perfil3,
        planta=planta
    )
    print(f"Admin-planta asignado: {admin_planta}")
    
    print("\n=== PROBANDO AUTENTICACIÓN ===")
    test_users = [
        ('ed-rubio@axyoma.com', '1234'),
        ('juan.perez@codewave.com', '1234'), 
        ('maria.gomez@codewave.com', '1234')
    ]
    
    for username, password in test_users:
        user = authenticate(username=username, password=password)
        if user and hasattr(user, 'perfil'):
            print(f"✅ {username} - {user.perfil.nivel_usuario}")
        elif user:
            print(f"❌ {username} - Usuario autenticado pero sin perfil")
        else:
            print(f"❌ {username} - Fallo de autenticación")
    
    print("\n✅ Datos de prueba creados exitosamente!")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
