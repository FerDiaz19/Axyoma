#!/usr/bin/env python
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')
django.setup()

from django.contrib.auth.models import User
from apps.users.models import PerfilUsuario, Empresa
from django.db import transaction

def fix_all_users_final():
    """Arreglar TODOS los usuarios sin empresa"""
    print('=== ARREGLO FINAL DE USUARIOS ===')
    
    # Obtener empresa CodeWave
    empresa = Empresa.objects.filter(nombre='CodeWave Technologies').first()
    if not empresa:
        print('❌ No se encontró la empresa CodeWave Technologies')
        return
    
    print(f'✅ Empresa encontrada: {empresa.nombre} (PK: {empresa.pk})')
    
    # Obtener todos los usuarios con perfil
    usuarios_con_perfil = User.objects.filter(perfil__isnull=False)
    print(f'Total usuarios con perfil: {usuarios_con_perfil.count()}')
    
    usuarios_arreglados = 0
    
    for user in usuarios_con_perfil:
        print(f'\nRevisando usuario: {user.username}')
        perfil = user.perfil
        
        # Verificar si tiene empresa de forma segura
        tiene_empresa = False
        try:
            empresa_actual = perfil.empresa
            if empresa_actual:
                print(f'  ✅ Ya tiene empresa: {empresa_actual.nombre}')
                tiene_empresa = True
        except Exception:
            print('  ❌ Sin empresa asignada')
        
        # Si no tiene empresa, asignarla
        if not tiene_empresa:
            try:
                with transaction.atomic():
                    perfil.empresa = empresa
                    perfil.save()
                    print(f'  ✅ Empresa {empresa.nombre} asignada')
                    usuarios_arreglados += 1
            except Exception as e:
                print(f'  ❌ Error al asignar empresa: {e}')
    
    print(f'\n=== RESUMEN ===')
    print(f'Usuarios arreglados: {usuarios_arreglados}')
    
    # Verificar evaluaciones sin empresa
    print('\n=== VERIFICANDO EVALUACIONES ===')
    from apps.evaluaciones.models import EvaluacionCompleta
    
    evaluaciones_sin_empresa = EvaluacionCompleta.objects.filter(empresa__isnull=True)
    print(f'Evaluaciones sin empresa: {evaluaciones_sin_empresa.count()}')
    
    for eval in evaluaciones_sin_empresa:
        print(f'  - ID {eval.pk}: {eval.titulo}')
        # Asignar empresa a evaluaciones que no la tengan
        eval.empresa = empresa
        eval.save()
        print(f'    ✅ Empresa asignada')

if __name__ == '__main__':
    fix_all_users_final()
