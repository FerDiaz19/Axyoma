#!/usr/bin/env python
import os
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')
django.setup()

def verificar_suscripciones():
    """Verificar si existen datos de suscripciones"""
    print("🔍 VERIFICANDO DATOS DE SUSCRIPCIONES")
    print("=" * 50)
    
    try:
        from apps.subscriptions.models import SuscripcionEmpresa, PlanSuscripcion
        from apps.users.models import Empresa
        
        # Verificar planes
        planes = PlanSuscripcion.objects.all()
        print(f"📋 Planes disponibles: {planes.count()}")
        for plan in planes[:3]:
            print(f"  • {plan.nombre} - ${plan.precio}")
        
        # Verificar empresas
        empresas = Empresa.objects.all()
        print(f"\n🏢 Empresas registradas: {empresas.count()}")
        for empresa in empresas[:3]:
            print(f"  • {empresa.nombre}")
        
        # Verificar suscripciones
        suscripciones = SuscripcionEmpresa.objects.all()
        print(f"\n📊 Suscripciones totales: {suscripciones.count()}")
        
        if suscripciones.count() == 0:
            print("⚠️ No hay suscripciones registradas!")
            
            # Crear una suscripción de prueba si hay planes y empresas
            if planes.count() > 0 and empresas.count() > 0:
                print("\n🔧 Creando suscripción de prueba...")
                from datetime import date, timedelta
                
                # Crear con todos los campos requeridos por la DB
                suscripcion_prueba = SuscripcionEmpresa.objects.create(
                    empresa=empresas.first(),
                    plan=planes.first(),
                    fecha_fin=date.today() + timedelta(days=30),  # Campo requerido por DB
                    estado='activa',  # Campo requerido por DB
                    status=True  # Campo faltante en el modelo original
                )
                print(f"✅ Suscripción de prueba creada: {suscripcion_prueba}")
        else:
            print("Suscripciones encontradas:")
            for suscripcion in suscripciones[:5]:
                print(f"  • {suscripcion.empresa.nombre} - {suscripcion.plan.nombre} ({suscripcion.estado})")
                
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    verificar_suscripciones()
