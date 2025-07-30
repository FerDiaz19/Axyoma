#!/usr/bin/env python
"""
Script para crear respaldos completos y parciales de la base de datos
"""

import os
import sys
import django
import subprocess
from datetime import datetime
import json

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')
django.setup()

from django.conf import settings

def obtener_configuracion_db():
    """Obtener configuración de la base de datos"""
    db_config = settings.DATABASES['default']
    return {
        'host': db_config.get('HOST', 'localhost'),
        'port': db_config.get('PORT', '5432'),
        'name': db_config.get('NAME'),
        'user': db_config.get('USER'),
        'password': db_config.get('PASSWORD')
    }

def crear_respaldo_completo():
    """Crear respaldo completo de la base de datos"""
    print("💾 CREANDO RESPALDO COMPLETO DE LA BASE DE DATOS")
    print("=" * 60)
    
    try:
        db_config = obtener_configuracion_db()
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Crear directorio de respaldos si no existe
        backup_dir = os.path.join(os.path.dirname(__file__), '..', 'backups')
        os.makedirs(backup_dir, exist_ok=True)
        
        # Nombre del archivo de respaldo
        backup_file = os.path.join(backup_dir, f"respaldo_completo_{timestamp}.sql")
        
        # Configurar variables de entorno para PostgreSQL
        env = os.environ.copy()
        env['PGPASSWORD'] = db_config['password']
        
        # Comando pg_dump
        cmd = [
            'pg_dump',
            '-h', db_config['host'],
            '-p', str(db_config['port']),
            '-U', db_config['user'],
            '-d', db_config['name'],
            '--verbose',
            '--clean',
            '--create',
            '--if-exists',
            '-f', backup_file
        ]
        
        print(f"🔄 Ejecutando respaldo...")
        print(f"📁 Archivo: {backup_file}")
        
        resultado = subprocess.run(cmd, env=env, capture_output=True, text=True)
        
        if resultado.returncode == 0:
            # Verificar que el archivo se creó y tiene contenido
            if os.path.exists(backup_file) and os.path.getsize(backup_file) > 0:
                file_size = os.path.getsize(backup_file) / (1024 * 1024)  # MB
                print(f"✅ Respaldo completo creado exitosamente")
                print(f"📁 Archivo: {backup_file}")
                print(f"📊 Tamaño: {file_size:.2f} MB")
                
                # Crear archivo de metadata
                metadata = {
                    'tipo': 'completo',
                    'fecha': timestamp,
                    'archivo': backup_file,
                    'tamaño_mb': round(file_size, 2),
                    'base_datos': db_config['name']
                }
                
                metadata_file = backup_file.replace('.sql', '_metadata.json')
                with open(metadata_file, 'w') as f:
                    json.dump(metadata, f, indent=2)
                
                return backup_file
            else:
                print("❌ El archivo de respaldo está vacío o no se creó")
                return None
        else:
            print(f"❌ Error en pg_dump: {resultado.stderr}")
            return None
            
    except Exception as e:
        print(f"❌ Error creando respaldo completo: {e}")
        return None

def crear_respaldo_parcial(tablas):
    """Crear respaldo parcial de tablas específicas"""
    print(f"💾 CREANDO RESPALDO PARCIAL ({len(tablas)} tablas)")
    print("=" * 60)
    
    try:
        db_config = obtener_configuracion_db()
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Crear directorio de respaldos si no existe
        backup_dir = os.path.join(os.path.dirname(__file__), '..', 'backups')
        os.makedirs(backup_dir, exist_ok=True)
        
        # Nombre del archivo de respaldo
        tablas_str = "_".join(tablas)
        backup_file = os.path.join(backup_dir, f"respaldo_parcial_{tablas_str}_{timestamp}.sql")
        
        # Configurar variables de entorno para PostgreSQL
        env = os.environ.copy()
        env['PGPASSWORD'] = db_config['password']
        
        # Comando pg_dump para tablas específicas
        cmd = [
            'pg_dump',
            '-h', db_config['host'],
            '-p', str(db_config['port']),
            '-U', db_config['user'],
            '-d', db_config['name'],
            '--verbose',
            '--data-only',  # Solo datos, no estructura
            '-f', backup_file
        ]
        
        # Agregar cada tabla
        for tabla in tablas:
            cmd.extend(['-t', tabla])
        
        print(f"🔄 Ejecutando respaldo parcial...")
        print(f"📋 Tablas: {', '.join(tablas)}")
        print(f"📁 Archivo: {backup_file}")
        
        resultado = subprocess.run(cmd, env=env, capture_output=True, text=True)
        
        if resultado.returncode == 0:
            if os.path.exists(backup_file) and os.path.getsize(backup_file) > 0:
                file_size = os.path.getsize(backup_file) / (1024 * 1024)  # MB
                print(f"✅ Respaldo parcial creado exitosamente")
                print(f"📁 Archivo: {backup_file}")
                print(f"📊 Tamaño: {file_size:.2f} MB")
                
                # Crear archivo de metadata
                metadata = {
                    'tipo': 'parcial',
                    'fecha': timestamp,
                    'archivo': backup_file,
                    'tamaño_mb': round(file_size, 2),
                    'tablas': tablas,
                    'base_datos': db_config['name']
                }
                
                metadata_file = backup_file.replace('.sql', '_metadata.json')
                with open(metadata_file, 'w') as f:
                    json.dump(metadata, f, indent=2)
                
                return backup_file
            else:
                print("❌ El archivo de respaldo está vacío o no se creó")
                return None
        else:
            print(f"❌ Error en pg_dump: {resultado.stderr}")
            return None
            
    except Exception as e:
        print(f"❌ Error creando respaldo parcial: {e}")
        return None

