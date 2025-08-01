import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')

import django
django.setup()

from apps.subscriptions.models import PlanSuscripcion

print("📋 ESTADO DE PLANES EN BD:")
for plan in PlanSuscripcion.objects.all():
    print(f"  {plan.nombre}: status = {plan.status} ({'Activo' if plan.status else 'Inactivo'})")
