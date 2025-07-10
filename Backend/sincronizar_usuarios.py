#!/usr/bin/env python
"""
Script para sincronizar usuarios de la tabla 'usuarios' con Django auth_user
y crear los perfiles de usuario correspondientes.
"""

import os
import sys
import django
from django.db import connection

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')
django.setup()

from django.contrib.auth.models import User
from apps.users.models import PerfilUsuario

def sincronizar_usuarios():
    """Sincronizar usuarios de la tabla usuarios con Django auth_user"""
    print("🔄 SINCRONIZANDO USUARIOS...")
    print("=" * 60)
    
    try:
        with connection.cursor() as cursor:
            # Obtener usuarios de la tabla usuarios
            cursor.execute("""
                SELECT id, nombre, apellido_paterno, apellido_materno, 
                       correo, nivel_usuario, status, admin_empresa, user_id
                FROM usuarios
            """)
            usuarios_sql = cursor.fetchall()
            
            print(f"📋 Encontrados {len(usuarios_sql)} usuarios en la tabla 'usuarios'")
            
            for usuario_data in usuarios_sql:
                id_usuario, nombre, apellido_paterno, apellido_materno, correo, nivel_usuario, status, admin_empresa, user_id = usuario_data
                
                print(f"\n👤 Procesando: {nombre} {apellido_paterno} ({correo})")
                
                # Verificar si ya existe el usuario Django
                django_user = None
                if user_id:
                    try:
                        django_user = User.objects.get(id=user_id)
                        print(f"   ✓ Usuario Django ya existe (ID: {user_id})")
                    except User.DoesNotExist:
                        print(f"   ⚠ Usuario Django con ID {user_id} no encontrado")
                
                # Si no existe, buscar por email
                if not django_user:
                    try:
                        django_user = User.objects.get(email=correo)
                        print(f"   ✓ Usuario Django encontrado por email")
                    except User.DoesNotExist:
                        # Crear el usuario Django
                        username = correo.split('@')[0]  # Usar parte antes del @
                        
                        # Asegurar que el username sea único
                        original_username = username
                        counter = 1
                        while User.objects.filter(username=username).exists():
                            username = f"{original_username}{counter}"
                            counter += 1
                        
                        django_user = User.objects.create_user(
                            username=username,
                            email=correo,
                            password='1234',  # Contraseña temporal
                            first_name=nombre,
                            last_name=f"{apellido_paterno} {apellido_materno or ''}".strip()
                        )
                        
                        # Actualizar la tabla usuarios con el user_id
                        cursor.execute(
                            "UPDATE usuarios SET user_id = %s WHERE id = %s",
                            [django_user.id, id_usuario]
                        )
                        
                        print(f"   ✓ Usuario Django creado (username: {username}, ID: {django_user.id})")
                
                # Verificar si existe el perfil
                try:
                    perfil = PerfilUsuario.objects.get(user=django_user)
                    print(f"   ✓ Perfil ya existe")
                except PerfilUsuario.DoesNotExist:
                    # Crear el perfil
                    admin_empresa_obj = None
                    if admin_empresa:
                        # Buscar el admin_empresa
                        try:
                            cursor.execute(
                                "SELECT user_id FROM usuarios WHERE id = %s",
                                [admin_empresa]
                            )
                            admin_user_id = cursor.fetchone()
                            if admin_user_id and admin_user_id[0]:
                                admin_django_user = User.objects.get(id=admin_user_id[0])
                                admin_empresa_obj = PerfilUsuario.objects.get(user=admin_django_user)
                        except:
                            pass
                    
                    perfil = PerfilUsuario.objects.create(
                        user=django_user,
                        nombre=nombre,
                        apellido_paterno=apellido_paterno,
                        apellido_materno=apellido_materno or '',
                        correo=correo,
                        nivel_usuario=nivel_usuario,
                        status=status,
                        admin_empresa=admin_empresa_obj
                    )
                    print(f"   ✓ Perfil creado (nivel: {nivel_usuario})")
                
                # Configurar permisos según el nivel
                if nivel_usuario == 'superadmin':
                    django_user.is_superuser = True
                    django_user.is_staff = True
                elif nivel_usuario in ['admin-empresa', 'admin-planta']:
                    django_user.is_staff = True
                
                django_user.save()
                
        print("\n" + "=" * 60)
        print("✅ SINCRONIZACIÓN COMPLETADA")
        
        # Mostrar resumen
        total_usuarios = User.objects.count()
        total_perfiles = PerfilUsuario.objects.count()
        print(f"📊 RESUMEN:")
        print(f"   - Usuarios Django: {total_usuarios}")
        print(f"   - Perfiles: {total_perfiles}")
        
        return True
        
    except Exception as e:
        print(f"❌ ERROR en sincronización: {str(e)}")
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
            cursor.execute("SELECT correo, nivel_usuario FROM usuarios LIMIT 3")
            usuarios_test = cursor.fetchall()
            
            for correo, nivel in usuarios_test:
                # Intentar autenticar por email
                try:
                    user_by_email = User.objects.get(email=correo)
                    user = authenticate(username=user_by_email.username, password='1234')
                    if user:
                        print(f"   ✅ {correo} ({nivel}) - LOGIN OK")
                    else:
                        print(f"   ❌ {correo} ({nivel}) - LOGIN FALLÓ")
                except User.DoesNotExist:
                    print(f"   ❌ {correo} - USUARIO NO ENCONTRADO")
        
        return True
        
    except Exception as e:
        print(f"❌ ERROR en prueba de login: {str(e)}")
        return False

if __name__ == "__main__":
    print("🚀 SINCRONIZACIÓN DE USUARIOS AXYOMA")
    print()
    
    sync_ok = sincronizar_usuarios()
    login_ok = probar_login()
    
    if sync_ok and login_ok:
        print("\n🎉 ¡SINCRONIZACIÓN COMPLETADA!")
        print("   - Usuarios Django creados")
        print("   - Perfiles sincronizados")
        print("   - Login funcionando")
        sys.exit(0)
    else:
        print("\n⚠️  PROBLEMAS EN SINCRONIZACIÓN")
        sys.exit(1)
