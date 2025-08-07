#!/usr/bin/env python3
"""
Script para crear credenciales para plantas existentes sin administrador
"""
import os
import sys
import django
import random
import string

# Configuración de Django
sys.path.append('.')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from apps.users.models import PerfilUsuario, Empresa, Planta, AdminPlanta

def crear_credenciales_plantas_existentes():
    """Crear credenciales para plantas que no tienen administrador"""
    
    print("🔍 Buscando plantas sin administrador...")
    
    plantas_sin_admin = []
    
    for planta in Planta.objects.filter(status=True):
        if not AdminPlanta.objects.filter(planta=planta).exists():
            plantas_sin_admin.append(planta)
    
    print(f"📊 Plantas sin administrador encontradas: {len(plantas_sin_admin)}")
    
    if not plantas_sin_admin:
        print("✅ Todas las plantas ya tienen administrador asignado")
        return
    
    credenciales_creadas = []
    
    for planta in plantas_sin_admin:
        print(f"\n🏭 Procesando planta: {planta.nombre} (ID: {planta.planta_id})")
        print(f"   🏢 Empresa: {planta.empresa.nombre}")
        
        try:
            # Generar username único
            base_username = f"admin_{planta.nombre.lower().replace(' ', '_').replace('-', '_')}"
            username = base_username
            contador = 1
            
            while User.objects.filter(username=username).exists():
                username = f"{base_username}_{contador}"
                contador += 1
            
            # Generar contraseña segura
            password = ''.join(random.choices(string.ascii_letters + string.digits, k=12))
            
            # Crear usuario Django
            user = User.objects.create_user(
                username=username,
                email=f"{username}@{planta.empresa.nombre.lower().replace(' ', '')}.com",
                password=password,
                first_name=f"Admin {planta.nombre}",
                last_name="Plant Manager"
            )
            
            # Crear perfil de usuario
            perfil = PerfilUsuario.objects.create(
                user_id=user,  # Usar user_id correcto
                nombre=f"Admin {planta.nombre}",
                apellido_paterno="Plant",
                apellido_materno="Manager", 
                correo=user.email,
                nivel_usuario='admin-planta',
                admin_empresa=planta.empresa.administrador
            )
            
            # Crear relación AdminPlanta
            AdminPlanta.objects.create(
                usuario=perfil,
                planta=planta,
                status=True
            )
            
            # Crear token
            token = Token.objects.create(user=user)
            
            credenciales_creadas.append({
                'planta': planta.nombre,
                'username': username,
                'password': password,
                'email': user.email,
                'token': token.key
            })
            
            print(f"   ✅ Usuario creado: {username}")
            print(f"   🔑 Contraseña: {password}")
            print(f"   📧 Email: {user.email}")
            
        except Exception as e:
            print(f"   ❌ Error: {str(e)}")
            import traceback
            traceback.print_exc()
    
    # Resumen final
    print(f"\n🎉 RESUMEN: Se crearon {len(credenciales_creadas)} conjuntos de credenciales")
    print("=" * 80)
    
    for cred in credenciales_creadas:
        print(f"🏭 {cred['planta']}")
        print(f"   👤 Usuario: {cred['username']}")
        print(f"   🔑 Contraseña: {cred['password']}")
        print(f"   📧 Email: {cred['email']}")
        print(f"   🔐 Token: {cred['token']}")
        print("-" * 50)

if __name__ == "__main__":
    crear_credenciales_plantas_existentes()
