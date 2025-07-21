from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from apps.users.models import PerfilUsuario, Empresa

class Command(BaseCommand):
    help = 'Check user profile structure'

    def handle(self, *args, **options):
        try:
            user = User.objects.get(username='demo_admin')
            profile = user.perfil
            
            self.stdout.write(f"✅ User: {user.username}")
            self.stdout.write(f"   Profile ID: {profile.id}")
            self.stdout.write(f"   Profile level: {profile.nivel_usuario}")
            self.stdout.write(f"   Has empresa field: {hasattr(profile, 'empresa')}")
            
            # Check if profile has empresa attribute
            if hasattr(profile, 'empresa'):
                self.stdout.write(f"   Profile.empresa: {profile.empresa}")
            
            # Check empresa administered
            try:
                empresa = Empresa.objects.get(administrador=profile)
                self.stdout.write(f"   Administers empresa: {empresa.nombre}")
            except Empresa.DoesNotExist:
                self.stdout.write("   ❌ Does not administer any empresa")
                
            # Check model fields
            self.stdout.write(f"\n📋 PerfilUsuario model fields:")
            for field in PerfilUsuario._meta.fields:
                self.stdout.write(f"   - {field.name}: {field.__class__.__name__}")
                
        except Exception as e:
            self.stdout.write(f"❌ Error: {e}")
