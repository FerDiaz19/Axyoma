import os, sys, django
sys.path.insert(0, 'Backend')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.users.models import PerfilUsuario
from apps.evaluaciones.models import Evaluacion

print('=== Usuarios disponibles ===')
for user in PerfilUsuario.objects.all()[:5]:
    print(f'ID: {user.user_id}, Fields: {[field.name for field in user._meta.fields]}')

print()
print('=== Evaluaciones con problemas ===')
for eval in Evaluacion.objects.all()[:3]:
    print(f'ID: {eval.evaluacion_id}, Creado por: {eval.creado_por}, Tipo: {type(eval.creado_por).__name__}')
