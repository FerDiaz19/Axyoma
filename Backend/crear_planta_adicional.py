#!/usr/bin/env python
"""
Script para crear una planta adicional para la empresa axis88 y probar la creación automática de usuario
"""

import os
import sys
import django

# Configurar Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')
django.setup()

from apps.models import Empresa, Planta, AdminPlanta, Usuario
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
import random
import string

def crear_planta_adicional():
    """Crear una planta adicional para axis88 con usuario automático"""
    try:
        # Buscar empresa axis88
        empresa = Empresa.objects.get(empresa_id=10)
        print(f"🏢 Empresa encontrada: {empresa.nombre}")
        
        # Crear nueva planta
        nueva_planta = Planta.objects.create(
            nombre='Planta Producción Norte',
            empresa=empresa,
            direccion='Av. Industrial #123, Zona Norte',
            status=True
        )
        print(f"🏭 Planta creada: {nueva_planta.nombre} (ID: {nueva_planta.planta_id})")
        
        # Crear usuario automáticamente (simulando la función del viewset)
        def crear_usuario_planta(planta, empresa):
            # Generar username único
            base_username = f"admin_{planta.nombre.lower().replace(' ', '_').replace('-', '_')}"
            username = base_username
            contador = 1
            while User.objects.filter(username=username).exists():
                username = f"{base_username}_{contador}"
                contador += 1

            # Generar contraseña segura
            password = ''.join(random.choices(string.ascii_letters + string.digits, k=12))

            # Crear usuario
            import time
            timestamp = int(time.time())
            email = f"admin.planta.{timestamp}@ejemplo.com"  # Email simple y único
            print(f"📧 Email generado: {email}")
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=f"Admin {planta.nombre}",
                last_name="Plant Manager"
            )

            # Crear perfil de usuario
            perfil = Usuario.objects.create(
                user_id=user,
                nombre=f"Admin {planta.nombre}",
                apellido_paterno="Plant",
                apellido_materno="Manager",
                correo=email,  # Usar el email que generamos
                nivel_usuario='admin-planta',
                admin_empresa=empresa.administrador
            )

            # Crear relación AdminPlanta
            AdminPlanta.objects.create(
                usuario=perfil,
                planta=planta,
                password_temporal=password,  # Guardar la contraseña temporal
                status=True
            )

            # Crear token
            Token.objects.create(user=user)

            return username, password
        
        # Crear usuario automáticamente
        username, password = crear_usuario_planta(nueva_planta, empresa)
        print(f"👤 Usuario creado: {username}")
        print(f"🔑 Contraseña: {password}")
        
        # Verificar estado final
        print("\n📊 Estado final:")
        plantas = Planta.objects.filter(empresa=empresa, status=True)
        print(f"  - Total plantas: {plantas.count()}")
        
        for planta in plantas:
            admins = AdminPlanta.objects.filter(planta=planta)
            print(f"  - {planta.nombre}: {admins.count()} admin(s)")
            for admin in admins:
                print(f"    → {admin.usuario.user.username}")
        
        print("\n✅ Planta adicional creada exitosamente con usuario automático")
        
    except Empresa.DoesNotExist:
        print("❌ Error: Empresa 10 no encontrada")
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    crear_planta_adicional()
