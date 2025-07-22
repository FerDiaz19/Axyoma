#!/usr/bin/env python
"""
Script simple para crear empresas adicionales sin suscripciones
"""

import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')
django.setup()

from django.contrib.auth.models import User
from django.db import transaction
from apps.users.models import PerfilUsuario, Empresa, Planta, Departamento, Puesto, Empleado
from datetime import datetime, timedelta
import random

def crear_empresas_simples():
    """Crear empresas adicionales simples"""
    
    print("🏢 Creando empresas adicionales...")
    
    empresas_data = [
        {
            'nombre': 'TechSolutions México',
            'rfc': 'TSM850623AB1',
            'direccion': 'Av. Tecnológico 123, Guadalajara, Jalisco',
            'email_contacto': 'contacto@techsolutions.mx',
            'telefono_contacto': '33-1111-2222'
        },
        {
            'nombre': 'Innovación Digital SA',
            'rfc': 'IDS920815CD2',
            'direccion': 'Blvd. Innovación 456, Monterrey, Nuevo León',
            'email_contacto': 'info@innovacion.mx',
            'telefono_contacto': '81-3333-4444'
        }
    ]
    
    try:
        for i, empresa_info in enumerate(empresas_data, 2):
            print(f"📊 Creando empresa: {empresa_info['nombre']}")
            
            # Crear usuario administrador
            username = f"admin_empresa_{i}"
            user = User.objects.create_user(
                username=username,
                email=empresa_info['email_contacto'],
                password='1234'
            )
            
            # Crear perfil
            perfil = PerfilUsuario.objects.create(
                user=user,
                nombre=f"Admin {empresa_info['nombre'].split()[0]}",
                apellido_paterno="Administrador",
                apellido_materno="Empresa",
                correo=empresa_info['email_contacto'],
                nivel_usuario='admin-empresa'
            )
            
            # Crear empresa
            empresa = Empresa.objects.create(
                nombre=empresa_info['nombre'],
                rfc=empresa_info['rfc'],
                direccion=empresa_info['direccion'],
                email_contacto=empresa_info['email_contacto'],
                telefono_contacto=empresa_info['telefono_contacto'],
                administrador=perfil
            )
            
            print(f"✅ Empresa creada: {empresa.nombre}")
            
            # Crear planta para la empresa
            planta = Planta.objects.create(
                nombre=f"Oficina Principal {empresa_info['nombre'].split()[0]}",
                direccion=empresa_info['direccion'],
                empresa=empresa
            )
            print(f"🏭 Planta creada: {planta.nombre}")
            
            # Crear algunos departamentos básicos
            departamentos = ['Administración', 'Ventas', 'Desarrollo']
            for dept_nombre in departamentos:
                dept = Departamento.objects.create(
                    nombre=dept_nombre,
                    descripcion=f'{dept_nombre} de {empresa.nombre}',
                    planta=planta
                )
                
                # Crear un puesto por departamento
                if dept_nombre == 'Administración':
                    puesto_nombre = 'Gerente Administrativo'
                elif dept_nombre == 'Ventas':
                    puesto_nombre = 'Ejecutivo de Ventas'
                else:
                    puesto_nombre = 'Desarrollador'
                
                puesto = Puesto.objects.create(
                    nombre=puesto_nombre,
                    descripcion=f'{puesto_nombre} del departamento {dept_nombre}',
                    departamento=dept
                )
                
                # Crear 2-3 empleados por puesto
                nombres = ['Juan', 'María', 'Carlos', 'Ana', 'Luis']
                apellidos = ['García', 'López', 'Martínez', 'González', 'Pérez']
                
                for j in range(random.randint(2, 3)):
                    nombre = random.choice(nombres)
                    apellido = random.choice(apellidos)
                    
                    Empleado.objects.create(
                        nombre=nombre,
                        apellido_paterno=apellido,
                        apellido_materno=random.choice(apellidos),
                        email=f"{nombre.lower()}.{apellido.lower()}{j}@{empresa.nombre.lower().replace(' ', '')}.com",
                        telefono=f"55-{random.randint(1000, 9999)}-{random.randint(1000, 9999)}",
                        fecha_ingreso=datetime.now().date() - timedelta(days=random.randint(30, 365)),
                        puesto=puesto
                    )
                
                print(f"  📁 {dept_nombre} con {puesto_nombre} creado")
        
        print("\n🎉 ¡EMPRESAS ADICIONALES CREADAS!")
        print("="*50)
        print(f"📊 Empresas totales: {Empresa.objects.count()}")
        print(f"🏢 Plantas totales: {Planta.objects.count()}")
        print(f"🏬 Departamentos totales: {Departamento.objects.count()}")
        print(f"💼 Puestos totales: {Puesto.objects.count()}")
        print(f"👥 Empleados totales: {Empleado.objects.count()}")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    crear_empresas_simples()
