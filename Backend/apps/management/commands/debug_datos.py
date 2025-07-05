from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from apps.users.models import PerfilUsuario, Empresa

class Command(BaseCommand):
    help = 'Debug de inserción de datos'

    def handle(self, *args, **options):
        self.stdout.write('=== DEBUG INSERCIÓN ===')
        
        try:
            # Crear un usuario simple
            self.stdout.write('Creando usuario...')
            user = User.objects.create_user(
                username='test@test.com',
                email='test@test.com',
                password='1234'
            )
            self.stdout.write(f'Usuario creado: {user.username}')
            
            # Crear perfil
            self.stdout.write('Creando perfil...')
            perfil = PerfilUsuario.objects.create(
                user=user,
                nombre='Test',
                apellido_paterno='User',
                correo='test@test.com',
                nivel_usuario='superadmin'
            )
            self.stdout.write(f'Perfil creado: {perfil.nombre}')
            
            self.stdout.write('✅ Debug completado')
            
        except Exception as e:
            self.stdout.write(f'❌ Error: {str(e)}')
            import traceback
            self.stdout.write(traceback.format_exc())
