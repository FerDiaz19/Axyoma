from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from apps.users.models import PerfilUsuario, Empresa

class Command(BaseCommand):
    help = 'Associate demo user with empresa'

    def handle(self, *args, **options):
        try:
            # Get user
            user = User.objects.get(username='demo_admin')
            profile = PerfilUsuario.objects.get(user=user)
            self.stdout.write(f"✅ Found user: {user.username}")
            
            # Get first empresa
            empresa = Empresa.objects.first()
            if not empresa:
                self.stdout.write("❌ No empresas found")
                return
                
            self.stdout.write(f"   Empresa: {empresa.nombre}")
            self.stdout.write(f"   Current admin: {empresa.administrador}")
            
            # Set user as empresa administrator
            empresa.administrador = profile
            empresa.save()
            
            self.stdout.write(self.style.SUCCESS("✅ User set as empresa administrator successfully!"))
            self.stdout.write(f"   {user.username} -> {empresa.nombre} (ADMINISTRATOR)")
            
        except User.DoesNotExist:
            self.stdout.write("❌ User demo_admin not found")
        except PerfilUsuario.DoesNotExist:
            self.stdout.write("❌ Profile for demo_admin not found")
        except Exception as e:
            self.stdout.write(f"❌ Error: {e}")
