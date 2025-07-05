#!/usr/bin/env python
"""
Script para actualizar usuarios de planta existentes con contraseñas temporales
"""
import os
import django
import string
import random

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')
django.setup()

from apps.users.models import AdminPlanta

def generar_password():
    """Genera una contraseña temporal"""
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(12))

def actualizar_passwords_existentes():
    print("=== ACTUALIZANDO CONTRASEÑAS DE USUARIOS EXISTENTES ===")
    
    admin_plantas = AdminPlanta.objects.filter(password_temporal__isnull=True)
    
    if not admin_plantas.exists():
        print("✅ Todos los usuarios ya tienen contraseñas temporales asignadas")
        return
    
    print(f"📝 Actualizando {admin_plantas.count()} usuarios...")
    
    for admin_planta in admin_plantas:
        password_temporal = generar_password()
        admin_planta.password_temporal = password_temporal
        admin_planta.save()
        
        # También actualizar la contraseña real del usuario
        user = admin_planta.usuario.user
        user.set_password(password_temporal)
        user.save()
        
        print(f"✅ {admin_planta.planta.nombre} -> Usuario: {user.username} -> Password: {password_temporal}")
    
    print(f"\n🎉 ¡{admin_plantas.count()} usuarios actualizados correctamente!")

if __name__ == '__main__':
    actualizar_passwords_existentes()
