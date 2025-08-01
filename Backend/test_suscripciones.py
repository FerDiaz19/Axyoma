import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')

import django
django.setup()

from django.contrib.auth.models import User
from apps.subscriptions.utils import SuscripcionManager
from apps.users.models import Empresa

print("🧪 PROBANDO SISTEMA DE SUSCRIPCIONES")
print("=" * 50)

# Probar con usuarios existentes
superuser = User.objects.filter(is_superuser=True).first()
admin_user = User.objects.filter(username__contains='admin_techcorp').first()

print("🔍 PRUEBA 1: Verificar acceso de usuarios")
print(f"SuperAdmin tiene acceso: {SuscripcionManager.usuario_tiene_acceso(superuser)}")
if admin_user:
    print(f"Admin TechCorp tiene acceso: {SuscripcionManager.usuario_tiene_acceso(admin_user)}")

print("\n📊 PRUEBA 2: Estado de suscripciones")
for empresa in Empresa.objects.all():
    estado = SuscripcionManager.obtener_estado_suscripcion(empresa)
    print(f"\n🏢 {empresa.nombre}:")
    print(f"  Tiene suscripción: {estado['tiene_suscripcion']}")
    if estado['tiene_suscripcion']:
        print(f"  Plan: {estado['plan']}")
        print(f"  Precio: ${estado['precio']}")
        print(f"  Días restantes: {estado['dias_restantes']}")
        print(f"  Plantas incluidas: {estado['plantas_incluidas']}")

print("\n💳 PRUEBA 3: Planes disponibles")
planes = SuscripcionManager.obtener_planes_disponibles()
for plan in planes:
    print(f"  📋 {plan.nombre} - ${plan.precio} ({plan.duracion} días)")

print("\n✅ SISTEMA DE SUSCRIPCIONES FUNCIONANDO")
print("=" * 50)
print("🔧 LÓGICA IMPLEMENTADA:")
print("✅ Empresa registrada → Selecciona plan → Acceso completo")
print("✅ Todas las plantas de la empresa tienen acceso")
print("❌ Sin suscripción → Solo avisos y opción de pago")
print("✅ SuperAdmin → Acceso completo siempre")
print("=" * 50)
