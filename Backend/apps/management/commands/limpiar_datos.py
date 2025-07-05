from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from apps.users.models import PerfilUsuario, Empresa, Planta, AdminPlanta, Departamento, Puesto, Empleado

class Command(BaseCommand):
    help = 'Limpia todos los datos de la base de datos'

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING('🗑️  LIMPIANDO TODOS LOS DATOS...'))
        
        # Limpiar en orden correcto (respetando foreign keys)
        Empleado.objects.all().delete()
        self.stdout.write('  - Empleados eliminados')
        
        Puesto.objects.all().delete()
        self.stdout.write('  - Puestos eliminados')
        
        Departamento.objects.all().delete()
        self.stdout.write('  - Departamentos eliminados')
        
        AdminPlanta.objects.all().delete()
        self.stdout.write('  - Admin-Plantas eliminados')
        
        Planta.objects.all().delete()
        self.stdout.write('  - Plantas eliminadas')
        
        Empresa.objects.all().delete()
        self.stdout.write('  - Empresas eliminadas')
        
        PerfilUsuario.objects.all().delete()
        self.stdout.write('  - Perfiles de usuario eliminados')
        
        User.objects.filter(is_superuser=False).delete()
        self.stdout.write('  - Usuarios Django eliminados (excepto superusers)')
        
        self.stdout.write(self.style.SUCCESS('✅ BASE DE DATOS LIMPIA'))
