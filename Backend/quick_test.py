#!/usr/bin/env python
import os
import sys
import django

# Setup Django
sys.path.insert(0, 'c:/xampp2/htdocs/UTT4B/Axyoma2/Backend')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')
django.setup()

from django.contrib.auth.models import User
from apps.users.models import PerfilUsuario

print("Creating test user for login...")

# Limpiar usuario anterior si existe
User.objects.filter(username='ed-rubio@axyoma.com').delete()

# Crear usuario de prueba
user = User.objects.create_user(
    username='ed-rubio@axyoma.com',
    email='ed-rubio@axyoma.com', 
    password='1234',
    first_name='Ed',
    last_name='Rubio'
)

print(f"User created: {user.username}")

# Crear perfil
perfil = PerfilUsuario.objects.create(
    user=user,
    nombre='Ed',
    apellido_paterno='Rubio',
    correo='ed-rubio@axyoma.com',
    nivel_usuario='superadmin'
)

print(f"Profile created: {perfil.nombre} - {perfil.nivel_usuario}")

# Probar autenticación
from django.contrib.auth import authenticate
auth_user = authenticate(username='ed-rubio@axyoma.com', password='1234')

if auth_user and hasattr(auth_user, 'perfil'):
    print(f"✅ Authentication successful: {auth_user.perfil.nivel_usuario}")
else:
    print("❌ Authentication failed")

print("Done!")
