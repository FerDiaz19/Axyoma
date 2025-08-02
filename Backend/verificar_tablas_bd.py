#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
🗄️ VERIFICADOR DE TABLAS EN BASE DE DATOS
========================================
Muestra en qué tablas están las preguntas oficiales
"""

import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')
django.setup()

from apps.evaluaciones.models_oficiales import EvaluacionOficial, SeccionOficial, PreguntaOficial
from django.db import connection

def verificar_tablas():
    """Verificar tablas en la base de datos"""
    print("🗄️ TABLAS DE EVALUACIONES OFICIALES EN LA BASE DE DATOS")
    print("=" * 70)
    
    # Obtener nombres de tablas desde los modelos
    evaluacion_table = EvaluacionOficial._meta.db_table
    seccion_table = SeccionOficial._meta.db_table
    pregunta_table = PreguntaOficial._meta.db_table
    
    print(f"📋 TABLA DE EVALUACIONES: {evaluacion_table}")
    print(f"📂 TABLA DE SECCIONES: {seccion_table}")
    print(f"❓ TABLA DE PREGUNTAS: {pregunta_table}")
    print()
    
    # Verificar contenido de cada tabla
    print("📊 CONTENIDO DE LAS TABLAS:")
    print("-" * 50)
    
    # Evaluaciones Oficiales
    evaluaciones = EvaluacionOficial.objects.all()
    print(f"1️⃣ TABLA: {evaluacion_table}")
    print(f"   📈 Total registros: {evaluaciones.count()}")
    for eval in evaluaciones:
        print(f"   • ID: {eval.id} | Tipo: {eval.tipo_norma} | Nombre: {eval.nombre}")
    print()
    
    # Secciones Oficiales
    secciones = SeccionOficial.objects.all()
    print(f"2️⃣ TABLA: {seccion_table}")
    print(f"   📈 Total registros: {secciones.count()}")
    for seccion in secciones[:5]:  # Solo mostrar las primeras 5
        print(f"   • ID: {seccion.id} | Orden: {seccion.numero_orden} | Nombre: {seccion.nombre[:50]}...")
    if secciones.count() > 5:
        print(f"   ... y {secciones.count() - 5} secciones más")
    print()
    
    # Preguntas Oficiales
    preguntas = PreguntaOficial.objects.all()
    print(f"3️⃣ TABLA: {pregunta_table}")
    print(f"   📈 Total registros: {preguntas.count()}")
    
    # Agrupar preguntas por normativa
    for evaluacion in evaluaciones:
        preguntas_normativa = PreguntaOficial.objects.filter(seccion__evaluacion_oficial=evaluacion)
        print(f"   🔹 {evaluacion.tipo_norma}: {preguntas_normativa.count()} preguntas")
        
        # Mostrar algunas preguntas de ejemplo
        for pregunta in preguntas_normativa[:3]:
            texto_corto = pregunta.texto_pregunta[:60] + "..." if len(pregunta.texto_pregunta) > 60 else pregunta.texto_pregunta
            print(f"     • ID: {pregunta.id} | Orden: {pregunta.numero_orden} | {texto_corto}")
        
        if preguntas_normativa.count() > 3:
            print(f"     ... y {preguntas_normativa.count() - 3} preguntas más")
        print()
    
    print("🔍 ESTRUCTURA DE DATOS:")
    print("-" * 50)
    print("📋 EvaluacionOficial (evaluaciones_oficiales)")
    print("   ├── id, nombre, tipo_norma, descripcion, activa")
    print("   └── relacionada con SeccionOficial")
    print()
    print("📂 SeccionOficial (secciones_oficiales)")
    print("   ├── id, nombre, numero_orden, evaluacion_oficial_id")
    print("   └── relacionada con PreguntaOficial")
    print()
    print("❓ PreguntaOficial (preguntas_oficiales)")
    print("   ├── id, numero_orden, texto_pregunta, tipo_pregunta")
    print("   ├── opciones_respuesta, es_obligatoria, seccion_id")
    print("   └── contiene las preguntas reales de NOM-030 y NOM-035")
    print()
    
    # Verificar integridad referencial
    print("🔗 VERIFICACIÓN DE INTEGRIDAD:")
    print("-" * 50)
    
    total_evaluaciones = EvaluacionOficial.objects.count()
    total_secciones = SeccionOficial.objects.count()
    total_preguntas = PreguntaOficial.objects.count()
    
    secciones_sin_evaluacion = SeccionOficial.objects.filter(evaluacion_oficial__isnull=True).count()
    preguntas_sin_seccion = PreguntaOficial.objects.filter(seccion__isnull=True).count()
    
    print(f"✅ Evaluaciones: {total_evaluaciones}")
    print(f"✅ Secciones: {total_secciones} (sin evaluación: {secciones_sin_evaluacion})")
    print(f"✅ Preguntas: {total_preguntas} (sin sección: {preguntas_sin_seccion})")
    
    if secciones_sin_evaluacion == 0 and preguntas_sin_seccion == 0:
        print("🎉 ¡Integridad de datos PERFECTA!")
    else:
        print("⚠️ Hay algunos registros huérfanos")

def mostrar_consulta_sql():
    """Mostrar consultas SQL para acceder directamente"""
    print("\n" + "=" * 70)
    print("🔧 CONSULTAS SQL DIRECTAS:")
    print("-" * 50)
    
    print("-- Ver todas las evaluaciones oficiales")
    print("SELECT * FROM evaluaciones_oficiales;")
    print()
    
    print("-- Ver todas las secciones con sus evaluaciones")
    print("""SELECT s.id, s.nombre as seccion, s.numero_orden, 
       e.tipo_norma, e.nombre as evaluacion
FROM secciones_oficiales s 
JOIN evaluaciones_oficiales e ON s.evaluacion_oficial_id = e.id
ORDER BY e.tipo_norma, s.numero_orden;""")
    print()
    
    print("-- Ver todas las preguntas de NOM-035")
    print("""SELECT p.id, p.numero_orden, p.texto_pregunta, p.tipo_pregunta,
       s.nombre as seccion, e.tipo_norma
FROM preguntas_oficiales p
JOIN secciones_oficiales s ON p.seccion_id = s.id
JOIN evaluaciones_oficiales e ON s.evaluacion_oficial_id = e.id
WHERE e.tipo_norma = 'NOM-035'
ORDER BY p.numero_orden;""")
    print()
    
    print("-- Contar preguntas por normativa")
    print("""SELECT e.tipo_norma, COUNT(p.id) as total_preguntas
FROM evaluaciones_oficiales e
JOIN secciones_oficiales s ON e.id = s.evaluacion_oficial_id
JOIN preguntas_oficiales p ON s.id = p.seccion_id
GROUP BY e.tipo_norma;""")

if __name__ == "__main__":
    verificar_tablas()
    mostrar_consulta_sql()
