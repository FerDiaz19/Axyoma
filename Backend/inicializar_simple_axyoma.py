#!/usr/bin/env python
import os
import django
from datetime import datetime, timedelta

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')
django.setup()

from django.contrib.auth.models import User
from apps.users.models import PerfilUsuario, Empresa, Planta, Departamento, Puesto, Empleado
from apps.subscriptions.models import PlanSuscripcion, SuscripcionEmpresa
from rest_framework.authtoken.models import Token
from django.db import transaction
from django.core.management import execute_from_command_line

def limpiar_datos_seguros():
    """Limpiar datos de forma segura"""
    print('🧹 LIMPIANDO DATOS EXISTENTES...')
    
    try:
        # Solo limpiar tablas que sabemos que existen
        Empleado.objects.all().delete()
        Puesto.objects.all().delete() 
        Departamento.objects.all().delete()
        Planta.objects.all().delete()
        SuscripcionEmpresa.objects.all().delete()
        PlanSuscripcion.objects.all().delete()
        PerfilUsuario.objects.all().delete()
        Token.objects.all().delete()
        User.objects.all().delete()
        Empresa.objects.all().delete()
        print('✅ Datos limpiados exitosamente')
    except Exception as e:
        print(f'⚠️ Advertencia: {e}')

def crear_datos_axyoma():
    """Crear datos básicos para Axyoma"""
    print('🚀 CREANDO DATOS AXYOMA...')
    
    with transaction.atomic():
        # 1. SuperAdmin
        print('👤 Creando SuperAdmin...')
        superadmin = User.objects.create_user(
            username='superadmin',
            password='admin123', 
            email='superadmin@axyoma.com',
            first_name='Super',
            last_name='Admin',
            is_superuser=True,
            is_staff=True
        )
        
        PerfilUsuario.objects.create(
            user=superadmin,
            nivel_usuario='SuperAdmin',
            fecha_registro=datetime.now()
        )
        Token.objects.create(user=superadmin)
        
        # 2. Empresa Axyoma
        print('🏢 Creando Empresa...')
        empresa = Empresa.objects.create(
            nombre='Axyoma',
            rfc='AXY123456789',
            telefono='555-0123',
            correo='contacto@axyoma.com', 
            direccion='Av. Innovación 123, CDMX',
            status=True
        )
        
        # 3. Admin Empresa
        print('👥 Creando Admin Empresa...')
        admin = User.objects.create_user(
            username='admin_axyoma',
            password='admin123',
            email='admin@axyoma.com',
            first_name='Admin', 
            last_name='Axyoma'
        )
        
        PerfilUsuario.objects.create(
            user=admin,
            nivel_usuario='AdminEmpresa',
            admin_empresa=empresa.empresa_id,
            fecha_registro=datetime.now()
        )
        Token.objects.create(user=admin)
        
        # Actualizar empresa
        empresa.administrador = admin.id
        empresa.save()
        
        # 4. Plantas  
        print('🏭 Creando Plantas...')
        planta1 = Planta.objects.create(
            nombre='Planta Norte',
            empresa=empresa.empresa_id,
            telefono='555-1001',
            correo='norte@axyoma.com',
            direccion='Monterrey, NL',
            status=True
        )
        
        planta2 = Planta.objects.create(
            nombre='Planta Sur', 
            empresa=empresa.empresa_id,
            telefono='555-1002',
            correo='sur@axyoma.com',
            direccion='Guadalajara, JAL',
            status=True
        )
        
        # 5. Departamentos
        print('🏢 Creando Departamentos...')
        dept1 = Departamento.objects.create(
            nombre='Recursos Humanos',
            planta=planta1.planta_id,
            status=True
        )
        
        dept2 = Departamento.objects.create(
            nombre='Producción',
            planta=planta1.planta_id, 
            status=True
        )
        
        dept3 = Departamento.objects.create(
            nombre='Mantenimiento',
            planta=planta2.planta_id,
            status=True
        )
        
        # 6. Puestos
        print('💼 Creando Puestos...')
        puesto1 = Puesto.objects.create(
            nombre='Gerente RRHH',
            descripcion='Gestión de personal',
            departamento=dept1.departamento_id,
            status=True
        )
        
        puesto2 = Puesto.objects.create(
            nombre='Jefe Producción',
            descripcion='Supervisión producción',
            departamento=dept2.departamento_id,
            status=True
        )
        
        puesto3 = Puesto.objects.create(
            nombre='Técnico Mantenimiento',
            descripcion='Mantenimiento equipos',
            departamento=dept3.departamento_id,
            status=True
        )
        
        # 7. Empleados
        print('👨‍💼 Creando Empleados...')
        Empleado.objects.create(
            numero_empleado='EMP001',
            nombre='Juan Pérez',
            apellido='González',
            email='juan.perez@axyoma.com',
            telefono='555-2001',
            puesto=puesto1.puesto_id,
            status=True
        )
        
        Empleado.objects.create(
            numero_empleado='EMP002',
            nombre='María López',
            apellido='Martínez', 
            email='maria.lopez@axyoma.com',
            telefono='555-2002',
            puesto=puesto2.puesto_id,
            status=True
        )
        
        Empleado.objects.create(
            numero_empleado='EMP003',
            nombre='Carlos Ruiz',
            apellido='Hernández',
            email='carlos.ruiz@axyoma.com', 
            telefono='555-2003',
            puesto=puesto3.puesto_id,
            status=True
        )
        
        # 8. Planes
        print('💳 Creando Planes...')
        plan1 = PlanSuscripcion.objects.create(
            nombre='Plan Básico',
            descripcion='Hasta 50 empleados',
            duracion=30,
            precio=999.00,
            status=True
        )
        
        plan2 = PlanSuscripcion.objects.create(
            nombre='Plan Profesional',
            descripcion='Hasta 200 empleados',
            duracion=30,
            precio=2999.00,
            status=True
        )
        
        plan3 = PlanSuscripcion.objects.create(
            nombre='Plan Empresarial', 
            descripcion='Empleados ilimitados',
            duracion=30,
            precio=5999.00,
            status=True
        )
        
        # 9. Suscripción
        print('📋 Creando Suscripción...')
        fecha_inicio = datetime.now()
        fecha_fin = fecha_inicio + timedelta(days=365)
        
        SuscripcionEmpresa.objects.create(
            empresa=empresa.empresa_id,
            plan=plan3.plan_id,
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin,
            estado='Activa',
            status=True,
            fecha_creacion=datetime.now(),
            fecha_actualizacion=datetime.now()
        )
    
    print('✅ DATOS CREADOS EXITOSAMENTE')

def mostrar_resumen():
    """Mostrar resumen de datos creados"""
    print('\n' + '='*50)
    print('📊 RESUMEN DEL SISTEMA')
    print('='*50)
    print(f'Empresas: {Empresa.objects.count()}')
    print(f'Usuarios: {User.objects.count()}')  
    print(f'Plantas: {Planta.objects.count()}')
    print(f'Departamentos: {Departamento.objects.count()}')
    print(f'Puestos: {Puesto.objects.count()}')
    print(f'Empleados: {Empleado.objects.count()}')
    print(f'Planes: {PlanSuscripcion.objects.count()}')
    print(f'Suscripciones: {SuscripcionEmpresa.objects.count()}')
    print('='*50)
    print('🔑 CREDENCIALES:')
    print('SuperAdmin: superadmin / admin123')
    print('Admin Empresa: admin_axyoma / admin123')
    print('='*50)

def main():
    print('🚀 INICIALIZADOR AXYOMA SIMPLIFICADO')
    print('='*50)
    
    try:
        limpiar_datos_seguros()
        crear_datos_axyoma()
        mostrar_resumen()
        print('\n🎉 SISTEMA LISTO PARA USAR')
    except Exception as e:
        print(f'❌ ERROR: {e}')
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()
