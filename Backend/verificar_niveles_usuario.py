#!/usr/bin/env python3
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')
django.setup()

from apps.users.models import PerfilUsuario
from django.contrib.auth.models import User

print("🔍 VERIFICANDO NIVELES DE USUARIO EN LA BASE DE DATOS")
print("=" * 60)

# Obtener todos los usuarios
usuarios = User.objects.all()
print(f"Total usuarios Django: {usuarios.count()}")

# Obtener todos los perfiles
perfiles = PerfilUsuario.objects.all()
print(f"Total perfiles de usuario: {perfiles.count()}")

print("\n📋 LISTA DE USUARIOS Y SUS NIVELES:")
print("-" * 60)

for usuario in usuarios:
    try:
        perfil = PerfilUsuario.objects.get(correo=usuario.email)
        print(f"✅ {usuario.username} ({usuario.email})")
        print(f"   - Nivel: '{perfil.nivel_usuario}'")
        print(f"   - Activo: {perfil.status}")
        print(f"   - Superuser: {usuario.is_superuser}")
        print()
    except PerfilUsuario.DoesNotExist:
        print(f"⚠️  {usuario.username} ({usuario.email}) - SIN PERFIL")
        print(f"   - Superuser: {usuario.is_superuser}")
        print()

print("\n🎯 RESUMEN DE NIVELES:")
print("-" * 30)
niveles = {}
for perfil in perfiles:
    nivel = perfil.nivel_usuario
    if nivel in niveles:
        niveles[nivel] += 1
    else:
        niveles[nivel] = 1

for nivel, cantidad in niveles.items():
    print(f"'{nivel}': {cantidad} usuario(s)")

# Verificar opciones válidas en el modelo
print(f"\n📝 OPCIONES VÁLIDAS SEGÚN EL MODELO:")
print("-" * 40)
for choice in PerfilUsuario.NIVEL_CHOICES:
    print(f"'{choice[0]}': {choice[1]}")
