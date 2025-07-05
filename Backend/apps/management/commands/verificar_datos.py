from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from apps.users.models import PerfilUsuario, Empresa, Planta, AdminPlanta, Departamento, Puesto, Empleado

class Command(BaseCommand):
    help = 'Verifica qué datos existen en la base de datos'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('=== VERIFICANDO DATOS EN LA BASE DE DATOS ==='))
        
        # Verificar usuarios Django
        users = User.objects.all()
        self.stdout.write(f"\n📋 USUARIOS DJANGO (auth_user): {users.count()}")
        for user in users:
            self.stdout.write(f"  - ID: {user.id}, Username: {user.username}, Email: {user.email}")
        
        # Verificar perfiles
        perfiles = PerfilUsuario.objects.all()
        self.stdout.write(f"\n👤 PERFILES DE USUARIO (usuarios): {perfiles.count()}")
        for perfil in perfiles:
            user_info = f"User ID: {perfil.user.id}" if perfil.user else "Sin usuario Django"
            self.stdout.write(f"  - ID: {perfil.id}, {perfil.nombre} {perfil.apellido_paterno}, Nivel: {perfil.nivel_usuario}, {user_info}")
        
        # Verificar empresas
        empresas = Empresa.objects.all()
        self.stdout.write(f"\n🏢 EMPRESAS: {empresas.count()}")
        for empresa in empresas:
            self.stdout.write(f"  - ID: {empresa.empresa_id}, {empresa.nombre}, Admin: {empresa.administrador.nombre}")
        
        # Verificar plantas
        plantas = Planta.objects.all()
        self.stdout.write(f"\n🏭 PLANTAS: {plantas.count()}")
        for planta in plantas:
            self.stdout.write(f"  - ID: {planta.planta_id}, {planta.nombre}, Empresa: {planta.empresa.nombre}")
        
        # Verificar empleados
        empleados = Empleado.objects.all()
        self.stdout.write(f"\n👥 EMPLEADOS: {empleados.count()}")
        for empleado in empleados:
            self.stdout.write(f"  - ID: {empleado.empleado_id}, {empleado.nombre} {empleado.apellido_paterno}")
        
        self.stdout.write(self.style.SUCCESS('\n=== VERIFICACIÓN COMPLETADA ==='))
        
        # Verificar login de prueba
        self.stdout.write(self.style.WARNING('\n🔐 PROBANDO AUTENTICACIÓN:'))
        
        test_users = [
            ('ed-rubio@axyoma.com', '1234'),
            ('juan.perez@codewave.com', '1234'),
            ('maria.gomez@codewave.com', '1234')
        ]
        
        for username, password in test_users:
            try:
                user = authenticate(username=username, password=password)
                if user:
                    has_perfil = hasattr(user, 'perfil')
                    if has_perfil:
                        perfil_info = f"Perfil: {user.perfil.nivel_usuario}"
                        self.stdout.write(f"  ✅ {username} - {perfil_info}")
                    else:
                        self.stdout.write(f"  ❌ {username} - Sin perfil")
                else:
                    self.stdout.write(f"  ❌ {username} - FALLO DE AUTENTICACIÓN")
            except Exception as e:
                self.stdout.write(f"  ❌ {username} - Error: {str(e)}")

        self.stdout.write(self.style.SUCCESS('\n✅ Verificación de autenticación completada'))
