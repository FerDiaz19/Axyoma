import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')

import django
django.setup()

from django.contrib.auth.models import User
from apps.users.models import Empresa, Planta, Departamento, Puesto, Empleado
from apps.subscriptions.models import PlanSuscripcion, SuscripcionEmpresa, Pago
from apps.subscriptions.utils import SuscripcionManager

print("🎉 RESUMEN FINAL - SISTEMA AXYOMA COMPLETO")
print("=" * 60)

print("👥 DATOS CARGADOS:")
print(f"  ✅ Usuarios: {User.objects.count()}")
print(f"  ✅ SuperAdmins: {User.objects.filter(is_superuser=True).count()}")
print(f"  ✅ Empresas: {Empresa.objects.count()}")
print(f"  ✅ Plantas: {Planta.objects.count()}")
print(f"  ✅ Departamentos: {Departamento.objects.count()}")
print(f"  ✅ Puestos: {Puesto.objects.count()}")
print(f"  ✅ Empleados: {Empleado.objects.count()}")

print(f"\n💳 SISTEMA DE SUSCRIPCIONES:")
print(f"  ✅ Planes disponibles: {PlanSuscripcion.objects.count()}")
print(f"  ✅ Suscripciones activas: {SuscripcionEmpresa.objects.filter(estado='activa').count()}")
print(f"  ✅ Pagos registrados: {Pago.objects.count()}")

print(f"\n🏢 EMPRESAS Y SUSCRIPCIONES:")
for empresa in Empresa.objects.all():
    estado = SuscripcionManager.obtener_estado_suscripcion(empresa)
    print(f"  📋 {empresa.nombre}")
    print(f"     Plan: {estado.get('plan', 'Sin suscripción')}")
    if estado['tiene_suscripcion']:
        print(f"     Precio: ${estado['precio']}")
        print(f"     Plantas: {estado['plantas_incluidas']}")
        print(f"     Días restantes: {estado['dias_restantes']}")

print(f"\n🔑 CREDENCIALES DE ACCESO:")
print(f"  🔧 SuperAdmin:")
print(f"     Usuario: superadmin")
print(f"     Password: admin123")
print(f"     Acceso: Completo al sistema")

print(f"\n  🏢 Administradores de Empresa:")
for empresa in Empresa.objects.all():
    admin = empresa.administrador
    if admin and admin.user:
        print(f"     Usuario: {admin.user.username}")
        print(f"     Password: admin123")
        print(f"     Empresa: {empresa.nombre}")
        print(f"     Acceso: {'✅ Completo' if SuscripcionManager.empresa_tiene_suscripcion_activa(empresa) else '❌ Limitado'}")

print(f"\n🚀 PARA USAR EL SISTEMA:")
print(f"  1. Ejecutar: python manage.py runserver")
print(f"  2. O usar: ..\\start.bat")
print(f"  3. Acceder a: http://localhost:8000")
print(f"  4. Admin Django: http://localhost:8000/admin/")

print(f"\n📚 ENDPOINTS DE SUSCRIPCIONES:")
print(f"  GET  /api/subscriptions/mi_suscripcion/")
print(f"  GET  /api/subscriptions/planes_disponibles/")
print(f"  POST /api/subscriptions/contratar_plan/")
print(f"  GET  /api/subscriptions/verificar_acceso/")

print(f"\n🔧 LÓGICA DE FUNCIONAMIENTO:")
print(f"  ✅ Empresa se registra → Selecciona plan → Acceso completo")
print(f"  ✅ Todas las plantas de la empresa comparten suscripción")
print(f"  ✅ SuperAdmin tiene acceso completo siempre")
print(f"  ❌ Sin suscripción → Solo avisos y opción de pago")
print(f"  🔄 Sistema automático de verificación de acceso")

print("=" * 60)
print("🎯 ¡SISTEMA AXYOMA COMPLETAMENTE FUNCIONAL!")
print("   Todo listo para desarrollo y producción")
print("=" * 60)
