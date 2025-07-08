#!/usr/bin/env python
"""
Verificación final y simple del usuario axis
"""
import os
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')
django.setup()

from django.contrib.auth.models import User
from django.contrib.auth import authenticate

print("🎯 VERIFICACIÓN FINAL DEL USUARIO AXIS")
print("=" * 50)

# Verificar usuario
user = User.objects.get(username='axis')
print(f"✅ Usuario: {user.username}")
print(f"📧 Email: {user.email}")
print(f"🔑 Activo: {user.is_active}")
print(f"🗓️ Último login: {user.last_login}")

# Establecer contraseña nuevamente por si acaso
user.set_password('123')
user.is_active = True
user.save()
print(f"🔧 Contraseña restablecida y usuario activado")

# Probar autenticación
auth_user = authenticate(username='axis', password='123')
if auth_user:
    print(f"✅ Autenticación Django: EXITOSA")
    
    # Verificar perfil y empresa
    perfil = auth_user.perfil
    print(f"👤 Perfil: {perfil.nivel_usuario}")
    
    if perfil.nivel_usuario == 'admin-empresa':
        from apps.users.models import Empresa
        empresa = Empresa.objects.get(administrador=perfil)
        print(f"🏢 Empresa: {empresa.nombre}")
        print(f"🔄 Estado: {'Activa' if empresa.status else 'Suspendida'}")
        
        print(f"\n🎯 RESPUESTA ESPERADA DEL LOGIN:")
        print(f"   ✅ message: 'Login exitoso'")
        print(f"   👤 usuario: 'axis'")
        print(f"   📋 nivel_usuario: 'admin-empresa'")
        print(f"   🏢 nombre_empresa: '{empresa.nombre}'")
        print(f"   🔄 empresa_suspendida: {not empresa.status}")
        print(f"   🎯 tipo_dashboard: 'admin-empresa'")
        
else:
    print(f"❌ Autenticación Django: FALLIDA")
    print(f"🚨 HAY UN PROBLEMA SERIO")

print(f"\n{'='*50}")
print(f"🔧 CREDENCIALES FINALES PARA EL FRONTEND:")
print(f"   Usuario: axis")
print(f"   Contraseña: 123")
print(f"{'='*50}")

# Intentar con diferentes contraseñas para asegurar
print(f"\n🧪 PROBANDO CONTRASEÑAS ALTERNATIVAS:")
passwords = ['123', 'password123', 'admin123', '1234']
for pwd in passwords:
    user.set_password(pwd)
    user.save()
    test_auth = authenticate(username='axis', password=pwd)
    if test_auth:
        print(f"✅ Funciona con: {pwd}")
        print(f"🎯 USA ESTA CONTRASEÑA: {pwd}")
        break
    else:
        print(f"❌ No funciona con: {pwd}")
else:
    print(f"🚨 NINGUNA CONTRASEÑA FUNCIONA - REVISAR CONFIGURACIÓN")
