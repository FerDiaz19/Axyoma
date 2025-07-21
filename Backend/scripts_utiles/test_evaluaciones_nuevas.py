#!/usr/bin/env python
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')
django.setup()

from django.contrib.auth.models import User
from apps.users.models import PerfilUsuario, Empresa, Empleado
from apps.evaluaciones.models import EvaluacionCompleta, AsignacionEvaluacion, TipoEvaluacion
from datetime import datetime, timedelta
from django.utils import timezone

def crear_evaluaciones_test():
    """Crear múltiples evaluaciones NOM-030 para probar identificadores únicos"""
    print('=== CREANDO EVALUACIONES DE PRUEBA ===')
    
    # Obtener empresa CodeWave
    empresa = Empresa.objects.get(nombre='CodeWave Technologies')
    admin_user = User.objects.get(username='admin_empresa')
    
    # Obtener tipo de evaluación NOM-030
    tipo_nom030 = TipoEvaluacion.objects.get(nombre='NOM-030')
    
    # Crear múltiples evaluaciones NOM-030
    evaluaciones_nom030 = [
        {
            'titulo': 'NOM-030 - Evaluación Q1 2025',
            'descripcion': 'Evaluación de servicios preventivos de seguridad - Primer trimestre 2025'
        },
        {
            'titulo': 'NOM-030 - Evaluación Planta Norte',
            'descripcion': 'Evaluación específica para empleados de la planta norte'
        },
        {
            'titulo': 'NOM-030 - Evaluación Supervisores',
            'descripcion': 'Evaluación enfocada en personal de supervisión'
        }
    ]
    
    evaluaciones_creadas = []
    
    for eval_data in evaluaciones_nom030:
        evaluacion = EvaluacionCompleta.objects.create(
            titulo=eval_data['titulo'],
            descripcion=eval_data['descripcion'],
            tipo_evaluacion=tipo_nom030,
            empresa=empresa,
            estado='activa',
            fecha_inicio=timezone.now(),
            fecha_fin=timezone.now() + timedelta(days=30),
            creada_por=admin_user,
            es_anonima=True
        )
        evaluaciones_creadas.append(evaluacion)
        print(f'✅ Creada: {evaluacion.titulo} - ID: {evaluacion.id}')
    
    print(f'\n=== EVALUACIONES NOM-030 DISPONIBLES ===')
    todas_nom030 = EvaluacionCompleta.objects.filter(tipo_evaluacion=tipo_nom030)
    for eval in todas_nom030:
        identificador = f"{eval.tipo_evaluacion.nombre}-{eval.id}-{eval.fecha_creacion.strftime('%Y%m%d')}"
        print(f'ID: {eval.id} | {eval.titulo}')
        print(f'  Identificador único: {identificador}')
        print(f'  Estado: {eval.estado}')
        print(f'  Fecha creación: {eval.fecha_creacion}')
        print()
    
    return evaluaciones_creadas

def asignar_empleados_test():
    """Asignar empleados a las evaluaciones para pruebas"""
    print('=== ASIGNANDO EMPLEADOS A EVALUACIONES ===')
    
    # Obtener empleados - usar planta en lugar de empresa
    empleados = Empleado.objects.all()[:3]  # Tomar cualquier empleado disponible
    admin_user = User.objects.get(username='admin_empresa')
    
    if not empleados:
        print('❌ No hay empleados disponibles')
        return
    
    # Obtener evaluaciones activas
    evaluaciones = EvaluacionCompleta.objects.filter(estado='activa')
    
    for evaluacion in evaluaciones:
        print(f'\nAsignando empleados a: {evaluacion.titulo}')
        
        for i, empleado in enumerate(empleados):
            # Crear asignación con duración
            asignacion, created = AsignacionEvaluacion.objects.get_or_create(
                evaluacion=evaluacion,
                empleado=empleado,
                defaults={
                    'fecha_inicio': timezone.now(),
                    'fecha_fin': timezone.now() + timedelta(days=15),
                    'asignado_por': admin_user,
                    'estado': 'pendiente',
                    'duracion_dias': 15,
                    'duracion_horas': 2,
                    'instrucciones_especiales': f'Esta evaluación debe completarse en un plazo máximo de 15 días. Tiempo estimado: 2 horas.'
                }
            )
            
            if created:
                print(f'  ✅ {empleado.nombre} asignado - Duración: {asignacion.duracion_dias} días')
            else:
                print(f'  ⚠️  {empleado.nombre} ya estaba asignado')

def mostrar_estadisticas():
    """Mostrar estadísticas de las evaluaciones"""
    print('\n=== ESTADÍSTICAS DE EVALUACIONES ===')
    
    evaluaciones = EvaluacionCompleta.objects.all()
    
    for evaluacion in evaluaciones:
        asignaciones = evaluacion.asignaciones.all()
        print(f'\n📊 {evaluacion.titulo}')
        print(f'   ID: {evaluacion.id}')
        print(f'   Tipo: {evaluacion.tipo_evaluacion.nombre}')
        print(f'   Total empleados asignados: {asignaciones.count()}')
        
        # Estadísticas por estado
        estados = {}
        for asignacion in asignaciones:
            estados[asignacion.estado] = estados.get(asignacion.estado, 0) + 1
        
        for estado, count in estados.items():
            print(f'   - {estado}: {count}')

if __name__ == '__main__':
    try:
        crear_evaluaciones_test()
        asignar_empleados_test()
        mostrar_estadisticas()
        print('\n✅ Script de prueba completado exitosamente')
    except Exception as e:
        print(f'❌ Error: {e}')
        import traceback
        traceback.print_exc()
