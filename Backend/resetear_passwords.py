#!/usr/bin/env python
"""
Script para resetear contraseñas de usuarios de prueba
"""
import os
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')
django.setup()

from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from apps.users.models import PerfilUsuario

def resetear_passwords():
    print("🔑 RESETEANDO CONTRASEÑAS")
    print("="*40)
    
    # Usuarios y sus nuevas contraseñas
    usuarios_passwords = [
        ("ed-rubio@axyoma.com", "123456"),
        ("juan.perez@codewave.com", "123456"),
        ("maria.gomez@codewave.com", "123456"),
        ("carlos.ruiz@codewave.com", "123456"),
    ]
    
    for username, password in usuarios_passwords:
        try:
            user = User.objects.get(username=username)
            user.set_password(password)
            user.save()
            print(f"✅ Contraseña actualizada para {username}")
        except User.DoesNotExist:
            print(f"❌ Usuario {username} no encontrado")
        except Exception as e:
            print(f"❌ Error actualizando {username}: {e}")

if __name__ == "__main__":
    resetear_passwords()
