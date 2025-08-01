import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')

import django
django.setup()

from django.contrib.auth.models import User
from apps.users.models import Empresa
from apps.subscriptions.models import PlanSuscripcion, SuscripcionEmpresa
from datetime import date, timedelta

print("💳 ASIGNANDO SUSCRIPCIONES A EMPRESAS")

# Obtener empresas y planes
empresas = Empresa.objects.all()
plan_profesional = PlanSuscripcion.objects.get(nombre='Plan Profesional')
plan_empresarial = PlanSuscripcion.objects.get(nombre='Plan Empresarial')

for i, empresa in enumerate(empresas):
    # Verificar si ya tiene suscripción
    if not SuscripcionEmpresa.objects.filter(empresa=empresa, estado='activa').exists():
        print(f"📋 Creando suscripción para {empresa.nombre}...")
        
        # Alternar entre planes para demostración
        plan = plan_profesional if i % 2 == 0 else plan_empresarial
        
        # Crear suscripción activa
        suscripcion = SuscripcionEmpresa.objects.create(
            empresa=empresa,
            plan=plan,
            fecha_inicio=date.today(),
            fecha_fin=date.today() + timedelta(days=plan.duracion),
            estado='activa'
        )
        
        print(f"  ✅ {empresa.nombre} → {plan.nombre} (${plan.precio})")
        print(f"  📅 Vigente hasta: {suscripcion.fecha_fin}")
    else:
        print(f"✅ {empresa.nombre} ya tiene suscripción activa")

print("\n🎉 ¡SUSCRIPCIONES CONFIGURADAS!")
print("=" * 50)

# Mostrar resumen
for empresa in empresas:
    suscripcion = SuscripcionEmpresa.objects.filter(empresa=empresa, estado='activa').first()
    if suscripcion:
        print(f"✅ {empresa.nombre}")
        print(f"   Plan: {suscripcion.plan.nombre}")
        print(f"   Precio: ${suscripcion.plan.precio}")
        print(f"   Vigencia: {suscripcion.fecha_inicio} → {suscripcion.fecha_fin}")
        print(f"   Plantas incluidas: {empresa.plantas.count()}")
        print()

print("🔧 LÓGICA DEL SISTEMA:")
print("✅ Empresa con suscripción activa → Todas sus plantas tienen acceso")
print("❌ Empresa sin suscripción → Solo avisos y opción de pago")
print("=" * 50)
