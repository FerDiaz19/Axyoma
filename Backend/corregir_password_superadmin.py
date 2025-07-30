#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para corregir específicamente la contraseña del superadmin
"""
import os
import sys
import django

# Configurar Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.base')
django.setup()

from django.contrib.auth.models import User
from apps.users.models import PerfilUsuario

def corregir_password_superadmin():
    print("🔒 CORRIGIENDO CONTRASEÑA DEL SUPERADMIN")
    print("=" * 50)
    
    try:
        # Buscar usuario superadmin
        superadmin = User.objects.get(username='superadmin')
        print(f"✅ Usuario encontrado: {superadmin.username}")
        print(f"📧 Email actual: {superadmin.email}")
        print(f"🔧 Staff: {superadmin.is_staff}")
        print(f"🔧 Superuser: {superadmin.is_superuser}")
        
        # Verificar contraseña actual
        if superadmin.check_password('1234'):
            print("✅ La contraseña '1234' ya está configurada correctamente")
        else:
            print("❌ La contraseña '1234' NO está configurada")
            print("🔧 Configurando contraseña '1234'...")
            superadmin.set_password('1234')
            superadmin.save()
            print("✅ Contraseña configurada")
        
        # Verificar después del cambio
        superadmin.refresh_from_db()
        if superadmin.check_password('1234'):
            print("✅ VERIFICACIÓN: Contraseña '1234' funciona correctamente")
        else:
            print("❌ PROBLEMA: La contraseña '1234' sigue sin funcionar")
        
        # Unificar emails
        perfil = superadmin.perfil
        if superadmin.email != perfil.correo:
            print(f"⚠️ Inconsistencia de emails:")
            print(f"  Django User: {superadmin.email}")
            print(f"  PerfilUsuario: {perfil.correo}")
            print("🔧 Unificando emails...")
            
            superadmin.email = 'superadmin@axyoma.com'
            perfil.correo = 'superadmin@axyoma.com'
            
            superadmin.save()
            perfil.save()
            
            print("✅ Emails unificados: superadmin@axyoma.com")
        
        print(f"\n🎯 CONFIGURACIÓN FINAL:")
        print(f"Usuario: {superadmin.username}")
        print(f"Email: {superadmin.email}")
        print(f"Contraseña: 1234")
        print(f"Staff: {superadmin.is_staff}")
        print(f"Superuser: {superadmin.is_superuser}")
        print(f"Perfil nivel: {perfil.nivel_usuario}")
        
        return True
        
    except User.DoesNotExist:
        print("❌ Usuario superadmin no encontrado")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    corregir_password_superadmin()
