#!/usr/bin/env python
import os
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')
django.setup()

from apps.users.models import PerfilUsuario

print("🔍 VERIFICANDO USUARIOS SUPERADMIN Y SUS CREDENCIALES...")
usuarios_superadmin = PerfilUsuario.objects.filter(nivel_usuario='superadmin')

print(f"Encontrados {usuarios_superadmin.count()} usuarios SuperAdmin:")
for perfil in usuarios_superadmin[:10]:  # Solo primeros 10
    print(f"- ID: {perfil.id}")
    print(f"  Nombre: {perfil.nombre} {perfil.apellido_paterno}")
    print(f"  Email: {perfil.correo}")
    
    # Buscar si tiene password_temporal
    if hasattr(perfil, 'password_temporal') and perfil.password_temporal:
        print(f"  Password temporal: {perfil.password_temporal}")
    
    # Buscar información adicional si existe
    try:
        print(f"  Status: {'Activo' if perfil.status else 'Inactivo'}")
    except:
        pass
    print()

# También buscar en la tabla de Django User si existe algún superuser
from django.contrib.auth.models import User
superusers = User.objects.filter(is_superuser=True)
if superusers.exists():
    print("🔑 USUARIOS DJANGO SUPERUSER:")
    for user in superusers:
        print(f"- Username: {user.username}")
        print(f"  Email: {user.email}")
        print(f"  Active: {user.is_active}")
        print()
