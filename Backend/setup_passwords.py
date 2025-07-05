#!/usr/bin/env python
"""
Script para agregar el campo password_temporal directamente
"""
import os
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')
django.setup()

from django.db import connection

def agregar_campo_password():
    print("=== AGREGANDO CAMPO PASSWORD_TEMPORAL ===")
    
    with connection.cursor() as cursor:
        try:
            # Verificar si la columna ya existe
            cursor.execute("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name='admin_plantas' AND column_name='password_temporal';
            """)
            
            if cursor.fetchone():
                print("✅ La columna password_temporal ya existe")
                return True
            
            # Agregar la columna
            cursor.execute("""
                ALTER TABLE admin_plantas 
                ADD COLUMN password_temporal VARCHAR(128) NULL;
            """)
            
            print("✅ Columna password_temporal agregada exitosamente")
            return True
            
        except Exception as e:
            print(f"❌ Error: {e}")
            return False

def actualizar_passwords():
    print("\n=== ACTUALIZANDO CONTRASEÑAS TEMPORALES ===")
    
    from apps.users.models import AdminPlanta
    import string
    import random
    
    try:
        admin_plantas = AdminPlanta.objects.filter(password_temporal__isnull=True)
        
        if not admin_plantas.exists():
            print("✅ Todos los usuarios ya tienen contraseñas")
            return
        
        print(f"📝 Actualizando {admin_plantas.count()} usuarios...")
        
        for admin_planta in admin_plantas:
            password = ''.join(random.choices(string.ascii_letters + string.digits, k=12))
            admin_planta.password_temporal = password
            admin_planta.save()
            
            # También actualizar la contraseña del usuario
            user = admin_planta.usuario.user
            user.set_password(password)
            user.save()
            
            print(f"✅ {admin_planta.planta.nombre} -> {user.username} -> {password}")
        
        print(f"\n🎉 ¡{admin_plantas.count()} usuarios actualizados!")
        
    except Exception as e:
        print(f"❌ Error actualizando passwords: {e}")

if __name__ == '__main__':
    if agregar_campo_password():
        actualizar_passwords()
    else:
        print("❌ No se pudo agregar el campo, abortando...")
