#!/usr/bin/env python
"""
Script para crear plantas adicionales con usuarios admin-planta automáticos
"""

import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')
django.setup()

from django.contrib.auth.models import User
from apps.users.models import PerfilUsuario, Empresa, Planta, AdminPlanta

def crear_plantas_con_usuarios():
    """Crear plantas adicionales y sus usuarios admin-planta automáticamente"""
    
    print("🏭 Creando plantas adicionales con usuarios admin-planta...")
    
    try:
        # Obtener empresas existentes
        empresas = Empresa.objects.all()
        
        for empresa in empresas:
            print(f"\n📊 Empresa: {empresa.nombre}")
            plantas_actuales = Planta.objects.filter(empresa=empresa).count()
            print(f"   Plantas actuales: {plantas_actuales}")
            
            # Crear plantas adicionales si la empresa tiene pocas
            if plantas_actuales < 2:
                nueva_planta_nombre = f"Sucursal {empresa.nombre.split()[0]} Norte"
                
                planta = Planta.objects.create(
                    nombre=nueva_planta_nombre,
                    direccion=f"Dirección de {nueva_planta_nombre}",
                    empresa=empresa,
                    status=True
                )
                
                print(f"🏢 Nueva planta creada: {planta.nombre}")
                
                # CREAR USUARIO ADMIN-PLANTA AUTOMÁTICAMENTE
                username_planta = f"admin_planta_{planta.planta_id}"
                email_planta = f"admin.planta.{planta.planta_id}@{empresa.nombre.lower().replace(' ', '')}.com"
                
                # Crear usuario Django para admin-planta
                user_planta = User.objects.create_user(
                    username=username_planta,
                    email=email_planta,
                    password='1234'
                )
                
                # Crear perfil admin-planta
                perfil_planta = PerfilUsuario.objects.create(
                    user=user_planta,
                    nombre=f"Admin {nueva_planta_nombre.split()[1]}",
                    apellido_paterno="Planta",
                    apellido_materno=f"{empresa.nombre.split()[0]}",
                    correo=email_planta,
                    nivel_usuario='admin-planta'
                )
                
                # Crear relación AdminPlanta
                AdminPlanta.objects.create(
                    usuario=perfil_planta,
                    planta=planta,
                    status=True,
                    password_temporal='1234'
                )
                
                print(f"👤 Usuario admin-planta creado: {username_planta}")
                print(f"📧 Email: {email_planta}")
                print(f"🔑 Password temporal: 1234")
        
        print("\n🎉 ¡PLANTAS Y USUARIOS CREADOS EXITOSAMENTE!")
        print("="*50)
        print(f"🏢 Plantas totales: {Planta.objects.count()}")
        print(f"👤 Usuarios totales: {PerfilUsuario.objects.count()}")
        
        # Mostrar resumen de usuarios admin-planta
        print("\n👥 USUARIOS ADMIN-PLANTA:")
        admin_plantas = PerfilUsuario.objects.filter(nivel_usuario='admin-planta')
        for perfil in admin_plantas:
            admin_planta = AdminPlanta.objects.filter(usuario=perfil, status=True).first()
            planta_nombre = admin_planta.planta.nombre if admin_planta else 'Sin asignar'
            print(f"- {perfil.nombre} {perfil.apellido_paterno} -> {planta_nombre}")
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    crear_plantas_con_usuarios()
