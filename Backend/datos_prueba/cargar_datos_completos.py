#!/usr/bin/env python
"""
🎯 CARGADOR DE DATOS DE PRUEBA - AXYOMA
=====================================
Script confiable para cargar todos los datos de prueba necesarios
"""

import os
import sys
from datetime import date, datetime, timedelta
import random

# Agregar el directorio padre al path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')

import django
django.setup()

from django.contrib.auth.models import User
from django.core.management import call_command
from django.db import transaction

def limpiar_datos():
    """Limpiar todos los datos existentes"""
    print("🧹 LIMPIANDO DATOS EXISTENTES...")
    
    try:
        # Limpiar usuarios
        User.objects.filter(is_superuser=False).delete()
        print("  ✅ Usuarios no-admin eliminados")
        
        # Limpiar datos de apps
        from apps.users.models import Empleado, Puesto, Departamento, Planta, Empresa
        from apps.subscriptions.models import PlanSuscripcion
        
        Empleado.objects.all().delete()
        print("  ✅ Empleados eliminados")
        
        Puesto.objects.all().delete() 
        print("  ✅ Puestos eliminados")
        
        Departamento.objects.all().delete()
        print("  ✅ Departamentos eliminados")
        
        Planta.objects.all().delete()
        print("  ✅ Plantas eliminadas")
        
        Empresa.objects.all().delete()
        print("  ✅ Empresas eliminadas")
        
        PlanSuscripcion.objects.all().delete()
        print("  ✅ Planes de suscripción eliminados")
        
        print("✅ Datos limpiados correctamente")
        return True
        
    except Exception as e:
        print(f"❌ Error limpiando datos: {e}")
        return False

def crear_superadmin():
    """Crear superadmin principal"""
    print("\n👑 CREANDO SUPERADMIN...")
    
    try:
        # Eliminar superadmin si existe
        User.objects.filter(username='superadmin').delete()
        
        # Crear nuevo superadmin
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
        
        # Crear perfil
        from apps.users.models import PerfilUsuario
        perfil = PerfilUsuario.objects.create(
            nombre='Super',
            apellido_paterno='Admin',
            correo='superadmin@axyoma.com',
            nivel_usuario='superadmin',
            status=True,
            user=superuser
        )
        
        print("✅ SuperAdmin creado: superadmin / admin123")
        return True
        
    except Exception as e:
        print(f"❌ Error creando superadmin: {e}")
        return False

def crear_empresas():
    """Crear empresas de prueba"""
    print("\n🏢 CREANDO EMPRESAS...")
    
    try:
        from apps.users.models import Empresa
        
        empresas_data = [
            {
                'nombre': 'TechCorp Solutions',
                'rfc': 'TCS950815MX3',
                'direccion': 'Av. Tecnológico #1500, Querétaro, Qro.',
                'email_contacto': 'contacto@techcorp.mx',
                'telefono_contacto': '4421234567'
            },
            {
                'nombre': 'InnovaSoft Industries',
                'rfc': 'ISI980320QR1', 
                'direccion': 'Blvd. Bernardo Quintana #2000, Querétaro, Qro.',
                'email_contacto': 'info@innovasoft.mx',
                'telefono_contacto': '4427654321'
            }
        ]
        
        empresas = []
        for empresa_data in empresas_data:
            empresa = Empresa.objects.create(
                nombre=empresa_data['nombre'],
                rfc=empresa_data['rfc'],
                direccion=empresa_data['direccion'],
                email_contacto=empresa_data['email_contacto'],
                telefono_contacto=empresa_data['telefono_contacto'],
                status=True
            )
            empresas.append(empresa)
            print(f"  ✅ {empresa.nombre}")
        
        print(f"✅ {len(empresas)} empresas creadas")
        return empresas
        
    except Exception as e:
        print(f"❌ Error creando empresas: {e}")
        return []

