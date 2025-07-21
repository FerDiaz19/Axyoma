from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from apps.users.models import PerfilUsuario, Empresa, Planta, Departamento, Puesto, Empleado

class Command(BaseCommand):
    help = 'Create test employees for demo empresa'

    def handle(self, *args, **options):
        try:
            # Get demo user's empresa
            user = User.objects.get(username='demo_admin')
            profile = user.perfil
            empresa = Empresa.objects.get(administrador=profile)
            
            self.stdout.write(f"✅ Working with empresa: {empresa.nombre}")
            
            # Create or get planta
            planta, created = Planta.objects.get_or_create(
                empresa=empresa,
                nombre='Planta Principal',
                defaults={
                    'direccion': 'Av. Principal 123',
                    'telefono': '555-0001',
                    'status': True
                }
            )
            if created:
                self.stdout.write(f"✅ Created planta: {planta.nombre}")
            else:
                self.stdout.write(f"✅ Using existing planta: {planta.nombre}")
            
            # Create departments
            departments = [
                {'nombre': 'Recursos Humanos', 'descripcion': 'Gestión de personal'},
                {'nombre': 'Tecnología', 'descripcion': 'Desarrollo y sistemas'},
                {'nombre': 'Ventas', 'descripcion': 'Área comercial'},
                {'nombre': 'Administración', 'descripcion': 'Gestión administrativa'}
            ]
            
            created_departments = []
            for dept_data in departments:
                dept, created = Departamento.objects.get_or_create(
                    planta=planta,
                    nombre=dept_data['nombre'],
                    defaults={'descripcion': dept_data['descripcion']}
                )
                created_departments.append(dept)
                if created:
                    self.stdout.write(f"✅ Created department: {dept.nombre}")
            
            # Create positions
            positions_data = [
                {'nombre': 'Gerente', 'departamento': 'Recursos Humanos'},
                {'nombre': 'Analista', 'departamento': 'Recursos Humanos'},
                {'nombre': 'Desarrollador', 'departamento': 'Tecnología'},
                {'nombre': 'Analista de Sistemas', 'departamento': 'Tecnología'},
                {'nombre': 'Vendedor', 'departamento': 'Ventas'},
                {'nombre': 'Supervisor de Ventas', 'departamento': 'Ventas'},
                {'nombre': 'Contador', 'departamento': 'Administración'},
                {'nombre': 'Asistente', 'departamento': 'Administración'}
            ]
            
            created_positions = []
            for pos_data in positions_data:
                dept = next(d for d in created_departments if d.nombre == pos_data['departamento'])
                pos, created = Puesto.objects.get_or_create(
                    departamento=dept,
                    nombre=pos_data['nombre'],
                    defaults={'descripcion': f'Puesto de {pos_data["nombre"]}'}
                )
                created_positions.append(pos)
                if created:
                    self.stdout.write(f"✅ Created position: {pos.nombre} in {dept.nombre}")
            
            # Create employees
            employees_data = [
                {'nombre': 'Ana', 'apellido': 'García', 'puesto': 'Gerente', 'genero': 'Femenino'},
                {'nombre': 'Carlos', 'apellido': 'López', 'puesto': 'Desarrollador', 'genero': 'Masculino'},
                {'nombre': 'María', 'apellido': 'Rodríguez', 'puesto': 'Vendedor', 'genero': 'Femenino'},
                {'nombre': 'José', 'apellido': 'Martínez', 'puesto': 'Contador', 'genero': 'Masculino'},
                {'nombre': 'Laura', 'apellido': 'Sánchez', 'puesto': 'Analista', 'genero': 'Femenino'},
                {'nombre': 'Pedro', 'apellido': 'Ramírez', 'puesto': 'Desarrollador', 'genero': 'Masculino'},
                {'nombre': 'Sofía', 'apellido': 'Torres', 'puesto': 'Asistente', 'genero': 'Femenino'},
                {'nombre': 'Diego', 'apellido': 'Flores', 'puesto': 'Vendedor', 'genero': 'Masculino'}
            ]
            
            created_count = 0
            for emp_data in employees_data:
                puesto = next(p for p in created_positions if p.nombre == emp_data['puesto'])
                
                if not Empleado.objects.filter(
                    nombre=emp_data['nombre'], 
                    apellido_paterno=emp_data['apellido'],
                    puesto=puesto
                ).exists():
                    empleado = Empleado.objects.create(
                        nombre=emp_data['nombre'],
                        apellido_paterno=emp_data['apellido'],
                        genero=emp_data['genero'],
                        puesto=puesto,
                        departamento=puesto.departamento,
                        planta=planta,
                        antiguedad=1,
                        status=True
                    )
                    created_count += 1
                    self.stdout.write(f"✅ Created employee: {empleado.nombre} {empleado.apellido_paterno} - {puesto.nombre}")
            
            self.stdout.write(self.style.SUCCESS(f"\n🎉 Demo data created successfully!"))
            self.stdout.write(f"   Empresa: {empresa.nombre}")
            self.stdout.write(f"   Planta: {planta.nombre}")
            self.stdout.write(f"   Departments: {len(created_departments)}")
            self.stdout.write(f"   Positions: {len(created_positions)}")
            self.stdout.write(f"   New Employees: {created_count}")
            self.stdout.write(f"   Total Employees: {Empleado.objects.filter(planta=planta).count()}")
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"❌ Error: {e}"))
