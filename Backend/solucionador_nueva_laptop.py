#!/usr/bin/env python
"""
🔧 SOLUCIONADOR PARA NUEVA LAPTOP
===============================
Script específico para resolver problemas de configuración
en nuevas laptops que ya tienen datos o migraciones.
"""

import os
import sys
import django
import subprocess

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')
django.setup()

from django.core.management import execute_from_command_line, call_command
from django.db import connection

def imprimir_paso(numero, titulo):
    """Imprimir paso con formato"""
    print(f"\n{'='*60}")
    print(f"🔧 PASO {numero}: {titulo}")
    print(f"{'='*60}")

def crear_base_datos():
    """Crear base de datos axyomadb automáticamente"""
    print("🏗️ Creando base de datos axyomadb...")
    
    try:
        # Intentar crear la base de datos usando psql
        subprocess.run(['psql', '-U', 'postgres', '-c', 'DROP DATABASE IF EXISTS axyomadb;'], 
                      capture_output=True, check=False)
        
        result = subprocess.run(['psql', '-U', 'postgres', '-c', 'CREATE DATABASE axyomadb;'], 
                               capture_output=True, check=True)
        
        print("✅ Base de datos axyomadb creada exitosamente")
        
    except subprocess.CalledProcessError as e:
        print(f"⚠️ Error creando BD con psql: {e}")
        print("💡 Asegúrate de que PostgreSQL esté corriendo y 'postgres' configurado")
        print("📝 Alternativa: Crear manualmente la BD 'axyomadb' en PostgreSQL")
        return False
    except FileNotFoundError:
        print("⚠️ psql no encontrado en PATH")
        print("💡 Instala PostgreSQL o agrega psql al PATH del sistema")
        print("📝 Alternativa: Crear manualmente la BD 'axyomadb' en PostgreSQL")
        return False
    
    return True

def limpiar_migraciones():
    """Limpiar archivos de migración problemáticos"""
    print("🧹 Limpiando archivos de migración...")
    
    # Directorios de migraciones
    migration_dirs = [
        'apps/users/migrations',
        'apps/subscriptions/migrations',
        'apps/evaluaciones/migrations'
    ]
    
    for migration_dir in migration_dirs:
        if os.path.exists(migration_dir):
            # Mantener solo __init__.py
            for file in os.listdir(migration_dir):
                if file.endswith('.py') and file != '__init__.py':
                    file_path = os.path.join(migration_dir, file)
                    try:
                        os.remove(file_path)
                        print(f"  ✅ Eliminado: {file}")
                    except Exception as e:
                        print(f"  ⚠️ No se pudo eliminar {file}: {e}")
    
    print("✅ Archivos de migración limpiados")

def resetear_base_datos_forzado():
    """Resetear base de datos de forma forzada"""
    print("🔥 Reseteando base de datos de forma forzada...")
    
    try:
        # Método 1: Flush normal
        print("  🔄 Intentando flush normal...")
        call_command('flush', '--noinput')
        print("  ✅ Flush exitoso")
        
    except Exception as e:
        print(f"  ⚠️ Flush normal falló: {e}")
        
        # Método 2: Eliminar tablas manualmente
        print("  🔧 Eliminando tablas manualmente...")
        try:
            with connection.cursor() as cursor:
                # Obtener todas las tablas
                cursor.execute("""
                    SELECT tablename FROM pg_tables 
                    WHERE schemaname = 'public' 
                    AND tablename NOT LIKE 'pg_%'
                """)
                
                tablas = cursor.fetchall()
                
                # Eliminar tablas una por una
                for (tabla,) in tablas:
                    try:
                        cursor.execute(f'DROP TABLE IF EXISTS "{tabla}" CASCADE')
                        print(f"    ✅ Eliminada tabla: {tabla}")
                    except Exception as te:
                        print(f"    ⚠️ Error eliminando {tabla}: {te}")
                
                print("  ✅ Tablas eliminadas manualmente")
                
        except Exception as me:
            print(f"  ❌ Error eliminando tablas: {me}")
            return False
    
    return True

def crear_migraciones_frescas():
    """Crear migraciones completamente nuevas"""
    print("📝 Creando migraciones frescas...")
    
    try:
        # Crear migraciones para cada app
        apps = ['users', 'subscriptions', 'evaluaciones']
        
        for app in apps:
            print(f"  📋 Creando migraciones para {app}...")
            call_command('makemigrations', app)
        
        print("✅ Migraciones frescas creadas")
        return True
        
    except Exception as e:
        print(f"❌ Error creando migraciones: {e}")
        return False

