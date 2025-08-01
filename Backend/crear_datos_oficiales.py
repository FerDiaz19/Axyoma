# -*- coding: utf-8 -*-
"""
Script Django para crear datos de prueba para las APIs oficiales
"""

from django.contrib.auth import get_user_model
from apps.evaluaciones.models_oficiales import (
    EvaluacionOficial, SeccionOficial, PreguntaOficial
)

User = get_user_model()

# Crear SuperAdmin si no existe
superadmin, created = User.objects.get_or_create(
    email='superadmin@axyoma.com',
    defaults={
        'first_name': 'Super',
        'last_name': 'Admin',
        'user_type': 'SuperAdmin',
        'is_active': True,
        'is_staff': True,
        'is_superuser': True
    }
)
if created:
    superadmin.set_password('superadmin123')
    superadmin.save()
    print(f"✅ SuperAdmin creado: {superadmin.email}")
else:
    print(f"✅ SuperAdmin ya existe: {superadmin.email}")

# Crear evaluación oficial NOM-035 si no existe
evaluacion_nom035, created = EvaluacionOficial.objects.get_or_create(
    tipo_norma='NOM-035',
    nombre='Evaluación NOM-035 Oficial',
    defaults={
        'descripcion': 'Evaluación oficial de factores de riesgo psicosocial NOM-035',
        'instrucciones': 'Complete todas las secciones de manera honesta y objetiva.',
        'tiempo_limite': 60,  # 60 minutos
        'activa': True
    }
)
if created:
    print(f"✅ Evaluación NOM-035 creada: {evaluacion_nom035.nombre}")
else:
    print(f"✅ Evaluación NOM-035 ya existe: {evaluacion_nom035.nombre}")

# Crear secciones básicas
seccion1, created = SeccionOficial.objects.get_or_create(
    evaluacion_oficial=evaluacion_nom035,
    numero_orden=1,
    defaults={
        'nombre': 'Información General',
        'descripcion': 'Datos generales del trabajador'
    }
)
if created:
    print(f"✅ Sección creada: {seccion1.nombre}")

seccion2, created = SeccionOficial.objects.get_or_create(
    evaluacion_oficial=evaluacion_nom035,
    numero_orden=2,
    defaults={
        'nombre': 'Condiciones del Trabajo',
        'descripcion': 'Evaluación de las condiciones laborales'
    }
)
if created:
    print(f"✅ Sección creada: {seccion2.nombre}")

# Crear preguntas básicas
pregunta1, created = PreguntaOficial.objects.get_or_create(
    seccion=seccion1,
    numero_orden=1,
    defaults={
        'texto_pregunta': '¿Cuál es su puesto de trabajo?',
        'tipo_pregunta': 'Abierta',
        'es_obligatoria': True
    }
)
if created:
    print(f"✅ Pregunta creada: {pregunta1.texto_pregunta}")

pregunta2, created = PreguntaOficial.objects.get_or_create(
    seccion=seccion2,
    numero_orden=1,
    defaults={
        'texto_pregunta': '¿Considera que su carga de trabajo es adecuada?',
        'tipo_pregunta': 'Múltiple',
        'opciones_respuesta': ['Totalmente de acuerdo', 'De acuerdo', 'En desacuerdo', 'Totalmente en desacuerdo'],
        'es_obligatoria': True
    }
)
if created:
    print(f"✅ Pregunta creada: {pregunta2.texto_pregunta}")

print("\n🎉 Datos de prueba creados exitosamente!")
print("\n📋 Credenciales del SuperAdmin:")
print("   Email: superadmin@axyoma.com")
print("   Password: superadmin123")
print("\n📊 Datos creados:")
print(f"   - Evaluaciones oficiales: {EvaluacionOficial.objects.count()}")
print(f"   - Secciones oficiales: {SeccionOficial.objects.count()}")
print(f"   - Preguntas oficiales: {PreguntaOficial.objects.count()}")
