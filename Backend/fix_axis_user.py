#!/usr/bin/env python
import os
import django
from django.conf import settings

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')
django.setup()

from django.contrib.auth.models import User
from apps.users.models import Empresa

print("🔧 REPARANDO USUARIO AXIS")
print("=" * 40)

try:
    # Obtener el usuario axis
    user_axis = User.objects.get(username='axis')
    
    print(f"📊 Estado actual:")
    print(f"   Usuario: {user_axis.username}")
    print(f"   is_active: {user_axis.is_active}")
    
    # Activar el usuario
    if not user_axis.is_active:
        user_axis.is_active = True
        user_axis.save()
        print(f"✅ Usuario activado exitosamente")
    else:
        print(f"ℹ️ Usuario ya estaba activo")
    
    # Verificar empresa
    empresa = Empresa.objects.get(administrador=user_axis.perfil)
    print(f"🏢 Empresa: {empresa.nombre}")
    print(f"   Status: {empresa.status}")
    
    print(f"\n🧪 Ahora probemos el login...")
    from django.contrib.auth import authenticate
    
    auth_user = authenticate(username='axis', password='123')
    if auth_user:
        print("✅ Autenticación exitosa!")
        print("🎯 El usuario 'axis' ahora puede hacer login")
    else:
        print("❌ Autenticación aún falla")
        print("💡 Puede ser problema de contraseña")
        
        # Cambiar contraseña para asegurar que funcione
        user_axis.set_password('123')
        user_axis.save()
        print("🔑 Contraseña restablecida a '123'")
        
        # Probar de nuevo
        auth_user2 = authenticate(username='axis', password='123')
        if auth_user2:
            print("✅ Autenticación exitosa después de restablecer contraseña!")
        else:
            print("❌ Autenticación aún falla - revisar configuración")
    
except User.DoesNotExist:
    print("❌ Usuario 'axis' no encontrado")
except Exception as e:
    print(f"❌ Error: {e}")

print(f"\n{'='*40}")
print("✅ REPARACIÓN COMPLETADA")
print("💡 Intenta hacer login nuevamente con: axis / 123")
