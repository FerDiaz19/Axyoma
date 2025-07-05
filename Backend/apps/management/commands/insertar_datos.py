from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.db import connection
from rest_framework.authtoken.models import Token
from apps.users.models import PerfilUsuario, Empresa, Planta, AdminPlanta, Departamento, Puesto, Empleado

class Command(BaseCommand):
    help = 'Inserta datos de prueba en la base de datos'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('🚀 Iniciando inserción de datos de prueba...'))
        
        try:
            # Verificar si ya existen usuarios para evitar duplicados
            if PerfilUsuario.objects.filter(correo='ed-rubio@axyoma.com').exists():
                self.stdout.write(self.style.WARNING('Los datos ya existen. Use "python manage.py limpiar_datos" primero.'))
                return
            
            # Asegurar que la tabla admin_plantas existe
            self._create_admin_plantas_table()
            
            # Crear usuarios Django con contraseñas hasheadas
            self.stdout.write('👤 Creando usuarios Django...')
            user1 = User.objects.create_user(
                username='ed-rubio@axyoma.com', 
                email='ed-rubio@axyoma.com', 
                password='1234', 
                first_name='Ed', 
                last_name='Rubio',
                is_active=True
            )
            user2 = User.objects.create_user(
                username='juan.perez@codewave.com', 
                email='juan.perez@codewave.com', 
                password='1234', 
                first_name='Juan', 
                last_name='Perez',
                is_active=True
            )
            user3 = User.objects.create_user(
                username='maria.gomez@codewave.com', 
                email='maria.gomez@codewave.com', 
                password='1234', 
                first_name='Maria', 
                last_name='Gomez',
                is_active=True
            )
            user4 = User.objects.create_user(
                username='carlos.ruiz@codewave.com', 
                email='carlos.ruiz@codewave.com', 
                password='1234', 
                first_name='Carlos', 
                last_name='Ruiz',
                is_active=True
            )
            self.stdout.write(f'  ✅ Creados 4 usuarios Django')
            
            # Crear tokens para los usuarios
            self.stdout.write('🔑 Creando tokens de autenticación...')
            token1, _ = Token.objects.get_or_create(user=user1)
            token2, _ = Token.objects.get_or_create(user=user2)
            token3, _ = Token.objects.get_or_create(user=user3)
            token4, _ = Token.objects.get_or_create(user=user4)
            self.stdout.write(f'  ✅ Tokens creados para todos los usuarios')

            # Crear perfiles de usuario según tabla USUARIOS
            self.stdout.write('📋 Creando perfiles de usuario...')
            perfil1 = PerfilUsuario.objects.create(
                user=user1,
                nombre='Ed',
                apellido_paterno='Rubio',
                correo='ed-rubio@axyoma.com',
                nivel_usuario='superadmin',
                admin_empresa=None
            )
            perfil2 = PerfilUsuario.objects.create(
                user=user2,
                nombre='Juan',
                apellido_paterno='Perez',
                correo='juan.perez@codewave.com',
                nivel_usuario='admin-empresa',
                admin_empresa=None
            )
            self.stdout.write(f'  ✅ Creados perfiles base')
            
            # Crear empresa ANTES de los admin-planta
            self.stdout.write('🏢 Creando empresa...')
            empresa1 = Empresa.objects.create(
                nombre='CodeWave Solutions',
                rfc='CWS920314ABC',
                direccion='Av. Tecnología 123, Col. Centro, CDMX',
                logotipo='https://via.placeholder.com/150x75/0066cc/ffffff?text=CodeWave',
                email_contacto='contacto@codewave.com',
                telefono_contacto='5551234567',
                administrador=perfil2
            )
            self.stdout.write(f'  ✅ Empresa creada: {empresa1.nombre}')
            self.stdout.write(f'  📋 Admin empresa: {perfil2.nombre} (ID: {perfil2.id})')
            
            # Verificar que la empresa fue asignada correctamente
            empresa_verificada = Empresa.objects.get(administrador=perfil2)
            self.stdout.write(f'  ✅ Verificación: {empresa_verificada.nombre} -> {empresa_verificada.administrador.correo}')
            
            # Ahora crear los admin-planta
            perfil3 = PerfilUsuario.objects.create(
                user=user3,
                nombre='Maria',
                apellido_paterno='Gomez',
                correo='maria.gomez@codewave.com',
                nivel_usuario='admin-planta',
                admin_empresa=perfil2  # Referencia al admin de empresa
            )
            perfil4 = PerfilUsuario.objects.create(
                user=user4,
                nombre='Carlos',
                apellido_paterno='Ruiz',
                correo='carlos.ruiz@codewave.com',
                nivel_usuario='admin-planta',
                admin_empresa=perfil2  # Referencia al admin de empresa
            )
            self.stdout.write(f'  ✅ Creados admin-planta')
            self.stdout.write(f'  ✅ Creados admin-planta')

            # Crear plantas según tabla PLANTAS
            self.stdout.write('🏭 Creando plantas...')
            planta1 = Planta.objects.create(
                nombre='Oficina Central Tijuana', 
                direccion='Av. Principal 456, Tijuana, BC', 
                empresa=empresa1
            )
            planta2 = Planta.objects.create(
                nombre='Oficina Monterrey', 
                direccion='Blvd. Constitución 789, Monterrey, NL', 
                empresa=empresa1
            )
            self.stdout.write(f'  ✅ Creadas 2 plantas')

            # Crear relaciones ADMIN_PLANTAS
            self.stdout.write('🔗 Creando relaciones admin-plantas...')
            AdminPlanta.objects.create(
                usuario=perfil3,  # Maria Gomez
                planta=planta1    # Oficina Central Tijuana
            )
            self.stdout.write(f'  ✅ Maria asignada a Tijuana')

            # Crear departamentos
            self.stdout.write('Creando departamentos...')
            dept1 = Departamento.objects.create(
                nombre='Recursos Humanos', 
                descripcion='Gestión de personal', 
                planta=planta1
            )
            dept2 = Departamento.objects.create(
                nombre='Desarrollo de Software', 
                descripcion='Creación de aplicaciones', 
                planta=planta1
            )
            dept3 = Departamento.objects.create(
                nombre='Operaciones', 
                descripcion='Gestión de operaciones', 
                planta=planta1
            )
            dept4 = Departamento.objects.create(
                nombre='Calidad', 
                descripcion='Control de calidad', 
                planta=planta2
            )
            dept5 = Departamento.objects.create(
                nombre='Mantenimiento', 
                descripcion='Mantenimiento de equipos', 
                planta=planta2
            )

            # Crear puestos
            self.stdout.write('Creando puestos...')
            puesto1 = Puesto.objects.create(
                nombre='Gerente de RRHH', 
                descripcion='Líder del equipo de RRHH', 
                departamento=dept1
            )
            puesto2 = Puesto.objects.create(
                nombre='Desarrollador Senior', 
                descripcion='Programador experimentado', 
                departamento=dept2
            )
            puesto3 = Puesto.objects.create(
                nombre='Desarrollador Junior', 
                descripcion='Programador en formación', 
                departamento=dept2
            )
            puesto4 = Puesto.objects.create(
                nombre='Supervisor de Operaciones', 
                descripcion='Supervisión de procesos', 
                departamento=dept3
            )
            puesto5 = Puesto.objects.create(
                nombre='Especialista en Calidad', 
                descripcion='Control de calidad', 
                departamento=dept4
            )
            puesto6 = Puesto.objects.create(
                nombre='Técnico de Mantenimiento', 
                descripcion='Mantenimiento preventivo', 
                departamento=dept5
            )

            # Crear empleados
            self.stdout.write('Creando empleados...')
            Empleado.objects.create(
                nombre='Laura', 
                apellido_paterno='Fernández', 
                apellido_materno='Torres', 
                genero='Femenino', 
                antiguedad=5, 
                puesto=puesto1, 
                departamento=dept1, 
                planta=planta1
            )
            Empleado.objects.create(
                nombre='José', 
                apellido_paterno='Martínez', 
                apellido_materno='López', 
                genero='Masculino', 
                antiguedad=2, 
                puesto=puesto2, 
                departamento=dept2, 
                planta=planta1
            )
            Empleado.objects.create(
                nombre='Ana', 
                apellido_paterno='García', 
                apellido_materno='Ruiz', 
                genero='Femenino', 
                antiguedad=3, 
                puesto=puesto3, 
                departamento=dept2, 
                planta=planta1
            )
            Empleado.objects.create(
                nombre='Carlos', 
                apellido_paterno='López', 
                apellido_materno='Hernández', 
                genero='Masculino', 
                antiguedad=4, 
                puesto=puesto4, 
                departamento=dept3, 
                planta=planta1
            )
            Empleado.objects.create(
                nombre='María', 
                apellido_paterno='Rodríguez', 
                apellido_materno='Sánchez', 
                genero='Femenino', 
                antiguedad=1, 
                puesto=puesto5, 
                departamento=dept4, 
                planta=planta2
            )
            Empleado.objects.create(
                nombre='Pedro', 
                apellido_paterno='González', 
                apellido_materno='Morales', 
                genero='Masculino', 
                antiguedad=6, 
                puesto=puesto6, 
                departamento=dept5, 
                planta=planta2
            )

            self.stdout.write(self.style.SUCCESS('✓ Datos insertados correctamente!'))
            self.stdout.write(self.style.SUCCESS('\nUsuarios creados:'))
            self.stdout.write('- ed-rubio@axyoma.com / 1234 (SuperAdmin)')
            self.stdout.write('- juan.perez@codewave.com / 1234 (Admin Empresa)')
            self.stdout.write('- maria.gomez@codewave.com / 1234 (Admin Planta)')
            self.stdout.write('- carlos.ruiz@codewave.com / 1234 (Admin Planta)')

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error al insertar datos: {str(e)}'))
            raise e

    def _create_admin_plantas_table(self):
        """Crear la tabla admin_plantas si no existe"""
        with connection.cursor() as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS admin_plantas (
                    id SERIAL PRIMARY KEY,
                    usuario_id INTEGER NOT NULL REFERENCES usuarios(id) ON DELETE CASCADE,
                    planta_id INTEGER NOT NULL REFERENCES plantas(planta_id) ON DELETE CASCADE,
                    fecha_asignacion TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
                    status BOOLEAN DEFAULT TRUE,
                    UNIQUE(usuario_id, planta_id)
                );
            """)
