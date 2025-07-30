#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para generar respaldo limpio de la base de datos compatible con pgAdmin
"""
import os
import sys
import subprocess
import django
from datetime import datetime

# Configurar Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.base')
django.setup()

from django.conf import settings

def generar_respaldo_limpio():
    print("🔄 GENERANDO RESPALDO LIMPIO COMPATIBLE CON PGADMIN")
    print("=" * 60)
    
    # Configuración de la base de datos
    db_config = settings.DATABASES['default']
    db_name = db_config['NAME']
    db_user = db_config['USER']
    db_password = db_config['PASSWORD']
    db_host = db_config['HOST'] or 'localhost'
    db_port = db_config['PORT'] or '5432'
    
    print(f"📊 Base de datos: {db_name}")
    print(f"🖥️ Host: {db_host}:{db_port}")
    print(f"👤 Usuario: {db_user}")
    
    # Crear directorio de respaldos
    backup_dir = os.path.join(os.path.dirname(__file__), '..', 'backups')
    os.makedirs(backup_dir, exist_ok=True)
    
    # Nombre del archivo de respaldo
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_filename = f"respaldo_limpio_{timestamp}.sql"
    backup_path = os.path.join(backup_dir, backup_filename)
    
    print(f"💾 Archivo: {backup_filename}")
    
    # Comando pg_dump con opciones para pgAdmin
    pg_dump_cmd = [
        'pg_dump',
        '--host', db_host,
        '--port', str(db_port),
        '--username', db_user,
        '--dbname', db_name,
        '--no-password',
        '--verbose',
        '--clean',                # Incluir comandos DROP
        '--if-exists',           # Solo DROP si existe
        '--create',              # Incluir comando CREATE DATABASE
        '--encoding', 'UTF8',    # Encoding UTF-8
        '--no-owner',            # Sin comandos de propietario
        '--no-privileges',       # Sin comandos de privilegios
        '--file', backup_path
    ]
    
    # Configurar variable de entorno para password
    env = os.environ.copy()
    env['PGPASSWORD'] = db_password
    
    print("\n🚀 EJECUTANDO RESPALDO...")
    print("Comando:", ' '.join(pg_dump_cmd))
    
    try:
        # Ejecutar pg_dump
        result = subprocess.run(
            pg_dump_cmd,
            env=env,
            capture_output=True,
            text=True,
            check=True
        )
        
        print("✅ RESPALDO COMPLETADO EXITOSAMENTE")
        print(f"📁 Ubicación: {backup_path}")
        
        # Verificar que el archivo se creó
        if os.path.exists(backup_path):
            file_size = os.path.getsize(backup_path)
            print(f"📊 Tamaño: {file_size:,} bytes ({file_size / 1024 / 1024:.2f} MB)")
            
            # Mostrar primeras líneas del archivo
            print("\n📄 CONTENIDO DEL RESPALDO (primeras líneas):")
            with open(backup_path, 'r', encoding='utf-8') as f:
                for i, line in enumerate(f):
                    if i >= 10:
                        break
                    print(f"   {line.rstrip()}")
            
            print("\n🎯 PARA USAR EN PGADMIN:")
            print("1. Abre pgAdmin")
            print("2. Click derecho en tu base de datos")
            print("3. Restore > Selecciona el archivo SQL")
            print(f"4. Archivo: {backup_path}")
            print("5. Ejecuta la restauración")
            
            return backup_path
        else:
            print("❌ ERROR: El archivo de respaldo no se creó")
            return None
            
    except subprocess.CalledProcessError as e:
        print(f"❌ ERROR EN PG_DUMP:")
        print(f"Código de salida: {e.returncode}")
        print(f"STDOUT: {e.stdout}")
        print(f"STDERR: {e.stderr}")
        
        # Verificar si pg_dump está instalado
        try:
            subprocess.run(['pg_dump', '--version'], capture_output=True, check=True)
        except FileNotFoundError:
            print("\n💡 SOLUCIÓN: Instala PostgreSQL client tools")
            print("🔗 Descarga: https://www.postgresql.org/download/windows/")
            print("📌 Asegúrate de que pg_dump esté en el PATH")
            
        return None
    except Exception as e:
        print(f"❌ ERROR INESPERADO: {str(e)}")
        return None

def verificar_postgresql_tools():
    """Verificar que las herramientas de PostgreSQL están disponibles"""
    print("\n🔍 VERIFICANDO HERRAMIENTAS POSTGRESQL...")
    
    tools = ['pg_dump', 'psql', 'pg_restore']
    available_tools = []
    
    for tool in tools:
        try:
            result = subprocess.run([tool, '--version'], capture_output=True, text=True, check=True)
            version = result.stdout.strip().split('\n')[0]
            print(f"✅ {tool}: {version}")
            available_tools.append(tool)
        except FileNotFoundError:
            print(f"❌ {tool}: No encontrado")
        except Exception as e:
            print(f"⚠️ {tool}: Error - {str(e)}")
    
    return available_tools

if __name__ == '__main__':
    print("🛠️ RESPALDO LIMPIO PARA PGADMIN - AXYOMA")
    print("=" * 50)
    
    # Verificar herramientas
    tools = verificar_postgresql_tools()
    
    if 'pg_dump' not in tools:
        print("\n❌ FALTA PG_DUMP")
        print("No se puede generar el respaldo sin pg_dump")
        sys.exit(1)
    
    # Generar respaldo
    backup_path = generar_respaldo_limpio()
    
    if backup_path:
        print(f"\n🎉 ¡RESPALDO LIMPIO GENERADO EXITOSAMENTE!")
        print(f"📁 {backup_path}")
        print("✅ Compatible con pgAdmin")
    else:
        print("\n❌ FALLO AL GENERAR RESPALDO")
        sys.exit(1)
