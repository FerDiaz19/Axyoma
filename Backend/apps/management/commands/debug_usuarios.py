from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from apps.users.models import PerfilUsuario, Empresa, AdminPlanta

class Command(BaseCommand):
    help = 'Verifica usuarios para login'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('🔍 Verificando usuarios de login...'))
        
        users = User.objects.all()
        
        if not users:
            self.stdout.write(self.style.ERROR('❌ No hay usuarios en la base de datos'))
            return
            
        for user in users:
            self.stdout.write(f'\n👤 Usuario: {user.username}')
            self.stdout.write(f'   📧 Email: {user.email}')
            self.stdout.write(f'   🔑 Activo: {user.is_active}')
            self.stdout.write(f'   🆔 ID: {user.id}')
            
            # Verificar perfil
            if hasattr(user, 'perfil'):
                perfil = user.perfil
                self.stdout.write(f'   📋 Perfil: {perfil.nivel_usuario}')
                self.stdout.write(f'   🏷️ Nombre: {perfil.nombre} {perfil.apellido_paterno}')
                
                # Verificar empresa o planta
                if perfil.nivel_usuario == 'admin-empresa':
                    try:
                        empresa = Empresa.objects.get(administrador=perfil)
                        self.stdout.write(f'   🏢 Empresa: {empresa.nombre}')
                    except Empresa.DoesNotExist:
                        self.stdout.write(f'   ❌ Sin empresa asignada')
                        
                elif perfil.nivel_usuario == 'admin-planta':
                    try:
                        admin_planta = AdminPlanta.objects.get(usuario=perfil)
                        self.stdout.write(f'   🏭 Planta: {admin_planta.planta.nombre}')
                    except AdminPlanta.DoesNotExist:
                        self.stdout.write(f'   ❌ Sin planta asignada')
            else:
                self.stdout.write(f'   ❌ Sin perfil asociado')
        
        self.stdout.write(f'\n📊 Total usuarios: {users.count()}')
        
        # Probar autenticación
        self.stdout.write(f'\n🧪 Probando autenticación...')
        from django.contrib.auth import authenticate
        
        test_credentials = [
            ('ed-rubio@axyoma.com', '1234'),
            ('juan.perez@codewave.com', '1234'),
            ('maria.gomez@codewave.com', '1234')
        ]
        
        for username, password in test_credentials:
            user = authenticate(username=username, password=password)
            if user:
                self.stdout.write(f'   ✅ {username} - Autenticación exitosa')
            else:
                self.stdout.write(f'   ❌ {username} - Fallo en autenticación')
