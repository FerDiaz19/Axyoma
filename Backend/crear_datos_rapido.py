#!/usr/bin/env python
"""
Script para crear datos rápido
"""
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import User
from apps.users.models import PerfilUsuario, Empresa, Planta, Departamento, Puesto, Empleado

print("🔄 Creando datos de prueba...")

# Crear superadmin si no existe
if not User.objects.filter(username='superadmin').exists():
    superuser = User.objects.create_user(
        username='superadmin',
        email='superadmin@axyoma.com', 
        password='admin123',
        first_name='Super',
        last_name='Admin'
    )
    superuser.is_superuser = True
    superuser.is_staff = True
    superuser.save()
    
    perfil = PerfilUsuario.objects.create(
        nombre='Super',
        apellido_paterno='Admin',
        correo='superadmin@axyoma.com',
        nivel_usuario='superadmin',
        status=True,
        user=superuser
    )
    print('✅ SuperAdmin creado')

# Crear empresas de prueba
empresas_data = [
    {
        'nombre': 'TechCorp Solutions', 
        'rfc': 'TCS230515ABC', 
        'email_contacto': 'contacto@techcorp.mx', 
        'telefono_contacto': '4421234567', 
        'direccion': 'Av. Tecnológico 1500',
        'status': True
    },
    {
        'nombre': 'InnovaSoft Industries', 
        'rfc': 'ISI180720DEF', 
        'email_contacto': 'info@innovasoft.mx', 
        'telefono_contacto': '4427654321', 
        'direccion': 'Blvd. Bernardo Quintana 2000',
        'status': True
    }
]

# Crear perfil administrador temporal
if not PerfilUsuario.objects.filter(correo='admin_temp@axyoma.com').exists():
    user_temp = User.objects.create_user(
        username='admin_temp',
        email='admin_temp@axyoma.com',
        password='temp123'
    )
    admin_perfil = PerfilUsuario.objects.create(
        nombre='Admin',
        apellido_paterno='Temporal',
        correo='admin_temp@axyoma.com',
        nivel_usuario='admin-empresa',
        status=True,
        user=user_temp
    )
    print('✅ Admin temporal creado')
else:
    admin_perfil = PerfilUsuario.objects.get(correo='admin_temp@axyoma.com')

for emp_data in empresas_data:
    if not Empresa.objects.filter(nombre=emp_data['nombre']).exists():
        # Crear empresa con administrador
        empresa = Empresa.objects.create(
            **emp_data,
            administrador=admin_perfil
        )
        print(f'✅ Empresa creada: {empresa.nombre}')
        
        # Crear una planta para la empresa
        planta = Planta.objects.create(
            nombre=f'Planta Principal {empresa.nombre}',
            direccion=empresa.direccion or 'Sin dirección',
            empresa=empresa,
            status=True
        )
        print(f'  🏭 Planta creada: {planta.nombre}')

print(f'📊 Total empresas: {Empresa.objects.count()}')
print(f'🏭 Total plantas: {Planta.objects.count()}')
