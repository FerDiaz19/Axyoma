import os
import django
import sys

# Configurar Django
sys.path.append('C:\\Users\\Ernesto\\Documents\\GitHub\\Axyoma2\\Backend')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'axyoma.settings')
django.setup()

from sistema_evaluacion.models import Planta
from django.contrib.auth.models import User

print("DEBUGGEANDO ENDPOINT DE PLANTAS")
print("=" * 40)

try:
    # Verificar plantas en la BD
    plantas = Planta.objects.all()
    print(f"Total plantas en BD: {plantas.count()}")
    
    if plantas.exists():
        primera_planta = plantas.first()
        print(f"Primera planta: {primera_planta}")
        print(f"Atributos de planta:")
        for field in primera_planta._meta.fields:
            valor = getattr(primera_planta, field.name, 'N/A')
            print(f"  - {field.name}: {valor}")
    
    # Probar el método específico que está fallando
    from sistema_evaluacion.views import listar_todas_plantas
    print(f"\nImportación de vista exitosa: {listar_todas_plantas}")
    
    # Verificar superadmin
    superadmin = User.objects.get(username='superadmin')
    print(f"SuperAdmin encontrado: {superadmin}")
    
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 40)
