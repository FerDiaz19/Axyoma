import os
import sys
import django

# Configurar Django
sys.path.append('c:\\xampp2\\htdocs\\UTT4B\\Axyoma2\\Backend')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')
django.setup()

from django.contrib.auth.models import User
from apps.users.models import PerfilUsuario

print("=== VERIFICANDO DATOS ===")

# Verificar usuarios
users = User.objects.all()
print(f"Usuarios Django: {users.count()}")
for user in users:
    print(f"  - {user.username} ({user.email})")

# Verificar perfiles
perfiles = PerfilUsuario.objects.all()
print(f"Perfiles: {perfiles.count()}")
for perfil in perfiles:
    print(f"  - {perfil.nombre} {perfil.apellido_paterno} - {perfil.nivel_usuario}")

# Probar autenticación
from django.contrib.auth import authenticate

print("\n=== PROBANDO AUTENTICACIÓN ===")
test_users = [
    ('ed-rubio@axyoma.com', '1234'),
    ('juan.perez@codewave.com', '1234'),
    ('maria.gomez@codewave.com', '1234')
]

for username, password in test_users:
    user = authenticate(username=username, password=password)
    if user:
        has_perfil = hasattr(user, 'perfil')
        if has_perfil:
            print(f"  ✅ {username} - Perfil: {user.perfil.nivel_usuario}")
        else:
            print(f"  ❌ {username} - Usuario autenticado pero sin perfil")
    else:
        print(f"  ❌ {username} - FALLO DE AUTENTICACIÓN")

print("\n=== VERIFICACIÓN COMPLETADA ===")
