#!/usr/bin/env python
"""
Script para crear un admin de planta enlazado a la planta 3
"""

import os
import sys
import django

# Configurar Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')
django.setup()

from django.contrib.auth.models import User
from apps.users.models import PerfilUsuario, AdminPlanta, Planta
from django.db import transaction

def crear_admin_planta():
    try:
        with transaction.atomic():
            # Verificar que la planta 3 existe
            try:
                planta = Planta.objects.get(planta_id=3)
                print(f"✅ Planta encontrada: {planta.nombre} (ID: {planta.planta_id})")
                print(f"   Empresa: {planta.empresa.nombre}")
            except Planta.DoesNotExist:
                print("❌ Error: La planta con ID 3 no existe")
                return False

            # Verificar si ya existe un admin para esta planta
            admin_existente = AdminPlanta.objects.filter(planta=planta).first()
            if admin_existente:
                print(f"⚠️  Ya existe un admin para esta planta: {admin_existente.usuario.nombre} {admin_existente.usuario.apellido_paterno}")
                respuesta = input("¿Deseas crear otro admin para la misma planta? (s/n): ")
                if respuesta.lower() != 's':
                    return False

            # Datos del nuevo admin de planta
            username = f"admin_planta3_{planta.nombre.lower().replace(' ', '_')}"
            email = f"admin.planta3@{planta.empresa.nombre.lower().replace(' ', '')}.com"
            
            print(f"\n🔧 Creando admin de planta...")
            print(f"   Username: {username}")
            print(f"   Email: {email}")
            
            # Crear usuario de Django
            user = User.objects.create_user(
                username=username,
                email=email,
                password='admin123',  # Contraseña temporal
                first_name='Admin',
                last_name=f'Planta {planta.nombre}'
            )
            print(f"✅ Usuario Django creado: {user.username}")

            # Crear perfil de usuario
            perfil = PerfilUsuario.objects.create(
                user=user,
                nombre='Admin',
                apellido_paterno='Planta',
                apellido_materno=planta.nombre,
                nivel_usuario='admin-planta',
                telefono='555-0103',
                activo=True
            )
            print(f"✅ Perfil de usuario creado: {perfil.nombre} {perfil.apellido_paterno} {perfil.apellido_materno}")

            # Crear AdminPlanta
            admin_planta = AdminPlanta.objects.create(
                usuario=perfil,
                planta=planta,
                activo=True
            )
            print(f"✅ Admin de planta creado con ID: {admin_planta.admin_planta_id}")

            print(f"\n🎉 ¡Admin de planta creado exitosamente!")
            print(f"   ID Admin: {admin_planta.admin_planta_id}")
            print(f"   Usuario: {perfil.nombre} {perfil.apellido_paterno} {perfil.apellido_materno}")
            print(f"   Username: {user.username}")
            print(f"   Password: admin123")
            print(f"   Email: {user.email}")
            print(f"   Planta: {planta.nombre} (ID: {planta.planta_id})")
            print(f"   Empresa: {planta.empresa.nombre}")
            
            return True

    except Exception as e:
        print(f"❌ Error creando admin de planta: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🚀 Iniciando creación de admin de planta para planta 3...")
    exito = crear_admin_planta()
    
    if exito:
        print("\n✅ Proceso completado exitosamente")
    else:
        print("\n❌ Proceso fallido")
