#!/usr/bin/env python
"""
Script SIMPLE para crear usuarios Django desde la tabla usuarios
sin usar los modelos ORM para evitar conflictos de estructura.
"""

import os
import sys
import django
from django.db import connection

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')
django.setup()

from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

def crear_usuarios_django():
    """Crear usuarios Django desde la tabla usuarios usando SQL directo"""
    print("🔄 CREANDO USUARIOS DJANGO...")
    print("=" * 60)
    
    try:
        with connection.cursor() as cursor:
            # Obtener usuarios de la tabla usuarios
            cursor.execute("""
                SELECT id, nombre, apellido_paterno, apellido_materno, 
                       correo, nivel_usuario, status
                FROM usuarios
            """)
            usuarios_sql = cursor.fetchall()
            
            print(f"📋 Encontrados {len(usuarios_sql)} usuarios en la tabla 'usuarios'")
            
            for usuario_data in usuarios_sql:
                id_usuario, nombre, apellido_paterno, apellido_materno, correo, nivel_usuario, status = usuario_data
                
                print(f"\n👤 Procesando: {nombre} {apellido_paterno} ({correo})")
                
                # Verificar si ya existe el usuario Django por email
                cursor.execute("SELECT id FROM auth_user WHERE email = %s", [correo])
                existing_user = cursor.fetchone()
                
                if existing_user:
                    print(f"   ✓ Usuario Django ya existe (ID: {existing_user[0]})")
                    django_user_id = existing_user[0]
                else:
                    # Crear username único
                    username = correo.split('@')[0]
                    original_username = username
                    counter = 1
                    
                    while True:
                        cursor.execute("SELECT id FROM auth_user WHERE username = %s", [username])
                        if not cursor.fetchone():
                            break
                        username = f"{original_username}{counter}"
                        counter += 1
                    
                    # Crear el usuario Django usando SQL directo
                    password_hash = make_password('1234')
                    
                    cursor.execute("""
                        INSERT INTO auth_user (
                            password, last_login, is_superuser, username, first_name, 
                            last_name, email, is_staff, is_active, date_joined
                        ) VALUES (
                            %s, NULL, %s, %s, %s, %s, %s, %s, TRUE, NOW()
                        ) RETURNING id
                    """, [
                        password_hash,
                        nivel_usuario == 'superadmin',  # is_superuser
                        username,
                        nombre,
                        f"{apellido_paterno} {apellido_materno or ''}".strip(),
                        correo,
                        nivel_usuario in ['superadmin', 'admin-empresa', 'admin-planta']  # is_staff
                    ])
                    
                    django_user_id = cursor.fetchone()[0]
                    print(f"   ✓ Usuario Django creado (username: {username}, ID: {django_user_id})")
                
                # Actualizar la tabla usuarios con el user_id
                cursor.execute(
                    "UPDATE usuarios SET user_id = %s WHERE id = %s",
                    [django_user_id, id_usuario]
                )
                print(f"   ✓ Vinculado user_id {django_user_id} con usuario {id_usuario}")
                
        print("\n" + "=" * 60)
        print("✅ USUARIOS DJANGO CREADOS")
        
        # Mostrar resumen
        cursor.execute("SELECT COUNT(*) FROM auth_user")
        total_usuarios = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM usuarios WHERE user_id IS NOT NULL")
        usuarios_vinculados = cursor.fetchone()[0]
        
        print(f"📊 RESUMEN:")
        print(f"   - Usuarios Django: {total_usuarios}")
        print(f"   - Usuarios vinculados: {usuarios_vinculados}")
        
        return True
        
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def probar_login():
    """Probar login con los usuarios creados"""
    print("\n🔑 PROBANDO LOGIN...")
    print("=" * 60)
    
    try:
        from django.contrib.auth import authenticate
        
        # Obtener usuarios para probar
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT u.correo, u.nivel_usuario, au.username 
                FROM usuarios u 
                JOIN auth_user au ON u.user_id = au.id 
                LIMIT 4
            """)
            usuarios_test = cursor.fetchall()
            
            print("Probando login con contraseña '1234':")
            for correo, nivel, username in usuarios_test:
                user = authenticate(username=username, password='1234')
                if user:
                    print(f"   ✅ {correo} (username: {username}, nivel: {nivel}) - LOGIN OK")
                else:
                    print(f"   ❌ {correo} (username: {username}, nivel: {nivel}) - LOGIN FALLÓ")
        
        return True
        
    except Exception as e:
        print(f"❌ ERROR en prueba de login: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def mostrar_credenciales():
    """Mostrar las credenciales para login"""
    print("\n🔑 CREDENCIALES PARA LOGIN:")
    print("=" * 60)
    
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT u.nombre, u.correo, u.nivel_usuario, au.username 
                FROM usuarios u 
                JOIN auth_user au ON u.user_id = au.id 
                ORDER BY u.nivel_usuario, u.nombre
            """)
            usuarios = cursor.fetchall()
            
            print("Todos los usuarios tienen contraseña: 1234")
            print()
            for nombre, correo, nivel, username in usuarios:
                print(f"👤 {nombre} ({nivel})")
                print(f"   Email: {correo}")
                print(f"   Username: {username}")
                print(f"   Password: 1234")
                print()
        
        return True
        
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        return False

if __name__ == "__main__":
    print("🚀 CONFIGURACIÓN DE USUARIOS PARA LOGIN")
    print()
    
    crear_ok = crear_usuarios_django()
    login_ok = probar_login()
    
    if crear_ok and login_ok:
        mostrar_credenciales()
        print("🎉 ¡USUARIOS LISTOS PARA LOGIN!")
        print("   - Usuarios Django creados")
        print("   - Login funcionando")
        print("   - Credenciales mostradas arriba")
        sys.exit(0)
    else:
        print("\n⚠️  PROBLEMAS EN CONFIGURACIÓN")
        sys.exit(1)
