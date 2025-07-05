#!/usr/bin/env python
"""
Script de configuración única para agregar campo password_temporal
"""
import os
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')
django.setup()

from django.db import connection
from apps.users.models import AdminPlanta
import string
import random

def setup_database():
    """Configurar base de datos con campo password_temporal"""
    print("🔧 CONFIGURANDO BASE DE DATOS...")
    
    with connection.cursor() as cursor:
        try:
            # Verificar si la columna existe
            cursor.execute("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name='admin_plantas' AND column_name='password_temporal';
            """)
            
            if cursor.fetchone():
                print("✅ Campo password_temporal ya existe")
            else:
                # Agregar la columna
                cursor.execute("""
                    ALTER TABLE admin_plantas 
                    ADD COLUMN password_temporal VARCHAR(128) NULL;
                """)
                print("✅ Campo password_temporal agregado")
            
            # Actualizar usuarios existentes sin contraseña temporal
            admin_plantas = AdminPlanta.objects.filter(password_temporal__isnull=True)
            
            for admin_planta in admin_plantas:
                password = ''.join(random.choices(string.ascii_letters + string.digits, k=12))
                admin_planta.password_temporal = password
                admin_planta.save()
                
                # Actualizar contraseña del usuario
                user = admin_planta.usuario.user
                user.set_password(password)
                user.save()
                
                print(f"✅ Usuario {user.username} actualizado")
            
            print("🎉 Base de datos configurada correctamente")
            
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == '__main__':
    setup_database()
