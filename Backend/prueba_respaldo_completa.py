#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Prueba completa del sistema de respaldos con la nueva configuración
"""
import os
import sys
import django
from pathlib import Path
import subprocess

# Configurar Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.base')
django.setup()

from django.conf import settings
from apps.admin_bd.views_respaldos import get_backup_directory, obtener_config_db

def prueba_respaldo_completa():
    print("🧪 PRUEBA COMPLETA DEL SISTEMA DE RESPALDOS")
    print("=" * 60)
    
    # 1. Verificar configuración
    print("1️⃣ Verificando configuración...")
    try:
        backup_dir = get_backup_directory()
        print(f"✅ Directorio de respaldos: {backup_dir}")
        
        db_config = obtener_config_db()
        print(f"✅ Base de datos: {db_config['name']}")
        
    except Exception as e:
        print(f"❌ Error en configuración: {e}")
        return False
    
    # 2. Simular creación de respaldo (sin pg_dump real)
    print("\n2️⃣ Simulando creación de respaldo...")
    try:
        from datetime import datetime
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        test_backup_file = Path(backup_dir) / f"test_backup_{timestamp}.sql"
        
        # Crear archivo de prueba
        with test_backup_file.open('w', encoding='utf-8') as f:
            f.write("-- Archivo de prueba del sistema de respaldos\n")
            f.write("-- Generado por sistema universal de rutas\n")
            f.write(f"-- Timestamp: {timestamp}\n")
            f.write("SELECT 'Sistema de respaldos funcionando' as status;\n")
        
        print(f"✅ Archivo de prueba creado: {test_backup_file.name}")
        
        # Verificar tamaño
        size = test_backup_file.stat().st_size
        print(f"✅ Tamaño: {size} bytes")
        
        # Crear metadata
        metadata_file = test_backup_file.with_suffix('.json')
        import json
        metadata = {
            "tipo": "test",
            "timestamp": timestamp,
            "archivo": test_backup_file.name,
            "tamaño_bytes": size,
            "proyecto": Path(backup_dir).parent.parent.name,
            "ruta_completa": str(test_backup_file)
        }
        
        with metadata_file.open('w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Metadata creada: {metadata_file.name}")
        
    except Exception as e:
        print(f"❌ Error creando archivo de prueba: {e}")
        return False
    
    # 3. Verificar archivos existentes
    print("\n3️⃣ Listando archivos de respaldo...")
    try:
        backup_path = Path(backup_dir)
        sql_files = list(backup_path.glob("*.sql"))
        json_files = list(backup_path.glob("*.json"))
        
        print(f"📄 Archivos SQL encontrados: {len(sql_files)}")
        for sql_file in sql_files[:5]:  # Mostrar máximo 5
            print(f"   - {sql_file.name}")
        
        print(f"📋 Archivos metadata: {len(json_files)}")
        
    except Exception as e:
        print(f"❌ Error listando archivos: {e}")
        return False
    
    # 4. Cleanup (eliminar archivo de prueba)
    print("\n4️⃣ Limpieza...")
    try:
        test_backup_file.unlink()
        metadata_file.unlink()
        print("✅ Archivos de prueba eliminados")
    except Exception as e:
        print(f"⚠️ No se pudieron eliminar archivos de prueba: {e}")
    
    # 5. Verificar que pg_dump esté disponible (opcional)
    print("\n5️⃣ Verificando herramientas...")
    try:
        result = subprocess.run(['pg_dump', '--version'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ pg_dump disponible: {result.stdout.strip()}")
        else:
            print("⚠️ pg_dump no encontrado (requerido para respaldos reales)")
    except FileNotFoundError:
        print("⚠️ pg_dump no encontrado en PATH")
    
    print(f"\n🎉 PRUEBA COMPLETADA EXITOSAMENTE")
    print("=" * 60)
    print(f"📁 El sistema guardará respaldos en: {backup_dir}")
    print(f"🌐 Acceso vía: SuperAdmin Dashboard → Gestión BD → Respaldos")
    print(f"🔑 Credenciales: superadmin / 1234")
    
    return True

if __name__ == '__main__':
    prueba_respaldo_completa()
