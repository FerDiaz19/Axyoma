#!/usr/bin/env python3
"""
🧪 PRUEBA DE RESPALDOS COMPATIBLES CON PGADMIN
===============================================

Este script verifica que los respaldos generados sean compatibles con pgAdmin
y no contengan comandos problemáticos como \connect.

Autor: Sistema Axyoma
Fecha: Enero 2025
"""

import os
import sys
import django
import subprocess
from pathlib import Path

# Configurar Django
sys.path.append('/c/xampp2/htdocs/UTT4B/Axyoma2/Backend')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.conf import settings

def obtener_config_db():
    """Obtener configuración de la base de datos"""
    db_config = settings.DATABASES['default']
    return {
        'host': db_config.get('HOST', 'localhost'),
        'port': db_config.get('PORT', '5432'),
        'name': db_config.get('NAME'),
        'user': db_config.get('USER'),
        'password': db_config.get('PASSWORD'),
    }

def crear_respaldo_compatible():
    """Crear un respaldo compatible con pgAdmin"""
    print("🔄 Creando respaldo compatible con pgAdmin...")
    
    db_config = obtener_config_db()
    
    # Directorio de respaldos
    backup_dir = Path("backups")
    backup_dir.mkdir(exist_ok=True)
    
    # Nombre del archivo
    archivo_respaldo = backup_dir / "respaldo_compatible_pgadmin.sql"
    
    # Comando pg_dump optimizado para pgAdmin
    cmd = [
        'C:/Program Files/PostgreSQL/17/bin/pg_dump.exe',
        f"--host={db_config['host']}",
        f"--port={db_config['port']}",
        f"--username={db_config['user']}",
        f"--dbname={db_config['name']}",
        '--no-password',
        '--clean',
        '--if-exists',
        '--no-owner',
        '--no-privileges',
        '--format=plain',
        '--file', str(archivo_respaldo)
    ]
    
    # Variables de entorno
    env = os.environ.copy()
    env['PGPASSWORD'] = db_config['password']
    
    print(f"📄 Archivo de destino: {archivo_respaldo}")
    print(f"🔧 Ejecutando comando...")
    
    # Ejecutar pg_dump
    result = subprocess.run(cmd, env=env, capture_output=True, text=True)
    
    if result.returncode != 0:
        print(f"❌ Error en pg_dump:")
        print(result.stderr)
        return False
    
    if not archivo_respaldo.exists():
        print("❌ El archivo de respaldo no fue creado")
        return False
    
    print(f"✅ Respaldo creado exitosamente")
    print(f"💾 Tamaño: {archivo_respaldo.stat().st_size / 1024:.2f} KB")
    
    return archivo_respaldo

def verificar_compatibilidad_pgadmin(archivo_respaldo):
    """Verificar que el respaldo sea compatible con pgAdmin"""
    print(f"\n🔍 Verificando compatibilidad con pgAdmin...")
    
    with open(archivo_respaldo, 'r', encoding='utf-8') as f:
        contenido = f.read()
    
    # Verificar comandos problemáticos
    comandos_problematicos = [
        r'\\connect',
        r'\\c ',
        r'CREATE DATABASE',
        r'DROP DATABASE'
    ]
    
    problemas_encontrados = []
    
    for comando in comandos_problematicos:
        if comando in contenido:
            problemas_encontrados.append(comando)
    
    if problemas_encontrados:
        print("❌ Comandos problemáticos encontrados:")
        for problema in problemas_encontrados:
            print(f"   - {problema}")
        return False
    else:
        print("✅ No se encontraron comandos problemáticos")
    
    # Verificar estructura básica
    elementos_esperados = [
        'SET statement_timeout = 0;',
        'SET lock_timeout = 0;',
        'SET client_encoding = ',
        'CREATE TABLE',
        'COPY '
    ]
    
    elementos_encontrados = 0
    for elemento in elementos_esperados:
        if elemento in contenido:
            elementos_encontrados += 1
    
    print(f"📋 Elementos SQL encontrados: {elementos_encontrados}/{len(elementos_esperados)}")
    
    if elementos_encontrados >= 3:
        print("✅ El respaldo tiene estructura SQL válida")
        return True
    else:
        print("⚠️ El respaldo podría tener problemas de estructura")
        return False

def mostrar_instrucciones_pgadmin():
    """Mostrar instrucciones para usar el respaldo en pgAdmin"""
    print("\n📋 INSTRUCCIONES PARA PGADMIN:")
    print("=====================================")
    print("1. Abrir pgAdmin 4")
    print("2. Conectar al servidor PostgreSQL")
    print("3. Crear una nueva base de datos (si es necesario)")
    print("4. Click derecho en la base de datos → 'Restore...'")
    print("5. Seleccionar 'Custom or tar' como formato")
    print("6. Navegar y seleccionar el archivo .sql")
    print("7. En la pestaña 'Restore options':")
    print("   ✓ Pre-data: ✅")
    print("   ✓ Data: ✅") 
    print("   ✓ Post-data: ✅")
    print("   ✓ Clean before restore: ✅ (si quieres limpiar datos existentes)")
    print("8. Click 'Restore'")
    print("\n⚠️ IMPORTANTE:")
    print("   - El respaldo NO incluye comandos CREATE DATABASE")
    print("   - Debes crear la base de datos manualmente antes de restaurar")
    print("   - Usa 'Clean before restore' solo si quieres eliminar datos existentes")

def main():
    print("🎯 PRUEBA DE RESPALDOS COMPATIBLES CON PGADMIN")
    print("=" * 50)
    
    try:
        # Crear respaldo
        archivo_respaldo = crear_respaldo_compatible()
        if not archivo_respaldo:
            print("❌ Error al crear respaldo")
            return
        
        # Verificar compatibilidad
        es_compatible = verificar_compatibilidad_pgadmin(archivo_respaldo)
        
        # Mostrar resultados
        print("\n" + "=" * 50)
        print("📊 RESULTADOS:")
        if es_compatible:
            print("✅ ÉXITO: Respaldo compatible con pgAdmin generado")
            print(f"📁 Ubicación: {archivo_respaldo}")
            mostrar_instrucciones_pgadmin()
        else:
            print("❌ FALLO: El respaldo tiene problemas de compatibilidad")
        
        print("\n🎉 Prueba completada")
        
    except Exception as e:
        print(f"❌ Error inesperado: {e}")

if __name__ == "__main__":
    main()
