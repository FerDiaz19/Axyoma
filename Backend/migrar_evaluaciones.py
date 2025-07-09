#!/usr/bin/env python
"""
Script para migrar a la nueva estructura de base de datos de evaluaciones
basada en el esquema SQL original
"""

import os
import sys
import django

# Configurar Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')
django.setup()

from apps.surveys.models_new import TipoEvaluacion, Evaluacion, PreguntaEvaluacion
from apps.surveys.models import Evaluacion as EvaluacionOld, PreguntaEvaluacion as PreguntaOld
from django.contrib.auth.models import User

def crear_tipos_evaluacion():
    """
    Crear los tipos de evaluación predefinidos
    """
    tipos = [
        ('Normativa', 'Evaluaciones basadas en normativas oficiales'),
        ('Interna', 'Evaluaciones creadas para fines de evaluación internos'),
        ('360 Grados', 'Evaluaciones donde se recibe feedback de múltiples fuentes'),
    ]
    
    for nombre, descripcion in tipos:
        tipo, created = TipoEvaluacion.objects.get_or_create(
            nombre=nombre,
            defaults={'descripcion': descripcion}
        )
        if created:
            print(f"✅ Tipo de evaluación creado: {nombre}")
        else:
            print(f"ℹ️  Tipo de evaluación ya existe: {nombre}")

def migrar_evaluaciones():
    """
    Migrar evaluaciones existentes a la nueva estructura
    """
    # Obtener tipos de evaluación
    tipo_normativa = TipoEvaluacion.objects.get(nombre='Normativa')
    tipo_interna = TipoEvaluacion.objects.get(nombre='Interna')
    
    evaluaciones_old = EvaluacionOld.objects.all()
    
    for eval_old in evaluaciones_old:
        # Determinar tipo de evaluación
        if eval_old.tipo == 'normativa':
            tipo_eval = tipo_normativa
        else:
            tipo_eval = tipo_interna
        
        # Crear nueva evaluación
        eval_new, created = Evaluacion.objects.get_or_create(
            nombre=eval_old.titulo,
            defaults={
                'descripcion': eval_old.descripcion,
                'status': eval_old.estado == 'activa',
                'tipo_evaluacion': tipo_eval,
                'empresa': eval_old.empresa,
                'creado_por': eval_old.creado_por,
                'instrucciones': eval_old.instrucciones,
                'tiempo_limite': eval_old.tiempo_limite,
            }
        )
        
        if created:
            print(f"✅ Evaluación migrada: {eval_old.titulo}")
            
            # Migrar preguntas
            preguntas_old = PreguntaOld.objects.filter(evaluacion=eval_old)
            for pregunta_old in preguntas_old:
                pregunta_new = PreguntaEvaluacion.objects.create(
                    evaluacion=eval_new,
                    orden=pregunta_old.orden,
                    texto=pregunta_old.texto,
                    tipo=pregunta_old.tipo,
                    es_requerida=pregunta_old.es_requerida,
                    opciones=pregunta_old.opciones,
                    escala_min=pregunta_old.escala_min,
                    escala_max=pregunta_old.escala_max,
                )
                print(f"  ✅ Pregunta migrada: {pregunta_old.texto[:50]}...")
        else:
            print(f"ℹ️  Evaluación ya existe: {eval_old.titulo}")

def main():
    print("🚀 Iniciando migración de evaluaciones...")
    print("=" * 50)
    
    # Crear tipos de evaluación
    print("📝 Creando tipos de evaluación...")
    crear_tipos_evaluacion()
    
    print("\n" + "=" * 50)
    
    # Migrar evaluaciones existentes
    print("🔄 Migrando evaluaciones existentes...")
    migrar_evaluaciones()
    
    print("\n" + "=" * 50)
    print("✅ Migración completada exitosamente!")
    
    # Mostrar estadísticas
    print(f"📊 Estadísticas finales:")
    print(f"  - Tipos de evaluación: {TipoEvaluacion.objects.count()}")
    print(f"  - Evaluaciones totales: {Evaluacion.objects.count()}")
    print(f"  - Preguntas totales: {PreguntaEvaluacion.objects.count()}")

if __name__ == "__main__":
    main()
