#!/usr/bin/env python
"""
Script para verificar el filtrado de plantas por empresa
"""
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')
django.setup()

from apps.users.models import Empresa, Planta, PerfilUsuario
from django.contrib.auth.models import User

def verificar_plantas_por_empresa():
    """Verificar qué plantas tiene cada empresa"""
    print("=== PLANTAS POR EMPRESA ===\n")
    
    empresas = Empresa.objects.all()
    
    for empresa in empresas:
        print(f"📢 EMPRESA: {empresa.nombre}")
        print(f"   Admin: {empresa.administrador.user.username}")
        
        plantas = Planta.objects.filter(empresa=empresa, status=True)
        print(f"   Plantas: {plantas.count()}")
        
        if plantas.exists():
            for planta in plantas:
                print(f"     - {planta.nombre} (ID: {planta.planta_id})")
        else:
            print(f"     ⚠️ No tiene plantas")
        print()

def verificar_usuarios_empresa():
    """Verificar usuarios de tipo admin-empresa"""
    print("=== USUARIOS ADMIN-EMPRESA ===\n")
    
    admins = PerfilUsuario.objects.filter(nivel_usuario='admin-empresa')
    
    for admin in admins:
        print(f"👤 Usuario: {admin.user.username}")
        print(f"   Email: {admin.correo}")
        
        try:
            empresa = Empresa.objects.get(administrador=admin)
            print(f"   Empresa: {empresa.nombre}")
            
            plantas = Planta.objects.filter(empresa=empresa, status=True)
            print(f"   Plantas: {plantas.count()}")
        except Empresa.DoesNotExist:
            print(f"   ⚠️ SIN EMPRESA ASIGNADA")
        print()

def crear_empresa_limpia():
    """Crear una empresa nueva sin plantas para probar"""
    print("=== CREANDO EMPRESA DE PRUEBA LIMPIA ===\n")
    
    try:
        # Verificar si ya existe
        if User.objects.filter(username='admin_test_limpio').exists():
            print("⚠️ Usuario de prueba ya existe, eliminando...")
            user = User.objects.get(username='admin_test_limpio')
            user.delete()
        
        # Crear usuario
        user = User.objects.create_user(
            username='admin_test_limpio',
            email='admin@empresalimpia.com',
            password='test123'
        )
        
        # Crear perfil
        perfil = PerfilUsuario.objects.create(
            user=user,
            nombre='Admin',
            apellido_paterno='Test',
            apellido_materno='Limpio',
            correo='admin@empresalimpia.com',
            nivel_usuario='admin-empresa'
        )
        
        # Crear empresa
        empresa = Empresa.objects.create(
            nombre='Empresa Test Limpia',
            rfc='TEST123LIMPIA',
            direccion='Dir test limpia',
            email_contacto='admin@empresalimpia.com',
            telefono_contacto='555-TEST',
            administrador=perfil
        )
        
        print(f"✅ Empresa creada: {empresa.nombre}")
        print(f"   Usuario: {user.username}")
        print(f"   Password: test123")
        print(f"   Esta empresa NO tiene plantas")
        
    except Exception as e:
        print(f"❌ Error creando empresa: {str(e)}")

if __name__ == "__main__":
    verificar_plantas_por_empresa()
    verificar_usuarios_empresa()
    crear_empresa_limpia()
