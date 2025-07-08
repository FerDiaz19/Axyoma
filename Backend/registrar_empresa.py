#!/usr/bin/env python
"""
Función de ejemplo: Registro automático de nueva empresa
Simula lo que ocurre cuando una empresa se registra por primera vez

FLUJO DE REGISTRO:
1. Empresa se registra en la plataforma
2. Se crea automáticamente:
   - Usuario admin-empresa (quien contrató el servicio)
   - Suscripción al plan seleccionado
   - Planta Principal (ubicación principal de la empresa)
   - Departamentos básicos (Administración, RRHH, Finanzas, Producción, etc.)
   - Puestos básicos para cada departamento
3. El admin-empresa puede inmediatamente:
   - Gestionar empleados, departamentos y puestos
   - Crear evaluaciones y reportes
   - Expandir la estructura organizacional

REGLA DE NEGOCIO IMPORTANTE:
- TODA empresa tiene una "Planta Principal" desde el momento del registro
- Esta planta es la ubicación/instalación que contrató el servicio
- Solo se crean plantas adicionales si la empresa tiene múltiples ubicaciones
- El admin-empresa puede gestionar TODO desde su dashboard sin necesidad de admin-planta
"""

import os
import sys
import django
from django.db import transaction

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')
django.setup()

from django.contrib.auth.models import User
from apps.models import (
    Empresa, Usuario, Planta, Departamento, Puesto, 
    PlanSuscripcion, Suscripcion
)
from datetime import datetime, timedelta

