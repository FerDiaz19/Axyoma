#!/usr/bin/env python
"""
Crear/corregir usuario axis con credenciales correctas
"""
import os
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')
django.setup()

from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from apps.users.models import PerfilUsuario, Empresa

print("🔧 CREANDO/CORRIGIENDO USUARIO AXIS")
print("=" * 50)

try:
    # Intentar obtener el usuario axis
    try:
        user = User.objects.get(username='axis')
        print(f"✅ Usuario 'axis' encontrado")
    except User.DoesNotExist:
        print("❌ Usuario 'axis' no existe - creándolo...")
        user = User.objects.create_user(
            username='axis',
            email='axis@gmail.com',
            password='123',
            first_name='Axis',
            last_name='User'
        )
        print("✅ Usuario 'axis' creado")

    # Asegurar que esté activo
    user.is_active = True
    user.set_password('123')  # Establecer contraseña explícitamente
    user.save()
    print(f"✅ Usuario activado y contraseña establecida")

    # Verificar autenticación inmediatamente
    auth_test = authenticate(username='axis', password='123')
    if auth_test:
        print("✅ Autenticación con Django: EXITOSA")
    else:
        print("❌ Autenticación con Django: FALLIDA")
        
        # Intentar con diferentes métodos
        print("🔄 Intentando con diferentes configuraciones...")
        
        # Método 1: Cambiar contraseña directamente
        user.set_password('123')
        user.save()
        
        # Método 2: Verificar que no hay espacios
        test_passwords = ['123', ' 123', '123 ', ' 123 ']
        for pwd in test_passwords:
            user.set_password(pwd.strip())
            user.save()
            auth_test = authenticate(username='axis', password=pwd.strip())
            if auth_test:
                print(f"✅ Autenticación exitosa con: '{pwd.strip()}'")
                break
        else:
            print("❌ No se pudo establecer autenticación")

    # Verificar/crear perfil
    try:
        perfil = user.perfil
        print(f"✅ Perfil encontrado: {perfil.nivel_usuario}")
    except:
        print("❌ Perfil no encontrado - creándolo...")
        perfil = PerfilUsuario.objects.create(
            user=user,
            nombre='Axis',
            apellido_paterno='User',
            correo='axis@gmail.com',
            nivel_usuario='admin-empresa'
        )
        print("✅ Perfil creado")

    # Verificar/crear empresa
    try:
        empresa = Empresa.objects.get(administrador=perfil)
        print(f"✅ Empresa encontrada: {empresa.nombre}")
    except:
        print("❌ Empresa no encontrada - creándola...")
        empresa = Empresa.objects.create(
            nombre='Axis Company',
            rfc='AXIS123456789',
            direccion='Calle Axis 123',
            telefono_contacto='1234567890',
            email_contacto='axis@gmail.com',
            administrador=perfil,
            status=True
        )
        print("✅ Empresa creada")

    # Verificar estado final
    print(f"\n📊 ESTADO FINAL:")
    print(f"   Usuario: {user.username}")
    print(f"   Email: {user.email}")
    print(f"   Activo: {user.is_active}")
    print(f"   Perfil: {perfil.nivel_usuario}")
    print(f"   Empresa: {empresa.nombre}")
    print(f"   Empresa activa: {empresa.status}")

    # Prueba final de autenticación
    final_auth = authenticate(username='axis', password='123')
    if final_auth:
        print(f"\n✅ AUTENTICACIÓN FINAL: EXITOSA")
        print(f"🎯 Credenciales confirmadas:")
        print(f"   Usuario: axis")
        print(f"   Contraseña: 123")
    else:
        print(f"\n❌ AUTENTICACIÓN FINAL: FALLIDA")
        
        # Última tentativa con contraseña alternativa
        user.set_password('password123')
        user.save()
        alt_auth = authenticate(username='axis', password='password123')
        if alt_auth:
            print(f"✅ Autenticación exitosa con contraseña alternativa")
            print(f"🎯 Credenciales finales:")
            print(f"   Usuario: axis")
            print(f"   Contraseña: password123")
        else:
            print(f"❌ No se pudo establecer autenticación")

except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()

print(f"\n{'='*50}")
print("🎯 INTENTA HACER LOGIN AHORA")
print("=" * 50)
