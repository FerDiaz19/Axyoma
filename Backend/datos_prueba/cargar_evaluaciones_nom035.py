#!/usr/bin/env python
"""
📋 CARGADOR DE EVALUACIONES NOM-035
=================================
Script específico para cargar la evaluación NOM-035 completa
"""

import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')
django.setup()

from django.db import transaction

def cargar_tipos_evaluacion():
    """Cargar tipos de evaluación"""
    print("📋 Cargando tipos de evaluación...")
    
    try:
        from apps.evaluaciones.models import TipoEvaluacion
        
        tipos = [
            {
                'nombre': 'Normativa',
                'descripcion': 'Evaluación estandarizada que cumple con normativas o estándares oficiales.'
            },
            {
                'nombre': 'Interna', 
                'descripcion': 'Evaluación exclusiva de una empresa para su aplicación en el contexto interno de esta misma.'
            }
        ]
        
        for tipo_data in tipos:
            tipo, created = TipoEvaluacion.objects.get_or_create(
                nombre=tipo_data['nombre'],
                defaults={'descripcion': tipo_data['descripcion']}
            )
            print(f"  ✅ {tipo.nombre}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error cargando tipos: {e}")
        return False

def cargar_evaluacion_nom035():
    """Cargar evaluación NOM-035"""
    print("\n📊 Cargando evaluación NOM-035...")
    
    try:
        from apps.evaluaciones.models import TipoEvaluacion, Evaluacion
        
        tipo_normativa = TipoEvaluacion.objects.get(nombre='Normativa')
        
        evaluacion, created = Evaluacion.objects.get_or_create(
            nombre='Factores de riesgo psicosocial: NOM-035 STPS 2018',
            defaults={
                'descripcion': 'Evaluación diseñada para identificar los factores de riesgo psicosocial y evaluar el entorno organizacional en los centros de trabajo',
                'instrucciones': '''Para responder de forma efectiva, por favor:
• Busca un lugar tranquilo y cómodo: Sin interrupciones para concentrarte.
• Sé totalmente honesto: Tu sinceridad es clave; no hay respuestas correctas o incorrectas.
• Lee con atención cada pregunta: Tómate tu tiempo para entender bien antes de responder.
• Considera tu experiencia general: Piensa en los últimos meses, no solo en eventos recientes.

Tu honestidad y participación son muy importantes para mejorar nuestro entorno de trabajo.''',
                'tiempo_limite': None,
                'umbral_aprobacion': None,
                'status': True,
                'tipo_evaluacion': tipo_normativa,
                'empresa': None,
                'creado_por': None
            }
        )
        
        print(f"  ✅ {evaluacion.nombre}")
        return evaluacion
        
    except Exception as e:
        print(f"❌ Error cargando evaluación: {e}")
        return None

def cargar_secciones(evaluacion):
    """Cargar secciones de la evaluación"""
    print("\n📝 Cargando secciones...")
    
    try:
        from apps.evaluaciones.models import SeccionEvaluacion
        
        secciones_data = [
            ('Condiciones ambientales del centro de trabajo', 'Para responder las preguntas siguientes considere las condiciones ambientales de su centro de trabajo.'),
            ('Cantidad y ritmo de trabajo', 'Para responder a las preguntas siguientes piense en la cantidad y ritmo de trabajo que tiene.'),
            ('Esfuerzo mental', 'Las preguntas siguientes están relacionadas con el esfuerzo mental que le exige su trabajo.'),
            ('Actividades y responsabilidades', 'Las preguntas siguientes están relacionadas con las actividades que realiza en su trabajo y las responsabilidades que tiene.'),
            ('Jornada de trabajo', 'Las preguntas siguientes están relacionadas con su jornada de trabajo.'),
            ('Decisiones en el trabajo', 'Las preguntas siguientes están relacionadas con las decisiones que puede tomar en su trabajo.'),
            ('Cambios en el trabajo', 'Las preguntas siguientes están relacionadas con cualquier tipo de cambio que ocurra en su trabajo.'),
            ('Capacitación e información', 'Las preguntas siguientes están relacionadas con la capacitación e información que se le proporciona sobre su trabajo.'),
            ('Relación con los jefes', 'Las preguntas siguientes están relacionadas con el o los jefes con quien tiene contacto.'),
            ('Relaciones con los compañeros', 'Las preguntas siguientes se refieren a las relaciones con sus compañeros.'),
            ('Rendimiento, reconocimiento, pertenencia y estabilidad', 'Las preguntas siguientes están relacionadas con la información que recibe sobre su rendimiento en el trabajo.'),
            ('Actos de violencia laboral', 'Las preguntas siguientes están relacionadas con actos de violencia laboral.'),
            ('Atención a clientes y usuarios', 'Las preguntas siguientes están relacionadas con la atención a clientes y usuarios.'),
            ('Jefe de otros trabajadores', 'Las preguntas siguientes están relacionadas con las actitudes de las personas que supervisa.')
        ]
        
        secciones = []
        for i, (nombre, descripcion) in enumerate(secciones_data, 1):
            seccion, created = SeccionEvaluacion.objects.get_or_create(
                nombre=nombre,
                evaluacion=evaluacion,
                defaults={
                    'descripcion': descripcion,
                    'numero_orden': i,
                    'es_evaluable': False
                }
            )
            secciones.append(seccion)
            print(f"  ✅ {seccion.nombre}")
        
        return secciones
        
    except Exception as e:
        print(f"❌ Error cargando secciones: {e}")
        return []

