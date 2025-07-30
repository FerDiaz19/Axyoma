#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para arreglar las contraseñas de admin_empresa y admin_planta
"""
import os
import sys
import django

# Configurar Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.base')
django.setup()

from django.contrib.auth.models import User
from apps.users.models import PerfilUsuario

def arreglar_admin_empresa():
    print("🔧 ARREGLANDO CONTRASEÑAS DE ADMINS")
    print("=" * 50)
    
    # Lista de usuarios a arreglar
    usuarios_arreglar = ['admin_empresa', 'admin_planta']
    
    for username in usuarios_arreglar:
        try:
            print(f"\n👤 Procesando: {username}")
            
            # Buscar o crear usuario Django
            user, created = User.objects.get_or_create(
                username=username,
                defaults={
                    'email': f'{username}@axyoma.com',
                    'first_name': username.replace('_', ' ').title(),
                    'is_staff': True,
                    'is_active': True
                }
            )
            
            # Configurar contraseña
            user.set_password('1234')
            user.is_staff = True
            user.is_active = True
            user.save()
            
            print(f"✅ Usuario Django configurado: {username}")
            print(f"   📧 Email: {user.email}")
            print(f"   🔑 Contraseña: 1234")
            print(f"   ✅ Staff: {user.is_staff}")
            print(f"   ✅ Activo: {user.is_active}")
            
            # Verificar perfil
            try:
                perfil = user.perfil
                print(f"✅ Perfil existe: {perfil.nivel_usuario}")
            except:
                print("⚠️ SIN PERFIL - creando uno...")
                nivel = 'admin-empresa' if 'empresa' in username else 'admin-planta'
                perfil = PerfilUsuario.objects.create(
                    user=user,
                    nombre=username.replace('_', ' ').title(),
                    apellido_paterno='Sistema',
                    correo=user.email,
                    nivel_usuario=nivel
                )
                print(f"✅ Perfil creado: {perfil.nivel_usuario}")
            
            # Verificar contraseña
            if user.check_password('1234'):
                print("✅ Contraseña '1234' verificada correctamente")
            else:
                print("❌ Problema con contraseña - reconfigurar...")
                user.set_password('1234')
                user.save()
                print("✅ Contraseña reconfigurada")
                
        except Exception as e:
            print(f"❌ Error con {username}: {e}")
    
    print(f"\n" + "=" * 50)
    print("🎯 CREDENCIALES FINALES:")
    print("🔸 superadmin / 1234")
    print("🔸 admin_empresa / 1234") 
    print("🔸 admin_planta / 1234")
    print(f"\n🌐 Prueba en: http://127.0.0.1:8000/admin/")
    
    # Mostrar todos los usuarios
    print(f"\n📊 TODOS LOS USUARIOS DISPONIBLES:")
    users = User.objects.all().order_by('username')
    for u in users:
        print(f"• {u.username} ({'Activo' if u.is_active else 'Inactivo'})")

if __name__ == '__main__':
    arreglar_admin_empresa()
