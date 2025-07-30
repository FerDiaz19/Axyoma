#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para probar respaldos directamente con Django
"""
import os
import sys
import django

# Configurar Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.base')
django.setup()

from django.conf import settings
from django.contrib.auth.models import User
from apps.admin_bd.views_respaldos import obtener_config_db, get_backup_directory

def probar_sistema():
    print("🧪 PRUEBA DIRECTA CON DJANGO")
    print("=" * 40)
    
    # Verificar configuración
    try:
        print("1. Verificando configuración de BD...")
        db_config = obtener_config_db()
        print(f"✅ BD: {db_config['name']}")
        print(f"✅ Host: {db_config['host']}")
        print(f"✅ Puerto: {db_config['port']}")
        print(f"✅ Usuario: {db_config['user']}")
        
        print("\n2. Verificando directorio de respaldos...")
        backup_dir = get_backup_directory()
        print(f"✅ Directorio: {backup_dir}")
        print(f"✅ Existe: {os.path.exists(backup_dir)}")
        
        if os.path.exists(backup_dir):
            archivos = [f for f in os.listdir(backup_dir) if f.endswith('.sql')]
            print(f"✅ Archivos SQL: {len(archivos)}")
            
        print("\n3. Verificando usuario SuperAdmin...")
        try:
            superadmin = User.objects.get(username='superadmin')
            print(f"✅ SuperAdmin existe: {superadmin.username}")
            perfil = getattr(superadmin, 'perfil', None)
            if perfil:
                print(f"✅ Nivel: {perfil.nivel_usuario}")
            else:
                print("⚠️ No tiene perfil asociado")
        except User.DoesNotExist:
            print("❌ Usuario SuperAdmin no existe")
            
        print("\n4. Probando creación manual de archivo...")
        test_file = os.path.join(backup_dir, 'test_manual.sql')
        try:
            with open(test_file, 'w') as f:
                f.write('-- Test de creación manual\n')
                f.write('SELECT 1;\n')
            print(f"✅ Archivo de prueba creado: {test_file}")
            
            # Verificar tamaño
            size = os.path.getsize(test_file)
            print(f"✅ Tamaño: {size} bytes")
            
            # Eliminar archivo de prueba
            os.remove(test_file)
            print("✅ Archivo de prueba eliminado")
            
        except Exception as e:
            print(f"❌ Error al crear archivo: {e}")
            
        print("\n✅ SISTEMA LISTO PARA USO")
        print(f"📁 Los respaldos se guardarán en: {backup_dir}")
        
    except Exception as e:
        print(f"❌ Error en verificación: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    probar_sistema()
