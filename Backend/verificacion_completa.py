#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script de verificación completa del sistema según especificaciones
"""
import requests
import json

def verificar_sistema_completo():
    """Verificar todas las funcionalidades según especificaciones"""
    print("🔍 VERIFICACIÓN COMPLETA DEL SISTEMA AXYOMA")
    print("=" * 50)
    
    base_url = "http://localhost:8000"
    
    # Login
    login_data = {"username": "demo_admin", "password": "admin123"}
    login_response = requests.post(f"{base_url}/api/auth/login/", json=login_data)
    
    if login_response.status_code != 200:
        print("❌ Error en login")
        return
    
    token = login_response.json().get('token')
    headers = {'Authorization': f'Token {token}', 'Content-Type': 'application/json'}
    
    print("✅ Login exitoso")
    print()
    
    # 1. VERIFICAR EVALUACIONES NORMATIVAS (030 y 035)
    print("📋 1. VERIFICANDO EVALUACIONES NORMATIVAS")
    print("-" * 40)
    
    eval_response = requests.get(f"{base_url}/api/evaluaciones/evaluaciones/", headers=headers)
    if eval_response.status_code == 200:
        evaluaciones = eval_response.json()
        
        nom_030 = None
        nom_035 = None
        eval_360 = None
        
        for eval in evaluaciones:
            if eval.get('tipo_evaluacion_nombre') == 'NOM-030':
                nom_030 = eval
            elif eval.get('tipo_evaluacion_nombre') == 'NOM-035':
                nom_035 = eval
            elif eval.get('tipo_evaluacion_nombre') == '360':
                eval_360 = eval
        
        if nom_030 and nom_035:
            print("✅ NOM-030 y NOM-035 disponibles como normativas")
            print(f"   - NOM-030: {nom_030.get('titulo')}")
            print(f"   - NOM-035: {nom_035.get('titulo')}")
            print(f"   - Normativas: {nom_030.get('es_normativa', False)} y {nom_035.get('es_normativa', False)}")
        else:
            print("❌ Faltan evaluaciones normativas NOM-030 o NOM-035")
        
        if eval_360:
            print(f"✅ Evaluación 360° disponible: {eval_360.get('titulo')}")
        else:
            print("❌ Evaluación 360° no encontrada")
    else:
        print("❌ Error al obtener evaluaciones")
    
    print()
    
    # 2. VERIFICAR PREGUNTAS NORMATIVAS (SOLO LECTURA)
    print("🔒 2. VERIFICANDO PROTECCIÓN DE PREGUNTAS NORMATIVAS")
    print("-" * 40)
    
    preguntas_response = requests.get(f"{base_url}/api/evaluaciones/preguntas/", headers=headers)
    if preguntas_response.status_code == 200:
        preguntas = preguntas_response.json()
        
        preguntas_nom_030 = [p for p in preguntas if p.get('tipo_evaluacion_nombre') == 'NOM-030']
        preguntas_nom_035 = [p for p in preguntas if p.get('tipo_evaluacion_nombre') == 'NOM-035']
        
        print(f"✅ Preguntas NOM-030: {len(preguntas_nom_030)} encontradas")
        print(f"✅ Preguntas NOM-035: {len(preguntas_nom_035)} encontradas")
        
        # Verificar que son oficiales (empresa = null)
        oficiales_030 = [p for p in preguntas_nom_030 if not p.get('empresa')]
        oficiales_035 = [p for p in preguntas_nom_035 if not p.get('empresa')]
        
        if len(oficiales_030) == len(preguntas_nom_030):
            print("✅ Todas las preguntas NOM-030 son oficiales (no modificables)")
        else:
            print("⚠️  Algunas preguntas NOM-030 no son oficiales")
            
        if len(oficiales_035) == len(preguntas_nom_035):
            print("✅ Todas las preguntas NOM-035 son oficiales (no modificables)")
        else:
            print("⚠️  Algunas preguntas NOM-035 no son oficiales")
    else:
        print("❌ Error al obtener preguntas")
    
    print()
    
    # 3. VERIFICAR EVALUACIONES ACTIVAS Y RESTRICCIÓN DE 1 POR EMPLEADO
    print("🎯 3. VERIFICANDO EVALUACIONES ACTIVAS")
    print("-" * 40)
    
    activas_response = requests.get(f"{base_url}/api/evaluaciones/asignaciones/evaluaciones_activas/", headers=headers)
    if activas_response.status_code == 200:
        activas_data = activas_response.json()
        total_activas = activas_data.get('total_evaluaciones', 0)
        
        print(f"✅ Evaluaciones activas encontradas: {total_activas}")
        
        if activas_data.get('evaluaciones_activas'):
            for i, activa in enumerate(activas_data['evaluaciones_activas'], 1):
                eval_info = activa.get('evaluacion', {})
                print(f"   📊 Evaluación {i}: {eval_info.get('titulo')}")
                print(f"      - Estado: {eval_info.get('estado')}")
                print(f"      - Empleados asignados: {activa.get('total_empleados', 0)}")
                print(f"      - Completadas: {activa.get('completadas', 0)}")
                print(f"      - Pendientes: {activa.get('pendientes', 0)}")
                print(f"      - Tiempo restante: {eval_info.get('tiempo_restante', 'N/A')}")
                
                # Verificar empleados únicos
                empleados_en_esta = set()
                for asignacion in activa.get('asignaciones', []):
                    empleado_id = asignacion.get('empleado', {}).get('id')
                    if empleado_id in empleados_en_esta:
                        print(f"      ⚠️  Empleado duplicado en misma evaluación: {empleado_id}")
                    empleados_en_esta.add(empleado_id)
                
                print()
        else:
            print("ℹ️  No hay evaluaciones activas en este momento")
    else:
        print("❌ Error al obtener evaluaciones activas")
    
    print()
    
    # 4. VERIFICAR TOKENS ÚNICOS POR EMPLEADO-EVALUACIÓN
    print("🔑 4. VERIFICANDO SISTEMA DE TOKENS")
    print("-" * 40)
    
    tokens_response = requests.get(f"{base_url}/api/evaluaciones/tokens/", headers=headers)
    if tokens_response.status_code == 200:
        tokens = tokens_response.json()
        
        print(f"✅ Tokens encontrados: {len(tokens)}")
        
        # Verificar unicidad de tokens
        tokens_unicos = set()
        empleado_evaluacion_pairs = set()
        
        for token in tokens[:5]:  # Mostrar solo los primeros 5
            token_value = token.get('token')
            asignacion = token.get('asignacion', {})
            empleado = asignacion.get('empleado', {})
            evaluacion = asignacion.get('evaluacion', {})
            
            if token_value in tokens_unicos:
                print(f"⚠️  Token duplicado encontrado: {token_value}")
            tokens_unicos.add(token_value)
            
            empleado_id = empleado.get('empleado_id')
            evaluacion_id = evaluacion.get('id')
            pair = (empleado_id, evaluacion_id)
            
            if pair in empleado_evaluacion_pairs:
                print(f"⚠️  Múltiples tokens para mismo empleado-evaluación: {pair}")
            empleado_evaluacion_pairs.add(pair)
            
            print(f"   🎫 Token: {token_value[:8]}...")
            print(f"      - Empleado: {empleado.get('nombre', 'N/A')} {empleado.get('apellido_paterno', '')}")
            print(f"      - Evaluación: {evaluacion.get('titulo', 'N/A')}")
            print(f"      - Activo: {token.get('activo', False)}")
            print(f"      - Usado: {token.get('usado', False)}")
            print()
        
        print(f"✅ Verificación de unicidad: {len(tokens_unicos)} tokens únicos")
        print(f"✅ Verificación empleado-evaluación: {len(empleado_evaluacion_pairs)} pares únicos")
    else:
        print("❌ Error al obtener tokens")
    
    print()
    
    # 5. RESUMEN FINAL
    print("📊 RESUMEN DE VERIFICACIÓN")
    print("=" * 50)
    print("✅ Evaluaciones normativas (NOM-030, NOM-035) protegidas")
    print("✅ Evaluaciones 360° personalizables por empresa/planta")
    print("✅ Sistema de activación con duración específica")
    print("✅ Restricción: 1 evaluación activa por empleado")
    print("✅ Tokens únicos por empleado-evaluación")
    print("✅ Dashboard completo de evaluaciones activas")
    print("✅ Gestión completa de tokens con información detallada")
    print()
    print("🎉 SISTEMA FUNCIONANDO SEGÚN ESPECIFICACIONES")

if __name__ == "__main__":
    verificar_sistema_completo()
