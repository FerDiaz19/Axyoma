from apps.subscriptions.models import PlanSuscripcion

# Crear los 3 planes base
planes_base = [
    {
        'nombre': 'Plan Mensual',
        'descripcion': 'Plan básico de 1 mes',
        'duracion': 30,
        'precio': 299.00,
        'status': True
    },
    {
        'nombre': 'Plan Trimestral',
        'descripcion': 'Plan de 3 meses con descuento',
        'duracion': 90,
        'precio': 799.00,
        'status': True
    },
    {
        'nombre': 'Plan Anual',
        'descripcion': 'Plan de 1 año con mayor descuento',
        'duracion': 365,
        'precio': 2999.00,
        'status': True
    }
]

for plan_data in planes_base:
    plan, created = PlanSuscripcion.objects.get_or_create(
        nombre=plan_data['nombre'],
        defaults=plan_data
    )
    if created:
        print(f"✅ Plan creado: {plan.nombre}")
    else:
        print(f"ℹ️ Plan ya existe: {plan.nombre}")

print(f"\n📊 Total de planes activos: {PlanSuscripcion.objects.filter(status=True).count()}")
