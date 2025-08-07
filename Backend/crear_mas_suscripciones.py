#!/usr/bin/env python
import os
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')
django.setup()

def crear_mas_suscripciones():
    """Crear varias suscripciones de prueba"""
    print("🔧 CREANDO SUSCRIPCIONES DE PRUEBA")
    print("=" * 50)
    
    try:
        from apps.subscriptions.models import SuscripcionEmpresa, PlanSuscripcion
        from apps.users.models import Empresa
        from datetime import date, timedelta
        import random
        
        planes = PlanSuscripcion.objects.all()
        empresas = Empresa.objects.all()
        
        print(f"📋 Planes disponibles: {planes.count()}")
        print(f"🏢 Empresas disponibles: {empresas.count()}")
        
        # Crear suscripciones para varias empresas
        created_count = 0
        for empresa in empresas[:5]:  # Primeras 5 empresas
            try:
                # Evitar duplicados
                if not SuscripcionEmpresa.objects.filter(empresa=empresa).exists():
                    plan = random.choice(planes)
                    
                    suscripcion = SuscripcionEmpresa.objects.create(
                        empresa=empresa,
                        plan=plan,
                        fecha_fin=date.today() + timedelta(days=random.randint(30, 365)),
                        estado=random.choice(['activa', 'vencida', 'cancelada']),
                        status=True
                    )
                    
                    print(f"✅ Creada: {empresa.nombre} - {plan.nombre}")
                    created_count += 1
                else:
                    print(f"⚠️ Ya existe suscripción para: {empresa.nombre}")
                    
            except Exception as e:
                print(f"❌ Error creando suscripción para {empresa.nombre}: {e}")
        
        total_suscripciones = SuscripcionEmpresa.objects.count()
        print(f"\n🎉 Proceso completado!")
        print(f"   • Suscripciones creadas: {created_count}")
        print(f"   • Total suscripciones: {total_suscripciones}")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    crear_mas_suscripciones()
