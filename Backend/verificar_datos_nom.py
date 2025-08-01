# -*- coding: utf-8 -*-
"""
Script para verificar datos existentes en las evaluaciones oficiales
"""

from django.contrib.auth import get_user_model
from apps.evaluaciones.models_oficiales import (
    EvaluacionOficial, SeccionOficial, PreguntaOficial,
    AsignacionEvaluacion, EmpleadoAsignado, RespuestaEmpleado
)

User = get_user_model()

print("🔍 VERIFICANDO DATOS EN BASE DE DATOS")
print("=" * 60)

# Verificar evaluaciones oficiales
evaluaciones = EvaluacionOficial.objects.all()
print(f"\n📊 EVALUACIONES OFICIALES ({evaluaciones.count()}):")
for eval_obj in evaluaciones:
    print(f"   - {eval_obj.tipo_norma}: {eval_obj.nombre}")
    print(f"     Activa: {eval_obj.activa}")
    print(f"     Fecha creación: {eval_obj.fecha_creacion}")

# Verificar secciones
secciones = SeccionOficial.objects.all()
print(f"\n📋 SECCIONES OFICIALES ({secciones.count()}):")
for seccion in secciones:
    print(f"   - {seccion.evaluacion_oficial.tipo_norma}: {seccion.nombre}")
    print(f"     Orden: {seccion.numero_orden}")

# Verificar preguntas
preguntas = PreguntaOficial.objects.all()
print(f"\n❓ PREGUNTAS OFICIALES ({preguntas.count()}):")
for pregunta in preguntas:
    print(f"   - {pregunta.seccion.evaluacion_oficial.tipo_norma}: {pregunta.texto_pregunta[:50]}...")
    print(f"     Tipo: {pregunta.tipo_pregunta}, Obligatoria: {pregunta.es_obligatoria}")

# Verificar asignaciones
asignaciones = AsignacionEvaluacion.objects.all()
print(f"\n📅 ASIGNACIONES ({asignaciones.count()}):")
for asignacion in asignaciones:
    print(f"   - {asignacion.evaluacion_oficial.nombre}")

# Verificar empleados asignados
empleados_asignados = EmpleadoAsignado.objects.all()
print(f"\n👥 EMPLEADOS ASIGNADOS ({empleados_asignados.count()}):")

# Verificar respuestas
respuestas = RespuestaEmpleado.objects.all()
print(f"\n💬 RESPUESTAS ({respuestas.count()}):")

# Verificar si hay datos específicos de NOM-030
nom030_evaluaciones = EvaluacionOficial.objects.filter(tipo_norma='NOM-030')
print(f"\n🔍 ESPECÍFICO NOM-030:")
print(f"   Evaluaciones NOM-030: {nom030_evaluaciones.count()}")

if nom030_evaluaciones.exists():
    for eval_030 in nom030_evaluaciones:
        print(f"   - {eval_030.nombre}")
        secciones_030 = eval_030.secciones.all()
        print(f"     Secciones: {secciones_030.count()}")
        for seccion in secciones_030:
            preguntas_seccion = seccion.preguntas.all()
            print(f"       - {seccion.nombre}: {preguntas_seccion.count()} preguntas")
else:
    print("   ⚠️ No se encontraron evaluaciones NOM-030")

print("\n" + "=" * 60)
print("✅ Verificación completada")

# Crear datos básicos de NOM-030 si no existen
if not nom030_evaluaciones.exists():
    print("\n🔧 CREANDO DATOS BÁSICOS NOM-030...")
    
    # Crear evaluación NOM-030
    evaluacion_030 = EvaluacionOficial.objects.create(
        tipo_norma='NOM-030',
        nombre='Evaluación NOM-030 Oficial',
        descripcion='Evaluación oficial de servicios preventivos de seguridad y salud en el trabajo',
        instrucciones='Complete todas las secciones relacionadas con los servicios preventivos.',
        tiempo_limite=45,  # 45 minutos
        activa=True
    )
    print(f"✅ Evaluación NOM-030 creada: {evaluacion_030.nombre}")
    
    # Crear secciones básicas NOM-030
    seccion1_030 = SeccionOficial.objects.create(
        evaluacion_oficial=evaluacion_030,
        numero_orden=1,
        nombre='Servicios Preventivos',
        descripcion='Evaluación de servicios preventivos disponibles'
    )
    
    seccion2_030 = SeccionOficial.objects.create(
        evaluacion_oficial=evaluacion_030,
        numero_orden=2,
        nombre='Capacitación y Entrenamiento',
        descripcion='Evaluación de programas de capacitación'
    )
    
    print(f"✅ Secciones NOM-030 creadas: {seccion1_030.nombre}, {seccion2_030.nombre}")
    
    # Crear preguntas básicas NOM-030
    pregunta1_030 = PreguntaOficial.objects.create(
        seccion=seccion1_030,
        numero_orden=1,
        texto_pregunta='¿La empresa cuenta con servicios preventivos de seguridad y salud?',
        tipo_pregunta='Si/No',
        es_obligatoria=True
    )
    
    pregunta2_030 = PreguntaOficial.objects.create(
        seccion=seccion1_030,
        numero_orden=2,
        texto_pregunta='¿Qué tipo de servicios preventivos considera más importantes?',
        tipo_pregunta='Múltiple',
        opciones_respuesta=[
            'Medicina del trabajo',
            'Higiene industrial', 
            'Seguridad en el trabajo',
            'Ergonomía',
            'Psicosociología aplicada'
        ],
        es_obligatoria=True
    )
    
    pregunta3_030 = PreguntaOficial.objects.create(
        seccion=seccion2_030,
        numero_orden=1,
        texto_pregunta='¿Con qué frecuencia recibe capacitación en seguridad?',
        tipo_pregunta='Múltiple',
        opciones_respuesta=[
            'Mensual',
            'Trimestral',
            'Semestral',
            'Anual',
            'Nunca'
        ],
        es_obligatoria=True
    )
    
    print(f"✅ Preguntas NOM-030 creadas: {PreguntaOficial.objects.filter(seccion__evaluacion_oficial=evaluacion_030).count()}")
    
    print("\n🎉 Datos NOM-030 inicializados correctamente!")

print(f"\n📊 RESUMEN FINAL:")
print(f"   - Evaluaciones totales: {EvaluacionOficial.objects.count()}")
print(f"   - Evaluaciones NOM-035: {EvaluacionOficial.objects.filter(tipo_norma='NOM-035').count()}")
print(f"   - Evaluaciones NOM-030: {EvaluacionOficial.objects.filter(tipo_norma='NOM-030').count()}")
print(f"   - Secciones totales: {SeccionOficial.objects.count()}")
print(f"   - Preguntas totales: {PreguntaOficial.objects.count()}")
