#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')
django.setup()

from django.contrib.auth.models import User
from apps.users.models import PerfilUsuario, Empresa

print("=== VERIFICACIÓN DE USUARIOS ===")

# Buscar admin_empresa_1
user = User.objects.filter(username='admin_empresa_1').first()
if user:
    print(f"✅ Usuario admin_empresa_1 existe")
    print(f"   Email: {user.email}")
    print(f"   Activo: {user.is_active}")
    
    if hasattr(user, 'perfil'):
        perfil = user.perfil
        print(f"   Nivel: {perfil.nivel_usuario}")
        
        try:
            empresa = Empresa.objects.get(administrador=perfil)
            print(f"   Empresa: {empresa.nombre}")
        except Empresa.DoesNotExist:
            print(f"   ⚠️ Sin empresa asignada")
    else:
        print(f"   ⚠️ Sin perfil")
else:
    print("❌ Usuario admin_empresa_1 NO existe")
    
    # Mostrar usuarios disponibles
    print("\n📋 Usuarios disponibles:")
    for u in User.objects.all()[:10]:
        print(f"   - {u.username}")

print(f"\nTotal usuarios: {User.objects.count()}")
print(f"Total empresas: {Empresa.objects.count()}")
