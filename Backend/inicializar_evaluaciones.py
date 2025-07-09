#!/usr/bin/env python
"""
Script para inicializar los datos base de evaluaciones
según la estructura SQL original
"""

import os
import sys
import django

# Configurar Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')
django.setup()

from apps.surveys.models_new import (
    TipoEvaluacion, ConjuntoOpciones, OpcionConjunto
)

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

def crear_conjuntos_opciones():
    """
    Crear conjuntos de opciones predefinidos
    """
    # Conjunto Likert 5-Puntos
    conjunto_likert, created = ConjuntoOpciones.objects.get_or_create(
        nombre='Likert 5-Puntos (Acuerdo)',
        defaults={
            'descripcion': 'Escala estándar de 5 puntos para preguntas de acuerdo/desacuerdo.',
            'predefinido': True
        }
    )
    
    if created:
        print("✅ Conjunto Likert 5-Puntos creado")
        opciones_likert = [
            ('Totalmente en desacuerdo', 1, 1, 1),
            ('En desacuerdo', 2, 2, 2),
            ('Ni de acuerdo ni en desacuerdo', 3, 3, 3),
            ('De acuerdo', 4, 4, 4),
            ('Totalmente de acuerdo', 5, 5, 5),
        ]
        
        for texto, valor_num, puntuaje, orden in opciones_likert:
            OpcionConjunto.objects.create(
                conjunto_opciones=conjunto_likert,
                texto_opcion=texto,
                valor_numerico=valor_num,
                puntuaje_escala=puntuaje,
                numero_orden=orden
            )
            print(f"  ✅ Opción creada: {texto}")
    
    # Conjunto Sí/No
    conjunto_sino, created = ConjuntoOpciones.objects.get_or_create(
        nombre='Sí/No',
        defaults={
            'descripcion': 'Opciones de respuesta Sí o No.',
            'predefinido': True
        }
    )
    
    if created:
        print("✅ Conjunto Sí/No creado")
        opciones_sino = [
            ('Sí', True, 1),
            ('No', False, 2),
        ]
        
        for texto, valor_bool, orden in opciones_sino:
            OpcionConjunto.objects.create(
                conjunto_opciones=conjunto_sino,
                texto_opcion=texto,
                valor_booleano=valor_bool,
                numero_orden=orden
            )
            print(f"  ✅ Opción creada: {texto}")
    
    # Conjunto Nivel de Satisfacción
    conjunto_satisfaccion, created = ConjuntoOpciones.objects.get_or_create(
        nombre='Nivel de Satisfacción',
        defaults={
            'descripcion': 'Escala de 1 a 10 para medir satisfacción.',
            'predefinido': False
        }
    )
    
    if created:
        print("✅ Conjunto Nivel de Satisfacción creado")
        opciones_satisfaccion = [
            ('1 - Muy Insatisfecho', 1, 1, 1),
            ('5 - Neutro', 5, 5, 2),
            ('10 - Muy Satisfecho', 10, 10, 3),
        ]
        
        for texto, valor_num, puntuaje, orden in opciones_satisfaccion:
            OpcionConjunto.objects.create(
                conjunto_opciones=conjunto_satisfaccion,
                texto_opcion=texto,
                valor_numerico=valor_num,
                puntuaje_escala=puntuaje,
                numero_orden=orden
            )
            print(f"  ✅ Opción creada: {texto}")

def main():
    print("🚀 Inicializando datos base de evaluaciones...")
    print("=" * 50)
    
    # Crear tipos de evaluación
    print("📝 Creando tipos de evaluación...")
    crear_tipos_evaluacion()
    
    print("\n" + "=" * 50)
    
    # Crear conjuntos de opciones
    print("📋 Creando conjuntos de opciones...")
    crear_conjuntos_opciones()
    
    print("\n" + "=" * 50)
    print("✅ Inicialización completada exitosamente!")
    
    # Mostrar estadísticas
    print(f"📊 Estadísticas finales:")
    print(f"  - Tipos de evaluación: {TipoEvaluacion.objects.count()}")
    print(f"  - Conjuntos de opciones: {ConjuntoOpciones.objects.count()}")
    print(f"  - Opciones totales: {OpcionConjunto.objects.count()}")

if __name__ == "__main__":
    main()
