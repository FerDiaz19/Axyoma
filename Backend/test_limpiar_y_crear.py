#!/usr/bin/env python
"""
Script para limpiar plantas y probar creación con usuario automático
"""
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')
django.setup()

from django.contrib.auth.models import User
from apps.users.models import PerfilUsuario, Empresa, Planta, AdminPlanta

def limpiar_y_probar():
    """Limpiar plantas y probar creación con límite"""
    print("=== LIMPIEZA Y PRUEBA DE PLANTAS ===\n")
    
    # Obtener empresa
    empresa = Empresa.objects.first()
    print(f"Trabajando con empresa: {empresa.nombre}")
    
    # Mostrar plantas actuales
    plantas_actuales = Planta.objects.filter(empresa=empresa)
    print(f"Plantas actuales: {plantas_actuales.count()}")
    
    # Eliminar plantas en exceso para dejar solo 2
    for i, planta in enumerate(plantas_actuales):
        if i >= 2:  # Mantener solo las primeras 2
            print(f"Eliminando planta: {planta.nombre}")
            
            # Eliminar usuario de planta si existe
            admin_planta = AdminPlanta.objects.filter(planta=planta).first()
            if admin_planta:
                usuario = admin_planta.usuario.user
                print(f"  - Eliminando usuario: {usuario.username}")
                usuario.delete()
            
            planta.delete()
    
    # Verificar estado después de limpieza
    plantas_restantes = Planta.objects.filter(empresa=empresa)
    print(f"\nPlantas restantes: {plantas_restantes.count()}")
    for planta in plantas_restantes:
        print(f"- {planta.nombre} (ID: {planta.planta_id})")
    
    # Ahora probar creación de nuevas plantas
    print(f"\n=== CREANDO NUEVAS PLANTAS ===")
    
    for i in range(4):  # Intentar crear 4 más para llegar al límite
        nombre_planta = f"Nueva Planta {i+1}"
        plantas_count = Planta.objects.filter(empresa=empresa, status=True).count()
        
        print(f"\nCreando: {nombre_planta} (plantas actuales: {plantas_count})")
        
        if plantas_count >= 5:
            print("⚠ Límite alcanzado, no se puede crear más")
            break
        
        # Crear planta
        planta = Planta.objects.create(
            nombre=nombre_planta,
            direccion=f"Dirección Nueva {i+1}",
            empresa=empresa
        )
        print(f"✓ Planta creada: {planta.nombre} (ID: {planta.planta_id})")
        
        # Crear usuario de planta
        crear_usuario_planta(planta)
    
    # Estado final
    print(f"\n=== ESTADO FINAL ===")
    plantas_finales = Planta.objects.filter(empresa=empresa)
    print(f"Total plantas: {plantas_finales.count()}")
    
    for planta in plantas_finales:
        admin_planta = AdminPlanta.objects.filter(planta=planta).first()
        if admin_planta:
            usuario = admin_planta.usuario.user
            print(f"- {planta.nombre} -> Usuario: {usuario.username}")
        else:
            print(f"- {planta.nombre} -> Sin usuario")

def crear_usuario_planta(planta):
    """Crear usuario de planta como en el viewset"""
    import random
    import string
    
    # Generar username único
    base_username = f"admin_planta_{planta.planta_id}"
    username = base_username.lower().replace(' ', '_')[:30]
    
    counter = 1
    original_username = username
    while User.objects.filter(username=username).exists():
        username = f"{original_username}_{counter}"[:30]
        counter += 1
    
    # Generar contraseña temporal
    password_chars = string.ascii_letters + string.digits
    password = ''.join(random.choice(password_chars) for _ in range(12))
    
    try:
        # Crear usuario
        user = User.objects.create_user(
            username=username,
            email=f"admin.planta.{planta.planta_id}@{planta.empresa.nombre.lower().replace(' ', '')}.com",
            password=password,
            first_name="Admin",
            last_name=f"Planta {planta.nombre}"
        )
        
        # Crear perfil de usuario
        perfil = PerfilUsuario.objects.create(
            user=user,
            nombre="Admin",
            apellido_paterno="Planta",
            apellido_materno=planta.nombre,
            correo=user.email,
            nivel_usuario='admin-planta'
        )
        
        # Crear relación AdminPlanta
        AdminPlanta.objects.create(
            usuario=perfil,
            planta=planta
        )
        
        print(f"  ✓ Usuario creado: {username} (password: {password})")
        
        # Mostrar credenciales para login
        print(f"    📧 Email: {user.email}")
        
    except Exception as e:
        print(f"  ✗ Error creando usuario: {str(e)}")

if __name__ == "__main__":
    limpiar_y_probar()
