# -*- coding: utf-8 -*-
"""
Script para probar las nuevas APIs oficiales de evaluaciones (SuperAdmin)
"""

import os
import sys
import django
import requests
import json
from datetime import datetime, date
from django.conf import settings

# Configurar Django
import sys
sys.path.append('.')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')
django.setup()

from django.contrib.auth import get_user_model
from apps.users.models import Empresa, Planta, Empleado, Puesto, Departamento
from apps.evaluaciones.models_oficiales import (
    EvaluacionOficial, SeccionOficial, PreguntaOficial
)

User = get_user_model()

# URL base del servidor
BASE_URL = "http://127.0.0.1:8000"

def crear_datos_de_prueba():
    """Crear datos básicos para las pruebas"""
    print("📊 Creando datos de prueba...")
    
    # Crear SuperAdmin si no existe
    superadmin, created = User.objects.get_or_create(
        email='superadmin@axyoma.com',
        defaults={
            'first_name': 'Super',
            'last_name': 'Admin',
            'user_type': 'SuperAdmin',
            'is_active': True,
            'is_staff': True,
            'is_superuser': True
        }
    )
    if created:
        superadmin.set_password('superadmin123')
        superadmin.save()
        print(f"✅ SuperAdmin creado: {superadmin.email}")
    else:
        print(f"✅ SuperAdmin ya existe: {superadmin.email}")
    
    # Crear evaluación oficial NOM-035 si no existe
    evaluacion_nom035, created = EvaluacionOficial.objects.get_or_create(
        tipo_norma='NOM-035',
        nombre='Evaluación NOM-035 Oficial',
        defaults={
            'descripcion': 'Evaluación oficial de factores de riesgo psicosocial NOM-035',
            'vigente': True,
            'version': '1.0'
        }
    )
    if created:
        print(f"✅ Evaluación NOM-035 creada: {evaluacion_nom035.nombre}")
    else:
        print(f"✅ Evaluación NOM-035 ya existe: {evaluacion_nom035.nombre}")
    
    # Crear secciones básicas
    seccion1, created = SeccionOficial.objects.get_or_create(
        evaluacion_oficial=evaluacion_nom035,
        numero_orden=1,
        defaults={
            'nombre': 'Información General',
            'descripcion': 'Datos generales del trabajador'
        }
    )
    if created:
        print(f"✅ Sección creada: {seccion1.nombre}")
    
    seccion2, created = SeccionOficial.objects.get_or_create(
        evaluacion_oficial=evaluacion_nom035,
        numero_orden=2,
        defaults={
            'nombre': 'Condiciones del Trabajo',
            'descripcion': 'Evaluación de las condiciones laborales'
        }
    )
    if created:
        print(f"✅ Sección creada: {seccion2.nombre}")
    
    # Crear preguntas básicas
    pregunta1, created = PreguntaOficial.objects.get_or_create(
        seccion=seccion1,
        numero_orden=1,
        defaults={
            'texto_pregunta': '¿Cuál es su puesto de trabajo?',
            'tipo_pregunta': 'Abierta',
            'es_obligatoria': True
        }
    )
    if created:
        print(f"✅ Pregunta creada: {pregunta1.texto_pregunta}")
    
    pregunta2, created = PreguntaOficial.objects.get_or_create(
        seccion=seccion2,
        numero_orden=1,
        defaults={
            'texto_pregunta': '¿Considera que su carga de trabajo es adecuada?',
            'tipo_pregunta': 'Múltiple',
            'opciones_respuesta': ['Totalmente de acuerdo', 'De acuerdo', 'En desacuerdo', 'Totalmente en desacuerdo'],
            'es_obligatoria': True
        }
    )
    if created:
        print(f"✅ Pregunta creada: {pregunta2.texto_pregunta}")
    
    return superadmin

def obtener_token_auth(email, password):
    """Obtener token de autenticación"""
    try:
        response = requests.post(f"{BASE_URL}/api/auth/login/", {
            'email': email,
            'password': password
        })
        if response.status_code == 200:
            data = response.json()
            return data.get('access')
        else:
            print(f"❌ Error de autenticación: {response.status_code}")
            print(response.text)
            return None
    except requests.exceptions.ConnectionError:
        print("❌ Error: No se pudo conectar al servidor Django")
        print("   Asegúrate de que el servidor esté ejecutándose en http://127.0.0.1:8000")
        return None

