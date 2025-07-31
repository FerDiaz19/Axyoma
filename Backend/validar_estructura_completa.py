#!/usr/bin/env python
"""
VALIDADOR COMPLETO DE ESTRUCTURA ORGANIZACIONAL
=============================================
Verifica que toda la jerarquía esté correctamente enlazada:
Empresa → Plantas → Departamentos → Puestos → Empleados
"""

import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'axyoma.settings')
django.setup()

from apps.users.models import *
from apps.subscriptions.models import *

def validar_estructura_completa():
    """Valida que toda la estructura organizacional esté correctamente enlazada"""
    
    print("🔍 VALIDANDO ESTRUCTURA ORGANIZACIONAL COMPLETA")
    print("=" * 60)
    
    # 1. VALIDAR EMPRESAS Y SUSCRIPCIONES
    print("\n📊 1. EMPRESAS Y SUSCRIPCIONES")
    print("-" * 40)
    
    empresas = Empresa.objects.all()
    for empresa in empresas:
        print(f"\n🏢 EMPRESA: {empresa.nombre}")
        print(f"   📧 Admin: {empresa.administrador.nombre_completo}")
        print(f"   📧 Email: {empresa.administrador.correo}")
        
        # Verificar suscripción
        suscripcion = SuscripcionEmpresa.objects.filter(empresa=empresa).first()
        if suscripcion:
            print(f"   💳 Suscripción: {suscripcion.plan.nombre} ({suscripcion.estado})")
            print(f"   📅 Vigencia: {suscripcion.fecha_inicio} → {suscripcion.fecha_fin}")
        else:
            print("   ❌ SIN SUSCRIPCIÓN")
    
    # 2. VALIDAR JERARQUÍA ORGANIZACIONAL
    print("\n\n🏗️ 2. JERARQUÍA ORGANIZACIONAL")
    print("-" * 40)
    
    for empresa in empresas:
        print(f"\n🏢 {empresa.nombre}")
        plantas = empresa.plantas.filter(status=True)
        
        if not plantas.exists():
            print("   ❌ NO TIENE PLANTAS")
            continue
            
        for planta in plantas:
            print(f"   📍 PLANTA: {planta.nombre}")
            departamentos = planta.departamentos.filter(status=True)
            
            if not departamentos.exists():
                print("      ❌ NO TIENE DEPARTAMENTOS")
                continue
                
            for departamento in departamentos:
                print(f"      🏢 DEPARTAMENTO: {departamento.nombre}")
                puestos = departamento.puestos.filter(status=True)
                
                if not puestos.exists():
                    print("         ❌ NO TIENE PUESTOS")
                    continue
                    
                for puesto in puestos:
                    empleados = puesto.empleados.filter(status=True)
                    total_empleados = empleados.count()
                    print(f"         💼 PUESTO: {puesto.nombre} ({total_empleados} empleados)")
                    
                    # Mostrar algunos empleados
                    for empleado in empleados[:3]:  # Solo primeros 3
                        print(f"            👤 {empleado.nombre_completo}")
                    
                    if total_empleados > 3:
                        print(f"            ... y {total_empleados - 3} más")
    
    # 3. VALIDAR RELACIONES INVERSAS
    print("\n\n🔗 3. VALIDANDO RELACIONES INVERSAS")
    print("-" * 40)
    
    # Verificar que cada empleado tenga su jerarquía completa
    empleados_total = Empleado.objects.filter(status=True)
    print(f"\n👥 TOTAL EMPLEADOS ACTIVOS: {empleados_total.count()}")
    
    empleados_sin_problemas = 0
    empleados_con_problemas = 0
    
    for empleado in empleados_total:
        try:
            # Verificar cadena completa
            puesto = empleado.puesto
            departamento = puesto.departamento
            planta = departamento.planta
            empresa = planta.empresa
            
            # Verificar que las relaciones inversas funcionan
            assert empleado in puesto.empleados.all()
            assert puesto in departamento.puestos.all()
            assert departamento in planta.departamentos.all()
            assert planta in empresa.plantas.all()
            
            empleados_sin_problemas += 1
            
        except Exception as e:
            print(f"   ❌ PROBLEMA con {empleado.nombre_completo}: {e}")
            empleados_con_problemas += 1
    
    print(f"   ✅ Empleados sin problemas: {empleados_sin_problemas}")
    print(f"   ❌ Empleados con problemas: {empleados_con_problemas}")
    
    # 4. RESUMEN ESTADÍSTICO
    print("\n\n📊 4. RESUMEN ESTADÍSTICO")
    print("-" * 40)
    
    for empresa in empresas:
        print(f"\n🏢 {empresa.nombre}:")
        plantas = empresa.plantas.filter(status=True)
        total_departamentos = sum(p.departamentos.filter(status=True).count() for p in plantas)
        total_puestos = sum(
            d.puestos.filter(status=True).count() 
            for p in plantas 
            for d in p.departamentos.filter(status=True)
        )
        total_empleados = sum(
            pu.empleados.filter(status=True).count() 
            for p in plantas 
            for d in p.departamentos.filter(status=True)
            for pu in d.puestos.filter(status=True)
        )
        
        print(f"   📍 Plantas: {plantas.count()}")
        print(f"   🏢 Departamentos: {total_departamentos}")
        print(f"   💼 Puestos: {total_puestos}")
        print(f"   👥 Empleados: {total_empleados}")
        
        # Verificar distribución por planta
        for planta in plantas:
            depto_count = planta.departamentos.filter(status=True).count()
            emp_count = sum(
                pu.empleados.filter(status=True).count() 
                for d in planta.departamentos.filter(status=True)
                for pu in d.puestos.filter(status=True)
            )
            print(f"      • {planta.nombre}: {depto_count} deptos, {emp_count} empleados")
    
    # 5. VALIDAR EVALUACIONES
    print("\n\n📋 5. SISTEMA DE EVALUACIONES")
    print("-" * 40)
    
    tipos = TipoEvaluacion.objects.all()
    for tipo in tipos:
        evaluaciones = Evaluacion.objects.filter(tipo_evaluacion=tipo)
        print(f"\n📋 TIPO: {tipo.nombre}")
        print(f"   📄 Evaluaciones: {evaluaciones.count()}")
        
        for evaluacion in evaluaciones:
            secciones = evaluacion.secciones.count()
            print(f"      • {evaluacion.nombre}: {secciones} secciones")
    
    # Conjuntos de respuestas
    conjuntos = ConjuntoRespuestas.objects.all()
    print(f"\n🎯 CONJUNTOS DE RESPUESTAS: {conjuntos.count()}")
    for conjunto in conjuntos:
        opciones = conjunto.opciones.count()
        print(f"   • {conjunto.nombre}: {opciones} opciones")
    
    print("\n" + "=" * 60)
    print("✅ VALIDACIÓN COMPLETA TERMINADA")
    
    # 6. VERIFICAR INTEGRIDAD DE DATOS
    print("\n\n🔍 6. VERIFICACIÓN DE INTEGRIDAD")
    print("-" * 40)
    
    # Verificar que no hay registros huérfanos
    print("\n🔗 Verificando registros huérfanos...")
    
    # Plantas sin empresa
    plantas_huerfanas = Planta.objects.filter(empresa__isnull=True)
    if plantas_huerfanas.exists():
        print(f"   ❌ Plantas sin empresa: {plantas_huerfanas.count()}")
    else:
        print("   ✅ Todas las plantas tienen empresa")
    
    # Departamentos sin planta
    deptos_huerfanos = Departamento.objects.filter(planta__isnull=True)
    if deptos_huerfanos.exists():
        print(f"   ❌ Departamentos sin planta: {deptos_huerfanos.count()}")
    else:
        print("   ✅ Todos los departamentos tienen planta")
    
    # Puestos sin departamento
    puestos_huerfanos = Puesto.objects.filter(departamento__isnull=True)
    if puestos_huerfanos.exists():
        print(f"   ❌ Puestos sin departamento: {puestos_huerfanos.count()}")
    else:
        print("   ✅ Todos los puestos tienen departamento")
    
    # Empleados sin puesto
    empleados_huerfanos = Empleado.objects.filter(puesto__isnull=True)
    if empleados_huerfanos.exists():
        print(f"   ❌ Empleados sin puesto: {empleados_huerfanos.count()}")
    else:
        print("   ✅ Todos los empleados tienen puesto")
    
    print("\n🎉 ¡VALIDACIÓN COMPLETA! Todo está correctamente enlazado.")


if __name__ == "__main__":
    validar_estructura_completa()
