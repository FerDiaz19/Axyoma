import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')

import django
django.setup()

from apps.subscriptions.models import SuscripcionEmpresa

print("🔍 PROBANDO ENDPOINT DE SUSCRIPCIONES")

try:
    suscripciones = SuscripcionEmpresa.objects.select_related('empresa', 'plan').all()
    print(f"✅ Suscripciones encontradas: {suscripciones.count()}")
    
    for suscripcion in suscripciones:
        print(f"  - {suscripcion.empresa.nombre} → {suscripcion.plan.nombre}")
        print(f"    Días restantes: {suscripcion.dias_restantes}")
        print(f"    Estado: {suscripcion.estado}")
        print()

except Exception as e:
    print(f"❌ Error: {str(e)}")
    import traceback
    traceback.print_exc()
