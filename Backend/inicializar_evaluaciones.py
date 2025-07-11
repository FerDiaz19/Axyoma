#!/usr/bin/env python
"""
Script para inicializar datos de evaluaciones
"""
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')
django.setup()

from apps.evaluaciones.models import TipoEvaluacion, Pregunta
from django.contrib.auth.models import User

def main():
    print("🚀 Inicializando datos de evaluaciones...")
    
    # Crear tipos de evaluación
    nom035, created = TipoEvaluacion.objects.get_or_create(
        nombre='NOM-035',
        defaults={'descripcion': 'Evaluación de factores de riesgo psicosocial', 'normativa_oficial': True}
    )
    if created:
        print(f"✅ Tipo de evaluación creado: {nom035.nombre}")
    else:
        print(f"ℹ️  Tipo de evaluación ya existe: {nom035.nombre}")

    nom030, created = TipoEvaluacion.objects.get_or_create(
        nombre='NOM-030',
        defaults={'descripcion': 'Evaluación de seguridad e higiene', 'normativa_oficial': True}
    )
    if created:
        print(f"✅ Tipo de evaluación creado: {nom030.nombre}")
    else:
        print(f"ℹ️  Tipo de evaluación ya existe: {nom030.nombre}")

    evaluacion360, created = TipoEvaluacion.objects.get_or_create(
        nombre='360',
        defaults={'descripcion': 'Evaluación 360 grados', 'normativa_oficial': False}
    )
    if created:
        print(f"✅ Tipo de evaluación creado: {evaluacion360.nombre}")
    else:
        print(f"ℹ️  Tipo de evaluación ya existe: {evaluacion360.nombre}")

    # Crear superadmin si no existe
    superadmin, created = User.objects.get_or_create(
        username='superadmin',
        defaults={'email': 'superadmin@axyoma.com', 'is_staff': True, 'is_superuser': True}
    )
    if created:
        superadmin.set_password('admin123')
        superadmin.save()
        print("✅ SuperAdmin creado con credenciales: superadmin/admin123")
    else:
        print("ℹ️  SuperAdmin ya existe")

    # Crear preguntas de ejemplo para NOM-035
    preguntas_nom035 = [
        '¿Consideras que tu carga de trabajo es excesiva?',
        '¿Tienes control sobre tu trabajo?',
        '¿Recibes apoyo de tus compañeros?',
        '¿Tu supervisor te brinda apoyo?',
        '¿Sientes que tu trabajo es reconocido?'
    ]

    print("\n📝 Creando preguntas de ejemplo para NOM-035...")
    for i, texto in enumerate(preguntas_nom035, 1):
        pregunta, created = Pregunta.objects.get_or_create(
            tipo_evaluacion=nom035,
            texto_pregunta=texto,
            defaults={
                'tipo_respuesta': 'escala',
                'opciones_respuesta': ['Nunca', 'Casi nunca', 'A veces', 'Casi siempre', 'Siempre'],
                'orden': i,
                'creada_por': superadmin
            }
        )
        if created:
            print(f"✅ Pregunta creada: {texto}")
        else:
            print(f"ℹ️  Pregunta ya existe: {texto}")

    # Crear preguntas de ejemplo para NOM-030
    preguntas_nom030 = [
        '¿Conoces los procedimientos de seguridad de tu área?',
        '¿Utilizas el equipo de protección personal requerido?',
        '¿Has recibido capacitación en seguridad en los últimos 6 meses?',
        '¿Reportas los incidentes de seguridad?',
        '¿Consideras que tu área de trabajo es segura?'
    ]

    print("\n📝 Creando preguntas de ejemplo para NOM-030...")
    for i, texto in enumerate(preguntas_nom030, 1):
        tipo_respuesta = 'si_no' if i < 5 else 'escala'
        opciones = ['Sí', 'No'] if i < 5 else ['Muy insegura', 'Insegura', 'Regular', 'Segura', 'Muy segura']
        
        pregunta, created = Pregunta.objects.get_or_create(
            tipo_evaluacion=nom030,
            texto_pregunta=texto,
            defaults={
                'tipo_respuesta': tipo_respuesta,
                'opciones_respuesta': opciones,
                'orden': i,
                'creada_por': superadmin
            }
        )
        if created:
            print(f"✅ Pregunta creada: {texto}")
        else:
            print(f"ℹ️  Pregunta ya existe: {texto}")

    # Crear preguntas de ejemplo para 360°
    preguntas_360 = [
        '¿Cómo evalúas la comunicación del empleado?',
        '¿Cómo evalúas el trabajo en equipo?',
        '¿Cómo evalúas la iniciativa y proactividad?',
        '¿Cómo evalúas el cumplimiento de objetivos?',
        '¿Qué aspectos considera que debe mejorar?'
    ]

    print("\n📝 Creando preguntas de ejemplo para 360°...")
    for i, texto in enumerate(preguntas_360, 1):
        tipo_respuesta = 'texto' if i == 5 else 'escala'
        opciones = [] if i == 5 else ['Deficiente', 'Regular', 'Buena', 'Muy buena', 'Excelente']
        
        pregunta, created = Pregunta.objects.get_or_create(
            tipo_evaluacion=evaluacion360,
            texto_pregunta=texto,
            defaults={
                'tipo_respuesta': tipo_respuesta,
                'opciones_respuesta': opciones,
                'orden': i,
                'creada_por': superadmin
            }
        )
        if created:
            print(f"✅ Pregunta creada: {texto}")
        else:
            print(f"ℹ️  Pregunta ya existe: {texto}")

    print("\n🎉 Datos de evaluaciones inicializados exitosamente!")
    print("\n📊 Resumen:")
    print(f"   - Tipos de evaluación: {TipoEvaluacion.objects.count()}")
    print(f"   - Preguntas totales: {Pregunta.objects.count()}")
    print(f"   - Preguntas NOM-035: {Pregunta.objects.filter(tipo_evaluacion=nom035).count()}")
    print(f"   - Preguntas NOM-030: {Pregunta.objects.filter(tipo_evaluacion=nom030).count()}")
    print(f"   - Preguntas 360°: {Pregunta.objects.filter(tipo_evaluacion=evaluacion360).count()}")

if __name__ == '__main__':
    main()
