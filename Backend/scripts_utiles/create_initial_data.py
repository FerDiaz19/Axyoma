#!/usr/bin/env python
"""
Script para crear datos iniciales del sistema Axyoma
Crea usuarios, empresa, plantas, departamentos, puestos y planes de suscripción
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
    PlanSuscripcion, Suscripcion, Empleado, AdminPlanta
)
from datetime import datetime, timedelta

def create_initial_data():
    """Crear todos los datos iniciales del sistema"""
    
    print("🚀 Iniciando creación de datos iniciales...")
    
    with transaction.atomic():
        # 1. Crear Planes de Suscripción
        print("📋 Creando planes de suscripción...")
        
        plan_basico, created = PlanSuscripcion.objects.get_or_create(
            nombre="Básico",
            defaults={
                'descripcion': 'Plan básico para empresas pequeñas',
                'duracion': 30,
                'precio': 499.00,
                'status': True
            }
        )
        
        plan_profesional, created = PlanSuscripcion.objects.get_or_create(
            nombre="Profesional",
            defaults={
                'descripcion': 'Plan profesional para empresas medianas',
                'duracion': 30,
                'precio': 999.00,
                'status': True
            }
        )
        
        plan_empresarial, created = PlanSuscripcion.objects.get_or_create(
            nombre="Empresarial",
            defaults={
                'descripcion': 'Plan empresarial para grandes corporaciones',
                'duracion': 30,
                'precio': 1999.00,
                'status': True
            }
        )
        
        print(f"   ✅ Creados 3 planes de suscripción")
        
        # 2. Crear Usuario SuperAdmin
        print("👤 Creando SuperAdmin...")
        
        # Usuario Django para SuperAdmin
        superadmin_user, created = User.objects.get_or_create(
            username='superadmin',
            defaults={
                'email': 'ed-rubio@axyoma.com',
                'first_name': 'Eduardo',
                'last_name': 'Rubio',
                'is_staff': True,
                'is_superuser': True
            }
        )
        if created:
            superadmin_user.set_password('1234')
            superadmin_user.save()
        
        # Usuario Axyoma para SuperAdmin
        superadmin_usuario, created = Usuario.objects.get_or_create(
            correo='ed-rubio@axyoma.com',
            defaults={
                'nombre': 'Eduardo',
                'apellido_paterno': 'Rubio',
                'apellido_materno': 'González',
                'nivel_usuario': 'superadmin',
                'status': True,
                'user': superadmin_user
            }
        )
        
        print(f"   ✅ SuperAdmin creado: {superadmin_usuario.correo}")
          # 3. Crear Admin Empresa (temporalmente sin empresa)
        print("👤 Creando Admin Empresa...")
        
        admin_empresa_user, created = User.objects.get_or_create(
            username='admin_empresa',
            defaults={
                'email': 'juan.perez@codewave.com',
                'first_name': 'Juan',
                'last_name': 'Pérez',
                'is_staff': False,
                'is_superuser': False
            }
        )
        if created:
            admin_empresa_user.set_password('1234')
            admin_empresa_user.save()

        admin_empresa, created = Usuario.objects.get_or_create(
            correo='juan.perez@codewave.com',
            defaults={
                'nombre': 'Juan',
                'apellido_paterno': 'Pérez',
                'apellido_materno': 'López',
                'nivel_usuario': 'admin-empresa',
                'status': True,
                'user': admin_empresa_user
            }
        )
        
        print(f"   ✅ Admin Empresa creado: {admin_empresa.correo}")

        # 4. Crear Empresa de prueba
        print("🏢 Creando empresa de prueba...")
        
        empresa, created = Empresa.objects.get_or_create(
            rfc='CWT240701ABC',
            defaults={
                'nombre': 'CodeWave Technologies',
                'direccion': 'Av. Revolución 1234, Col. San Ángel, CDMX',
                'email_contacto': 'contacto@codewave.com',
                'telefono_contacto': '+525598765432',
                'status': True,
                'administrador': admin_empresa
            }
        )
        
        print(f"   ✅ Empresa creada: {empresa.nombre}")

        # 5. Crear Suscripción para la empresa
        print("💳 Creando suscripción...")
        
        suscripcion, created = Suscripcion.objects.get_or_create(
            empresa=empresa,
            defaults={
                'plan_suscripcion': plan_profesional,
                'fecha_inicio': datetime.now().date(),
                'fecha_fin': (datetime.now() + timedelta(days=365)).date(),
                'estado': 'Activa',
                'status': True
            }
        )
        
        print(f"   ✅ Suscripción creada: Plan {suscripcion.plan_suscripcion.nombre}")

        # 6. Crear Planta Principal de la empresa (automática al registrarse)
        print("🏭 Creando planta principal de la empresa...")
        
        planta_principal, created = Planta.objects.get_or_create(
            nombre='Planta Principal',
            empresa=empresa,
            defaults={
                'direccion': 'Av. Revolución 1234, Col. San Ángel, CDMX',  # Misma dirección que la empresa inicialmente
                'status': True
            }
        )
        
        print(f"   ✅ Planta Principal creada: {planta_principal.nombre} (planta donde contrató el servicio)")
        
        # 7. Crear Departamentos en la Planta Principal
        print("🏢 Creando departamentos en la planta principal...")
        
        departamentos_data = [
            # Departamentos administrativos
            {'nombre': 'Administración', 'descripcion': 'Gestión administrativa general'},
            {'nombre': 'Recursos Humanos', 'descripcion': 'Gestión del personal y nómina'},
            {'nombre': 'Finanzas', 'descripcion': 'Gestión financiera y contable'},
            # Departamentos operativos
            {'nombre': 'Producción', 'descripcion': 'Operaciones de manufactura'},
            {'nombre': 'Calidad', 'descripcion': 'Control y aseguramiento de calidad'},
            {'nombre': 'Mantenimiento', 'descripcion': 'Mantenimiento de equipos e instalaciones'},
            {'nombre': 'Logística', 'descripcion': 'Almacén y distribución'},
        ]
        
        departamentos = []
        for dept_data in departamentos_data:
            dept, created = Departamento.objects.get_or_create(
                nombre=dept_data['nombre'],
                planta=planta_principal,
                defaults={
                    'descripcion': dept_data['descripcion']
                }
            )
            departamentos.append(dept)
        
        print(f"   ✅ Creados {len(departamentos)} departamentos en la planta principal")
        
        # 8. Crear Puestos para todos los departamentos
        print("💼 Creando puestos...")
        
        puestos_data = [
            # Administración
            {'nombre': 'Gerente General', 'departamento': 'Administración'},
            {'nombre': 'Asistente Administrativo', 'departamento': 'Administración'},
            
            # Recursos Humanos
            {'nombre': 'Gerente de RRHH', 'departamento': 'Recursos Humanos'},
            {'nombre': 'Especialista en Nómina', 'departamento': 'Recursos Humanos'},
            {'nombre': 'Reclutador', 'departamento': 'Recursos Humanos'},
            
            # Finanzas
            {'nombre': 'Contador', 'departamento': 'Finanzas'},
            {'nombre': 'Analista Financiero', 'departamento': 'Finanzas'},
            
            # Producción
            {'nombre': 'Supervisor de Producción', 'departamento': 'Producción'},
            {'nombre': 'Operador de Máquina', 'departamento': 'Producción'},
            {'nombre': 'Técnico de Proceso', 'departamento': 'Producción'},
            
            # Calidad
            {'nombre': 'Inspector de Calidad', 'departamento': 'Calidad'},
            {'nombre': 'Auditor Interno', 'departamento': 'Calidad'},
            
            # Mantenimiento
            {'nombre': 'Técnico de Mantenimiento', 'departamento': 'Mantenimiento'},
            {'nombre': 'Electricista Industrial', 'departamento': 'Mantenimiento'},
            
            # Logística
            {'nombre': 'Coordinador de Almacén', 'departamento': 'Logística'},
            {'nombre': 'Montacarguista', 'departamento': 'Logística'},
        ]
        
        puestos = []
        for puesto_data in puestos_data:
            dept = next((d for d in departamentos if d.nombre == puesto_data['departamento']), None)
            if dept:
                puesto, created = Puesto.objects.get_or_create(
                    nombre=puesto_data['nombre'],
                    departamento=dept
                )
                puestos.append(puesto)
        
        print(f"   ✅ Creados {len(puestos)} puestos en la planta principal")
        
        # 9. Crear Usuario Admin Planta
        print("👤 Creando Admin Planta...")
        
        admin_planta_user, created = User.objects.get_or_create(
            username='admin_planta',
            defaults={
                'email': 'maria.gomez@codewave.com',
                'first_name': 'María',
                'last_name': 'Gómez',
                'is_staff': False,
                'is_superuser': False
            }
        )
        if created:
            admin_planta_user.set_password('1234')
            admin_planta_user.save()
        
        admin_planta, created = Usuario.objects.get_or_create(
            correo='maria.gomez@codewave.com',
            defaults={
                'nombre': 'María',
                'apellido_paterno': 'Gómez',
                'apellido_materno': 'Rodríguez',
                'nivel_usuario': 'admin-planta',
                'status': True,
                'user': admin_planta_user
            }
        )
        
        # Asignar la planta al admin_planta usando la tabla intermedia
        admin_planta_asignacion, created = AdminPlanta.objects.get_or_create(
            usuario=admin_planta,
            planta=planta_principal,
            defaults={
                'status': True
            }
        )
        
        print(f"   ✅ Admin Planta creado: {admin_planta.correo} - Planta: {planta_principal.nombre}")
        
        # 10. Crear empleados de muestra
        print("👥 Creando empleados de muestra...")
        
        empleados_data = [
            # Empleados administrativos
            {'nombre': 'Laura', 'apellido_paterno': 'Jiménez', 'apellido_materno': 'Ruiz', 'genero': 'Femenino', 'puesto': 'Especialista en Nómina', 'antiguedad': 2},
            {'nombre': 'Pedro', 'apellido_paterno': 'González', 'apellido_materno': 'Morales', 'genero': 'Masculino', 'puesto': 'Contador', 'antiguedad': 4},
            
            # Empleados operativos
            {'nombre': 'Carlos', 'apellido_paterno': 'Martínez', 'apellido_materno': 'Sánchez', 'genero': 'Masculino', 'puesto': 'Supervisor de Producción', 'antiguedad': 5},
            {'nombre': 'Ana', 'apellido_paterno': 'López', 'apellido_materno': 'García', 'genero': 'Femenino', 'puesto': 'Inspector de Calidad', 'antiguedad': 3},
            {'nombre': 'Roberto', 'apellido_paterno': 'Hernández', 'apellido_materno': 'Morales', 'genero': 'Masculino', 'puesto': 'Técnico de Mantenimiento', 'antiguedad': 7},
            {'nombre': 'Diego', 'apellido_paterno': 'Vargas', 'apellido_materno': 'Castro', 'genero': 'Masculino', 'puesto': 'Operador de Máquina', 'antiguedad': 4},
        ]
        
        empleados_creados = 0
        for emp_data in empleados_data:
            puesto = next((p for p in puestos if p.nombre == emp_data['puesto']), None)
            if puesto:
                empleado, created = Empleado.objects.get_or_create(
                    nombre=emp_data['nombre'],
                    apellido_paterno=emp_data['apellido_paterno'],
                    planta=planta_principal,
                    defaults={
                        'apellido_materno': emp_data['apellido_materno'],
                        'genero': emp_data['genero'],
                        'antiguedad': emp_data['antiguedad'],
                        'puesto': puesto,
                        'departamento': puesto.departamento,
                        'status': True
                    }
                )
                if created:
                    empleados_creados += 1
        
        print(f"   ✅ Creados {empleados_creados} empleados en la planta principal")
    
    print("\n🎉 ¡DATOS INICIALES CREADOS EXITOSAMENTE!")
    print("\n📊 RESUMEN:")
    print(f"   ✅ {PlanSuscripcion.objects.count()} planes de suscripción")
    print(f"   ✅ {Usuario.objects.count()} usuarios del sistema")
    print(f"   ✅ {Empresa.objects.count()} empresa")
    print(f"   ✅ {Planta.objects.count()} planta principal (automática al registrarse)")
    print(f"   ✅ {AdminPlanta.objects.count()} asignaciones admin-planta")
    print(f"   ✅ {Departamento.objects.count()} departamentos")
    print(f"   ✅ {Puesto.objects.count()} puestos")
    print(f"   ✅ {Empleado.objects.count()} empleados")
    print(f"   ✅ {Suscripcion.objects.count()} suscripción activa")
    
    print("\n👤 USUARIOS CREADOS:")
    print("   🔑 SuperAdmin:     ed-rubio@axyoma.com / 1234")
    print("   🏢 Admin Empresa:  juan.perez@codewave.com / 1234")
    print("   🏭 Admin Planta:   maria.gomez@codewave.com / 1234")
    
    print("\n🏢 EMPRESA CREADA:")
    print("   📋 Nombre: CodeWave Technologies S.A. de C.V.")
    print("   📄 RFC: CWT240701ABC")
    print("   🏭 Planta Principal: Creada automáticamente al registrarse")
    print("   💳 Plan: Profesional (activo)")
    print("   📝 Nota: Puede crear plantas adicionales desde 'Gestión de Plantas'")
    
    return True

if __name__ == '__main__':
    try:
        success = create_initial_data()
        if success:
            print("\n✅ Proceso completado exitosamente")
            sys.exit(0)
        else:
            print("\n❌ Error en el proceso")
            sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