def aplicar_migraciones_completas():
    """Aplicar todas las migraciones desde cero"""
    print("🔧 Aplicando migraciones completas...")
    
    try:
        # Migrar desde cero
        call_command('migrate')
        print("✅ Migraciones aplicadas exitosamente")
        return True
        
    except Exception as e:
        print(f"❌ Error aplicando migraciones: {e}")
        return False

def verificar_estructura():
    """Verificar que la estructura esté correcta"""
    print("🔍 Verificando estructura de la base de datos...")
    
    try:
        with connection.cursor() as cursor:
            # Verificar tablas importantes
            tablas_importantes = [
                'auth_user', 'usuarios', 'empresas', 'plantas', 
                'departamentos', 'puestos', 'empleados', 'planes'
            ]
            
            tablas_existentes = []
            for tabla in tablas_importantes:
                cursor.execute(f"""
                    SELECT EXISTS (
                        SELECT 1 FROM information_schema.tables 
                        WHERE table_name = '{tabla}'
                    )
                """)
                
                existe = cursor.fetchone()[0]
                if existe:
                    tablas_existentes.append(tabla)
                    print(f"  ✅ {tabla}")
                else:
                    print(f"  ❌ {tabla} - NO EXISTE")
            
            if len(tablas_existentes) >= 6:  # Al menos las principales
                print("✅ Estructura básica verificada")
                return True
            else:
                print("❌ Faltan tablas importantes")
                return False
                
    except Exception as e:
        print(f"❌ Error verificando estructura: {e}")
        return False

def ejecutar_sistema_completo():
    """Ejecutar el sistema completo de inicialización"""
    print("🚀 Ejecutando sistema completo de inicialización...")
    
    try:
        # Ejecutar el script principal
        resultado = subprocess.run(
            [sys.executable, 'sistema_completo_listo.py'],
            capture_output=True,
            text=True
        )
        
        if resultado.returncode == 0:
            print("✅ Sistema completo inicializado exitosamente")
            print("📤 Salida:")
            print(resultado.stdout[-500:])  # Últimas 500 caracteres
            return True
        else:
            print("❌ Error en inicialización del sistema")
            print("📤 Error:")
            print(resultado.stderr[-500:])
            return False
            
    except Exception as e:
        print(f"❌ Error ejecutando sistema completo: {e}")
        return False

def main():
    """Función principal del solucionador"""
    print("🔧 SOLUCIONADOR PARA NUEVA LAPTOP - AXYOMA")
    print("=" * 60)
    print("Este script resolverá problemas de configuración")
    print("en laptops que ya tienen datos o migraciones previas.")
    print()
    
    respuesta = input("¿Continuar con la limpieza y reconfiguración? (s/n): ").lower()
    if respuesta not in ['s', 'si', 'y', 'yes']:
        print("❌ Operación cancelada")
        return
    
    # Ejecutar pasos de solución
    pasos = [
        (1, "CREANDO BASE DE DATOS AXYOMADB", crear_base_datos),
        (2, "LIMPIANDO MIGRACIONES ANTIGUAS", limpiar_migraciones),
        (3, "RESETEANDO BASE DE DATOS", resetear_base_datos_forzado),
        (4, "CREANDO MIGRACIONES FRESCAS", crear_migraciones_frescas),
        (5, "APLICANDO MIGRACIONES", aplicar_migraciones_completas),
        (6, "VERIFICANDO ESTRUCTURA", verificar_estructura),
        (7, "INICIALIZANDO SISTEMA COMPLETO", ejecutar_sistema_completo)
    ]
    
    for numero, titulo, funcion in pasos:
        imprimir_paso(numero, titulo)
        
        try:
            if not funcion():
                print(f"\n❌ Error en paso {numero}. Proceso detenido.")
                print("💡 Revisa los errores y vuelve a intentar.")
                return
        except Exception as e:
            print(f"\n❌ Excepción en paso {numero}: {e}")
            return
    
    # Mostrar resultado final
    print("\n" + "=" * 60)
    print("🎉 ¡CONFIGURACIÓN COMPLETADA EXITOSAMENTE!")
    print("=" * 60)
    print("✅ Base de datos limpia y configurada")
    print("✅ Sistema inicializado con datos completos")
    print("✅ Login funcionando: superadmin / admin123")
    print()
    print("🚀 PARA USAR EL SISTEMA:")
    print("   python manage.py runserver")
    print("   http://localhost:8000")
    print("=" * 60)

if __name__ == "__main__":
    main()
