#!/usr/bin/env python
"""
Script simple para verificar el estado del usuario axis
"""
import os
import django
import sys

try:
    # Configurar Django
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')
    django.setup()

    from django.contrib.auth.models import User
    from django.contrib.auth import authenticate
    from apps.users.models import Empresa

    print("🔍 VERIFICACIÓN FINAL - USUARIO AXIS")
    print("=" * 45)

    # Verificar usuario
    user = User.objects.get(username='axis')
    print(f"✅ Usuario: {user.username}")
    print(f"📧 Email: {user.email}")
    print(f"🔑 Activo: {user.is_active}")

    # Verificar autenticación
    auth_user = authenticate(username='axis', password='123')
    if auth_user:
        print("✅ Autenticación: EXITOSA")
        
        # Verificar empresa
        empresa = Empresa.objects.get(administrador=auth_user.perfil)
        print(f"🏢 Empresa: {empresa.nombre}")
        print(f"🔄 Estado: {'Activa' if empresa.status else 'Suspendida'}")
        
        print(f"\n🎯 RESULTADO:")
        print("✅ El usuario 'axis' PUEDE hacer login")
        if empresa.status:
            print("✅ Con empresa activa - Login normal")
        else:
            print("⚠️ Con empresa suspendida - Login con advertencias")
            
    else:
        print("❌ Autenticación: FALLIDA")
        print("🔧 Necesita reparación")

except Exception as e:
    print(f"❌ Error: {e}")
    sys.exit(1)

print(f"\n{'='*45}")
print("💡 PRUEBA AHORA EN EL FRONTEND:")
print("   Usuario: axis")
print("   Contraseña: 123")
