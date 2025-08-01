#!/usr/bin/env python
"""
🔧 SOLUCIONADOR ESPECÍFICO PARA ERROR DE FECHA REGISTRO
====================================================
Soluciona errores relacionados con fecha_registro en tabla usuarios
"""

import os
import sys
import django
from datetime import datetime

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')
django.setup()

from django.core.management import call_command
from django.db import connection, transaction
from django.contrib.auth.models import User
from django.utils import timezone

def imprimir_paso(numero, titulo):
    """Imprimir paso con formato"""
    print(f"\n{'='*60}")
    print(f"🔧 PASO {numero}: {titulo}")
    print(f"{'='*60}")

def verificar_problema_fecha():
    """Verificar si existe el problema de fecha_registro"""
    print("🔍 Verificando problema con fecha_registro...")
    
    try:
        with connection.cursor() as cursor:
            # Verificar si existe columna fecha_registro problemática
            cursor.execute("""
                SELECT column_name, data_type, is_nullable
                FROM information_schema.columns 
                WHERE table_name = 'usuarios' 
                AND column_name LIKE '%fecha%'
            """)
            
            columnas_fecha = cursor.fetchall()
            print(f"📋 Columnas de fecha encontradas: {len(columnas_fecha)}")
            
            for col in columnas_fecha:
                print(f"  📅 {col[0]} - Tipo: {col[1]} - Nulo: {col[2]}")
            
            # Verificar tabla auth_user
            cursor.execute("""
                SELECT column_name, data_type 
                FROM information_schema.columns 
                WHERE table_name = 'auth_user' 
                AND column_name IN ('date_joined', 'last_login')
            """)
            
            columnas_auth = cursor.fetchall()
            print(f"📋 Columnas auth_user: {len(columnas_auth)}")
            
            for col in columnas_auth:
                print(f"  🔑 {col[0]} - Tipo: {col[1]}")
                
            return True
            
    except Exception as e:
        print(f"❌ Error verificando problema: {e}")
        return False

def corregir_fechas_usuarios():
    """Corregir fechas en usuarios existentes"""
    print("🔧 Corrigiendo fechas en usuarios...")
    
    try:
        # Obtener fecha actual
        ahora = timezone.now()
        
        # Actualizar usuarios sin fecha
        usuarios_sin_fecha = User.objects.filter(date_joined__isnull=True)
        count_actualizados = 0
        
        for usuario in usuarios_sin_fecha:
            usuario.date_joined = ahora
            usuario.save()
            count_actualizados += 1
            print(f"  ✅ Actualizado: {usuario.username}")
        
        # Verificar usuarios con fechas inválidas
        usuarios_fecha_invalida = User.objects.filter(date_joined__year__lt=2020)
        
        for usuario in usuarios_fecha_invalida:
            usuario.date_joined = ahora
            usuario.save()
            count_actualizados += 1
            print(f"  ✅ Corregido fecha inválida: {usuario.username}")
        
        print(f"✅ {count_actualizados} usuarios actualizados")
        return True
        
    except Exception as e:
        print(f"❌ Error corrigiendo fechas: {e}")
        return False

def limpiar_migraciones_problemáticas():
    """Limpiar migraciones que pueden causar problemas con fechas"""
    print("🧹 Limpiando migraciones problemáticas...")
    
    try:
        migration_dirs = [
            'apps/users/migrations',
            'apps/subscriptions/migrations', 
            'apps/evaluaciones/migrations'
        ]
        
        for migration_dir in migration_dirs:
            if os.path.exists(migration_dir):
                for file in os.listdir(migration_dir):
                    if file.endswith('.py') and file != '__init__.py':
                        file_path = os.path.join(migration_dir, file)
                        try:
                            os.remove(file_path)
                            print(f"  ✅ Eliminado: {file}")
                        except Exception as e:
                            print(f"  ⚠️ No se pudo eliminar {file}: {e}")
        
        print("✅ Migraciones problemáticas eliminadas")
        return True
        
    except Exception as e:
        print(f"❌ Error limpiando migraciones: {e}")
        return False

