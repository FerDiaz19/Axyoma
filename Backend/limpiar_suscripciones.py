#!/usr/bin/env python
"""
Script para limpiar todas las suscripciones y pagos
Útil para resetear el sistema de suscripciones durante desarrollo
"""

import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')
django.setup()

def limpiar_suscripciones():
    """Elimina todas las suscripciones y pagos"""
    try:
        from apps.subscriptions.models import SuscripcionEmpresa, Pago
        
        print('🔄 Limpiando suscripciones y pagos...')
        
        # Eliminar suscripciones (esto eliminará pagos automáticamente por CASCADE)
        count_suscripciones = SuscripcionEmpresa.objects.count()
        count_pagos = Pago.objects.count()
        
        SuscripcionEmpresa.objects.all().delete()
        Pago.objects.all().delete()
        
        print(f'✅ {count_suscripciones} suscripciones eliminadas')
        print(f'✅ {count_pagos} pagos eliminados')
        print('🎯 Sistema de suscripciones limpio')
        
    except Exception as e:
        print(f'❌ Error limpiando suscripciones: {str(e)}')
        sys.exit(1)

if __name__ == '__main__':
    limpiar_suscripciones()
