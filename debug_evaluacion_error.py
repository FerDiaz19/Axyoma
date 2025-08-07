#!/usr/bin/env python3

"""
Script de debug para identificar el problema con el error 400 al actualizar evaluaciones
"""

import os
import sys
import django
import json
from datetime import datetime

# Configurar el entorno de Django
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'Backend'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.evaluaciones.models import *
from apps.evaluaciones.serializers import *
from apps.users.models import *

def test_evaluacion_update():
    print("=== Debug del Error 400 en Evaluaciones ===")
    
    # Intentar obtener la evaluación con ID 1
    try:
        evaluacion = Evaluacion.objects.get(evaluacion_id=1)
        print(f"✅ Evaluación encontrada: {evaluacion.titulo}")
        print(f"   - Tipo: {evaluacion.tipo_evaluacion}")
        print(f"   - Empresa: {evaluacion.empresa}")
        print(f"   - Estado: {evaluacion.estado}")
        print(f"   - Secciones: {evaluacion.secciones.count()}")
        
        # Serializar la evaluación actual
        serializer = EvaluacionSerializer(evaluacion)
        current_data = serializer.data
        print(f"\n📋 Datos actuales de la evaluación:")
        print(json.dumps(current_data, indent=2, ensure_ascii=False, default=str))
        
        # Simular una actualización simple
        update_data = {
            'titulo': evaluacion.titulo,
            'descripcion': evaluacion.descripcion or '',
            'instrucciones': evaluacion.instrucciones or '',
            'contenido_informativo': evaluacion.contenido_informativo or '',
            'tiempo_limite': evaluacion.tiempo_limite,
            'umbral_aprobacion': evaluacion.umbral_aprobacion,
            'estado': evaluacion.estado,
            'tipo_evaluacion_id': evaluacion.tipo_evaluacion.tipo_evaluacion_id,
            'empresa_id': evaluacion.empresa.empresa_id if evaluacion.empresa else None,
            'creado_por_id': evaluacion.creado_por.user_id if evaluacion.creado_por else None,
            'secciones': []
        }
        
        # Agregar las secciones existentes
        for seccion in evaluacion.secciones.all():
            seccion_data = {
                'seccion_id': seccion.seccion_id,
                'nombre': seccion.nombre,
                'descripcion': seccion.descripcion or '',
                'numero_orden': seccion.numero_orden,
                'es_evaluable': seccion.es_evaluable,
                'preguntas_seccion': []
            }
            
            for pregunta_seccion in seccion.preguntas_seccion.all():
                pregunta_data = {
                    'seccion_pregunta_id': pregunta_seccion.seccion_pregunta_id,
                    'pregunta': {
                        'pregunta_id': pregunta_seccion.pregunta.pregunta_id,
                        'texto_pregunta': pregunta_seccion.pregunta.texto_pregunta,
                        'tipo_pregunta': pregunta_seccion.pregunta.tipo_pregunta,
                        'es_obligatoria': pregunta_seccion.pregunta.es_obligatoria,
                        'pregunta_padre': pregunta_seccion.pregunta.pregunta_padre,
                        'activador_padre': pregunta_seccion.pregunta.activador_padre
                    },
                    'numero_orden': pregunta_seccion.numero_orden,
                    'conjunto_respuestas': None,
                    'respuesta_correcta': None
                }
                
                if pregunta_seccion.conjunto_respuestas:
                    pregunta_data['conjunto_respuestas'] = {
                        'conjunto_id': pregunta_seccion.conjunto_respuestas.conjunto_id,
                        'nombre': pregunta_seccion.conjunto_respuestas.nombre,
                        'descripcion': pregunta_seccion.conjunto_respuestas.descripcion,
                        'predefinido': pregunta_seccion.conjunto_respuestas.predefinido,
                        'opciones': [
                            {
                                'opcion_conjunto_id': op.opcion_conjunto_id,
                                'texto_opcion': op.texto_opcion,
                                'valor_booleano': op.valor_booleano,
                                'valor_numerico': op.valor_numerico,
                                'valor_decimal': op.valor_decimal,
                                'numero_orden': op.numero_orden
                            } for op in pregunta_seccion.conjunto_respuestas.opciones.all()
                        ]
                    }
                
                if pregunta_seccion.respuesta_correcta:
                    pregunta_data['respuesta_correcta'] = {
                        'opcion_conjunto_id': pregunta_seccion.respuesta_correcta.opcion_conjunto_id,
                        'texto_opcion': pregunta_seccion.respuesta_correcta.texto_opcion,
                        'valor_booleano': pregunta_seccion.respuesta_correcta.valor_booleano,
                        'valor_numerico': pregunta_seccion.respuesta_correcta.valor_numerico,
                        'valor_decimal': pregunta_seccion.respuesta_correcta.valor_decimal,
                        'numero_orden': pregunta_seccion.respuesta_correcta.numero_orden
                    }
                
                seccion_data['preguntas_seccion'].append(pregunta_data)
            
            update_data['secciones'].append(seccion_data)
        
        print(f"\n📤 Datos para actualización:")
        print(json.dumps(update_data, indent=2, ensure_ascii=False, default=str))
        
        # Intentar validar con el serializer
        print(f"\n🔍 Validando con serializer...")
        serializer = EvaluacionSerializer(evaluacion, data=update_data)
        
        if serializer.is_valid():
            print("✅ Serializer válido")
            # No guardamos realmente, solo validamos
            # serializer.save()
        else:
            print("❌ Errores de validación:")
            print(json.dumps(serializer.errors, indent=2, ensure_ascii=False))
        
    except Evaluacion.DoesNotExist:
        print("❌ Evaluación con ID 1 no encontrada")
    except Exception as e:
        print(f"❌ Error inesperado: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    test_evaluacion_update()
