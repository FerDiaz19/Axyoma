#!/usr/bin/env python
"""
Script para crear usuarios de prueba para Axyoma
Ejecutar con: python crear_usuarios_prueba.py
"""

import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')
django.setup()

from django.contrib.auth.models import User
from apps.users.models import PerfilUsuario, Empresa, Planta, AdminPlanta

def crear_usuarios_prueba():
    """Crear usuarios de prueba para el sistema"""
    print("\n🚀 CREANDO USUARIOS DE PRUEBA PARA AXYOMA")
    print("=" * 60)
    
    # 1. Crear usuario Admin Empresa
    try:
        # Verificar si ya existe
        if User.objects.filter(username='admin_empresa').exists():
            print("⚠️ Usuario admin_empresa ya existe. Actualizando contraseña...")
            user_empresa = User.objects.get(username='admin_empresa')
            user_empresa.set_password('admin123')
            user_empresa.save()
            perfil_empresa = PerfilUsuario.objects.get(user=user_empresa)
        else:
            # Crear usuario y perfil
            user_empresa = User.objects.create_user(
                username='admin_empresa',
                email='admin@empresa.com',
                password='admin123',
                first_name='Admin',
                last_name='Empresa',
                is_active=True
            )
            
            # Crear perfil
            perfil_empresa = PerfilUsuario.objects.create(
                user=user_empresa,
                nombre='Admin',
                apellido_paterno='Empresa',
                correo='admin@empresa.com',
                nivel_usuario='admin-empresa',
                status=True
            )
            
            # Crear empresa para este admin
            empresa = Empresa.objects.create(
                nombre='Empresa Demo',
                rfc='DEMO123456ABC',
                direccion='Calle Demo #123, Ciudad Demo',
                email_contacto='contacto@empresademo.com',
                telefono_contacto='5555555555',
                administrador=perfil_empresa
            )
            
            print(f"✅ Empresa 'Empresa Demo' creada y asociada a admin_empresa")
        
        print(f"✅ Usuario Admin Empresa creado/actualizado:")
        print(f"   - Username: admin_empresa")
        print(f"   - Password: admin123")
        
    except Exception as e:
        print(f"❌ Error creando usuario Admin Empresa: {str(e)}")

    # 2. Crear usuario Admin Planta
    try:
        # Verificar si ya existe
        if User.objects.filter(username='admin_planta').exists():
            print("⚠️ Usuario admin_planta ya existe. Actualizando contraseña...")
            user_planta = User.objects.get(username='admin_planta')
            user_planta.set_password('admin123')
            user_planta.save()
            perfil_planta = PerfilUsuario.objects.get(user=user_planta)
        else:
            # Crear usuario y perfil
            user_planta = User.objects.create_user(
                username='admin_planta',
                email='admin@planta.com',
                password='admin123',
                first_name='Admin',
                last_name='Planta',
                is_active=True
            )
            
            # Crear perfil
            perfil_planta = PerfilUsuario.objects.create(
                user=user_planta,
                nombre='Admin',
                apellido_paterno='Planta',
                correo='admin@planta.com',
                nivel_usuario='admin-planta',
                status=True
            )
            
            # Buscar o crear empresa y planta
            try:
                empresa = Empresa.objects.get(nombre='Empresa Demo')
            except Empresa.DoesNotExist:
                # Si no existe la empresa de admin_empresa, crear una nueva
                admin_empresa = User.objects.filter(username='admin_empresa').first()
                if admin_empresa and hasattr(admin_empresa, 'perfil'):
                    perfil_empresa = admin_empresa.perfil
                else:
                    perfil_empresa = perfil_empresa = PerfilUsuario.objects.create(
                        user=User.objects.create_user(
                            username='admin_empresa_auto',
                            email='auto@empresa.com',
                            password='admin123',
                            is_active=True
                        ),
                        nombre='Auto',
                        apellido_paterno='Admin',
                        correo='auto@empresa.com',
                        nivel_usuario='admin-empresa',
                        status=True
                    )
                
                empresa = Empresa.objects.create(
                    nombre='Empresa Demo',
                    rfc='DEMO123456ABC',
                    direccion='Calle Demo #123, Ciudad Demo',
                    email_contacto='contacto@empresademo.com',
                    telefono_contacto='5555555555',
                    administrador=perfil_empresa
                )
                
            # Crear planta
            planta = Planta.objects.create(
                nombre='Planta Demo',
                direccion='Calle Industrial #456, Parque Industrial',
                empresa=empresa,
                status=True
            )
            
            # Asociar admin con planta
            AdminPlanta.objects.create(
                usuario=perfil_planta,
                planta=planta,
                status=True
            )
            
            print(f"✅ Planta 'Planta Demo' creada y asociada a admin_planta")
        
        print(f"✅ Usuario Admin Planta creado/actualizado:")
        print(f"   - Username: admin_planta")
        print(f"   - Password: admin123")
        
    except Exception as e:
        print(f"❌ Error creando usuario Admin Planta: {str(e)}")

    print("\n✅ USUARIOS DE PRUEBA CREADOS EXITOSAMENTE")
    print("=" * 60)
    print("Credenciales disponibles:")
    print("  👤 SuperAdmin:    testuser / testpass123")
    print("  👤 Admin Empresa: admin_empresa / admin123")
    print("  👤 Admin Planta:  admin_planta / admin123")
    print("=" * 60)

if __name__ == "__main__":
    crear_usuarios_prueba()
