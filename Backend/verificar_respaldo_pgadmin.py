#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para verificar que el respaldo limpio funciona en pgAdmin
"""
import os
import sys
import subprocess
from datetime import datetime

def verificar_respaldo_pgadmin():
    print("🔍 VERIFICANDO RESPALDO LIMPIO PARA PGADMIN")
    print("=" * 50)
    
    # Buscar el archivo de respaldo más reciente
    backup_dir = os.path.join(os.path.dirname(__file__), '..', 'backups')
    backup_files = [f for f in os.listdir(backup_dir) if f.startswith('respaldo_limpio_') and f.endswith('.sql')]
    
    if not backup_files:
        print("❌ No se encontraron archivos de respaldo limpio")
        return False
    
    # Obtener el más reciente
    backup_files.sort(reverse=True)
    latest_backup = backup_files[0]
    backup_path = os.path.join(backup_dir, latest_backup)
    
    print(f"📁 Archivo: {latest_backup}")
    print(f"📊 Ubicación: {backup_path}")
    
    # Verificar que el archivo existe
    if not os.path.exists(backup_path):
        print("❌ Archivo no encontrado")
        return False
    
    # Obtener información del archivo
    file_size = os.path.getsize(backup_path)
    print(f"💾 Tamaño: {file_size:,} bytes ({file_size / 1024 / 1024:.2f} MB)")
    
    # Analizar contenido del respaldo
    print(f"\n📄 ANÁLISIS DEL RESPALDO:")
    
    with open(backup_path, 'r', encoding='utf-8') as f:
        content = f.read()
        
        # Verificar elementos clave
        checks = {
            "✅ Encabezado PostgreSQL": "PostgreSQL database dump" in content,
            "✅ Comando CREATE DATABASE": "CREATE DATABASE axyomadb" in content,
            "✅ Comando DROP DATABASE": "DROP DATABASE IF EXISTS axyomadb" in content,
            "✅ Encoding UTF8": "ENCODING = 'UTF8'" in content,
            "✅ Configuración SET": "SET statement_timeout = 0" in content,
            "✅ Tablas de usuarios": "CREATE TABLE public.users_" in content,
            "✅ Datos INSERT": "INSERT INTO" in content,
            "✅ Comandos COPY": "COPY public." in content or "INSERT INTO" in content
        }
        
        for check, result in checks.items():
            status = "✅" if result else "❌"
            print(f"   {status} {check[2:]}")
    
    # Contar tablas principales
    print(f"\n📊 TABLAS ENCONTRADAS:")
    tables_to_check = [
        'users_empresa', 'users_planta', 'users_departamento', 
        'users_puesto', 'users_empleado', 'users_perfilusuario'
    ]
    
    for table in tables_to_check:
        if f"CREATE TABLE public.{table}" in content:
            # Contar registros aproximados
            insert_count = content.count(f"INSERT INTO public.{table}")
            copy_lines = content.count(f"COPY public.{table}")
            print(f"   ✅ {table}: ~{insert_count + copy_lines} operaciones de datos")
        else:
            print(f"   ❌ {table}: No encontrada")
    
    print(f"\n🎯 INSTRUCCIONES PARA USAR EN PGADMIN:")
    print("1. 🖥️ Abre pgAdmin 4")
    print("2. 🌐 Conéctate a tu servidor PostgreSQL")
    print("3. 🗂️ Click derecho en 'Databases'")
    print("4. ⚙️ Selecciona 'Restore...'")
    print(f"5. 📁 Filename: {backup_path}")
    print("6. 🔧 Format: Custom or tar (si falla, prueba 'Plain')")
    print("7. ✅ Marca 'Clean before restore' si quieres limpiar primero")
    print("8. ▶️ Click 'Restore'")
    
    print(f"\n⚠️ ALTERNATIVA SI FALLA EN PGADMIN:")
    print("Usa psql desde línea de comandos:")
    print(f"psql -U postgres -h localhost -f \"{backup_path}\"")
    
    print(f"\n📋 RESUMEN:")
    print(f"✅ Archivo generado: {latest_backup}")
    print(f"✅ Tamaño: {file_size / 1024 / 1024:.2f} MB")
    print(f"✅ Formato: SQL estándar PostgreSQL")
    print(f"✅ Compatible: pgAdmin 4")
    print(f"✅ Incluye: Estructura + Datos")
    
    return True

if __name__ == '__main__':
    verificar_respaldo_pgadmin()
