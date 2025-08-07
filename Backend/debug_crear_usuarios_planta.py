#!/usr/bin/env python3
"""
Script para diagnosticar la creación de usuarios de planta
"""
import os
import sys
import django
import traceback

# Configuración de Django
sys.path.append('.')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from apps.users.models import PerfilUsuario, Empresa, Planta, AdminPlanta
import random
import string

def crear_usuario_planta_debug(planta, empresa):
    """Crear usuario para planta con debug completo"""
    print(f"🛠️ Creando usuario para planta: {planta.nombre}")
    print(f"   🏢 Empresa: {empresa.nombre}")
    
    try:
        # 1. Generar username único
        base_username = f"admin_{planta.nombre.lower().replace(' ', '_').replace('-', '_')}"
        username = base_username
        contador = 1
        
        print(f"   🔤 Base username: {base_username}")
        
        while User.objects.filter(username=username).exists():
            print(f"   ⚠️ Username {username} ya existe")
            username = f"{base_username}_{contador}"
            contador += 1
        
        print(f"   ✅ Username único: {username}")
        
        # 2. Generar contraseña
        password = ''.join(random.choices(string.ascii_letters + string.digits, k=12))
        print(f"   🔑 Contraseña generada: {password}")
        
        # 3. Crear usuario Django
        email = f"{username}@{empresa.nombre.lower().replace(' ', '')}.com"
        print(f"   📧 Email: {email}")
        
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=f"Admin {planta.nombre}",
            last_name="Plant Manager"
        )
        print(f"   👤 Usuario Django creado: ID {user.id}")
        
        # 4. Crear perfil de usuario
        print(f"   🔄 Creando perfil para admin-empresa: {empresa.administrador.id}")
        
        perfil = PerfilUsuario.objects.create(
            user=user,
            nombre=f"Admin {planta.nombre}",
            apellido_paterno="Plant",
            apellido_materno="Manager",
            correo=email,
            nivel_usuario='admin-planta',
            admin_empresa=empresa.administrador
        )
        print(f"   👤 Perfil creado: ID {perfil.id}")
        
        # 5. Crear relación AdminPlanta
        admin_planta = AdminPlanta.objects.create(
            usuario=perfil,
            planta=planta,
            status=True
        )
        print(f"   🔗 Relación AdminPlanta creada: ID {admin_planta.id}")
        
        # 6. Crear token
        token = Token.objects.create(user=user)
        print(f"   🔑 Token creado: {token.key}")
        
        print(f"   ✅ ÉXITO: Usuario {username} creado completamente")
        print(f"   📊 Credenciales: {username} / {password}")
        
        return True
        
    except Exception as e:
        print(f"   ❌ ERROR: {str(e)}")
        traceback.print_exc()
        return False

def test_plantas_sin_admin():
    """Encontrar plantas sin administrador y crearles uno"""
    print("🔍 Buscando plantas sin administrador...")
    
    # Buscar plantas sin AdminPlanta
    plantas_sin_admin = []
    
    for planta in Planta.objects.filter(status=True):
        admin_count = AdminPlanta.objects.filter(planta=planta).count()
        if admin_count == 0:
            plantas_sin_admin.append(planta)
    
    print(f"📊 Plantas sin administrador: {len(plantas_sin_admin)}")
    
    for planta in plantas_sin_admin[:3]:  # Solo las primeras 3
        print(f"\n🏭 Planta: {planta.nombre} (ID: {planta.planta_id})")
        print(f"   🏢 Empresa: {planta.empresa.nombre}")
        
        # Crear usuario
        success = crear_usuario_planta_debug(planta, planta.empresa)
        
        if success:
            print(f"   ✅ Usuario creado exitosamente para {planta.nombre}")
        else:
            print(f"   ❌ Falló la creación de usuario para {planta.nombre}")

if __name__ == "__main__":
    test_plantas_sin_admin()
