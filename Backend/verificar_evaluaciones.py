#!/usr/bin/env python
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')
django.setup()

from apps.evaluaciones.models import EvaluacionCompleta, TipoEvaluacion
from apps.users.models import Empresa

def verificar_evaluaciones():
    """Verificar evaluaciones disponibles en el sistema"""
    print('🔍 VERIFICANDO EVALUACIONES DISPONIBLES')
    print('=' * 50)
    
    # Verificar tipos de evaluación
    tipos = TipoEvaluacion.objects.all()
    print(f'📋 Tipos de evaluación disponibles: {tipos.count()}')
    for tipo in tipos:
        print(f'   - {tipo.nombre}: {tipo.descripcion[:50]}...')
    
    # Verificar evaluaciones completas
    evaluaciones = EvaluacionCompleta.objects.all()
    print(f'\n📊 Evaluaciones completas: {evaluaciones.count()}')
    
    for evaluacion in evaluaciones:
        print(f'\n🎯 ID: {evaluacion.id} | {evaluacion.titulo}')
        print(f'   Tipo: {evaluacion.tipo_evaluacion.nombre}')
        print(f'   Estado: {evaluacion.estado}')
        print(f'   Empresa: {evaluacion.empresa.nombre if evaluacion.empresa else "Sin empresa"}')
        print(f'   Fecha creación: {evaluacion.fecha_creacion}')
        print(f'   Creada por: {evaluacion.creada_por.username}')
        
        # Verificar asignaciones
        asignaciones = evaluacion.asignaciones.count()
        print(f'   Asignaciones: {asignaciones}')
    
    # Verificar empresas
    print(f'\n🏢 Empresas disponibles: {Empresa.objects.count()}')
    for empresa in Empresa.objects.all():
        print(f'   - {empresa.nombre}')
        evaluaciones_empresa = EvaluacionCompleta.objects.filter(empresa=empresa)
        print(f'     Evaluaciones: {evaluaciones_empresa.count()}')

if __name__ == '__main__':
    verificar_evaluaciones()
