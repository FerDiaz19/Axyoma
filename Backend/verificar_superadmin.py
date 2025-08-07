#!/usr/bin/env python
import os
import django
import sys

# Setup Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')
django.setup()

from django.contrib.auth.models import User
from apps.users.models import PerfilUsuario

def verificar_usuario_superadmin():
    print("🔍 Verificando usuario SuperAdmin...")
    
    try:
        # Buscar todos los usuarios superuser
        superusers = User.objects.filter(is_superuser=True)
        print(f"📊 Encontrados {superusers.count()} superusers:")
        
        for user in superusers:
            print(f"\n👤 Usuario: {user.username} (ID: {user.id})")
            print(f"   - Email: {user.email}")
            print(f"   - Activo: {user.is_active}")
            print(f"   - Staff: {user.is_staff}")
            print(f"   - Superuser: {user.is_superuser}")
            
            # Verificar perfil
            if hasattr(user, 'perfil'):
                perfil = user.perfil
                print(f"   ✅ Tiene perfil: {perfil.nombre} {perfil.apellido_paterno}")
                print(f"   - Nivel usuario: {perfil.nivel_usuario}")
                print(f"   - Status: {perfil.status}")
                
                if perfil.nivel_usuario == 'superadmin':
                    print(f"   ✅ Usuario válido para SuperAdmin!")
                else:
                    print(f"   ❌ Nivel incorrecto. Esperado: 'superadmin', Actual: '{perfil.nivel_usuario}'")
            else:
                print(f"   ❌ No tiene perfil asociado")
                
        # Buscar perfiles con nivel_usuario = superadmin
        print(f"\n🔍 Buscando perfiles SuperAdmin...")
        superadmin_perfiles = PerfilUsuario.objects.filter(nivel_usuario='superadmin')
        print(f"📊 Encontrados {superadmin_perfiles.count()} perfiles SuperAdmin:")
        
        for perfil in superadmin_perfiles:
            print(f"\n👤 Perfil: {perfil.nombre} {perfil.apellido_paterno}")
            print(f"   - Email: {perfil.correo}")
            print(f"   - Status: {perfil.status}")
            if perfil.user_id:
                print(f"   - Usuario asociado: {perfil.user_id.username}")
            else:
                print(f"   ❌ Sin usuario asociado")
                
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    verificar_usuario_superadmin()