def cargar_conjuntos_respuestas():
    """Cargar conjuntos de respuestas"""
    print("\n🎯 Cargando conjuntos de respuestas...")
    
    try:
        from apps.evaluaciones.models import ConjuntoRespuestas, PosibleRespuesta
        
        # Conjunto Escala
        conjunto_escala, created = ConjuntoRespuestas.objects.get_or_create(
            nombre='Escala (Siempre/Nunca)',
            defaults={
                'descripcion': 'Opciones de respuesta para una escala de "Siempre" a "Nunca".',
                'predefinido': True
            }
        )
        
        opciones_escala = [
            ('Siempre', 1),
            ('Casi siempre', 2), 
            ('Algunas veces', 3),
            ('Casi nunca', 4),
            ('Nunca', 5)
        ]
        
        for texto, orden in opciones_escala:
            PosibleRespuesta.objects.get_or_create(
                texto_opcion=texto,
                conjunto_respuestas=conjunto_escala,
                defaults={
                    'numero_orden': orden,
                    'valor_booleano': None,
                    'valor_int': None,
                    'valor_decimal': None
                }
            )
        
        print(f"  ✅ {conjunto_escala.nombre}")
        
        # Conjunto Booleano
        conjunto_bool, created = ConjuntoRespuestas.objects.get_or_create(
            nombre='Booleano (Sí/No)',
            defaults={
                'descripcion': 'Opciones de respuesta para preguntas booleanas.',
                'predefinido': True
            }
        )
        
        opciones_bool = [
            ('Sí', True, 1),
            ('No', False, 2)
        ]
        
        for texto, valor, orden in opciones_bool:
            PosibleRespuesta.objects.get_or_create(
                texto_opcion=texto,
                conjunto_respuestas=conjunto_bool,
                defaults={
                    'numero_orden': orden,
                    'valor_booleano': valor,
                    'valor_int': None,
                    'valor_decimal': None
                }
            )
        
        print(f"  ✅ {conjunto_bool.nombre}")
        
        return conjunto_escala, conjunto_bool
        
    except Exception as e:
        print(f"❌ Error cargando conjuntos: {e}")
        return None, None

@transaction.atomic
def main():
    """Función principal"""
    print("📋 CARGADOR DE EVALUACIONES NOM-035")
    print("=" * 50)
    print("Este script carga la evaluación NOM-035 completa.")
    print()
    
    respuesta = input("¿Continuar? (s/n): ").lower()
    if respuesta not in ['s', 'si', 'y', 'yes']:
        print("❌ Operación cancelada")
        return
    
    # Ejecutar pasos
    if not cargar_tipos_evaluacion():
        return
    
    evaluacion = cargar_evaluacion_nom035()
    if not evaluacion:
        return
    
    secciones = cargar_secciones(evaluacion)
    if not secciones:
        return
    
    conjunto_escala, conjunto_bool = cargar_conjuntos_respuestas()
    if not conjunto_escala or not conjunto_bool:
        return
    
    # Resultado final
    print("\n" + "=" * 50)
    print("🎉 ¡EVALUACIÓN NOM-035 CARGADA!")
    print("=" * 50)
    print("✅ Tipos de evaluación creados")
    print("✅ Evaluación NOM-035 creada")
    print("✅ 14 secciones creadas")
    print("✅ Conjuntos de respuestas creados")
    print()
    print("📋 NOTA: Las preguntas individuales deben")
    print("   cargarse por separado si es necesario.")
    print("=" * 50)

if __name__ == "__main__":
    main()
