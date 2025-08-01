import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')

import django
django.setup()

from django.contrib.auth.models import User
from apps.users.models import PerfilUsuario, Empresa, Planta, Departamento, Puesto, Empleado
from apps.subscriptions.models import PlanSuscripcion
from datetime import date, timedelta
import random

print("🎯 CARGANDO DATOS SIN LIMPIEZA")

# Crear superadmin solo si no existe
if not User.objects.filter(username='superadmin').exists():
    print("👑 Creando superadmin...")
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
    print("✅ SuperAdmin creado")
else:
    print("✅ SuperAdmin ya existe")

# Crear empresas solo si no existen
if not Empresa.objects.exists():
    print("🏢 Creando empresas...")
    
    # Crear usuarios administradores para las empresas
    admin_user1 = User.objects.create_user(
        username='admin_techcorp',
        email='admin@techcorp.mx',
        password='admin123',
        first_name='Admin',
        last_name='TechCorp'
    )
    
    admin_perfil1 = PerfilUsuario.objects.create(
        nombre='Admin',
        apellido_paterno='TechCorp',
        correo='admin@techcorp.mx',
        nivel_usuario='admin-empresa',
        status=True,
        user=admin_user1
    )
    
    admin_user2 = User.objects.create_user(
        username='admin_innovasoft',
        email='admin@innovasoft.mx',
        password='admin123',
        first_name='Admin',
        last_name='InnovaSoft'
    )
    
    admin_perfil2 = PerfilUsuario.objects.create(
        nombre='Admin',
        apellido_paterno='InnovaSoft',
        correo='admin@innovasoft.mx',
        nivel_usuario='admin-empresa',
        status=True,
        user=admin_user2
    )
    
    empresa1 = Empresa.objects.create(
        nombre='TechCorp Solutions',
        rfc='TCS950815MX3',
        direccion='Av. Tecnológico 1500',
        email_contacto='contacto@techcorp.mx',
        telefono_contacto='4421234567',
        administrador=admin_perfil1,
        status=True
    )

    empresa2 = Empresa.objects.create(
        nombre='InnovaSoft Industries',
        rfc='ISI980320QR1',
        direccion='Blvd. Bernardo Quintana 2000',
        email_contacto='info@innovasoft.mx',
        telefono_contacto='4427654321',
        administrador=admin_perfil2,
        status=True
    )
    print("✅ 2 empresas creadas con administradores")
else:
    print("✅ Empresas ya existen")
    empresa1 = Empresa.objects.first()
    empresa2 = Empresa.objects.last()

# Crear plantas solo si no existen
if not Planta.objects.exists():
    print("🏭 Creando plantas...")
    planta1 = Planta.objects.create(nombre='Planta Norte', direccion='Zona Norte', empresa=empresa1, status=True)
    planta2 = Planta.objects.create(nombre='Planta Sur', direccion='Zona Sur', empresa=empresa1, status=True)
    planta3 = Planta.objects.create(nombre='Planta Central', direccion='Zona Central', empresa=empresa2, status=True)
    planta4 = Planta.objects.create(nombre='Planta Satelite', direccion='Zona Satelite', empresa=empresa2, status=True)
    print("✅ 4 plantas creadas")
else:
    print("✅ Plantas ya existen")

# Crear estructura solo si no existe
if not Empleado.objects.exists():
    print("📋 Creando estructura...")
    plantas = list(Planta.objects.all())
    departamentos_nombres = ['RRHH', 'Producción', 'Mantenimiento', 'Calidad', 'Logística']
    puestos_nombres = ['Director', 'Gerente', 'Supervisor', 'Operador', 'Técnico']

    total_empleados = 0
    for planta in plantas:
        for dept_nombre in departamentos_nombres:
            dept = Departamento.objects.create(
                nombre=dept_nombre,
                descripcion=f'Departamento de {dept_nombre}',
                planta=planta,
                status=True
            )
            
            for puesto_nombre in puestos_nombres:
                puesto = Puesto.objects.create(
                    nombre=puesto_nombre,
                    descripcion=f'Puesto de {puesto_nombre}',
                    departamento=dept,
                    status=True
                )
                
                # Crear 1-2 empleados por puesto
                num_empleados = 2 if puesto_nombre in ['Operador', 'Técnico'] else 1
                
                for i in range(num_empleados):
                    emp_num = random.randint(1000, 9999)
                    empleado = Empleado.objects.create(
                        nombre=f'Empleado{emp_num}',
                        apellido_paterno=f'Apellido{emp_num}',
                        apellido_materno='Test',
                        email=f'emp{emp_num}@test.com',
                        telefono=f'442{random.randint(1000000, 9999999)}',
                        fecha_ingreso=date.today() - timedelta(days=random.randint(30, 365)),
                        puesto=puesto,
                        status=True
                    )
                    total_empleados += 1

    print(f"✅ {total_empleados} empleados creados")
