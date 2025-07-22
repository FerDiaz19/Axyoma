#!/usr/bin/env python
"""
Script para limpiar usuarios innecesarios de la BD
"""

import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')
django.setup()

from django.contrib.auth.models import User
from apps.users.models import PerfilUsuario
from django.db import transaction

def limpiar_usuarios():
    """Limpiar usuarios innecesarios"""
    
    print("🧹 Limpiando usuarios innecesarios...")
    
    try:
        with transaction.atomic():
            print("=== USUARIOS ANTES ===")
            print(f"Users Django: {User.objects.count()}")
            print(f"Perfiles: {PerfilUsuario.objects.count()}")
            
            # Mostrar usuarios actuales
            print("\nUsuarios actuales:")
            for user in User.objects.all():
                perfil = getattr(user, 'perfil', None)
                nivel = perfil.nivel_usuario if perfil else 'Sin perfil'
                print(f"- {user.username} ({nivel})")
            
            # Eliminar usuarios duplicados manteniendo solo esenciales
            usuarios_a_mantener = []
            
            # Mantener superadmin
            superadmins = User.objects.filter(is_superuser=True)
            for sa in superadmins:
                usuarios_a_mantener.append(sa.id)
                print(f"✅ Manteniendo superadmin: {sa.username}")
            
            # Mantener un admin por empresa
            empresas_vistas = set()
            for perfil in PerfilUsuario.objects.filter(nivel_usuario='admin-empresa').select_related('user'):
                if perfil.user and hasattr(perfil, 'empresa') and perfil.empresa:
                    empresa_id = perfil.empresa.empresa_id
                    if empresa_id not in empresas_vistas:
                        usuarios_a_mantener.append(perfil.user.id)
                        empresas_vistas.add(empresa_id)
                        print(f"✅ Manteniendo admin empresa: {perfil.user.username}")
                    else:
                        print(f"❌ Eliminando admin empresa duplicado: {perfil.user.username}")
            
            # Eliminar usuarios no esenciales
            usuarios_eliminados = 0
            for user in User.objects.all():
                if user.id not in usuarios_a_mantener:
                    print(f"❌ Eliminando usuario: {user.username}")
                    try:
                        user.delete()
                        usuarios_eliminados += 1
                    except Exception as e:
                        print(f"   Error eliminando {user.username}: {str(e)}")
            
            print(f"\n=== USUARIOS DESPUÉS ===")
            print(f"Users Django: {User.objects.count()}")
            print(f"Perfiles: {PerfilUsuario.objects.count()}")
            print(f"Usuarios eliminados: {usuarios_eliminados}")
            
            print("\nUsuarios restantes:")
            for user in User.objects.all():
                perfil = getattr(user, 'perfil', None)
                nivel = perfil.nivel_usuario if perfil else 'Sin perfil'
                print(f"- {user.username} ({nivel})")
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    limpiar_usuarios()
