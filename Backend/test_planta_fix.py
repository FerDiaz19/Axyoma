#!/usr/bin/env python3
"""
Test para crear planta con credenciales después del fix
"""
import os
import sys
import django

# Configuración de Django  
sys.path.append('.')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.users.models import Planta, AdminPlanta, PerfilUsuario, Empresa
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
import random
import string

def test_crear_planta_completa():
    """Test completo de creación de planta con credenciales"""
    
    print("🧪 Probando creación de planta con credenciales...")
    
    # 1. Encontrar admin-empresa
    admin_empresa = PerfilUsuario.objects.filter(nivel_usuario='admin-empresa').first()
    if not admin_empresa:
        print("❌ No hay admin-empresa disponible")
        return
    
    print(f"👤 Admin empresa: {admin_empresa.nombre} (ID: {admin_empresa.id})")
    
    # 2. Obtener empresa
    empresa = Empresa.objects.filter(administrador=admin_empresa).first()
    if not empresa:
        print("❌ No se encontró empresa")
        return
        
    print(f"🏢 Empresa: {empresa.nombre} (ID: {empresa.empresa_id})")
    
    # 3. Crear planta
    try:
        planta = Planta.objects.create(
            nombre="Planta Test Fix",
            direccion="Dirección Test 123",
            empresa=empresa
        )
        print(f"✅ Planta creada: {planta.nombre} (ID: {planta.planta_id})")
        
        # 4. Crear usuario para la planta
        base_username = f"admin_{planta.nombre.lower().replace(' ', '_')}"
        username = base_username
        contador = 1
        
        while User.objects.filter(username=username).exists():
            username = f"{base_username}_{contador}"
            contador += 1
        
        password = ''.join(random.choices(string.ascii_letters + string.digits, k=12))
        
        # 5. Crear usuario Django
        user = User.objects.create_user(
            username=username,
            email=f"{username}@{empresa.nombre.lower().replace(' ', '')}.com",
            password=password,
            first_name=f"Admin {planta.nombre}",
            last_name="Plant Manager"
        )
        print(f"✅ Usuario Django creado: {username}")
        
        # 6. Crear perfil
        perfil = PerfilUsuario.objects.create(
            user_id=user,
            nombre=f"Admin {planta.nombre}",
            apellido_paterno="Plant",
            apellido_materno="Manager",
            correo=user.email,
            nivel_usuario='admin-planta',
            admin_empresa=empresa.administrador
        )
        print(f"✅ Perfil creado: ID {perfil.id}")
        
        # 7. Crear AdminPlanta (ahora con fecha_asignacion automática)
        admin_planta = AdminPlanta.objects.create(
            usuario=perfil,
            planta=planta,
            status=True
        )
        print(f"✅ AdminPlanta creado: ID {admin_planta.id}")
        print(f"   📅 Fecha asignación: {admin_planta.fecha_asignacion}")
        
        # 8. Crear token
        token = Token.objects.create(user=user)
        print(f"✅ Token creado: {token.key}")
        
        print(f"\n🎉 ÉXITO COMPLETO!")
        print(f"   🏭 Planta: {planta.nombre}")
        print(f"   👤 Usuario: {username}")
        print(f"   🔑 Contraseña: {password}")
        print(f"   📧 Email: {user.email}")
        print(f"   🔐 Token: {token.key}")
        
        # Limpiar test
        print(f"\n🗑️ Limpiando test...")
        admin_planta.delete()
        token.delete()
        perfil.delete()
        user.delete()
        planta.delete()
        print("✅ Limpieza completada")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_crear_planta_completa()