def crear_migraciones_frescas():
    """Crear migraciones frescas sin problemas de fecha"""
    print("📝 Creando migraciones frescas...")
    
    try:
        # Crear migraciones para cada app
        apps = ['users', 'subscriptions', 'evaluaciones']
        
        for app in apps:
            print(f"  📋 Creando migraciones para {app}...")
            call_command('makemigrations', app, verbosity=1)
        
        # Migración general
        print("  📋 Creando migración general...")
        call_command('makemigrations', verbosity=1)
        
        print("✅ Migraciones frescas creadas")
        return True
        
    except Exception as e:
        print(f"❌ Error creando migraciones: {e}")
        return False

def aplicar_migraciones_con_fechas():
    """Aplicar migraciones asegurando fechas correctas"""
    print("🔧 Aplicando migraciones con fechas correctas...")
    
    try:
        # Aplicar migraciones
        call_command('migrate', verbosity=1)
        
        # Verificar que las fechas estén bien
        users_count = User.objects.count()
        print(f"📊 Usuarios en sistema: {users_count}")
        
        # Corregir fechas después de migración
        corregir_fechas_usuarios()
        
        print("✅ Migraciones aplicadas con fechas correctas")
        return True
        
    except Exception as e:
        print(f"❌ Error aplicando migraciones: {e}")
        return False

def verificar_solucion():
    """Verificar que el problema esté resuelto"""
    print("✅ Verificando solución...")
    
    try:
        # Verificar usuarios
        total_users = User.objects.count()
        users_con_fecha = User.objects.filter(date_joined__isnull=False).count()
        
        print(f"📊 Total usuarios: {total_users}")
        print(f"📊 Usuarios con fecha válida: {users_con_fecha}")
        
        if total_users == users_con_fecha and total_users > 0:
            print("✅ Problema de fechas resuelto")
            return True
        else:
            print("❌ Aún hay usuarios sin fecha")
            return False
            
    except Exception as e:
        print(f"❌ Error verificando solución: {e}")
        return False

def main():
    """Función principal"""
    print("🔧 SOLUCIONADOR ESPECÍFICO - ERROR FECHA REGISTRO")
    print("=" * 60)
    print("Este script soluciona errores específicos con fecha_registro")
    print("en la tabla de usuarios que afectan nuevas instalaciones.")
    print()
    
    respuesta = input("¿Continuar con la corrección de fechas? (s/n): ").lower()
    if respuesta not in ['s', 'si', 'y', 'yes']:
        print("❌ Operación cancelada")
        return
    
    # Ejecutar pasos de corrección
    pasos = [
        (1, "VERIFICANDO PROBLEMA DE FECHAS", verificar_problema_fecha),
        (2, "LIMPIANDO MIGRACIONES PROBLEMÁTICAS", limpiar_migraciones_problemáticas),
        (3, "CREANDO MIGRACIONES FRESCAS", crear_migraciones_frescas),
        (4, "APLICANDO MIGRACIONES CON FECHAS", aplicar_migraciones_con_fechas),
        (5, "VERIFICANDO SOLUCIÓN", verificar_solucion)
    ]
    
    for numero, titulo, funcion in pasos:
        imprimir_paso(numero, titulo)
        
        try:
            if not funcion():
                print(f"\n❌ Error en paso {numero}. Revisar manualmente.")
                print("💡 Considera ejecutar solucionador_nueva_laptop.py para reset completo")
                return
        except Exception as e:
            print(f"\n❌ Excepción en paso {numero}: {e}")
            return
    
    # Mostrar resultado final
    print("\n" + "=" * 60)
    print("🎉 ¡PROBLEMA DE FECHAS CORREGIDO!")
    print("=" * 60)
    print("✅ Fechas de usuarios corregidas")
    print("✅ Migraciones aplicadas correctamente")
    print("✅ Sistema listo para usar")
    print()
    print("🚀 SIGUIENTE PASO:")
    print("   python sistema_completo_listo.py")
    print("=" * 60)

if __name__ == "__main__":
    main()
