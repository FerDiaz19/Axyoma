#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para verificar y crear las rutas de respaldos estándar
Asegura que todos los equipos usen la misma estructura de directorios
"""
import os
import sys
import django

# Configurar Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.base')
django.setup()

from django.conf import settings

def verificar_rutas_respaldos():
    """Verificar y crear rutas estándar de respaldos"""
    
    print("🔍 VERIFICACIÓN DE RUTAS DE RESPALDOS")
    print("=" * 50)
    
    # Mostrar información del proyecto
    base_dir = settings.BASE_DIR
    print(f"📁 BASE_DIR del proyecto: {base_dir}")
    
    # Ruta estándar para respaldos
    backup_dir = os.path.join(base_dir, 'Backend', 'config', 'backups')
    print(f"📂 Directorio de respaldos estándar: {backup_dir}")
    
    # Verificar si existe
    if os.path.exists(backup_dir):
        print("✅ El directorio de respaldos ya existe")
        
        # Listar archivos existentes
        archivos = os.listdir(backup_dir)
        if archivos:
            print(f"📄 Archivos existentes: {len(archivos)}")
            for archivo in archivos[:5]:  # Mostrar solo los primeros 5
                print(f"   - {archivo}")
            if len(archivos) > 5:
                print(f"   ... y {len(archivos) - 5} más")
        else:
            print("📄 El directorio está vacío")
    else:
        print("❌ El directorio de respaldos NO existe")
        print("🔨 Creando directorio...")
        try:
            os.makedirs(backup_dir, exist_ok=True)
            print("✅ Directorio creado exitosamente")
        except Exception as e:
            print(f"❌ Error al crear directorio: {e}")
            return False
    
    # Verificar permisos
    try:
        test_file = os.path.join(backup_dir, 'test_permissions.tmp')
        with open(test_file, 'w') as f:
            f.write('test')
        os.remove(test_file)
        print("✅ Permisos de escritura: OK")
    except Exception as e:
        print(f"❌ Error de permisos de escritura: {e}")
        return False
    
    # Verificar configuración de la base de datos
    print("\n🗄️ CONFIGURACIÓN DE BASE DE DATOS")
    print("=" * 50)
    
    try:
        db_config = settings.DATABASES['default']
        print(f"📊 Base de datos: {db_config.get('NAME', 'No definida')}")
        print(f"🏠 Host: {db_config.get('HOST', 'localhost')}")
        print(f"🔌 Puerto: {db_config.get('PORT', '5432')}")
        print(f"👤 Usuario: {db_config.get('USER', 'No definido')}")
        print(f"🔑 Password: {'***' if db_config.get('PASSWORD') else 'No definida'}")
    except Exception as e:
        print(f"❌ Error al leer configuración de BD: {e}")
        return False
    
    # Crear archivo de configuración para el equipo
    config_file = os.path.join(backup_dir, 'config_equipo.txt')
    try:
        with open(config_file, 'w', encoding='utf-8') as f:
            f.write(f"Configuración de respaldos para este equipo\n")
            f.write(f"Generado: {os.popen('date').read().strip()}\n")
            f.write(f"BASE_DIR: {base_dir}\n")
            f.write(f"BACKUP_DIR: {backup_dir}\n")
            f.write(f"BD_NAME: {db_config.get('NAME', 'No definida')}\n")
            f.write(f"BD_HOST: {db_config.get('HOST', 'localhost')}\n")
            f.write(f"BD_PORT: {db_config.get('PORT', '5432')}\n")
        print(f"📋 Archivo de configuración creado: {config_file}")
    except Exception as e:
        print(f"⚠️ No se pudo crear archivo de configuración: {e}")
    
    print("\n✅ VERIFICACIÓN COMPLETADA")
    print("🚀 El sistema de respaldos está listo para funcionar")
    print(f"📁 Usar directorio: {backup_dir}")
    return True

if __name__ == '__main__':
    verificar_rutas_respaldos()
