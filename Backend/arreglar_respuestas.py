#!/usr/bin/env python3
"""
Script para arreglar las relaciones entre preguntas y conjuntos de respuestas
que están faltando en la evaluación NOM-035.
"""

import os
import sys
import django

# Configurar Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')
django.setup()

from apps.evaluaciones.models import (
    SeccionPregunta, ConjuntoRespuestas, PosiblesRespuestas, Pregunta
)

def main():
    print("🔧 INICIANDO REPARACIÓN DE RELACIONES PREGUNTA-RESPUESTAS")
    print("=" * 60)
    
    # 1. Verificar estado actual
    total_relaciones = SeccionPregunta.objects.count()
    sin_conjunto = SeccionPregunta.objects.filter(conjunto_respuestas__isnull=True).count()
    
    print(f"📊 Total relaciones SeccionPregunta: {total_relaciones}")
    print(f"❌ Sin conjunto de respuestas: {sin_conjunto}")
    print(f"✅ Con conjunto de respuestas: {total_relaciones - sin_conjunto}")
    print()
    
    # 2. Mostrar conjuntos disponibles
    print("📋 CONJUNTOS DE RESPUESTAS DISPONIBLES:")
    conjuntos = ConjuntoRespuestas.objects.all()
    for conjunto in conjuntos:
        opciones_count = conjunto.opciones.count()
        print(f"  🔸 ID {conjunto.conjunto_id}: {conjunto.nombre} ({opciones_count} opciones)")
    print()
    
    # 3. Buscar conjuntos típicos por nombre
    escala_conjunto = None
    bool_conjunto = None
    multiple_conjunto = None
    
    # Buscar conjunto de escala (normalmente tiene 5 opciones para NOM-035)
    for conjunto in conjuntos:
        if conjunto.opciones.count() == 5 and 'escala' in conjunto.nombre.lower():
            escala_conjunto = conjunto
            break
    
    # Buscar conjunto booleano (normalmente tiene 2 opciones: Sí/No)
    for conjunto in conjuntos:
        if conjunto.opciones.count() == 2:
            bool_conjunto = conjunto
            break
    
    # Buscar conjunto múltiple (puede variar)
    for conjunto in conjuntos:
        if conjunto.opciones.count() > 2 and conjunto.opciones.count() != 5:
            multiple_conjunto = conjunto
            break
    
    print("🎯 CONJUNTOS SELECCIONADOS PARA ASIGNACIÓN:")
    print(f"  📊 Escala: {escala_conjunto.nombre if escala_conjunto else 'NO ENCONTRADO'}")
    print(f"  ✅ Bool: {bool_conjunto.nombre if bool_conjunto else 'NO ENCONTRADO'}")
    print(f"  📝 Múltiple: {multiple_conjunto.nombre if multiple_conjunto else 'NO ENCONTRADO'}")
    print()
    
    if not escala_conjunto or not bool_conjunto:
        print("❌ ERROR: No se encontraron conjuntos adecuados")
        return
    
    # 4. Asignar conjuntos por tipo de pregunta
    print("🔄 ASIGNANDO CONJUNTOS DE RESPUESTAS...")
    
    relaciones_sin_conjunto = SeccionPregunta.objects.filter(conjunto_respuestas__isnull=True)
    
    asignaciones = {"Escala": 0, "Bool": 0, "Múltiple": 0, "Abierta": 0, "Otros": 0}
    
    for relacion in relaciones_sin_conjunto:
        tipo_pregunta = relacion.pregunta.tipo_pregunta
        
        if tipo_pregunta == "Escala":
            relacion.conjunto_respuestas = escala_conjunto
            relacion.save()
            asignaciones["Escala"] += 1
            
        elif tipo_pregunta == "Bool":
            relacion.conjunto_respuestas = bool_conjunto
            relacion.save()
            asignaciones["Bool"] += 1
            
        elif tipo_pregunta == "Múltiple":
            if multiple_conjunto:
                relacion.conjunto_respuestas = multiple_conjunto
                relacion.save()
                asignaciones["Múltiple"] += 1
            else:
                # Fallback: usar el conjunto de escala
                relacion.conjunto_respuestas = escala_conjunto
                relacion.save()
                asignaciones["Múltiple"] += 1
                
        elif tipo_pregunta == "Abierta":
            # Las preguntas abiertas no necesitan conjunto de respuestas
            asignaciones["Abierta"] += 1
            
        else:
            asignaciones["Otros"] += 1
    
    # 5. Mostrar resultados
    print("✅ ASIGNACIÓN COMPLETADA:")
    for tipo, cantidad in asignaciones.items():
        if cantidad > 0:
            print(f"  📝 {tipo}: {cantidad} preguntas")
    
    # 6. Verificar resultado final
    print()
    print("🔍 VERIFICACIÓN FINAL:")
    sin_conjunto_final = SeccionPregunta.objects.filter(conjunto_respuestas__isnull=True).count()
    con_conjunto_final = SeccionPregunta.objects.filter(conjunto_respuestas__isnull=False).count()
    
    print(f"❌ Sin conjunto: {sin_conjunto_final}")
    print(f"✅ Con conjunto: {con_conjunto_final}")
    
    if sin_conjunto_final == 0:
        print("🎉 ¡TODAS LAS PREGUNTAS TIENEN CONJUNTOS DE RESPUESTAS!")
    else:
        print(f"⚠️  Aún quedan {sin_conjunto_final} preguntas sin conjunto")
    
    print("=" * 60)
    print("🏁 REPARACIÓN COMPLETADA")

if __name__ == "__main__":
    main()