def listar_respaldos():
    """Listar respaldos existentes"""
    print("📋 RESPALDOS EXISTENTES")
    print("=" * 60)
    
    backup_dir = os.path.join(os.path.dirname(__file__), '..', 'backups')
    
    if not os.path.exists(backup_dir):
        print("📁 No existe directorio de respaldos")
        return []
    
    respaldos = []
    for archivo in os.listdir(backup_dir):
        if archivo.endswith('.sql'):
            filepath = os.path.join(backup_dir, archivo)
            size_mb = os.path.getsize(filepath) / (1024 * 1024)
            
            # Buscar metadata
            metadata_file = filepath.replace('.sql', '_metadata.json')
            metadata = {}
            if os.path.exists(metadata_file):
                try:
                    with open(metadata_file, 'r') as f:
                        metadata = json.load(f)
                except:
                    pass
            
            respaldo_info = {
                'archivo': archivo,
                'path': filepath,
                'tamaño_mb': round(size_mb, 2),
                'metadata': metadata
            }
            respaldos.append(respaldo_info)
    
    respaldos.sort(key=lambda x: x['archivo'], reverse=True)
    
    if respaldos:
        for i, respaldo in enumerate(respaldos, 1):
            tipo = respaldo['metadata'].get('tipo', 'desconocido')
            fecha = respaldo['metadata'].get('fecha', 'desconocida')
            print(f"{i}. {respaldo['archivo']}")
            print(f"   Tipo: {tipo.upper()}")
            print(f"   Fecha: {fecha}")
            print(f"   Tamaño: {respaldo['tamaño_mb']} MB")
            if tipo == 'parcial' and 'tablas' in respaldo['metadata']:
                print(f"   Tablas: {', '.join(respaldo['metadata']['tablas'])}")
            print()
    else:
        print("📭 No hay respaldos disponibles")
    
    return respaldos

def menu_principal():
    """Menú principal del sistema de respaldos"""
    while True:
        print("\n💾 SISTEMA DE RESPALDOS AXYOMA")
        print("=" * 40)
        print("1. Crear respaldo completo")
        print("2. Crear respaldo parcial (tablas específicas)")
        print("3. Listar respaldos existentes")
        print("4. Respaldo de empleados únicamente")
        print("5. Respaldo de estructura organizacional")
        print("6. Salir")
        print("=" * 40)
        
        opcion = input("Selecciona una opción (1-6): ").strip()
        
        if opcion == '1':
            crear_respaldo_completo()
            
        elif opcion == '2':
            print("\nTablas disponibles:")
            tablas_disponibles = [
                'empleados', 'puestos', 'departamentos', 'plantas', 'empresas',
                'usuarios', 'evaluaciones', 'asignaciones', 'respuestas_empleado'
            ]
            
            for i, tabla in enumerate(tablas_disponibles, 1):
                print(f"{i}. {tabla}")
            
            seleccion = input("\nIngresa los números de las tablas separados por coma: ").strip()
            try:
                indices = [int(x.strip()) - 1 for x in seleccion.split(',')]
                tablas_seleccionadas = [tablas_disponibles[i] for i in indices if 0 <= i < len(tablas_disponibles)]
                
                if tablas_seleccionadas:
                    crear_respaldo_parcial(tablas_seleccionadas)
                else:
                    print("❌ No se seleccionaron tablas válidas")
            except:
                print("❌ Selección inválida")
                
        elif opcion == '3':
            listar_respaldos()
            
        elif opcion == '4':
            crear_respaldo_parcial(['empleados'])
            
        elif opcion == '5':
            crear_respaldo_parcial(['empresas', 'plantas', 'departamentos', 'puestos'])
            
        elif opcion == '6':
            print("👋 ¡Hasta luego!")
            break
            
        else:
            print("❌ Opción inválida")

if __name__ == "__main__":
    menu_principal()
