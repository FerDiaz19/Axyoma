from django.core.management.base import BaseCommand
from apps.subscriptions.models import PlanSuscripcion
from decimal import Decimal

class Command(BaseCommand):
    help = 'Crear planes de suscripción de ejemplo'

    def handle(self, *args, **options):
        # Verificar si ya existen planes
        if PlanSuscripcion.objects.exists():
            self.stdout.write(
                self.style.WARNING('Ya existen planes en la base de datos. Saltando creación.')
            )
            return

        planes = [
            {
                'nombre_plan': 'Plan Básico',
                'descripcion': 'Perfecto para empresas pequeñas que están comenzando.',
                'precio_mensual': Decimal('299.00'),
                'limite_empleados': 50,
                'limite_plantas': 1,
                'caracteristicas': 'Gestión básica de empleados, 1 planta, reportes básicos, soporte por email',
                'status': True
            },
            {
                'nombre_plan': 'Plan Profesional', 
                'descripcion': 'Ideal para empresas medianas con múltiples ubicaciones.',
                'precio_mensual': Decimal('599.00'),
                'limite_empleados': 200,
                'limite_plantas': 3,
                'caracteristicas': 'Gestión completa, hasta 3 plantas, reportes avanzados, evaluaciones, soporte prioritario',
                'status': True
            },
            {
                'nombre_plan': 'Plan Enterprise',
                'descripcion': 'Solución completa para grandes empresas.',
                'precio_mensual': Decimal('1299.00'),
                'limite_empleados': None,  # Sin límite
                'limite_plantas': None,    # Sin límite
                'caracteristicas': 'Sin límites, todas las funcionalidades, API completa, soporte 24/7, personalización',
                'status': True
            },
            {
                'nombre_plan': 'Plan Prueba',
                'descripcion': 'Plan de prueba gratuito por 30 días.',
                'precio_mensual': Decimal('0.00'),
                'limite_empleados': 10,
                'limite_plantas': 1,
                'caracteristicas': 'Acceso limitado por 30 días, todas las funcionalidades básicas',
                'status': True
            }
        ]

        for plan_data in planes:
            plan = PlanSuscripcion.objects.create(**plan_data)
            self.stdout.write(
                self.style.SUCCESS(f'✅ Plan creado: {plan.nombre_plan} - ${plan.precio_mensual}/mes')
            )

        self.stdout.write(
            self.style.SUCCESS('🎉 Todos los planes de suscripción han sido creados exitosamente!')
        )
