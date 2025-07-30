#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script simple para verificar rutas de respaldos
"""
import os
import sys
import django

# Configurar Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.base')
django.setup()

from django.conf import settings

def verificar_rutas():
    print("🔍 VERIFICACIÓN SIMPLE DE RUTAS")
    print("=" * 40)
    
    base_dir = settings.BASE_DIR
    print(f"📁 BASE_DIR: {base_dir}")
    
    backup_dir = os.path.join(base_dir, 'backups')
    print(f"📂 BACKUP_DIR: {backup_dir}")
    
    print(f"📁 Directorio existe: {os.path.exists(backup_dir)}")
    
    # Crear directorio si no existe
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir, exist_ok=True)
        print("✅ Directorio creado")
    
    # Verificar archivos existentes
    if os.path.exists(backup_dir):
        archivos = os.listdir(backup_dir)
        print(f"📄 Archivos: {len(archivos)}")
        for archivo in archivos[:3]:
            print(f"   - {archivo}")
    
    print("✅ Verificación completada")

if __name__ == '__main__':
    verificar_rutas()
