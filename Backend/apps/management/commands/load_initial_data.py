from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.db import transaction
from apps.users.models import PerfilUsuario, Empresa, Planta, Departamento, Puesto, Empleado
from apps.subscriptions.models import PlanSuscripcion, SuscripcionEmpresa, Pago
from django.utils import timezone
from datetime import timedelta

class Command(BaseCommand):
    help = 'Carga datos iniciales para el sistema Axyoma'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('🚀 Iniciando carga de datos iniciales...'))
        
        try:
            with transaction.atomic():
                # 1. Crear usuarios básicos
                self.crear_usuarios()
                
                # 2. Crear planes de suscripción
                self.crear_planes()
                
                # 3. Crear empresa de ejemplo
                self.crear_empresa_ejemplo()
                
                self.stdout.write(self.style.SUCCESS('✅ Datos iniciales cargados exitosamente'))
                
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ Error cargando datos iniciales: {str(e)}'))
            raise

    def crear_usuarios(self):
        """Crear usuarios básicos del sistema"""
        self.stdout.write('👥 Creando usuarios básicos...')
        
        # SuperAdmin
        if not User.objects.filter(username='superadmin').exists():
            superadmin_user = User.objects.create(
                username='superadmin',
                password=make_password('1234'),
                email='superadmin@axyoma.com',
                first_name='Super',
                last_name='Admin',
                is_staff=True,
                is_superuser=True,
                is_active=True
            )
            
            PerfilUsuario.objects.create(
                user=superadmin_user,
                nombre='Super',
                apellido_paterno='Admin',
                apellido_materno='Axyoma',
                correo='superadmin@axyoma.com',
                nivel_usuario='superadmin'
            )
            self.stdout.write('✅ SuperAdmin creado')

    def crear_planes(self):
        """Crear planes de suscripción básicos"""
        self.stdout.write('💳 Creando planes de suscripción...')
        
        planes = [
            {
                'nombre': 'Básico',
                'descripcion': 'Plan básico para empresas pequeñas',
                'precio': 499.00,
                'duracion': 30,
                'limite_empleados': 50,
                'limite_plantas': 2,
                'caracteristicas': 'Gestión básica de empleados, reportes básicos'
            },
            {
                'nombre': 'Profesional',
                'descripcion': 'Plan profesional para empresas medianas',
                'precio': 999.00,
                'duracion': 30,
                'limite_empleados': 200,
                'limite_plantas': 5,
                'caracteristicas': 'Gestión avanzada, evaluaciones completas, reportes detallados'
            },
            {
                'nombre': 'Enterprise',
                'descripcion': 'Plan empresarial para grandes organizaciones',
                'precio': 1999.00,
                'duracion': 30,
                'limite_empleados': None,
                'limite_plantas': None,
                'caracteristicas': 'Sin límites, todas las funciones, soporte prioritario'
            }
        ]
        
        for plan_data in planes:
            plan, created = PlanSuscripcion.objects.get_or_create(
                nombre=plan_data['nombre'],
                defaults=plan_data
            )
            if created:
                self.stdout.write(f'✅ Plan "{plan.nombre}" creado')

    def crear_empresa_ejemplo(self):
        """Crear empresa de ejemplo con estructura completa"""
        self.stdout.write('🏢 Creando empresa de ejemplo...')
        
        # Crear usuario admin empresa
        if not User.objects.filter(username='admin_empresa').exists():
            admin_user = User.objects.create(
                username='admin_empresa',
                password=make_password('1234'),
                email='admin@empresa.com',
                first_name='Admin',
                last_name='Empresa',
                is_active=True
            )
            
            admin_perfil = PerfilUsuario.objects.create(
                user=admin_user,
                nombre='Admin',
                apellido_paterno='Empresa',
                apellido_materno='Demo',
                correo='admin@empresa.com',
                nivel_usuario='admin-empresa'
            )
            
            # Crear empresa
            empresa = Empresa.objects.create(
                administrador=admin_perfil,
                nombre='Empresa Demo S.A. de C.V.',
                rfc='EDE123456789',
                direccion='Av. Principal #123, Ciudad Demo',
                email_contacto='admin@empresa.com',
                telefono_contacto='+52 55 1234 5678',
                status=True
            )
            
            # Crear planta principal
            planta_principal = Planta.objects.create(
                nombre='Planta Principal',
                empresa=empresa,
                direccion='Av. Principal #123, Ciudad Demo',
                status=True
            )
            
            # Crear departamentos
            departamentos_data = [
                {'nombre': 'Administración', 'descripcion': 'Gestión administrativa general'},
                {'nombre': 'Recursos Humanos', 'descripcion': 'Gestión del personal y nómina'},
                {'nombre': 'Producción', 'descripcion': 'Operaciones de manufactura'},
                {'nombre': 'Calidad', 'descripcion': 'Control y aseguramiento de calidad'},
            ]
            
            departamentos = []
            for dept_data in departamentos_data:
                dept = Departamento.objects.create(
                    nombre=dept_data['nombre'],
                    descripcion=dept_data['descripcion'],
                    planta=planta_principal,
                    status=True
                )
                departamentos.append(dept)
            
            # Crear puestos
            puestos_data = [
                {'nombre': 'Gerente General', 'departamento': 'Administración'},
                {'nombre': 'Gerente de RRHH', 'departamento': 'Recursos Humanos'},
                {'nombre': 'Supervisor de Producción', 'departamento': 'Producción'},
                {'nombre': 'Inspector de Calidad', 'departamento': 'Calidad'},
            ]
            
            for puesto_data in puestos_data:
                dept = next((d for d in departamentos if d.nombre == puesto_data['departamento']), None)
                if dept:
                    Puesto.objects.create(
                        nombre=puesto_data['nombre'],
                        departamento=dept,
                        status=True
                    )
            
            # Crear suscripción automática
            plan_basico = PlanSuscripcion.objects.get(nombre='Básico')
            fecha_inicio = timezone.now().date()
            fecha_fin = fecha_inicio + timedelta(days=plan_basico.duracion)
            
            suscripcion = SuscripcionEmpresa.objects.create(
                empresa=empresa,
                plan_suscripcion=plan_basico,
                fecha_inicio=fecha_inicio,
                fecha_fin=fecha_fin,
                estado='Activa',
                status=True
            )
            
            # Crear pago completado
            Pago.objects.create(
                suscripcion=suscripcion,
                costo=plan_basico.precio,
                monto_pago=plan_basico.precio,
                estado_pago='Completado',
                fecha_pago=timezone.now(),
                transaccion_id=f"DEMO-{empresa.empresa_id}-{timezone.now().strftime('%Y%m%d%H%M%S')}",
                usuario=admin_user
            )
            
            self.stdout.write('✅ Empresa demo creada con estructura completa')
