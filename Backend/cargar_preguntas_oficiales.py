#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
📋 CARGADOR DE PREGUNTAS OFICIALES NOM-030 Y NOM-035
=================================================
Script para cargar las preguntas oficiales reales de las normativas
"""

import os
import sys
import django
from django.db import transaction

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')
django.setup()

from apps.evaluaciones.models_oficiales import EvaluacionOficial, SeccionOficial, PreguntaOficial

@transaction.atomic
def cargar_preguntas_nom035():
    """Cargar preguntas oficiales NOM-035"""
    print("🧠 Cargando preguntas NOM-035...")
    
    # Obtener o crear evaluación NOM-035
    evaluacion, created = EvaluacionOficial.objects.get_or_create(
        tipo_norma='NOM-035',
        defaults={
            'nombre': 'Evaluación NOM-035 Oficial',
            'descripcion': 'Factores de riesgo psicosocial en el trabajo - NOM-035-STPS-2018',
            'instrucciones': 'Evaluación para identificar los factores de riesgo psicosocial en el trabajo',
            'tiempo_limite': 45,
            'activa': True
        }
    )
    
    if created:
        print(f"✅ Evaluación NOM-035 creada: {evaluacion.nombre}")
    else:
        print(f"✅ Evaluación NOM-035 ya existe: {evaluacion.nombre}")
    
    # Crear secciones
    secciones_data = [
        ("Condiciones en el ambiente de trabajo", 1),
        ("Cantidad y ritmo de trabajo", 2),
        ("Esfuerzo mental", 3),
        ("Actividades y responsabilidades", 4),
        ("Jornada de trabajo", 5),
        ("Decisiones en el trabajo", 6),
        ("Cambios en el trabajo", 7),
        ("Capacitación e información", 8),
        ("Relación con los jefes", 9),
        ("Relaciones con los compañeros", 10),
        ("Rendimiento, reconocimiento, pertenencia y estabilidad", 11),
        ("Actos de violencia laboral", 12),
        ("Atención a clientes y usuarios", 13),
        ("Jefe de otros trabajadores", 14),
    ]
    
    secciones = {}
    for nombre, orden in secciones_data:
        seccion, created = SeccionOficial.objects.get_or_create(
            evaluacion_oficial=evaluacion,
            nombre=nombre,
            defaults={
                'descripcion': f'Preguntas relacionadas con {nombre.lower()}',
                'numero_orden': orden
            }
        )
        secciones[orden] = seccion
        if created:
            print(f"  ✅ Sección creada: {nombre}")
    
    # Preguntas NOM-035
    preguntas_data = [
        # Sección 1: Condiciones en el ambiente de trabajo
        (1, 1, 'El espacio donde trabajo me permite realizar mis actividades de manera segura e higiénica', 'Escala', ['Siempre', 'Casi siempre', 'Algunas veces', 'Casi nunca', 'Nunca'], True),
        (1, 2, 'Mi trabajo me exige hacer mucho esfuerzo físico', 'Escala', ['Siempre', 'Casi siempre', 'Algunas veces', 'Casi nunca', 'Nunca'], True),
        (1, 3, 'Me preocupa sufrir un accidente en mi trabajo', 'Escala', ['Siempre', 'Casi siempre', 'Algunas veces', 'Casi nunca', 'Nunca'], True),
        (1, 4, 'Considero que en mi trabajo se aplican las normas de seguridad y salud en el trabajo', 'Escala', ['Siempre', 'Casi siempre', 'Algunas veces', 'Casi nunca', 'Nunca'], True),
        (1, 5, 'Considero que las actividades que realizo son peligrosas', 'Escala', ['Siempre', 'Casi siempre', 'Algunas veces', 'Casi nunca', 'Nunca'], True),
        
        # Sección 2: Cantidad y ritmo de trabajo
        (2, 6, 'Por la cantidad de trabajo que tengo debo quedarme tiempo adicional a mi turno', 'Escala', ['Siempre', 'Casi siempre', 'Algunas veces', 'Casi nunca', 'Nunca'], True),
        (2, 7, 'Por la cantidad de trabajo que tengo debo trabajar sin parar', 'Escala', ['Siempre', 'Casi siempre', 'Algunas veces', 'Casi nunca', 'Nunca'], True),
        (2, 8, 'Considero que es necesario mantener un ritmo de trabajo acelerado', 'Escala', ['Siempre', 'Casi siempre', 'Algunas veces', 'Casi nunca', 'Nunca'], True),
        
        # Sección 3: Esfuerzo mental
        (3, 9, 'Mi trabajo exige que esté muy concentrado', 'Escala', ['Siempre', 'Casi siempre', 'Algunas veces', 'Casi nunca', 'Nunca'], True),
        (3, 10, 'Mi trabajo requiere que memorice mucha información', 'Escala', ['Siempre', 'Casi siempre', 'Algunas veces', 'Casi nunca', 'Nunca'], True),
        (3, 11, 'En mi trabajo tengo que tomar decisiones difíciles muy rápido', 'Escala', ['Siempre', 'Casi siempre', 'Algunas veces', 'Casi nunca', 'Nunca'], True),
        (3, 12, 'Mi trabajo exige que atienda varios asuntos al mismo tiempo', 'Escala', ['Siempre', 'Casi siempre', 'Algunas veces', 'Casi nunca', 'Nunca'], True),
        
        # Sección 4: Actividades y responsabilidades
        (4, 13, 'En mi trabajo soy responsable de cosas de mucho valor', 'Escala', ['Siempre', 'Casi siempre', 'Algunas veces', 'Casi nunca', 'Nunca'], True),
        (4, 14, 'Respondo ante mi jefe por los resultados de toda mi área de trabajo', 'Escala', ['Siempre', 'Casi siempre', 'Algunas veces', 'Casi nunca', 'Nunca'], True),
        (4, 15, 'En el trabajo me dan órdenes contradictorias', 'Escala', ['Siempre', 'Casi siempre', 'Algunas veces', 'Casi nunca', 'Nunca'], True),
        (4, 16, 'Considero que en mi trabajo me piden hacer cosas innecesarias', 'Escala', ['Siempre', 'Casi siempre', 'Algunas veces', 'Casi nunca', 'Nunca'], True),
        
        # Sección 9: Relación con los jefes
        (9, 33, 'Mi jefe ayuda a organizar mejor el trabajo', 'Escala', ['Siempre', 'Casi siempre', 'Algunas veces', 'Casi nunca', 'Nunca'], True),
        (9, 34, 'Mi jefe tiene en cuenta mis puntos de vista y opiniones', 'Escala', ['Siempre', 'Casi siempre', 'Algunas veces', 'Casi nunca', 'Nunca'], True),
        (9, 35, 'Mi jefe me comunica a tiempo la información relacionada con el trabajo', 'Escala', ['Siempre', 'Casi siempre', 'Algunas veces', 'Casi nunca', 'Nunca'], True),
        
        # Sección 12: Actos de violencia laboral
        (12, 57, 'En mi trabajo puedo expresarme libremente sin interrupciones', 'Escala', ['Siempre', 'Casi siempre', 'Algunas veces', 'Casi nunca', 'Nunca'], True),
        (12, 58, 'Recibo críticas constantes a mi persona y/o trabajo', 'Escala', ['Siempre', 'Casi siempre', 'Algunas veces', 'Casi nunca', 'Nunca'], True),
        
        # Preguntas condicionales
        (13, 65, 'En mi trabajo debo brindar servicio a clientes o usuarios', 'Si/No', ['Sí', 'No'], True),
        (14, 70, 'Soy jefe de otros trabajadores', 'Si/No', ['Sí', 'No'], True),
    ]
    
    preguntas_creadas = 0
    for seccion_num, orden, texto, tipo, opciones, obligatoria in preguntas_data:
        seccion = secciones[seccion_num]
        pregunta, created = PreguntaOficial.objects.get_or_create(
            seccion=seccion,
            numero_orden=orden,
            defaults={
                'texto_pregunta': texto,
                'tipo_pregunta': tipo,
                'opciones_respuesta': opciones,
                'es_obligatoria': obligatoria
            }
        )
        if created:
            preguntas_creadas += 1
    
    print(f"✅ Preguntas NOM-035 creadas: {preguntas_creadas}")
    return evaluacion

@transaction.atomic 
def cargar_preguntas_nom030():
    """Cargar preguntas oficiales NOM-030"""
    print("🛡️ Cargando preguntas NOM-030...")
    
    # Obtener o crear evaluación NOM-030
    evaluacion, created = EvaluacionOficial.objects.get_or_create(
        tipo_norma='NOM-030',
        defaults={
            'nombre': 'Evaluación NOM-030 Oficial',
            'descripcion': 'Servicios preventivos de seguridad y salud en el trabajo - NOM-030-STPS-2009',
            'instrucciones': 'Evaluación sobre los servicios preventivos de seguridad y salud en el trabajo',
            'tiempo_limite': 30,
            'activa': True
        }
    )
    
    if created:
        print(f"✅ Evaluación NOM-030 creada: {evaluacion.nombre}")
    else:
        print(f"✅ Evaluación NOM-030 ya existe: {evaluacion.nombre}")
    
    # Crear secciones
    secciones_data = [
        ("Servicios preventivos", 1),
        ("Diagnóstico y programa de seguridad y salud", 2),
        ("Medidas de prevención y atención de emergencias", 3),
        ("Capacitación y promoción de la salud", 4),
        ("Reportes, investigación y adecuaciones", 5),
    ]
    
    secciones = {}
    for nombre, orden in secciones_data:
        seccion, created = SeccionOficial.objects.get_or_create(
            evaluacion_oficial=evaluacion,
            nombre=nombre,
            defaults={
                'descripcion': f'Preguntas sobre {nombre.lower()}',
                'numero_orden': orden
            }
        )
        secciones[orden] = seccion
        if created:
            print(f"  ✅ Sección creada: {nombre}")
    
    # Preguntas NOM-030
    preguntas_data = [
        (1, 75, '¿Qué debe demostrar el patrón referente al personal de la empresa que forma parte de los servicios preventivos de seguridad y salud en el trabajo?', 
         'Múltiple', ['Que es capacitado en las funciones y actividades', 'Que no se han presentado accidentes recientes', 'Que tienen conocimiento acerca de las funciones y actividades a realizar', 'Que es actualizado constantemente dentro del centro de trabajo'], True),
        
        (1, 76, 'El patrón cumple cuando presenta mediante una entrevista que asume funciones y actividades de seguridad y ______',
         'Múltiple', ['Preventivas - Salud', 'Seguras - Prevención', 'Funcionales - Salud', 'Esenciales - Prevención'], True),
         
        (2, 80, '¿Cuál es el fin de orientar al patrón y a los trabajadores de las funciones y actividades a desarrollar por los servicios preventivos y salud en el trabajo?',
         'Múltiple', ['Cumplir con la obligación de brindar capacitación', 'Prever que los trabajadores desarrollen sus actividades en condiciones seguras', 'Prever que los trabajadores no tengan accidentes y esto produzca costos adicionales', 'Fortalecer una cultura de reacción ante accidentes'], True),
         
        (3, 81, '¿Cuáles son las características que el botiquín debe cumplir?',
         'Múltiple', ['Ser de fácil transporte, visible y de fácil acceso, que contenga material suficiente, identificable con una cruz roja, de peso no excesivo', 'Ser de fácil transporte, visible y de fácil acceso, identificable con una cruz roja, de peso no excesivo, sin candados o dispositivos que dificulten el acceso a su contenido', 'Ser de fácil transporte, colocado en un lugar donde todos tengan acceso a él, identificable con una cruz roja, de material resistente y sin candados o dispositivos que dificulten el acceso a su contenido', 'Ser de fácil transporte y de fácil acceso, en una ubicación fácil para los trabajadores, con contenido suficiente para todos, sin candados que dificulten el acceso a su contenido'], True),
         
        (3, 82, 'El programa de seguridad y salud en el trabajo, deberá tener las fechas de inicio y término programadas para instrumentar las acciones preventivas o correctivas y para la atención de emergencias',
         'Si/No', ['Sí', 'No'], True),
         
        (3, 84, '¿En qué situaciones se brindará atención de consulta médica?',
         'Múltiple', ['Por enfermedad general y por enfermedad de trabajo', 'Por enfermedad de trabajo y por una situación de emergencia en el trabajo', 'Por enfermedad general y por accidente de trabajo', 'Por enfermedad general y por lesiones graves de trabajo'], True),
         
        (4, 85, '¿Cómo se realiza la capacitación para mandos superiores?',
         'Múltiple', ['Brindándoles asesoramiento sobre las dudas que tengan respecto a la seguridad y salud en el trabajo', 'Mediante el asesoramiento sobre los temas que los especialistas en seguridad y salud deben conocer', 'A través del asesoramiento para enseñarles como realizar un programa y normas internas de salud en el trabajo', 'Mediante el asesoramiento para el establecimiento de políticas y normas internas de salud en el trabajo'], True),
         
        (5, 88, 'Cuando las unidades de verificación evalúan el cumplimiento de esta norma, ¿Qué documento se debe emitir?',
         'Múltiple', ['Acta', 'Dictamen', 'Recibo', 'Reglamento'], True),
         
        (5, 93, 'En las acciones recomendadas se deben considerar aspectos como la planeación y dirección; la capacitación e información a los trabajadores y las medidas de prevención. Se deben exceptuar las medidas de protección y las políticas temporales',
         'Si/No', ['Sí', 'No'], True),
    ]
    
    preguntas_creadas = 0
    for seccion_num, orden, texto, tipo, opciones, obligatoria in preguntas_data:
        seccion = secciones[seccion_num]
        pregunta, created = PreguntaOficial.objects.get_or_create(
            seccion=seccion,
            numero_orden=orden,
            defaults={
                'texto_pregunta': texto,
                'tipo_pregunta': tipo,
                'opciones_respuesta': opciones,
                'es_obligatoria': obligatoria
            }
        )
        if created:
            preguntas_creadas += 1
    
    print(f"✅ Preguntas NOM-030 creadas: {preguntas_creadas}")
    return evaluacion

def main():
    """Función principal"""
    print("🚀 INICIANDO CARGA DE PREGUNTAS OFICIALES")
    print("=" * 60)
    
    try:
        # Cargar NOM-035
        evaluacion_035 = cargar_preguntas_nom035()
        print(f"📊 Total secciones NOM-035: {evaluacion_035.secciones.count()}")
        print(f"❓ Total preguntas NOM-035: {PreguntaOficial.objects.filter(seccion__evaluacion_oficial=evaluacion_035).count()}")
        
        print()
        
        # Cargar NOM-030  
        evaluacion_030 = cargar_preguntas_nom030()
        print(f"📊 Total secciones NOM-030: {evaluacion_030.secciones.count()}")
        print(f"❓ Total preguntas NOM-030: {PreguntaOficial.objects.filter(seccion__evaluacion_oficial=evaluacion_030).count()}")
        
        print("\n" + "=" * 60)
        print("🎉 CARGA COMPLETADA CON ÉXITO")
        print(f"📈 Total evaluaciones oficiales: {EvaluacionOficial.objects.count()}")
        print(f"📋 Total secciones oficiales: {SeccionOficial.objects.count()}")
        print(f"❓ Total preguntas oficiales: {PreguntaOficial.objects.count()}")
        
    except Exception as e:
        print(f"❌ Error durante la carga: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