def crear_plantas(empresas):
    """Crear plantas para las empresas"""
    print("\n🏭 CREANDO PLANTAS...")
    
    try:
        from apps.users.models import Planta
        
        plantas_data = [
            # TechCorp
            {'nombre': 'Planta Norte TechCorp', 'direccion': 'Zona Industrial Norte, Querétaro'},
            {'nombre': 'Planta Sur TechCorp', 'direccion': 'Zona Industrial Sur, Querétaro'},
            # InnovaSoft  
            {'nombre': 'Planta Central InnovaSoft', 'direccion': 'Parque Industrial Central, Querétaro'},
            {'nombre': 'Planta Satelite InnovaSoft', 'direccion': 'Ciudad Satelite, Querétaro'},
        ]
        
        plantas = []
        for i, planta_data in enumerate(plantas_data):
            empresa = empresas[i // 2]  # 2 plantas por empresa
            planta = Planta.objects.create(
                nombre=planta_data['nombre'],
                direccion=planta_data['direccion'],
                empresa=empresa,
                status=True
            )
            plantas.append(planta)
            print(f"  ✅ {planta.nombre} ({empresa.nombre})")
        
        print(f"✅ {len(plantas)} plantas creadas")
        return plantas
        
    except Exception as e:
        print(f"❌ Error creando plantas: {e}")
        return []

def crear_planes_suscripcion():
    """Crear planes de suscripción"""
    print("\n💳 CREANDO PLANES DE SUSCRIPCIÓN...")
    
    try:
        from apps.subscriptions.models import PlanSuscripcion
        
        planes_data = [
            {
                'nombre': 'Plan Básico',
                'descripcion': 'Plan básico para empresas pequeñas con funcionalidades esenciales',
                'precio': 99.00,
                'duracion_dias': 30,
                'max_usuarios': 50,
                'max_evaluaciones': 10,
                'soporte_incluido': True,
                'activo': True
            },
            {
                'nombre': 'Plan Profesional',
                'descripcion': 'Plan profesional para empresas medianas con funcionalidades avanzadas',
                'precio': 199.00,
                'duracion_dias': 30,
                'max_usuarios': 200,
                'max_evaluaciones': 50,
                'soporte_incluido': True,
                'activo': True
            },
            {
                'nombre': 'Plan Enterprise',
                'descripcion': 'Plan empresarial para grandes corporaciones con funcionalidades completas',
                'precio': 399.00,
                'duracion_dias': 30,
                'max_usuarios': 1000,
                'max_evaluaciones': 200,
                'soporte_incluido': True,
                'activo': True
            },
            {
                'nombre': 'Plan Anual Básico',
                'descripcion': 'Plan básico con descuento por pago anual',
                'precio': 999.00,
                'duracion_dias': 365,
                'max_usuarios': 50,
                'max_evaluaciones': 120,
                'soporte_incluido': True,
                'activo': True
            },
            {
                'nombre': 'Plan Anual Profesional',
                'descripcion': 'Plan profesional con descuento por pago anual',
                'precio': 1999.00,
                'duracion_dias': 365,
                'max_usuarios': 200,
                'max_evaluaciones': 600,
                'soporte_incluido': True,
                'activo': True
            }
        ]
        
        for plan_data in planes_data:
            plan, created = PlanSuscripcion.objects.get_or_create(
                nombre=plan_data['nombre'],
                defaults=plan_data
            )
            if created:
                print(f"  ✅ {plan.nombre} - ${plan.precio}")
            else:
                print(f"  🔄 {plan.nombre} (ya existía)")
        
        print(f"✅ {len(planes_data)} planes de suscripción configurados")
        return True
        
    except Exception as e:
        print(f"❌ Error creando planes: {e}")
        return False

def crear_departamentos_puestos_empleados(plantas):
    """Crear estructura organizacional completa"""
    print("\n📋 CREANDO ESTRUCTURA ORGANIZACIONAL...")
    
    try:
        from apps.users.models import Departamento, Puesto, Empleado
        
        # Departamentos por planta
        departamentos_nombres = [
            'Recursos Humanos',
            'Producción', 
            'Mantenimiento',
            'Calidad',
            'Logística',
            'Administración',
            'Ventas'
        ]
        
        # Puestos por departamento
        puestos_data = {
            'Recursos Humanos': ['Director de RRHH', 'Gerente de RRHH', 'Especialista en RRHH', 'Asistente de RRHH'],
            'Producción': ['Director de Producción', 'Gerente de Producción', 'Supervisor', 'Operador', 'Técnico'],
            'Mantenimiento': ['Jefe de Mantenimiento', 'Técnico Mecánico', 'Técnico Eléctrico', 'Auxiliar'],
            'Calidad': ['Jefe de Calidad', 'Inspector de Calidad', 'Analista de Calidad'],
            'Logística': ['Jefe de Logística', 'Coordinador', 'Almacenista', 'Auxiliar de Almacén'],
            'Administración': ['Director Administrativo', 'Contador', 'Auxiliar Contable', 'Recepcionista'],
            'Ventas': ['Director de Ventas', 'Gerente de Ventas', 'Ejecutivo de Ventas', 'Asistente de Ventas']
        }
        
        total_empleados = 0
        
        for planta in plantas:
            print(f"\n  🏭 {planta.nombre}:")
            
            for dept_nombre in departamentos_nombres:
                # Crear departamento
                departamento = Departamento.objects.create(
                    nombre=dept_nombre,
                    descripcion=f"Departamento de {dept_nombre} - {planta.nombre}",
                    planta=planta,
                    status=True
                )
                print(f"    📋 {dept_nombre}")
                
                # Crear puestos y empleados
                for puesto_nombre in puestos_data[dept_nombre]:
                    # Crear puesto
                    puesto = Puesto.objects.create(
                        nombre=puesto_nombre,
                        descripcion=f"Puesto de {puesto_nombre}",
                        departamento=departamento,
                        status=True
                    )
                    
                    # Crear empleados (1-3 por puesto según el tipo)
                    num_empleados = 3 if 'Operador' in puesto_nombre or 'Auxiliar' in puesto_nombre else 1
                    if 'Director' in puesto_nombre or 'Jefe' in puesto_nombre:
                        num_empleados = 1
                    
                    for i in range(num_empleados):
                        empleado_num = random.randint(1000, 9999)
                        empleado = Empleado.objects.create(
                            nombre=f"Empleado{empleado_num}",
                            apellido_paterno=f"Apellido{empleado_num}",
                            apellido_materno="Prueba",
                            email=f"empleado{empleado_num}@{planta.empresa.nombre.lower().replace(' ', '')}.mx",
                            telefono=f"442{random.randint(1000000, 9999999)}",
                            fecha_ingreso=date.today() - timedelta(days=random.randint(30, 365)),
                            puesto=puesto,
                            status=True
                        )
                        total_empleados += 1
        
        print(f"\n✅ Estructura completa creada:")
        print(f"  📋 {len(departamentos_nombres) * len(plantas)} departamentos")
        print(f"  💼 {Puesto.objects.count()} puestos")
        print(f"  👥 {total_empleados} empleados")
        
        return True
        
    except Exception as e:
        print(f"❌ Error creando estructura: {e}")
        return False

@transaction.atomic
def main():
    """Función principal"""
    print("🎯 CARGADOR DE DATOS DE PRUEBA - AXYOMA")
    print("=" * 60)
    print("Este script cargará datos de prueba completos para el sistema.")
    print()
    
    respuesta = input("¿Continuar? (s/n): ").lower()
    if respuesta not in ['s', 'si', 'y', 'yes']:
        print("❌ Operación cancelada")
        return
    
    # Ejecutar pasos
    pasos_exitosos = 0
    total_pasos = 6
    
    if limpiar_datos():
        pasos_exitosos += 1
    else:
        print("❌ Error en limpieza, deteniendo proceso")
        return
    
    if crear_superadmin():
        pasos_exitosos += 1
    else:
        print("❌ Error creando superadmin, deteniendo proceso")
        return
    
    if crear_planes_suscripcion():
        pasos_exitosos += 1
    else:
        print("❌ Error creando planes, deteniendo proceso")
        return
    
    empresas = crear_empresas()
    if empresas:
        pasos_exitosos += 1
    else:
        print("❌ Error creando empresas, deteniendo proceso")
        return
    
    plantas = crear_plantas(empresas)
    if plantas:
        pasos_exitosos += 1
    else:
        print("❌ Error creando plantas, deteniendo proceso")
        return
    
    if crear_departamentos_puestos_empleados(plantas):
        pasos_exitosos += 1
    else:
        print("❌ Error creando estructura organizacional")
        return
    
    # Resultado final
    print("\n" + "=" * 60)
    print("🎉 ¡DATOS DE PRUEBA CARGADOS EXITOSAMENTE!")
    print("=" * 60)
    print(f"✅ {pasos_exitosos}/{total_pasos} pasos completados")
    print()
    print("📊 DATOS CREADOS:")
    print("  👑 1 SuperAdmin (superadmin / admin123)")
    print("  💳 5 Planes de Suscripción (Básico, Profesional, Enterprise)")
    print("  🏢 2 Empresas (TechCorp, InnovaSoft)")
    print("  🏭 4 Plantas (2 por empresa)")
    print("  📋 28 Departamentos (7 por planta)")
    print("  💼 ~100 Puestos diferentes")
    print("  👥 ~200 Empleados distribuidos")
    print()
    print("🔑 CREDENCIALES:")
    print("  Usuario: superadmin")
    print("  Password: admin123")
    print()
    print("🚀 PARA USAR:")
    print("  python manage.py runserver")
    print("  http://localhost:8000")
    print("=" * 60)

if __name__ == "__main__":
    main()
