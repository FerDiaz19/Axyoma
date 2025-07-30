#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para verificar rutas independientes del nombre del proyecto
Funciona con 'axyoma', 'Axyoma2', o cualquier otro nombre
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

def verificar_rutas_universales():
    print("🔍 VERIFICACIÓN DE RUTAS UNIVERSALES")
    print("=" * 50)
    
    base_dir = settings.BASE_DIR
    print(f"📁 BASE_DIR (Django): {base_dir}")
    
    # Detectar el directorio del proyecto automáticamente
    backend_dir = base_dir.parent  # Backend/config -> Backend/
    proyecto_dir = backend_dir.parent  # Backend/ -> [Proyecto]/
    
    print(f"📂 Directorio Backend: {backend_dir}")
    print(f"🏠 Directorio del Proyecto: {proyecto_dir}")
    print(f"📝 Nombre del Proyecto: {proyecto_dir.name}")
    
    # Ruta de respaldos
    backup_dir = backend_dir / 'config' / 'backups'
    print(f"💾 Directorio de Respaldos: {backup_dir}")
    
    # Verificar si existe
    if backup_dir.exists():
        print("✅ El directorio de respaldos existe")
        
        # Listar archivos
        archivos_sql = list(backup_dir.glob('*.sql'))
        archivos_json = list(backup_dir.glob('*.json'))
        
        print(f"📄 Archivos SQL: {len(archivos_sql)}")
        print(f"📋 Archivos Metadata: {len(archivos_json)}")
        
        # Mostrar algunos archivos
        for archivo in archivos_sql[:3]:
            print(f"   - {archivo.name}")
        
    else:
        print("❌ El directorio de respaldos NO existe")
        print("🔨 Creando directorio...")
        backup_dir.mkdir(parents=True, exist_ok=True)
        print("✅ Directorio creado")
    
    # Verificar permisos
    try:
        test_file = backup_dir / 'test_universal.tmp'
        test_file.write_text('test de permisos')
        test_file.unlink()
        print("✅ Permisos de escritura: OK")
    except Exception as e:
        print(f"❌ Error de permisos: {e}")
    
    # Configuración de BD
    print(f"\n🗄️ CONFIGURACIÓN DE BD:")
    db_config = settings.DATABASES['default']
    print(f"📊 Base de datos: {db_config.get('NAME')}")
    print(f"🏠 Host: {db_config.get('HOST', 'localhost')}")
    print(f"🔌 Puerto: {db_config.get('PORT', '5432')}")
    
    # Crear archivo de info del equipo
    info_file = backup_dir / 'info_equipo.txt'
    try:
        with info_file.open('w', encoding='utf-8') as f:
            f.write(f"Información del Equipo\n")
            f.write(f"Fecha: {os.popen('date /T').read().strip()}\n")
            f.write(f"Proyecto: {proyecto_dir.name}\n")
            f.write(f"Ruta Proyecto: {proyecto_dir}\n")
            f.write(f"Ruta Backend: {backend_dir}\n")
            f.write(f"Ruta Respaldos: {backup_dir}\n")
            f.write(f"BD: {db_config.get('NAME')}\n")
        print(f"📋 Info del equipo guardada: {info_file}")
    except Exception as e:
        print(f"⚠️ No se pudo crear info del equipo: {e}")
    
    print(f"\n✅ SISTEMA UNIVERSAL VERIFICADO")
    print(f"🎯 Funciona con cualquier nombre de proyecto")
    print(f"📁 Respaldos en: {backup_dir}")
    
    return backup_dir

if __name__ == '__main__':
    verificar_rutas_universales()
