#!/usr/bin/env python
import django
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.users.models import Empresa
import json

print('=== DATOS API EMPRESAS ===')
empresas = Empresa.objects.all()
empresas_data = []

for empresa in empresas:
    data = {
        'empresa_id': empresa.empresa_id,
        'nombre': empresa.nombre,
        'rfc': empresa.rfc,
        'direccion': empresa.direccion or '',
        'correo': empresa.email_contacto or '',  # Mapear email_contacto a correo
        'telefono': empresa.telefono_contacto or '',  # Mapear telefono_contacto a telefono
        'status': empresa.status,
        'plantas_count': empresa.plantas.count(),
    }
    empresas_data.append(data)
    print(f'Empresa: {data["nombre"]}')
    print(f'  correo: "{data["correo"]}"')
    print(f'  telefono: "{data["telefono"]}"')
    print(f'  direccion: "{data["direccion"]}"')
    print(f'  plantas_count: {data["plantas_count"]}')
    print('---')

print('\nJSON para frontend:')
result = {
    'empresas': empresas_data,
    'total': len(empresas_data)
}
print(json.dumps(result, indent=2, ensure_ascii=False))