else:
    print("✅ Empleados ya existen")

# Crear planes de suscripción
if not PlanSuscripcion.objects.exists():
    print("💳 Creando planes de suscripción...")
    
    planes = [
        {
            'nombre': 'Plan Básico',
            'descripcion': 'Plan básico para empresas pequeñas',
            'precio': 299.00,
            'duracion': 30,  # días
            'fecha_registro': date.today(),
            'status': True
        },
        {
            'nombre': 'Plan Profesional', 
            'descripcion': 'Plan profesional para empresas medianas',
            'precio': 599.00,
            'duracion': 30,  # días
            'fecha_registro': date.today(),
            'status': True
        },
        {
            'nombre': 'Plan Empresarial',
            'descripcion': 'Plan empresarial para grandes organizaciones',
            'precio': 1299.00,
            'duracion': 30,  # días
            'fecha_registro': date.today(),
            'status': True
        }
    ]
    
    for plan_data in planes:
        plan = PlanSuscripcion.objects.create(**plan_data)
        print(f"  ✅ {plan.nombre} - ${plan.precio}")
    
    print("✅ Planes de suscripción creados")
else:
    print("✅ Planes de suscripción ya existen")

# Crear tipos de evaluación y evaluaciones básicas
try:
    from apps.evaluaciones.models import TipoEvaluacion, EvaluacionCompleta
    
    if not TipoEvaluacion.objects.exists():
        print("📊 Creando tipos de evaluación...")
        
        tipos_eval = [
            {
                'nombre': 'Normativa',
                'descripcion': 'Evaluaciones que cumplen con normativas oficiales',
                'normativa_oficial': True,
                'activo': True
            },
            {
                'nombre': 'Interna',
                'descripcion': 'Evaluaciones internas de la empresa',
                'normativa_oficial': False,
                'activo': True
            }
        ]
        
        for tipo_data in tipos_eval:
            tipo = TipoEvaluacion.objects.create(**tipo_data)
            print(f"  ✅ {tipo.nombre}")
        
        print("✅ Tipos de evaluación creados")
    else:
        print("✅ Tipos de evaluación ya existen")
        
    if not EvaluacionCompleta.objects.exists():
        print("📋 Creando evaluación NOM-035...")
        
        tipo_normativa = TipoEvaluacion.objects.filter(nombre='Normativa').first()
        superuser = User.objects.filter(is_superuser=True).first()
        
        evaluacion_nom035 = EvaluacionCompleta.objects.create(
            titulo='Evaluación NOM-035 - Factores de Riesgo Psicosocial',
            descripcion='Evaluación oficial para identificar factores de riesgo psicosocial en el trabajo',
            estado='activa',
            fecha_inicio=date.today(),
            fecha_fin=date.today() + timedelta(days=365),
            es_anonima=True,
            creada_por=superuser,
            empresa=None,  # Evaluación global
            tipo_evaluacion=tipo_normativa
        )
        
        print(f"  ✅ {evaluacion_nom035.titulo}")
        print("✅ Evaluación NOM-035 creada")
    else:
        print("✅ Evaluaciones ya existen")
        
except ImportError:
    print("⚠️  Modelos de evaluaciones no disponibles, saltando...")
except Exception as e:
    print(f"⚠️  Error creando evaluaciones: {e}")

print("")
print("🎉 ¡DATOS VERIFICADOS Y CARGADOS!")
print("=" * 50)
print(f"✅ SuperAdmins: {User.objects.filter(is_superuser=True).count()}")
print(f"✅ Empresas: {Empresa.objects.count()}")
print(f"✅ Plantas: {Planta.objects.count()}")
print(f"✅ Departamentos: {Departamento.objects.count()}")
print(f"✅ Puestos: {Puesto.objects.count()}")
print(f"✅ Empleados: {Empleado.objects.count()}")
print(f"✅ Planes de Suscripción: {PlanSuscripcion.objects.count()}")

try:
    from apps.evaluaciones.models import TipoEvaluacion, EvaluacionCompleta
    print(f"✅ Tipos de Evaluación: {TipoEvaluacion.objects.count()}")
    print(f"✅ Evaluaciones: {EvaluacionCompleta.objects.count()}")
except:
    pass

print("")
print("🔑 CREDENCIALES:")
print("  SuperAdmin: superadmin / admin123")
print("  Admin TechCorp: admin_techcorp / admin123")
print("  Admin InnovaSoft: admin_innovasoft / admin123")
print("")
print("🚀 PARA INICIAR:")
print("  python manage.py runserver")
print("  O ejecutar: ..\\start.bat")
print("=" * 50)