def registrar_nueva_empresa(
    empresa_nombre, 
    empresa_rfc, 
    empresa_direccion,
    admin_nombre,
    admin_apellido,
    admin_email,
    admin_password,
    plan_nombre="Básico"
):
    """
    Función que simula el registro de una nueva empresa
    Automáticamente crea:
    1. Usuario admin-empresa
    2. Empresa
    3. Planta Principal (donde contrató el servicio)
    4. Departamentos básicos
    5. Puestos básicos
    6. Suscripción al plan seleccionado
    """
    
    print(f"🚀 Registrando nueva empresa: {empresa_nombre}")
    
    with transaction.atomic():
        # 1. Crear usuario admin-empresa
        print("👤 Creando usuario administrador...")
        
        admin_user, created = User.objects.get_or_create(
            username=admin_email,
            defaults={
                'email': admin_email,
                'first_name': admin_nombre,
                'last_name': admin_apellido,
                'is_staff': False,
                'is_superuser': False
            }
        )
        if created:
            admin_user.set_password(admin_password)
            admin_user.save()

        admin_usuario, created = Usuario.objects.get_or_create(
            correo=admin_email,
            defaults={
                'nombre': admin_nombre,
                'apellido_paterno': admin_apellido,
                'nivel_usuario': 'admin-empresa',
                'status': True,
                'user': admin_user
            }
        )
        
        print(f"   ✅ Usuario creado: {admin_usuario.correo}")

        # 2. Crear empresa
        print("🏢 Creando empresa...")
        
        empresa, created = Empresa.objects.get_or_create(
            rfc=empresa_rfc,
            defaults={
                'nombre': empresa_nombre,
                'direccion': empresa_direccion,
                'email_contacto': admin_email,
                'telefono_contacto': '',
                'status': True,
                'administrador': admin_usuario
            }
        )
        
        print(f"   ✅ Empresa creada: {empresa.nombre}")

        # 3. Crear suscripción
        print("💳 Activando suscripción...")
        
        plan = PlanSuscripcion.objects.get(nombre=plan_nombre)
        
        suscripcion, created = Suscripcion.objects.get_or_create(
            empresa=empresa,
            defaults={
                'plan_suscripcion': plan,
                'fecha_inicio': datetime.now().date(),
                'fecha_fin': (datetime.now() + timedelta(days=plan.duracion)).date(),
                'estado': 'Activa',
                'status': True
            }
        )
        
        print(f"   ✅ Suscripción activada: Plan {suscripcion.plan_suscripcion.nombre}")

        # 4. Crear Planta Principal (automática)
        print("🏭 Creando planta principal...")
        
        planta_principal, created = Planta.objects.get_or_create(
            nombre='Planta Principal',
            empresa=empresa,
            defaults={
                'direccion': empresa_direccion,  # Inicialmente misma dirección que la empresa
                'status': True
            }
        )
        
        print(f"   ✅ Planta Principal creada automáticamente")

        # 5. Crear departamentos básicos
        print("🏢 Creando departamentos básicos...")
        
        departamentos_basicos = [
            {'nombre': 'Administración', 'descripcion': 'Gestión administrativa general'},
            {'nombre': 'Recursos Humanos', 'descripcion': 'Gestión del personal'},
            {'nombre': 'Finanzas', 'descripcion': 'Gestión financiera'},
            {'nombre': 'Operaciones', 'descripcion': 'Operaciones principales del negocio'},
        ]
        
        departamentos = []
        for dept_data in departamentos_basicos:
            dept, created = Departamento.objects.get_or_create(
                nombre=dept_data['nombre'],
                planta=planta_principal,
                defaults={
                    'descripcion': dept_data['descripcion']
                }
            )
            departamentos.append(dept)
        
        print(f"   ✅ Creados {len(departamentos)} departamentos básicos")

        # 6. Crear puestos básicos
        print("💼 Creando puestos básicos...")
        
        puestos_basicos = [
            {'nombre': 'Director General', 'departamento': 'Administración'},
            {'nombre': 'Asistente Administrativo', 'departamento': 'Administración'},
            {'nombre': 'Gerente de RRHH', 'departamento': 'Recursos Humanos'},
            {'nombre': 'Contador', 'departamento': 'Finanzas'},
            {'nombre': 'Supervisor de Operaciones', 'departamento': 'Operaciones'},
            {'nombre': 'Operario', 'departamento': 'Operaciones'},
        ]
        
        puestos = []
        for puesto_data in puestos_basicos:
            dept = next((d for d in departamentos if d.nombre == puesto_data['departamento']), None)
            if dept:
                puesto, created = Puesto.objects.get_or_create(
                    nombre=puesto_data['nombre'],
                    departamento=dept
                )
                puestos.append(puesto)
        
        print(f"   ✅ Creados {len(puestos)} puestos básicos")

    print(f"\n🎉 ¡EMPRESA {empresa_nombre.upper()} REGISTRADA EXITOSAMENTE!")
    print(f"\n📊 RESUMEN:")
    print(f"   ✅ Empresa: {empresa.nombre}")
    print(f"   ✅ RFC: {empresa.rfc}")
    print(f"   ✅ Admin: {admin_usuario.correo}")
    print(f"   ✅ Planta Principal: Creada automáticamente")
    print(f"   ✅ Departamentos: {len(departamentos)} básicos")
    print(f"   ✅ Puestos: {len(puestos)} básicos")
    print(f"   ✅ Suscripción: {plan.nombre} activa")
    print(f"\n📝 SIGUIENTE PASO:")
    print(f"   El admin-empresa puede ahora:")
    print(f"   • Gestionar empleados en su planta principal")
    print(f"   • Crear departamentos adicionales")
    print(f"   • Crear puestos adicionales")
    print(f"   • Crear plantas adicionales si se expande")
    
    return empresa, admin_usuario, planta_principal

if __name__ == '__main__':
    # Ejemplo de uso
    registrar_nueva_empresa(
        empresa_nombre="Industrias Acme S.A. de C.V.",
        empresa_rfc="IAC240701XYZ",
        empresa_direccion="Calle Industrial 123, Col. Industrial, León, Gto.",
        admin_nombre="Carlos",
        admin_apellido="Mendoza",
        admin_email="carlos.mendoza@acme.com",
        admin_password="acme2024",
        plan_nombre="Profesional"
    )
