#!/usr/bin/env python
"""
Script para inicializar la base de datos y crear un usuario superadmin
"""

import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')
django.setup()

from django.contrib.auth.models import User
from django.db import connection, transaction
from django.core.management import call_command

def ejecutar_migraciones():
    """Ejecutar todas las migraciones pendientes"""
    print("🔄 Ejecutando migraciones...")
    try:
        call_command('migrate', interactive=False)
        print("✅ Migraciones completadas")
        return True
    except Exception as e:
        print(f"❌ Error ejecutando migraciones: {str(e)}")
        return False

def crear_superadmin():
    """Crear un superadmin básico"""
    print("\n🔑 Creando usuario SuperAdmin...")
    try:
        # Verificar si existe el usuario
        if User.objects.filter(username='superadmin').exists():
            user = User.objects.get(username='superadmin')
            user.set_password('1234')
            user.is_staff = True
            user.is_superuser = True
            user.save()
            print("✅ Usuario SuperAdmin actualizado")
        else:
            # Crear nuevo superusuario
            User.objects.create_superuser(
                username='superadmin',
                email='superadmin@axyoma.com',
                password='1234',
                first_name='Super',
                last_name='Admin'
            )
            print("✅ Usuario SuperAdmin creado")
        
        # Verificar la estructura de la tabla usuarios primero
        with connection.cursor() as cursor:
            # Obtener el nombre exacto de las columnas en la tabla usuarios
            cursor.execute("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name = 'usuarios'
            """)
            columnas = [col[0] for col in cursor.fetchall()]
            print(f"📋 Columnas en tabla 'usuarios': {', '.join(columnas)}")
            
            # Verificar si existe el perfil de superadmin
            cursor.execute("SELECT COUNT(*) FROM usuarios WHERE user_id = (SELECT id FROM auth_user WHERE username = 'superadmin')")
            resultado = cursor.fetchone()
            
            if resultado[0] == 0:
                # Crear perfil directamente en la base de datos
                with transaction.atomic():
                    user = User.objects.get(username='superadmin')
                    
                    # Construir la consulta SQL basada en las columnas existentes
                    if 'admin_empresa' in columnas:
                        # Usar admin_empresa si existe (sin _id)
                        cursor.execute("""
                            INSERT INTO usuarios 
                            (nombre, apellido_paterno, correo, nivel_usuario, status, user_id, admin_empresa, fecha_registro) 
                            VALUES (%s, %s, %s, %s, %s, %s, NULL, NOW())
                        """, ['Super', 'Admin', 'superadmin@axyoma.com', 'superadmin', True, user.id])
                    else:
                        # Versión básica sin admin_empresa
                        cursor.execute("""
                            INSERT INTO usuarios 
                            (nombre, apellido_paterno, correo, nivel_usuario, status, user_id, fecha_registro) 
                            VALUES (%s, %s, %s, %s, %s, %s, NOW())
                        """, ['Super', 'Admin', 'superadmin@axyoma.com', 'superadmin', True, user.id])
                    
                print("✅ Perfil de usuario creado manualmente en la tabla 'usuarios'")
        
        print("\n📝 CREDENCIALES SUPERADMIN:")
        print("   Usuario: superadmin")
        print("   Contraseña: 1234")
        
        return True
    except Exception as e:
        print(f"❌ Error creando superadmin: {str(e)}")
        return False

def verificar_estructura_bd():
    """Verificar la estructura de la base de datos"""
    print("\n🔍 Verificando estructura de la base de datos...")
    tablas_requeridas = [
        'auth_user', 
        'usuarios', 
        'empresas', 
        'plantas', 
        'departamentos', 
        'puestos'
    ]
    
    tablas_faltantes = []
    
    try:
        with connection.cursor() as cursor:
            for tabla in tablas_requeridas:
                try:
                    cursor.execute(f"SELECT COUNT(*) FROM {tabla}")
                    cursor.fetchone()
                    print(f"✅ Tabla '{tabla}' existe")
                except Exception as e:
                    print(f"❌ Tabla '{tabla}' no existe: {str(e)}")
                    tablas_faltantes.append(tabla)
        
        if tablas_faltantes:
            print(f"\n⚠️ Faltan {len(tablas_faltantes)} tablas en la base de datos")
            return False
        else:
            print("✅ Todas las tablas requeridas existen")
            return True
    except Exception as e:
        print(f"❌ Error verificando estructura de BD: {str(e)}")
        return False

def main():
    print("\n🚀 INICIALIZACIÓN DE BASE DE DATOS AXYOMA")
    print("=" * 60)
    
    # 1. Verificar estructura de la base de datos
    estructura_ok = verificar_estructura_bd()
    
    if not estructura_ok:
        print("\n⚠️ La estructura de la base de datos no está completa.")
        respuesta = input("¿Desea ejecutar las migraciones para crear las tablas faltantes? (s/n): ")
        if respuesta.lower() == 's':
            ejecutar_migraciones()
        else:
            print("❌ Operación cancelada por el usuario")
            return
    
    # 2. Crear superadmin
    crear_superadmin()
    
    print("\n🏁 INICIALIZACIÓN COMPLETADA")
    print("\nAhora puede intentar iniciar sesión con:")
    print("  Usuario: superadmin")
    print("  Contraseña: 1234")

if __name__ == "__main__":
    main()