def probar_apis_superadmin(token):
    """Probar todas las APIs del SuperAdmin"""
    headers = {'Authorization': f'Bearer {token}'}
    
    print("\n🔍 Probando APIs de SuperAdmin...")
    
    # 1. Listar evaluaciones oficiales
    print("\n1️⃣ Listando evaluaciones oficiales...")
    try:
        response = requests.get(f"{BASE_URL}/api/evaluaciones/oficial/superadmin/evaluaciones-oficiales/", headers=headers)
        if response.status_code == 200:
            evaluaciones = response.json()
            print(f"✅ Encontradas {evaluaciones['count']} evaluaciones oficiales")
            for eval_data in evaluaciones['results']:
                print(f"   - {eval_data['nombre']} ({eval_data['tipo_norma']})")
        else:
            print(f"❌ Error: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # 2. Listar secciones oficiales
    print("\n2️⃣ Listando secciones oficiales...")
    try:
        response = requests.get(f"{BASE_URL}/api/evaluaciones/oficial/superadmin/secciones-oficiales/", headers=headers)
        if response.status_code == 200:
            secciones = response.json()
            print(f"✅ Encontradas {secciones['count']} secciones oficiales")
            for seccion in secciones['results']:
                print(f"   - {seccion['nombre']} (Orden: {seccion['numero_orden']})")
        else:
            print(f"❌ Error: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # 3. Listar preguntas oficiales
    print("\n3️⃣ Listando preguntas oficiales...")
    try:
        response = requests.get(f"{BASE_URL}/api/evaluaciones/oficial/superadmin/preguntas-oficiales/", headers=headers)
        if response.status_code == 200:
            preguntas = response.json()
            print(f"✅ Encontradas {preguntas['count']} preguntas oficiales")
            for pregunta in preguntas['results']:
                print(f"   - {pregunta['texto_pregunta'][:50]}... ({pregunta['tipo_pregunta']})")
        else:
            print(f"❌ Error: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # 4. Crear nueva pregunta oficial
    print("\n4️⃣ Creando nueva pregunta oficial...")
    try:
        # Obtener primera sección para asociar la pregunta
        response = requests.get(f"{BASE_URL}/api/evaluaciones/oficial/superadmin/secciones-oficiales/", headers=headers)
        if response.status_code == 200:
            secciones = response.json()
            if secciones['results']:
                seccion_id = secciones['results'][0]['id']
                
                nueva_pregunta = {
                    'seccion': seccion_id,
                    'texto_pregunta': '¿Considera que tiene autonomía en su trabajo?',
                    'tipo_pregunta': 'Si/No',
                    'es_obligatoria': True,
                    'numero_orden': 3
                }
                
                response = requests.post(
                    f"{BASE_URL}/api/evaluaciones/oficial/superadmin/preguntas-oficiales/",
                    headers=headers,
                    json=nueva_pregunta
                )
                
                if response.status_code == 201:
                    pregunta_creada = response.json()
                    print(f"✅ Pregunta creada: {pregunta_creada['texto_pregunta']}")
                else:
                    print(f"❌ Error al crear pregunta: {response.status_code} - {response.text}")
            else:
                print("❌ No se encontraron secciones para asociar la pregunta")
        else:
            print(f"❌ Error al obtener secciones: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # 5. Probar endpoint de estadísticas
    print("\n5️⃣ Probando estadísticas de evaluación...")
    try:
        # Obtener primera evaluación
        response = requests.get(f"{BASE_URL}/api/evaluaciones/oficial/superadmin/evaluaciones-oficiales/", headers=headers)
        if response.status_code == 200:
            evaluaciones = response.json()
            if evaluaciones['results']:
                evaluacion_id = evaluaciones['results'][0]['id']
                
                response = requests.get(
                    f"{BASE_URL}/api/evaluaciones/oficial/superadmin/evaluaciones-oficiales/{evaluacion_id}/estadisticas/",
                    headers=headers
                )
                
                if response.status_code == 200:
                    stats = response.json()
                    print(f"✅ Estadísticas obtenidas:")
                    print(f"   - Total asignaciones: {stats['total_asignaciones']}")
                    print(f"   - Total empleados: {stats['total_empleados']}")
                    print(f"   - Total secciones: {stats['total_secciones']}")
                    print(f"   - Total preguntas: {stats['total_preguntas']}")
                else:
                    print(f"❌ Error al obtener estadísticas: {response.status_code} - {response.text}")
        else:
            print(f"❌ Error: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # 6. Probar dashboard de asignaciones
    print("\n6️⃣ Probando dashboard de asignaciones...")
    try:
        response = requests.get(f"{BASE_URL}/api/evaluaciones/oficial/superadmin/asignaciones/dashboard/", headers=headers)
        if response.status_code == 200:
            dashboard = response.json()
            print(f"✅ Dashboard obtenido:")
            resumen = dashboard['resumen_general']
            print(f"   - Total asignaciones: {resumen['total_asignaciones']}")
            print(f"   - Asignaciones activas: {resumen['asignaciones_activas']}")
            print(f"   - Asignaciones completadas: {resumen['asignaciones_completadas']}")
        else:
            print(f"❌ Error al obtener dashboard: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"❌ Error: {e}")

def main():
    """Función principal"""
    print("🚀 Iniciando pruebas de APIs oficiales de evaluaciones")
    print("=" * 60)
    
    # Crear datos de prueba
    superadmin = crear_datos_de_prueba()
    
    # Obtener token de autenticación
    print("\n🔐 Obteniendo token de autenticación...")
    token = obtener_token_auth('superadmin@axyoma.com', 'superadmin123')
    
    if not token:
        print("❌ No se pudo obtener el token. Verifica que el servidor esté ejecutándose.")
        return
    
    print("✅ Token obtenido exitosamente")
    
    # Probar APIs
    probar_apis_superadmin(token)
    
    print("\n" + "=" * 60)
    print("🎉 Pruebas completadas!")
    print("\n📋 URLs disponibles para el SuperAdmin:")
    print("   - Evaluaciones: /api/evaluaciones/oficial/superadmin/evaluaciones-oficiales/")
    print("   - Secciones: /api/evaluaciones/oficial/superadmin/secciones-oficiales/")
    print("   - Preguntas: /api/evaluaciones/oficial/superadmin/preguntas-oficiales/")
    print("   - Asignaciones: /api/evaluaciones/oficial/superadmin/asignaciones/")
    print("   - Dashboard: /api/evaluaciones/oficial/superadmin/asignaciones/dashboard/")

if __name__ == '__main__':
    main()
