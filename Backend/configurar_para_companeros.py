#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SCRIPT DE CONFIGURACIÓN PARA COMPAÑEROS CON DIRECTORIO 'axyoma'
Este script configura automáticamente el sistema de respaldos
"""
import os
import sys
import django
from pathlib import Path

# Configurar Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.base')
django.setup()

from django.conf import settings
from django.contrib.auth.models import User
from apps.users.models import PerfilUsuario

def configurar_sistema_completo():
    print("🚀 CONFIGURACIÓN AUTOMÁTICA PARA EQUIPOS")
    print("=" * 50)
    
    # 1. Verificar rutas
    print("1️⃣ Verificando rutas del proyecto...")
    base_dir = settings.BASE_DIR
    backend_dir = base_dir.parent
    proyecto_dir = backend_dir.parent
    
    print(f"📁 Proyecto: {proyecto_dir.name}")
    print(f"📂 Ruta completa: {proyecto_dir}")
    
    # 2. Crear directorio de respaldos
    print("\n2️⃣ Configurando directorio de respaldos...")
    backup_dir = backend_dir / 'config' / 'backups'
    backup_dir.mkdir(parents=True, exist_ok=True)
    print(f"✅ Directorio: {backup_dir}")
    
    # 3. Verificar permisos
    print("\n3️⃣ Verificando permisos...")
    try:
        test_file = backup_dir / 'test_config.tmp'
        test_file.write_text('test')
        test_file.unlink()
        print("✅ Permisos de escritura: OK")
    except Exception as e:
        print(f"❌ Error de permisos: {e}")
        return False
    
    # 4. Configurar usuario SuperAdmin
    print("\n4️⃣ Configurando usuario SuperAdmin...")
    try:
        # Buscar o crear usuario Django
        django_user, created = User.objects.get_or_create(
            username='superadmin',
            defaults={
                'email': 'superadmin@axyoma.com',
                'first_name': 'Super',
                'last_name': 'Admin',
                'is_staff': True,
                'is_superuser': True
            }
        )
        
        if created:
            django_user.set_password('1234')
            django_user.save()
            print("✅ Usuario Django 'superadmin' creado")
        else:
            print("✅ Usuario Django 'superadmin' ya existe")
            # Asegurar permisos
            django_user.is_staff = True
            django_user.is_superuser = True
            django_user.save()
        
        # Buscar o crear perfil
        try:
            perfil = PerfilUsuario.objects.get(correo='superadmin@axyoma.com')
            # Corregir asociación si es necesaria
            if perfil.user != django_user:
                perfil.user = django_user
                perfil.save()
                print("✅ Asociación de perfil corregida")
            else:
                print("✅ Perfil ya existe y está bien asociado")
                
        except PerfilUsuario.DoesNotExist:
            # Crear perfil
            perfil = PerfilUsuario.objects.create(
                user=django_user,
                nombre='Super',
                apellido_paterno='Admin',
                correo='superadmin@axyoma.com',
                nivel_usuario='superadmin'
            )
            print("✅ Perfil de SuperAdmin creado")
        
    except Exception as e:
        print(f"❌ Error configurando SuperAdmin: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    # 5. Probar sistema de respaldos
    print("\n5️⃣ Probando sistema de respaldos...")
    try:
        from apps.admin_bd.views_respaldos import get_backup_directory
        test_backup_dir = get_backup_directory()
        print(f"✅ Función de respaldos: {test_backup_dir}")
        
        # Crear archivo de prueba
        test_sql = Path(test_backup_dir) / 'test_sistema.sql'
        test_sql.write_text('-- Archivo de prueba\nSELECT 1;')
        print(f"✅ Archivo de prueba creado: {test_sql.name}")
        test_sql.unlink()
        print("✅ Archivo de prueba eliminado")
        
    except Exception as e:
        print(f"❌ Error en sistema de respaldos: {e}")
        return False
    
    # 6. Resumen final
    print(f"\n🎉 CONFIGURACIÓN COMPLETADA")
    print("=" * 50)
    print(f"📁 Proyecto: {proyecto_dir.name}")
    print(f"💾 Respaldos: {backup_dir}")
    print(f"👤 Usuario: superadmin")
    print(f"🔑 Password: 1234")
    print(f"🌐 Frontend: http://localhost:3000")
    print(f"🔧 Backend: http://localhost:8000")
    
    # Crear archivo de confirmación
    try:
        config_file = backup_dir / 'configuracion_completada.txt'
        with config_file.open('w', encoding='utf-8') as f:
            f.write(f"Configuración completada exitosamente\n")
            f.write(f"Fecha: {os.popen('date /T').read().strip()}\n")
            f.write(f"Proyecto: {proyecto_dir.name}\n")
            f.write(f"Ruta: {proyecto_dir}\n")
            f.write(f"Usuario SuperAdmin: configurado\n")
            f.write(f"Sistema de respaldos: funcionando\n")
        print(f"📋 Confirmación guardada: {config_file}")
    except:
        pass
    
    print(f"\n✅ EL SISTEMA ESTÁ LISTO PARA USAR")
    return True

if __name__ == '__main__':
    configurar_sistema_completo()
