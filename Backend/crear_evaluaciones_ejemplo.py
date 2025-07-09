#!/usr/bin/env python
"""
Script para verificar y crear datos de ejemplo para evaluaciones
"""

import os
import sys
import django

# Configurar Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')
django.setup()

from apps.surveys.models import Evaluacion, PreguntaEvaluacion
from apps.users.models import Empresa, Empleado
from django.contrib.auth.models import User

def crear_evaluacion_ejemplo():
    """
    Crear una evaluación de ejemplo para probar el sistema
    """
    try:
        # Buscar un usuario superadmin
        superadmin = User.objects.filter(is_superuser=True).first()
        if not superadmin:
            print("❌ No se encontró un usuario superadmin")
            return
        
        # Crear evaluación normativa
        evaluacion_normativa, created = Evaluacion.objects.get_or_create(
            titulo="Evaluación NOM-035 de Prueba",
            tipo="normativa",
            defaults={
                'descripcion': 'Evaluación de prueba basada en la NOM-035 para verificar el sistema',
                'instrucciones': 'Responda todas las preguntas de forma honesta y completa.',
                'tiempo_limite': 60,
                'creado_por': superadmin,
                'estado': 'activa',
            }
        )
        
        if created:
            print("✅ Evaluación normativa creada")
            
            # Crear preguntas de ejemplo
            preguntas = [
                {
                    'orden': 1,
                    'texto': '¿Trabaja usted en horario nocturno?',
                    'tipo': 'verdadero_falso',
                    'es_requerida': True,
                    'opciones': []
                },
                {
                    'orden': 2,
                    'texto': '¿Experimenta estrés debido a la carga de trabajo?',
                    'tipo': 'escala',
                    'es_requerida': True,
                    'opciones': [],
                    'escala_min': 1,
                    'escala_max': 5
                },
                {
                    'orden': 3,
                    'texto': '¿Qué tipo de apoyo necesita para manejar el estrés?',
                    'tipo': 'texto',
                    'es_requerida': False,
                    'opciones': []
                },
                {
                    'orden': 4,
                    'texto': '¿Considera que su entorno de trabajo es seguro?',
                    'tipo': 'verdadero_falso',
                    'es_requerida': True,
                    'opciones': []
                },
                {
                    'orden': 5,
                    'texto': '¿Cuál de las siguientes herramientas de software utiliza más frecuentemente?',
                    'tipo': 'multiple',
                    'es_requerida': True,
                    'opciones': ['Microsoft Office', 'Google Workspace', 'LibreOffice']
                }
            ]
            
            for pregunta_data in preguntas:
                pregunta = PreguntaEvaluacion.objects.create(
                    evaluacion=evaluacion_normativa,
                    **pregunta_data
                )
                print(f"  ✅ Pregunta creada: {pregunta.texto[:50]}...")
        else:
            print("ℹ️  Evaluación normativa ya existe")
        
        # Crear evaluación interna si existe una empresa
        empresa = Empresa.objects.first()
        if empresa:
            # Usar el superadmin para crear la evaluación interna de ejemplo
            evaluacion_interna, created = Evaluacion.objects.get_or_create(
                titulo="Evaluación de Desempeño Q2",
                tipo="interna",
                empresa=empresa,
                defaults={
                    'descripcion': 'Evaluación trimestral de desempeño para empleados',
                    'instrucciones': 'Evalúe su desempeño en el último trimestre.',
                    'tiempo_limite': 45,
                    'creado_por': superadmin,
                    'estado': 'activa',
                }
            )
            
            if created:
                print("✅ Evaluación interna creada")
                
                # Crear preguntas de ejemplo
                preguntas_internas = [
                    {
                        'orden': 1,
                        'texto': '¿Cómo calificaría su desempeño técnico en este trimestre?',
                        'tipo': 'escala',
                        'es_requerida': True,
                        'opciones': [],
                        'escala_min': 1,
                        'escala_max': 10
                    },
                    {
                        'orden': 2,
                        'texto': 'Describa sus principales logros en este período',
                        'tipo': 'texto',
                        'es_requerida': True,
                        'opciones': []
                    },
                    {
                        'orden': 3,
                        'texto': '¿Qué aspectos necesita mejorar?',
                        'tipo': 'texto',
                        'es_requerida': False,
                        'opciones': []
                    }
                ]
                
                for pregunta_data in preguntas_internas:
                    pregunta = PreguntaEvaluacion.objects.create(
                        evaluacion=evaluacion_interna,
                        **pregunta_data
                    )
                    print(f"  ✅ Pregunta creada: {pregunta.texto[:50]}...")
            else:
                print("ℹ️  Evaluación interna ya existe")
        
        print("\n📊 Estadísticas finales:")
        print(f"  - Evaluaciones totales: {Evaluacion.objects.count()}")
        print(f"  - Preguntas totales: {PreguntaEvaluacion.objects.count()}")
        print(f"  - Evaluaciones normativas: {Evaluacion.objects.filter(tipo='normativa').count()}")
        print(f"  - Evaluaciones internas: {Evaluacion.objects.filter(tipo='interna').count()}")
        
    except Exception as e:
        print(f"❌ Error al crear evaluaciones de ejemplo: {e}")

def main():
    print("🚀 Creando datos de ejemplo para evaluaciones...")
    print("=" * 50)
    
    crear_evaluacion_ejemplo()
    
    print("\n" + "=" * 50)
    print("✅ Proceso completado!")

if __name__ == "__main__":
    main()
