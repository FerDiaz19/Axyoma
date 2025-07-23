#!/usr/bin/env python
"""
Script para verificar los usuarios disponibles y sus credenciales en el sistema
"""

import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')
django.setup()

from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from apps.users.models import PerfilUsuario, Empresa, Planta, AdminPlanta

def listar_usuarios():
    """Listar todos los usuarios del sistema y sus detalles"""
    print("\n🔍 USUARIOS EN EL SISTEMA:")
    print("=" * 60)
    
    # Obtener usuarios de Django
    users = User.objects.all()
    
    if not users:
        print("❌ NO HAY USUARIOS EN LA BASE DE DATOS")
        return
    
    for user in users:
        print(f"\n👤 Usuario: {user.username}")
        print(f"   Email: {user.email}")
        print(f"   Nombre: {user.first_name} {user.last_name}")
        print(f"   ID: {user.id}")
        print(f"   Activo: {'✅' if user.is_active else '❌'}")
        print(f"   Admin: {'✅' if user.is_staff else '❌'}")
        print(f"   SuperAdmin: {'✅' if user.is_superuser else '❌'}")
        
        # Verificar si tiene perfil
        try:
            perfil = PerfilUsuario.objects.get(user=user)
            print(f"   Nivel: {perfil.nivel_usuario}")
            
            # Verificar rol específico
            if perfil.nivel_usuario == 'superadmin':
                print(f"   Rol: SuperAdmin del Sistema")
                
            elif perfil.nivel_usuario == 'admin-empresa':
                try:
                    empresa = Empresa.objects.get(administrador=perfil)
                    print(f"   Empresa: {empresa.nombre} (ID: {empresa.empresa_id})")
                except Empresa.DoesNotExist:
                    print(f"   ⚠️ Es admin-empresa pero no tiene empresa asignada")
                    
            elif perfil.nivel_usuario == 'admin-planta':
                try:
                    admin_planta = AdminPlanta.objects.get(usuario=perfil)
                    planta = admin_planta.planta
                    empresa = planta.empresa
                    print(f"   Planta: {planta.nombre} (ID: {planta.planta_id})")
                    print(f"   Empresa: {empresa.nombre} (ID: {empresa.empresa_id})")
                except AdminPlanta.DoesNotExist:
                    print(f"   ⚠️ Es admin-planta pero no tiene planta asignada")
                    
        except PerfilUsuario.DoesNotExist:
            print(f"   ⚠️ Usuario sin perfil asociado")
    
    print(f"\n📊 Total usuarios: {users.count()}")

def probar_credenciales():
    """Probar credenciales de usuarios en el sistema"""
    print("\n🔑 PROBANDO CREDENCIALES COMUNES:")
    print("=" * 60)
    
    # Lista de posibles credenciales comunes para probar
    credenciales = [
        # Formato: (username, password, descripción)
        ('superadmin', '1234', 'SuperAdmin predeterminado'),
        ('admin', '1234', 'Admin genérico'),
        ('admin@empresa.com', '1234', 'Admin Empresa'),
        ('planta@empresa.com', '1234', 'Admin Planta'),
        ('superadmin@axyoma.com', 'admin123', 'SuperAdmin Axyoma'),
        ('ed-rubio@axyoma.com', '1234', 'Ed Rubio'),
        ('juan.perez@codewave.com', '1234', 'Juan Pérez'),
        ('maria.gomez@codewave.com', '1234', 'María Gómez'),
    ]
    
    # Probar también todos los usernames de la base de datos
    for user in User.objects.all():
        credenciales.append((user.username, '1234', f'Usuario existente: {user.username}'))
        credenciales.append((user.username, 'admin123', f'Usuario existente: {user.username}'))
        # Si el usuario tiene email, probar también con él
        if user.email:
            credenciales.append((user.email, '1234', f'Email existente: {user.email}'))
            credenciales.append((user.email, 'admin123', f'Email existente: {user.email}'))
    
    # Eliminar duplicados
    credenciales = list(set(credenciales))
    
    # Probar cada credencial
    for username, password, desc in credenciales:
        user = authenticate(username=username, password=password)
        if user:
            print(f"✅ {desc}: {username}/{password} - AUTENTICACIÓN EXITOSA")
            print(f"   - Nombre: {user.first_name} {user.last_name}")
            print(f"   - Email: {user.email}")
            try:
                perfil = PerfilUsuario.objects.get(user=user)
                print(f"   - Nivel: {perfil.nivel_usuario}")
            except PerfilUsuario.DoesNotExist:
                print(f"   - Sin perfil asociado")
        else:
            print(f"❌ {desc}: {username}/{password} - FALLO")
    
    print("\n✨ FIN DE LA VERIFICACIÓN DE CREDENCIALES")

def crear_usuario_test():
    """Crear un usuario de prueba con credenciales conocidas"""
    print("\n🛠️ CREANDO USUARIO DE PRUEBA:")
    print("=" * 60)
    
    try:
        # Verificar si ya existe
        if User.objects.filter(username='testuser').exists():
            print("⚠️ El usuario de prueba ya existe. Actualizando contraseña...")
            user = User.objects.get(username='testuser')
            user.set_password('testpass123')
            user.save()
        else:
            # Crear usuario y perfil
            user = User.objects.create_user(
                username='testuser',
                email='test@axyoma.com',
                password='testpass123',
                first_name='Usuario',
                last_name='Prueba',
                is_active=True
            )
            
            # Crear perfil
            perfil = PerfilUsuario.objects.create(
                user=user,
                nombre='Usuario',
                apellido_paterno='Prueba',
                correo='test@axyoma.com',
                nivel_usuario='superadmin',
                status=True
            )
        
        print("✅ Usuario de prueba creado/actualizado exitosamente")
        print("   - Username: testuser")
        print("   - Password: testpass123")
        print("   - Nivel: superadmin")
        
    except Exception as e:
        print(f"❌ Error creando usuario de prueba: {str(e)}")

def main():
    print("\n🚀 VERIFICACIÓN DE USUARIOS Y CREDENCIALES DE AXYOMA")
    print("=" * 60)
    
    # 1. Listar usuarios existentes
    listar_usuarios()
    
    # 2. Probar credenciales
    probar_credenciales()
    
    # 3. Crear usuario de prueba
    crear_usuario_test()
    
    print("\n🏁 VERIFICACIÓN COMPLETADA")

if __name__ == "__main__":
    main()
