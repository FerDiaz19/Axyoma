#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para mostrar dónde se guardan las contraseñas
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
from django.db import connection

def mostrar_contraseñas():
    print("🔐 UBICACIÓN DE CONTRASEÑAS EN AXYOMA")
    print("=" * 50)
    
    print("\n📋 ESQUEMA DE AUTENTICACIÓN:")
    print("1. 🗄️  TABLA 'auth_user' (Django) - Aquí están las contraseñas HASHEADAS")
    print("2. 👤 TABLA 'usuarios' (Tu modelo) - Aquí está el perfil del usuario")
    print("3. 🔗 RELACIÓN: auth_user.id ←→ usuarios.user_id")
    
    print("\n💡 EXPLICACIÓN:")
    print("• Django usa su propia tabla 'auth_user' para autenticación")
    print("• Tu tabla 'usuarios' solo guarda datos del perfil")
    print("• La contraseña NUNCA se guarda en texto plano")
    print("• Se guarda como HASH seguro en 'auth_user.password'")
    
    print("\n🔍 USUARIOS EN EL SISTEMA:")
    users = User.objects.all()
    for user in users:
        try:
            perfil = user.perfil
            print(f"\n👤 Usuario: {user.username}")
            print(f"   📧 Email: {user.email}")
            print(f"   🔐 Password Hash: {user.password[:30]}...")
            print(f"   👥 Perfil: {perfil.nombre} {perfil.apellido_paterno}")
            print(f"   🎯 Nivel: {perfil.nivel_usuario}")
            print(f"   🔗 auth_user.id={user.id} ←→ usuarios.user_id={perfil.user.id}")
        except:
            print(f"   ⚠️ Sin perfil asociado")
    
    print("\n🏗️ ESTRUCTURA DE TABLAS:")
    with connection.cursor() as cursor:
        # Mostrar estructura de auth_user
        cursor.execute("""
            SELECT column_name, data_type 
            FROM information_schema.columns 
            WHERE table_name = 'auth_user' 
            ORDER BY ordinal_position;
        """)
        print("\n📊 TABLA auth_user:")
        for row in cursor.fetchall():
            print(f"   • {row[0]} ({row[1]})")
            
        # Mostrar estructura de usuarios
        cursor.execute("""
            SELECT column_name, data_type 
            FROM information_schema.columns 
            WHERE table_name = 'usuarios' 
            ORDER BY ordinal_position;
        """)
        print("\n📊 TABLA usuarios:")
        for row in cursor.fetchall():
            print(f"   • {row[0]} ({row[1]})")
    
    print("\n🎯 RESUMEN:")
    print("✅ Las contraseñas están en: auth_user.password (HASHEADAS)")
    print("✅ Los perfiles están en: usuarios.* (SIN contraseña)")
    print("✅ Se conectan por: auth_user.id = usuarios.user_id")
    print("✅ Django maneja la autenticación automáticamente")

if __name__ == '__main__':
    mostrar_contraseñas()
