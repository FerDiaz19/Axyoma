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
from apps.evaluaciones.models import TipoEvaluacion, EvaluacionCompleta, AsignacionEvaluacion, TokenEvaluacion
from rest_framework.authtoken.models import Token
from django.db import transaction

def limpiar_base_datos():
    """Limpiar toda la base de datos"""
    print('🧹 LIMPIANDO BASE DE DATOS...')
    
    # Eliminar en orden para evitar problemas de foreign keys
    TokenEvaluacion.objects.all().delete()
    AsignacionEvaluacion.objects.all().delete()
    EvaluacionCompleta.objects.all().delete()
    TipoEvaluacion.objects.all().delete()
    SuscripcionEmpresa.objects.all().delete()
    PlanSuscripcion.objects.all().delete()
    Empleado.objects.all().delete()
    Puesto.objects.all().delete()
    Departamento.objects.all().delete()
    Planta.objects.all().delete()
    PerfilUsuario.objects.all().delete()
    Token.objects.all().delete()
    User.objects.all().delete()
    Empresa.objects.all().delete()
    
    print('✅ Base de datos limpiada exitosamente')

def crear_datos_iniciales():
    """Crear datos completos de inicio para Axyoma"""
    print('🚀 CREANDO DATOS INICIALES PARA AXYOMA...')
    
    with transaction.atomic():
        # 1. Crear SuperAdmin
        print('👤 Creando SuperAdmin...')
        superadmin_user = User.objects.create_user(
            username='superadmin',
            password='admin123',
            email='superadmin@axyoma.com',
            first_name='Super',
            last_name='Admin',
            is_superuser=True,
            is_staff=True
        )
        
        superadmin_profile = PerfilUsuario.objects.create(
            user=superadmin_user,
            nivel_usuario='SuperAdmin',
            fecha_registro=datetime.now()
        )
        
        # Crear token para SuperAdmin
        Token.objects.create(user=superadmin_user)
        
        # 2. Crear Empresa Axyoma
        print('🏢 Creando Empresa Axyoma...')
        empresa_axyoma = Empresa.objects.create(
            nombre='Axyoma',
            rfc='AXY123456789',
            telefono='555-0123',
            correo='contacto@axyoma.com',
            direccion='Av. Innovación 123, Ciudad de México',
            fecha_registro=datetime.now(),
            status=True
        )
        
        # 3. Crear Admin de Empresa
        print('👥 Creando Admin de Empresa...')
        admin_user = User.objects.create_user(
            username='admin_axyoma',
            password='admin123',
            email='admin@axyoma.com',
            first_name='Admin',
            last_name='Axyoma'
        )
        
        admin_profile = PerfilUsuario.objects.create(
            user=admin_user,
            nivel_usuario='AdminEmpresa',
            admin_empresa=empresa_axyoma.empresa_id,
            fecha_registro=datetime.now()
        )
        
        # Actualizar empresa con administrador
        empresa_axyoma.administrador = admin_user.id
        empresa_axyoma.save()
        
        Token.objects.create(user=admin_user)
        
        # 4. Crear Plantas
        print('🏭 Creando Plantas...')
        planta_norte = Planta.objects.create(
            nombre='Planta Norte',
            empresa=empresa_axyoma.empresa_id,
            telefono='555-0124',
            correo='norte@axyoma.com',
            direccion='Zona Industrial Norte, Monterrey',
            fecha_registro=datetime.now(),
            status=True
        )
        
        planta_sur = Planta.objects.create(
            nombre='Planta Sur',
            empresa=empresa_axyoma.empresa_id,
            telefono='555-0125',
            correo='sur@axyoma.com',
            direccion='Zona Industrial Sur, Guadalajara',
            fecha_registro=datetime.now(),
            status=True
        )
        
        plantas = [planta_norte, planta_sur]
        
        # 5. Crear usuarios de planta
        print('👷 Creando Usuarios de Planta...')
        for i, planta in enumerate(plantas, 1):
            user_planta = User.objects.create_user(
                username=f'planta_{planta.planta_id}',
                password='planta123',
                email=f'planta{i}@axyoma.com',
                first_name=f'Usuario',
                last_name=f'Planta {i}'
            )
            
            PerfilUsuario.objects.create(
                user=user_planta,
                nivel_usuario='AdminPlanta',
                admin_empresa=empresa_axyoma.empresa_id,
                planta_asignada=planta.planta_id,
                fecha_registro=datetime.now()
            )
            
            Token.objects.create(user=user_planta)
            
            # Actualizar username de la planta
            planta.username = user_planta.username
            planta.save()
        
        # 6. Crear Departamentos
        print('🏢 Creando Departamentos...')
        departamentos_data = [
            {'nombre': 'Recursos Humanos', 'planta': planta_norte},
            {'nombre': 'Producción', 'planta': planta_norte},
            {'nombre': 'Control de Calidad', 'planta': planta_norte},
            {'nombre': 'Mantenimiento', 'planta': planta_sur},
            {'nombre': 'Logística', 'planta': planta_sur},
            {'nombre': 'Seguridad Industrial', 'planta': planta_sur}
        ]
        
        departamentos = []
        for dept_data in departamentos_data:
            departamento = Departamento.objects.create(
                nombre=dept_data['nombre'],
                planta=dept_data['planta'].planta_id,
                fecha_registro=datetime.now(),
                status=True
            )
            departamentos.append(departamento)
        
        # 7. Crear Puestos
        print('💼 Creando Puestos...')
        puestos_data = [
            # Recursos Humanos
            {'nombre': 'Gerente de RRHH', 'descripcion': 'Gestión del personal', 'departamento': departamentos[0]},
            {'nombre': 'Analista de RRHH', 'descripcion': 'Análisis y procesos de personal', 'departamento': departamentos[0]},
            # Producción
            {'nombre': 'Jefe de Producción', 'descripcion': 'Supervisión de procesos productivos', 'departamento': departamentos[1]},
            {'nombre': 'Operador de Máquina', 'descripcion': 'Operación de equipos de producción', 'departamento': departamentos[1]},
            {'nombre': 'Técnico de Proceso', 'descripcion': 'Optimización de procesos', 'departamento': departamentos[1]},
            # Control de Calidad
            {'nombre': 'Supervisor de Calidad', 'descripcion': 'Control y aseguramiento de calidad', 'departamento': departamentos[2]},
            {'nombre': 'Inspector de Calidad', 'descripcion': 'Inspección de productos', 'departamento': departamentos[2]},
            # Mantenimiento
            {'nombre': 'Jefe de Mantenimiento', 'descripcion': 'Coordinación de mantenimiento', 'departamento': departamentos[3]},
            {'nombre': 'Técnico Mecánico', 'descripcion': 'Mantenimiento mecánico', 'departamento': departamentos[3]},
            # Logística
            {'nombre': 'Coordinador Logístico', 'descripcion': 'Gestión de inventarios y envíos', 'departamento': departamentos[4]},
            # Seguridad Industrial
            {'nombre': 'Jefe de Seguridad', 'descripcion': 'Supervisión de seguridad industrial', 'departamento': departamentos[5]}
        ]
        
        puestos = []
        for puesto_data in puestos_data:
            puesto = Puesto.objects.create(
                nombre=puesto_data['nombre'],
                descripcion=puesto_data['descripcion'],
                departamento=puesto_data['departamento'].departamento_id,
                fecha_registro=datetime.now(),
                status=True
            )
            puestos.append(puesto)
        
        # 8. Crear Empleados
        print('👨‍💼 Creando Empleados...')
        empleados_data = [
            {'numero': 'EMP001', 'nombre': 'Juan', 'apellido': 'Pérez', 'email': 'juan.perez@axyoma.com', 'telefono': '555-1001', 'puesto': puestos[0]},
            {'numero': 'EMP002', 'nombre': 'María', 'apellido': 'González', 'email': 'maria.gonzalez@axyoma.com', 'telefono': '555-1002', 'puesto': puestos[1]},
            {'numero': 'EMP003', 'nombre': 'Carlos', 'apellido': 'López', 'email': 'carlos.lopez@axyoma.com', 'telefono': '555-1003', 'puesto': puestos[2]},
            {'numero': 'EMP004', 'nombre': 'Ana', 'apellido': 'Martínez', 'email': 'ana.martinez@axyoma.com', 'telefono': '555-1004', 'puesto': puestos[3]},
            {'numero': 'EMP005', 'nombre': 'Luis', 'apellido': 'Rodríguez', 'email': 'luis.rodriguez@axyoma.com', 'telefono': '555-1005', 'puesto': puestos[4]},
            {'numero': 'EMP006', 'nombre': 'Carmen', 'apellido': 'Hernández', 'email': 'carmen.hernandez@axyoma.com', 'telefono': '555-1006', 'puesto': puestos[5]},
            {'numero': 'EMP007', 'nombre': 'Miguel', 'apellido': 'Torres', 'email': 'miguel.torres@axyoma.com', 'telefono': '555-1007', 'puesto': puestos[6]},
            {'numero': 'EMP008', 'nombre': 'Laura', 'apellido': 'Ramírez', 'email': 'laura.ramirez@axyoma.com', 'telefono': '555-1008', 'puesto': puestos[7]},
            {'numero': 'EMP009', 'nombre': 'José', 'apellido': 'Flores', 'email': 'jose.flores@axyoma.com', 'telefono': '555-1009', 'puesto': puestos[8]},
            {'numero': 'EMP010', 'nombre': 'Patricia', 'apellido': 'Cruz', 'email': 'patricia.cruz@axyoma.com', 'telefono': '555-1010', 'puesto': puestos[9]},
            {'numero': 'EMP011', 'nombre': 'Roberto', 'apellido': 'Morales', 'email': 'roberto.morales@axyoma.com', 'telefono': '555-1011', 'puesto': puestos[10]}
        ]
        
        empleados = []
        for emp_data in empleados_data:
            empleado = Empleado.objects.create(
                numero_empleado=emp_data['numero'],
                nombre=emp_data['nombre'],
                apellido=emp_data['apellido'],
                email=emp_data['email'],
                telefono=emp_data['telefono'],
                puesto=emp_data['puesto'].puesto_id,
                fecha_registro=datetime.now(),
                status=True
            )
            empleados.append(empleado)
        
        # 9. Crear Planes de Suscripción
        print('💳 Creando Planes de Suscripción...')
        plan_basico = PlanSuscripcion.objects.create(
            nombre='Plan Básico',
            descripcion='Hasta 50 empleados, evaluaciones básicas',
            duracion=30,  # 30 días
            precio=999.00,
            status=True
        )
        
        plan_profesional = PlanSuscripcion.objects.create(
            nombre='Plan Profesional',
            descripcion='Hasta 200 empleados, evaluaciones avanzadas',
            duracion=30,  # 30 días
            precio=2999.00,
            status=True
        )
        
        plan_empresarial = PlanSuscripcion.objects.create(
            nombre='Plan Empresarial',
            descripcion='Empleados ilimitados, todas las funciones',
            duracion=30,  # 30 días
            precio=5999.00,
            status=True
        )
        
        # 10. Crear Suscripción para Axyoma
        print('📋 Creando Suscripción para Axyoma...')
        fecha_inicio = datetime.now()
        fecha_fin = fecha_inicio + timedelta(days=365)  # 1 año
        
        suscripcion = SuscripcionEmpresa.objects.create(
            empresa=empresa_axyoma.empresa_id,
            plan=plan_empresarial.plan_id,
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin,
            estado='Activa',
            status=True,
            fecha_creacion=datetime.now(),
            fecha_actualizacion=datetime.now()
        )
        
        # 11. Crear Tipos de Evaluación
        print('📊 Creando Tipos de Evaluación...')
        tipos_evaluacion = [
            {'nombre': 'Evaluación de Desempeño 360°', 'descripcion': 'Evaluación integral de desempeño'},
            {'nombre': 'Evaluación de Competencias', 'descripcion': 'Evaluación de competencias técnicas y blandas'},
            {'nombre': 'Evaluación de Clima Laboral', 'descripcion': 'Evaluación del ambiente de trabajo'},
            {'nombre': 'Evaluación de Satisfacción', 'descripcion': 'Evaluación de satisfacción laboral'},
            {'nombre': 'Evaluación de Liderazgo', 'descripcion': 'Evaluación de habilidades de liderazgo'}
        ]
        
        tipos_obj = []
        for tipo_data in tipos_evaluacion:
            tipo = TipoEvaluacion.objects.create(
                nombre=tipo_data['nombre'],
                descripcion=tipo_data['descripcion']
            )
            tipos_obj.append(tipo)
        
        # 12. Crear Evaluaciones de Ejemplo
        print('📝 Creando Evaluaciones de Ejemplo...')
        evaluaciones_data = [
            {
                'titulo': 'Evaluación de Desempeño Q1 2025',
                'descripcion': 'Evaluación de desempeño del primer trimestre',
                'tipo': tipos_obj[0],
                'activa': True
            },
            {
                'titulo': 'Evaluación de Competencias Técnicas',
                'descripcion': 'Evaluación de competencias técnicas específicas',
                'tipo': tipos_obj[1],
                'activa': True
            },
            {
                'titulo': 'Clima Laboral 2025',
                'descripcion': 'Evaluación anual de clima laboral',
                'tipo': tipos_obj[2],
                'activa': False
            }
        ]
        
        for eval_data in evaluaciones_data:
            evaluacion = EvaluacionCompleta.objects.create(
                titulo=eval_data['titulo'],
                descripcion=eval_data['descripcion'],
                tipo_evaluacion=eval_data['tipo'].id,
                empresa_id=empresa_axyoma.empresa_id,
                activa=eval_data['activa'],
                fecha_creacion=datetime.now(),
                identificador_unico=f"EVAL-{datetime.now().strftime('%Y%m%d')}-{eval_data['titulo'][:10].upper()}"
            )
    
    print('✅ DATOS INICIALES CREADOS EXITOSAMENTE')
    print('=' * 60)
    print('📋 RESUMEN DE DATOS CREADOS:')
    print(f'• Empresa: {Empresa.objects.count()}')
    print(f'• Usuarios: {User.objects.count()}')
    print(f'• Plantas: {Planta.objects.count()}')
    print(f'• Departamentos: {Departamento.objects.count()}')
    print(f'• Puestos: {Puesto.objects.count()}')
    print(f'• Empleados: {Empleado.objects.count()}')
    print(f'• Planes: {PlanSuscripcion.objects.count()}')
    print(f'• Suscripciones: {SuscripcionEmpresa.objects.count()}')
    print(f'• Tipos de Evaluación: {TipoEvaluacion.objects.count()}')
    print(f'• Evaluaciones: {EvaluacionCompleta.objects.count()}')
    print('=' * 60)
    print('🔑 CREDENCIALES DE ACCESO:')
    print('SuperAdmin:')
    print('  Usuario: superadmin')
    print('  Contraseña: admin123')
    print()
    print('Admin Empresa (Axyoma):')
    print('  Usuario: admin_axyoma')
    print('  Contraseña: admin123')
    print()
    print('Usuarios Planta:')
    print('  Usuario: planta_1')
    print('  Usuario: planta_2')
    print('  Contraseña: planta123')
    print('=' * 60)

def main():
    """Función principal"""
    print('🚀 INICIALIZANDO SISTEMA AXYOMA')
    print('=' * 60)
    
    try:
        # Limpiar base de datos
        limpiar_base_datos()
        
        # Crear datos iniciales
        crear_datos_iniciales()
        
        print('🎉 SISTEMA INICIALIZADO EXITOSAMENTE')
        
    except Exception as e:
        print(f'❌ ERROR: {e}')
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()
