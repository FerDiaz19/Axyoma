#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
🔍 VERIFICADOR DE PREGUNTAS OFICIALES
===================================
Script para verificar que las preguntas oficiales se cargaron correctamente
"""

import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')
django.setup()

from apps.evaluaciones.models_oficiales import EvaluacionOficial, SeccionOficial, PreguntaOficial

def verificar_preguntas():
    """Verificar todas las preguntas cargadas"""
    print("🔍 VERIFICANDO PREGUNTAS OFICIALES CARGADAS")
    print("=" * 60)
    
    # Obtener evaluaciones
    evaluaciones = EvaluacionOficial.objects.all()
    
    for evaluacion in evaluaciones:
        print(f"\n📋 {evaluacion.tipo_norma}: {evaluacion.nombre}")
        print(f"   📝 Descripción: {evaluacion.descripcion}")
        print(f"   ⏱️  Tiempo límite: {evaluacion.tiempo_limite} minutos")
        print(f"   ✅ Activa: {evaluacion.activa}")
        
        secciones = evaluacion.secciones.all().order_by('numero_orden')
        print(f"   📊 Total secciones: {secciones.count()}")
        
        total_preguntas = 0
        for seccion in secciones:
            preguntas_count = seccion.preguntas.count()
            total_preguntas += preguntas_count
            print(f"     └─ {seccion.numero_orden:2d}. {seccion.nombre} ({preguntas_count} preguntas)")
            
            # Mostrar algunas preguntas de ejemplo
            preguntas = seccion.preguntas.all()[:2]  # Solo las primeras 2
            for pregunta in preguntas:
                texto_corto = pregunta.texto_pregunta[:60] + "..." if len(pregunta.texto_pregunta) > 60 else pregunta.texto_pregunta
                print(f"        • {pregunta.numero_orden:2d}. {texto_corto}")
                print(f"          Tipo: {pregunta.tipo_pregunta}, Opciones: {len(pregunta.opciones_respuesta)}")
        
        print(f"   ❓ Total preguntas: {total_preguntas}")
    
    print("\n" + "=" * 60)
    print("📈 RESUMEN GENERAL:")
    print(f"   📋 Evaluaciones oficiales: {EvaluacionOficial.objects.count()}")
    print(f"   📊 Secciones oficiales: {SeccionOficial.objects.count()}")
    print(f"   ❓ Preguntas oficiales: {PreguntaOficial.objects.count()}")

def mostrar_preguntas_detalladas(tipo_norma):
    """Mostrar todas las preguntas de una normativa específica"""
    try:
        evaluacion = EvaluacionOficial.objects.get(tipo_norma=tipo_norma)
        print(f"\n🔍 PREGUNTAS DETALLADAS - {tipo_norma}")
        print("=" * 60)
        
        secciones = evaluacion.secciones.all().order_by('numero_orden')
        
        for seccion in secciones:
            print(f"\n📂 SECCIÓN {seccion.numero_orden}: {seccion.nombre}")
            print(f"   📝 {seccion.descripcion}")
            print("   " + "-" * 50)
            
            preguntas = seccion.preguntas.all().order_by('numero_orden')
            
            for pregunta in preguntas:
                print(f"\n   ❓ Pregunta {pregunta.numero_orden}:")
                print(f"      📄 {pregunta.texto_pregunta}")
                print(f"      🔧 Tipo: {pregunta.tipo_pregunta}")
                print(f"      📋 Opciones: {', '.join(pregunta.opciones_respuesta)}")
                print(f"      ⚠️  Obligatoria: {'Sí' if pregunta.es_obligatoria else 'No'}")
                
    except EvaluacionOficial.DoesNotExist:
        print(f"❌ No se encontró la evaluación {tipo_norma}")

def main():
    """Función principal"""
    print("🚀 INICIANDO VERIFICACIÓN")
    
    # Verificación general
    verificar_preguntas()
    
    # Mostrar menú para detalles
    print("\n" + "=" * 60)
    print("¿Deseas ver preguntas detalladas de alguna normativa?")
    print("1. NOM-035 (Factores de Riesgo Psicosocial)")
    print("2. NOM-030 (Servicios Preventivos)")
    print("3. Salir")
    
    try:
        opcion = input("\nSelecciona una opción (1-3): ").strip()
        
        if opcion == "1":
            mostrar_preguntas_detalladas("NOM-035")
        elif opcion == "2":
            mostrar_preguntas_detalladas("NOM-030")
        elif opcion == "3":
            print("👋 ¡Hasta luego!")
        else:
            print("❌ Opción no válida")
            
    except KeyboardInterrupt:
        print("\n👋 ¡Hasta luego!")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
