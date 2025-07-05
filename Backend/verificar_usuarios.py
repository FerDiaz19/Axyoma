#!/usr/bin/env python
"""
Script para verificar usuarios disponibles
"""
import os
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')
django.setup()

from django.contrib.auth.models import User
from apps.users.models import PerfilUsuario, Empresa, Planta

def verificar_usuarios():
    print("👤 USUARIOS DISPONIBLES")
    print("="*40)
    
    # Verificar usuarios Django
    users = User.objects.all()
    print(f"Total de usuarios Django: {users.count()}")
    
    for user in users:
        print(f"\n🔸 Usuario: {user.username}")
        print(f"   Email: {user.email}")
        print(f"   Activo: {user.is_active}")
        
        # Verificar perfil
        try:
            perfil = user.perfil
            print(f"   Perfil: {perfil.nombre} {perfil.apellido_paterno}")
            print(f"   Nivel: {perfil.nivel_usuario}")
            print(f"   Contraseña (model): {perfil.contrasena}")
            
            # Si es admin de empresa, ver empresa
            if perfil.nivel_usuario == 'admin-empresa':
                try:
                    empresa = Empresa.objects.get(administrador=perfil)
                    print(f"   Empresa: {empresa.nombre}")
                    
                    # Ver plantas de la empresa
                    plantas = Planta.objects.filter(empresa=empresa)
                    print(f"   Plantas: {plantas.count()}")
                    for planta in plantas:
                        print(f"     - {planta.nombre}")
                        
                except Empresa.DoesNotExist:
                    print("   Sin empresa asignada")
                    
        except Exception as e:
            print(f"   Sin perfil: {e}")

if __name__ == "__main__":
    verificar_usuarios()
