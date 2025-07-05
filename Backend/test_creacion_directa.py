#!/usr/bin/env python
"""
Script para probar creación de plantas con límite y usuario automático
"""
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')
django.setup()

from django.contrib.auth.models import User
from apps.users.models import PerfilUsuario, Empresa, Planta, AdminPlanta

def test_creacion_plantas():
    """Probar creación de plantas con límite y usuario automático"""
    print("=== PRUEBA DIRECTA DE CREACIÓN DE PLANTAS ===\n")
    
    try:
        # Buscar empresa existente
        empresa = Empresa.objects.first()
        if not empresa:
            print("No hay empresas registradas. Creando una de prueba...")
            # Crear empresa de prueba si no existe
            admin_user = User.objects.create_user(
                username="test_admin",
                password="test123",
                email="test@test.com"
            )
            admin_perfil = PerfilUsuario.objects.create(
                user=admin_user,
                nombre="Test",
                apellido_paterno="Admin",
                correo="test@test.com",
                nivel_usuario="admin-empresa"
            )
            empresa = Empresa.objects.create(
                nombre="Empresa Test",
                direccion="Dir test",
                telefono="123456789",
                administrador=admin_perfil
            )
            print(f"✓ Empresa creada: {empresa.nombre}")
        
        print(f"Usando empresa: {empresa.nombre}")
        
        # Contar plantas actuales
        plantas_actuales = Planta.objects.filter(empresa=empresa, status=True).count()
        print(f"Plantas actuales: {plantas_actuales}")
        
        # Intentar crear plantas hasta el límite
        for i in range(6):  # Intentar crear 6 para probar el límite
            nombre_planta = f"Planta Test {i+1}"
            print(f"\nIntentando crear: {nombre_planta}")
            
            plantas_count = Planta.objects.filter(empresa=empresa, status=True).count()
            
            if plantas_count >= 5:
                print(f"⚠ Límite alcanzado. No se puede crear más plantas ({plantas_count}/5)")
                break
            
            # Crear planta
            planta = Planta.objects.create(
                nombre=nombre_planta,
                direccion=f"Dirección {i+1}",
                empresa=empresa
            )
            print(f"✓ Planta creada: {planta.nombre} (ID: {planta.planta_id})")
            
            # Simular la creación del usuario de planta (como en el viewset)
            crear_usuario_planta_simulado(planta)
        
        # Mostrar estado final
        print(f"\n=== ESTADO FINAL ===")
        plantas_finales = Planta.objects.filter(empresa=empresa, status=True)
        print(f"Total plantas: {plantas_finales.count()}")
        
        for planta in plantas_finales:
            print(f"- {planta.nombre} (ID: {planta.planta_id})")
            
            # Verificar usuario de planta
            admin_planta = AdminPlanta.objects.filter(planta=planta).first()
            if admin_planta:
                usuario = admin_planta.usuario.user
                print(f"  Usuario: {usuario.username} ({usuario.email})")
            else:
                print(f"  ⚠ Sin usuario de planta")
    
    except Exception as e:
        print(f"Error: {str(e)}")
        import traceback
        traceback.print_exc()

def crear_usuario_planta_simulado(planta):
    """Simular la creación del usuario de planta del viewset"""
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
        
    except Exception as e:
        print(f"  ✗ Error creando usuario: {str(e)}")

if __name__ == "__main__":
    test_creacion_plantas()
