#!/usr/bin/env python
import os
import django
from django.conf import settings

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')
django.setup()

from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from apps.users.models import PerfilUsuario, Empresa

print("🔍 DIAGNÓSTICO COMPLETO - USUARIO AXIS")
print("=" * 60)

# Buscar el usuario axis
try:
    user_axis = User.objects.get(username='axis')
    print(f"✅ Usuario 'axis' encontrado")
    print(f"   📧 Email: {user_axis.email}")
    print(f"   🔑 is_active: {user_axis.is_active}")
    print(f"   📅 Último login: {user_axis.last_login}")
    print(f"   📅 Fecha registro: {user_axis.date_joined}")
    
    # Verificar perfil
    if hasattr(user_axis, 'perfil'):
        perfil = user_axis.perfil
        print(f"   📋 Perfil encontrado")
        print(f"   👤 Nombre: {perfil.nombre} {perfil.apellido_paterno}")
        print(f"   🎯 Nivel usuario: {perfil.nivel_usuario}")
        print(f"   📧 Correo perfil: {perfil.correo}")
        
        # Si es admin-empresa, verificar su empresa
        if perfil.nivel_usuario == 'admin-empresa':
            try:
                empresa = Empresa.objects.get(administrador=perfil)
                print(f"   🏢 Empresa: {empresa.nombre}")
                print(f"   🆔 Empresa ID: {empresa.empresa_id}")
                print(f"   🔄 Empresa status: {empresa.status}")
                print(f"   📧 Empresa email: {empresa.email_contacto}")
                
                if not empresa.status:
                    print("   ⚠️ EMPRESA SUSPENDIDA - Esta es la causa del problema")
                else:
                    print("   ✅ Empresa activa")
                    
            except Empresa.DoesNotExist:
                print("   ❌ ERROR: Usuario admin-empresa sin empresa asignada")
    else:
        print("   ❌ ERROR: Usuario sin perfil")
        
    # Probar autenticación Django
    print(f"\n🧪 Probando autenticación Django...")
    auth_user = authenticate(username='axis', password='123')
    if auth_user:
        print("   ✅ Autenticación Django exitosa")
    else:
        print("   ❌ Autenticación Django fallida")
        
        # Probar con diferentes contraseñas comunes
        passwords_to_try = ['123', 'password123', 'admin123', '1234']
        for pwd in passwords_to_try:
            test_auth = authenticate(username='axis', password=pwd)
            if test_auth:
                print(f"   ✅ Autenticación exitosa con contraseña: {pwd}")
                break
        else:
            print("   ❌ No se pudo autenticar con ninguna contraseña común")
        
except User.DoesNotExist:
    print("❌ Usuario 'axis' NO encontrado en la base de datos")
    print("\n📊 Usuarios disponibles:")
    for user in User.objects.all()[:10]:
        print(f"   - {user.username} ({user.email})")

print(f"\n{'='*60}")
print("🔍 VERIFICANDO LÓGICA DE LOGIN EN VIEWS.PY")

# Simular el proceso de login paso a paso
print("\n1️⃣ Verificando que el usuario exista y tenga perfil...")
try:
    user = User.objects.get(username='axis')
    if hasattr(user, 'perfil'):
        profile = user.perfil
        print(f"   ✅ Usuario y perfil encontrados")
        
        print("\n2️⃣ Verificando nivel de usuario...")
        print(f"   Nivel: {profile.nivel_usuario}")
        
        if profile.nivel_usuario == 'admin-empresa':
            print("\n3️⃣ Verificando empresa asignada...")
            try:
                empresa = Empresa.objects.get(administrador=profile)
                print(f"   ✅ Empresa encontrada: {empresa.nombre}")
                print(f"   Status: {empresa.status}")
                
                print("\n4️⃣ Analizando respuesta que debería generar el login...")
                response_data = {
                    'message': 'Login exitoso',
                    'usuario': user.username,
                    'nivel_usuario': profile.nivel_usuario,
                    'empresa_id': empresa.empresa_id,
                    'nombre_empresa': empresa.nombre,
                    'empresa_suspendida': not empresa.status,
                }
                
                if not empresa.status:
                    response_data['advertencia'] = {
                        'tipo': 'empresa_suspendida',
                        'mensaje': 'Su empresa se encuentra suspendida. Las funcionalidades están limitadas.',
                        'detalles': 'Para reactivar su suscripción, contacte con soporte.'
                    }
                
                print(f"   📋 Respuesta esperada:")
                import json
                print(json.dumps(response_data, indent=4, ensure_ascii=False))
                
                print(f"\n💡 CONCLUSIÓN:")
                if empresa.status:
                    print("   ✅ La empresa está ACTIVA - El login debería funcionar normalmente")
                else:
                    print("   ⚠️ La empresa está SUSPENDIDA - El login debería funcionar pero con advertencias")
                    
            except Empresa.DoesNotExist:
                print("   ❌ ERROR: admin-empresa sin empresa asignada")
                print("   🚨 ESTE ES EL PROBLEMA - El views.py retornará error 400")
                
    else:
        print("   ❌ Usuario sin perfil")
        
except User.DoesNotExist:
    print("   ❌ Usuario no encontrado")
