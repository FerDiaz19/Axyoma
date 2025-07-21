#!/usr/bin/env python
import os
import sys
import django

# Configurar Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')
django.setup()

from django.contrib.auth.models import User
from apps.users.models import PerfilUsuario, Empresa

def mostrar_usuarios():
    print("👥 USUARIOS DEL SISTEMA")
    print("=" * 60)
    
    # Mostrar todos los usuarios
    users = User.objects.all()
    for user in users:
        print(f"\n🆔 ID: {user.id}")
        print(f"👤 Username: {user.username}")
        print(f"📧 Email: {user.email}")
        print(f"👨‍💼 Nombre: {user.first_name} {user.last_name}")
        print(f"🔐 Es superuser: {user.is_superuser}")
        print(f"🛡️ Es staff: {user.is_staff}")
        
        # Verificar si tiene perfil
        try:
            perfil = PerfilUsuario.objects.get(correo=user.email)
            print(f"📋 Nivel: {perfil.nivel_usuario}")
            print(f"✅ Status: {perfil.status}")
        except PerfilUsuario.DoesNotExist:
            print("❌ Sin perfil asociado")
        
        # Verificar si es admin de empresa
        try:
            if hasattr(user, 'email') and user.email:
                perfil = PerfilUsuario.objects.get(correo=user.email)
                empresas = Empresa.objects.filter(administrador=perfil)
                if empresas.exists():
                    for empresa in empresas:
                        print(f"🏢 Admin de empresa: {empresa.nombre}")
        except:
            pass
        
        print("-" * 40)

if __name__ == "__main__":
    mostrar_usuarios()
