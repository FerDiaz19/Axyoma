#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para mostrar todas las credenciales de usuarios del sistema
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

def mostrar_credenciales():
    print("🔑 CREDENCIALES DE TODOS LOS USUARIOS")
    print("=" * 50)
    
    usuarios = User.objects.all().order_by('username')
    
    if not usuarios:
        print("❌ No hay usuarios en el sistema")
        return
    
    print(f"📊 Total de usuarios: {len(usuarios)}")
    print("\n🔐 CREDENCIALES COMPLETAS:")
    print("-" * 50)
    
    for user in usuarios:
        try:
            perfil = user.perfil
            print(f"\n👤 USUARIO: {user.username}")
            print(f"   🔑 CONTRASEÑA: {'1234' if user.username in ['superadmin', 'admin_empresa', 'admin_planta'] else 'empleado123'}")
            print(f"   📧 EMAIL: {user.email}")
            print(f"   👥 NOMBRE: {perfil.nombre} {perfil.apellido_paterno}")
            print(f"   🎯 NIVEL: {perfil.nivel_usuario}")
            print(f"   ✅ ACTIVO: {'Sí' if user.is_active else 'No'}")
            
        except Exception as e:
            print(f"\n👤 USUARIO: {user.username}")
            print(f"   🔑 CONTRASEÑA: 1234")
            print(f"   📧 EMAIL: {user.email}")
            print(f"   ⚠️ SIN PERFIL ASOCIADO")
    
    print("\n" + "=" * 50)
    print("📋 RESUMEN DE CONTRASEÑAS:")
    print("🔸 SuperAdmin: superadmin / 1234")
    print("🔸 Admin Empresa: admin_empresa / 1234") 
    print("🔸 Admin Planta: admin_planta / 1234")
    print("🔸 Empleados: [usuario] / empleado123")
    print("\n🌐 URL LOGIN: http://127.0.0.1:8000/admin/")

if __name__ == '__main__':
    mostrar_credenciales()
