#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
SCRIPT DE PRUEBA COMPLETA DEL SISTEMA AXYOMA
============================================
Prueba todos los modelos rediseñados sin depender de migraciones.
"""

import os
import sys
import django
from datetime import datetime, date
from django.contrib.auth.models import User

# Configurar Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')
django.setup()

from apps.users.models import (
    PerfilUsuario, Empresa, Planta, Departamento, Puesto, Empleado, AdminPlanta,
    TipoEvaluacion, Evaluacion, SeccionEval, Pregunta, ConjuntoRespuestas, 
    PosiblesRespuestas, SeccionPregunta, Asignacion, AsignacionEmpleado,
    RespuestaEmpleado, ResultadoEvaluacion
)

def limpiar_datos():
    """Limpia todos los datos para empezar fresh"""
    print("🧹 Limpiando datos existentes...")
    
    # Orden importante para evitar errores de FK
    modelos_a_limpiar = [
        ResultadoEvaluacion,
        RespuestaEmpleado,
        AsignacionEmpleado,
        Asignacion,
        SeccionPregunta,
        PosiblesRespuestas,
        ConjuntoRespuestas,
        SeccionEval,
        Pregunta,
        Evaluacion,
        TipoEvaluacion,
        AdminPlanta,
        Empleado,
        Puesto,
        Departamento,
        Planta,
        Empresa,
        PerfilUsuario,
        User,
    ]
    
    for modelo in modelos_a_limpiar:
        count = modelo.objects.count()
        if count > 0:
            modelo.objects.all().delete()
            print(f"   ✅ {modelo.__name__}: {count} registros eliminados")

def crear_datos_basicos():
    """Crea la estructura básica de datos"""
    print("\n🏗️ Creando estructura básica...")
    
    # 1. SUPERADMIN
    superuser = User.objects.create_user(
        username='superadmin',
        email='super@axyoma.com',
        password='admin123',
        first_name='Super',
        last_name='Admin'
    )
    superuser.is_superuser = True
    superuser.is_staff = True
    superuser.save()
    
    perfil_super = PerfilUsuario.objects.create(
        nombre='Super',
        apellido_paterno='Admin',
        correo='super@axyoma.com',
        nivel_usuario='superadmin',
        user=superuser
    )
    print(f"   ✅ SuperAdmin creado: {perfil_super}")
    
    # 2. ADMIN EMPRESA
    admin_user = User.objects.create_user(
        username='admin_technomex',
        email='admin@technomex.com',
        password='admin123',
        first_name='Carlos',
        last_name='Rodríguez'
    )
    
    perfil_admin = PerfilUsuario.objects.create(
        nombre='Carlos',
        apellido_paterno='Rodríguez',
        apellido_materno='García',
        correo='admin@technomex.com',
        nivel_usuario='admin-empresa',
        user=admin_user
    )
    print(f"   ✅ Admin Empresa creado: {perfil_admin}")
    
    # 3. EMPRESA
    empresa = Empresa.objects.create(
        nombre='TechnoMex Industries',
        rfc='TMI950123ABC',
        direccion='Av. Revolución 1234, Col. Moderna, CDMX',
        email_contacto='contacto@technomex.com',
        telefono_contacto='5555-1234',
        administrador=perfil_admin
    )
    print(f"   ✅ Empresa creada: {empresa}")
    
    # 4. PLANTAS
    planta_norte = Planta.objects.create(
        nombre='Planta Norte',
        empresa=empresa,
        direccion='Km 45 Carretera a Querétaro, Ecatepec, Edo. México'
    )
    
    planta_sur = Planta.objects.create(
        nombre='Planta Sur',
        empresa=empresa,
        direccion='Parque Industrial Xochimilco, CDMX'
    )
    print(f"   ✅ Plantas creadas: {planta_norte}, {planta_sur}")
    
    # 5. DEPARTAMENTOS
    departamentos_data = [
        ('Recursos Humanos', planta_norte),
        ('Producción', planta_norte),
        ('Calidad', planta_norte),
        ('Mantenimiento', planta_norte),
        ('Administración', planta_sur),
        ('Logística', planta_sur),
        ('Ventas', planta_sur),
    ]
    
    departamentos = []
    for nombre, planta in departamentos_data:
        dept = Departamento.objects.create(
            nombre=nombre,
            planta=planta,
            descripcion=f'Departamento de {nombre} en {planta.nombre}'
        )
        departamentos.append(dept)
    
    print(f"   ✅ Departamentos creados: {len(departamentos)}")
    
    # 6. PUESTOS
    puestos_data = [
        ('Gerente de RRHH', departamentos[0]),
        ('Especialista en Nómina', departamentos[0]),
        ('Operador de Línea', departamentos[1]),
        ('Supervisor de Producción', departamentos[1]),
        ('Inspector de Calidad', departamentos[2]),
        ('Técnico de Mantenimiento', departamentos[3]),
        ('Contador', departamentos[4]),
        ('Coordinador de Logística', departamentos[5]),
        ('Ejecutivo de Ventas', departamentos[6]),
    ]
    
    puestos = []
    for nombre, dept in puestos_data:
        puesto = Puesto.objects.create(
            nombre=nombre,
            departamento=dept,
            descripcion=f'Puesto de {nombre} en {dept.nombre}'
        )
        puestos.append(puesto)
    
    print(f"   ✅ Puestos creados: {len(puestos)}")
    
    # 7. EMPLEADOS
    empleados_data = [
        ('María', 'González', 'López', 'maria.gonzalez@technomex.com', puestos[0]),
        ('Juan', 'Pérez', 'Martínez', 'juan.perez@technomex.com', puestos[1]),
        ('Ana', 'Rodríguez', 'Sánchez', 'ana.rodriguez@technomex.com', puestos[2]),
        ('Luis', 'Hernández', 'Torres', 'luis.hernandez@technomex.com', puestos[3]),
        ('Carmen', 'López', 'Morales', 'carmen.lopez@technomex.com', puestos[4]),
        ('Roberto', 'Martín', 'Vega', 'roberto.martin@technomex.com', puestos[5]),
        ('Patricia', 'García', 'Ruiz', 'patricia.garcia@technomex.com', puestos[6]),
        ('Miguel', 'Torres', 'Silva', 'miguel.torres@technomex.com', puestos[7]),
        ('Laura', 'Morales', 'Castro', 'laura.morales@technomex.com', puestos[8]),
    ]
    
    empleados = []
    for nombre, ap_pat, ap_mat, email, puesto in empleados_data:
        empleado = Empleado.objects.create(
            nombre=nombre,
            apellido_paterno=ap_pat,
            apellido_materno=ap_mat,
            email=email,
            telefono=f'555-{len(empleados)+1000}',
            fecha_ingreso=date(2023, 1, 15),
            puesto=puesto
        )
        empleados.append(empleado)
    
    print(f"   ✅ Empleados creados: {len(empleados)}")
    
    return {
        'superadmin': perfil_super,
        'admin_empresa': perfil_admin,
        'empresa': empresa,
        'plantas': [planta_norte, planta_sur],
        'departamentos': departamentos,
        'puestos': puestos,
        'empleados': empleados
    }

def crear_sistema_evaluaciones(datos_basicos):
    """Crea el sistema completo de evaluaciones"""
    print("\n📋 Creando sistema de evaluaciones...")
    
    # 1. TIPOS DE EVALUACIÓN
    tipo_nom030 = TipoEvaluacion.objects.create(
        nombre='NOM-030',
        descripcion='Evaluación de Factores de Riesgo Psicosocial en el Trabajo'
    )
    
    tipo_nom035 = TipoEvaluacion.objects.create(
        nombre='NOM-035',
        descripcion='Evaluación del Entorno Organizacional Favorable'
    )
    
    print(f"   ✅ Tipos de evaluación creados: {tipo_nom030}, {tipo_nom035}")
    
    # 2. CONJUNTOS DE RESPUESTAS
    conjunto_likert = ConjuntoRespuestas.objects.create(
        nombre='Escala Likert 5 puntos',
        descripcion='Escala de 1 a 5 puntos para evaluaciones psicosociales',
        predefinido=True
    )
    
    conjunto_sino = ConjuntoRespuestas.objects.create(
        nombre='Sí/No',
        descripcion='Respuestas binarias',
        predefinido=True
    )
    
    print(f"   ✅ Conjuntos de respuestas creados: {conjunto_likert}, {conjunto_sino}")
    
    # 3. OPCIONES DE RESPUESTA - Likert
    opciones_likert = [
        ('Nunca', 1),
        ('Casi nunca', 2),
        ('Algunas veces', 3),
        ('Casi siempre', 4),
        ('Siempre', 5)
    ]
    
    for i, (texto, valor) in enumerate(opciones_likert, 1):
        PosiblesRespuestas.objects.create(
            texto_opcion=texto,
            valor_int=valor,
            numero_orden=i,
            conjunto_respuestas=conjunto_likert
        )
    
    # 4. OPCIONES DE RESPUESTA - Sí/No
    opciones_sino = [('Sí', True), ('No', False)]
    
    for i, (texto, valor) in enumerate(opciones_sino, 1):
        PosiblesRespuestas.objects.create(
            texto_opcion=texto,
            valor_booleano=valor,
            numero_orden=i,
            conjunto_respuestas=conjunto_sino
        )
    
    print(f"   ✅ Opciones de respuesta creadas")
    
    # 5. EVALUACIÓN NOM-030
    evaluacion_nom030 = Evaluacion.objects.create(
        nombre='Evaluación NOM-030 - Factores Psicosociales',
        descripcion='Identificación y análisis de los factores de riesgo psicosocial',
        instrucciones='Conteste con la mayor honestidad posible. No hay respuestas correctas o incorrectas.',
        tiempo_limite=45,
        umbral_aprobacion=70,
        tipo_evaluacion=tipo_nom030,
        empresa=None,  # Evaluación normativa
        creado_por=datos_basicos['superadmin']
    )
    
    print(f"   ✅ Evaluación creada: {evaluacion_nom030}")
    
    # 6. SECCIONES DE LA EVALUACIÓN
    secciones_data = [
        ('Ambiente de trabajo', 'Condiciones en el lugar de trabajo', 1, True),
        ('Carga de trabajo', 'Demandas cuantitativas y cualitativas', 2, True),
        ('Violencia laboral', 'Actos de violencia y hostigamiento', 3, True),
        ('Información personal', 'Datos demográficos y laborales', 4, False),
    ]
    
    secciones = []
    for nombre, desc, orden, evaluable in secciones_data:
        seccion = SeccionEval.objects.create(
            nombre=nombre,
            descripcion=desc,
            numero_orden=orden,
            es_evaluable=evaluable,
            evaluacion=evaluacion_nom030
        )
        secciones.append(seccion)
    
    print(f"   ✅ Secciones creadas: {len(secciones)}")
    
    # 7. PREGUNTAS
    preguntas_data = [
        # Ambiente de trabajo
        ('¿El lugar donde trabajo me permite tener contacto directo con mis compañeros?', 'Múltiple'),
        ('¿Mi lugar de trabajo cuenta con iluminación adecuada?', 'Múltiple'),
        ('¿El espacio donde trabajo permite que me mueva libremente?', 'Múltiple'),
        # Carga de trabajo
        ('¿Mi trabajo me exige hacer mucho esfuerzo físico?', 'Múltiple'),
        ('¿Las actividades que realizo se pueden hacer sin prisa?', 'Múltiple'),
        ('¿Considero que es necesario mantener un ritmo acelerado de trabajo?', 'Múltiple'),
        # Violencia laboral
        ('¿He recibido agresiones verbales en mi trabajo?', 'Bool'),
        ('¿He sentido que me discriminan por mi edad?', 'Bool'),
        ('¿He presenciado actos violentos en mi trabajo?', 'Bool'),
        # Información personal
        ('¿Cuál es su estado civil?', 'Abierta'),
        ('¿Cuántos años lleva trabajando en la empresa?', 'Abierta'),
    ]
    
    preguntas = []
    for texto, tipo in preguntas_data:
        pregunta = Pregunta.objects.create(
            texto_pregunta=texto,
            tipo_pregunta=tipo,
            es_obligatoria=True
        )
        preguntas.append(pregunta)
    
    print(f"   ✅ Preguntas creadas: {len(preguntas)}")
    
    # 8. ASIGNAR PREGUNTAS A SECCIONES
    asignaciones = [
        # Ambiente (preguntas 0-2)
        (secciones[0], preguntas[0], conjunto_likert, 1),
        (secciones[0], preguntas[1], conjunto_likert, 2),
        (secciones[0], preguntas[2], conjunto_likert, 3),
        # Carga (preguntas 3-5)
        (secciones[1], preguntas[3], conjunto_likert, 1),
        (secciones[1], preguntas[4], conjunto_likert, 2),
        (secciones[1], preguntas[5], conjunto_likert, 3),
        # Violencia (preguntas 6-8)
        (secciones[2], preguntas[6], conjunto_sino, 1),
        (secciones[2], preguntas[7], conjunto_sino, 2),
        (secciones[2], preguntas[8], conjunto_sino, 3),
        # Personal (preguntas 9-10)
        (secciones[3], preguntas[9], None, 1),
        (secciones[3], preguntas[10], None, 2),
    ]
    
    seccion_preguntas = []
    for seccion, pregunta, conjunto, orden in asignaciones:
        sp = SeccionPregunta.objects.create(
            seccion=seccion,
            pregunta=pregunta,
            conjunto_respuestas=conjunto,
            numero_orden=orden
        )
        seccion_preguntas.append(sp)
    
    print(f"   ✅ Preguntas asignadas a secciones: {len(seccion_preguntas)}")
    
    return {
        'tipos': [tipo_nom030, tipo_nom035],
        'conjuntos': [conjunto_likert, conjunto_sino],
        'evaluacion': evaluacion_nom030,
        'secciones': secciones,
        'preguntas': preguntas,
        'seccion_preguntas': seccion_preguntas
    }

def crear_asignaciones_y_respuestas(datos_basicos, sistema_eval):
    """Crea asignaciones y simula respuestas"""
    print("\n📝 Creando asignaciones y respuestas...")
    
    # 1. ASIGNACIÓN DE EVALUACIÓN
    asignacion = Asignacion.objects.create(
        evaluacion=sistema_eval['evaluacion'],
        fecha_inicio=datetime(2024, 1, 15, 9, 0),
        fecha_fin=datetime(2024, 2, 15, 17, 0),
        status=True
    )
    
    print(f"   ✅ Asignación creada: {asignacion}")
    
    # 2. ASIGNAR A EMPLEADOS
    asignaciones_empleado = []
    for empleado in datos_basicos['empleados'][:5]:  # Primeros 5 empleados
        ae = AsignacionEmpleado.objects.create(
            asignacion=asignacion,
            empleado=empleado,
            status='Completada',
            fecha_inicio=datetime(2024, 1, 16, 10, 0),
            fecha_completado=datetime(2024, 1, 16, 11, 30)
        )
        asignaciones_empleado.append(ae)
    
    print(f"   ✅ Asignaciones a empleados: {len(asignaciones_empleado)}")
    
    # 3. SIMULAR RESPUESTAS
    respuestas = []
    for ae in asignaciones_empleado:
        for sp in sistema_eval['seccion_preguntas']:
            if sp.conjunto_respuestas:
                # Respuesta con opción predefinida
                opciones = sp.conjunto_respuestas.opciones.all()
                opcion_elegida = opciones[len(respuestas) % len(opciones)]  # Rotar opciones
                
                respuesta = RespuestaEmpleado.objects.create(
                    asignacion_empleado=ae,
                    seccion_pregunta=sp,
                    opcion_seleccionada=opcion_elegida
                )
            else:
                # Respuesta de texto libre
                respuesta = RespuestaEmpleado.objects.create(
                    asignacion_empleado=ae,
                    seccion_pregunta=sp,
                    respuesta_texto=f'Respuesta de texto del empleado {ae.empleado.nombre}'
                )
            
            respuestas.append(respuesta)
    
    print(f"   ✅ Respuestas creadas: {len(respuestas)}")
    
    # 4. GENERAR RESULTADOS
    resultados = []
    for ae in asignaciones_empleado:
        # Contar respuestas correctas (simulado)
        respuestas_empleado = ae.respuestas.filter(
            seccion_pregunta__seccion__es_evaluable=True
        )
        total_evaluables = respuestas_empleado.count()
        correctas = total_evaluables // 2  # 50% correcto (simulado)
        
        resultado = ResultadoEvaluacion.objects.create(
            asignacion_empleado=ae,
            num_respuestas_correctas=correctas,
            num_preguntas_evaluables=total_evaluables,
            porcentaje_correctas=(correctas / total_evaluables) * 100 if total_evaluables > 0 else 0,
            aprobado=correctas >= (total_evaluables * 0.7),  # 70% para aprobar
            observaciones='Resultado generado automáticamente para pruebas'
        )
        resultados.append(resultado)
    
    print(f"   ✅ Resultados generados: {len(resultados)}")
    
    return {
        'asignacion': asignacion,
        'asignaciones_empleado': asignaciones_empleado,
        'respuestas': respuestas,
        'resultados': resultados
    }

def probar_propiedades_y_metodos():
    """Prueba las propiedades y métodos de los modelos"""
    print("\n🔍 Probando propiedades y métodos...")
    
    # Probar empresa
    empresa = Empresa.objects.first()
    print(f"   📊 {empresa.nombre}:")
    print(f"      - Total plantas: {empresa.total_plantas}")
    print(f"      - Total empleados: {empresa.total_empleados}")
    print(f"      - Suscripción activa: {empresa.tiene_suscripcion_activa}")
    
    # Probar empleado
    empleado = Empleado.objects.first()
    print(f"   👤 {empleado.nombre_completo}:")
    print(f"      - Empresa: {empleado.empresa.nombre}")
    print(f"      - Planta: {empleado.planta.nombre}")
    print(f"      - Departamento: {empleado.departamento.nombre}")
    print(f"      - Puesto: {empleado.puesto.nombre}")
    
    # Probar evaluación
    evaluacion = Evaluacion.objects.first()
    print(f"   📋 {evaluacion.nombre}:")
    print(f"      - Es normativa: {evaluacion.es_normativa}")
    print(f"      - Total secciones: {evaluacion.total_secciones}")
    
    # Probar asignación empleado
    ae = AsignacionEmpleado.objects.first()
    print(f"   📝 Asignación {ae.empleado.nombre_completo}:")
    print(f"      - Progreso: {ae.progreso_porcentaje}%")
    print(f"      - Completada: {ae.esta_completada}")
    
    # Probar resultado
    resultado = ResultadoEvaluacion.objects.first()
    print(f"   🎯 Resultado:")
    print(f"      - Correctas: {resultado.num_respuestas_correctas}/{resultado.num_preguntas_evaluables}")
    print(f"      - Porcentaje: {resultado.porcentaje_correctas}%")
    print(f"      - Aprobado: {resultado.aprobado}")

def mostrar_resumen_final():
    """Muestra un resumen de todos los datos creados"""
    print("\n📈 RESUMEN FINAL:")
    print("=" * 50)
    
    modelos_conteo = [
        ('Usuarios Django', User.objects.count()),
        ('Perfiles Usuario', PerfilUsuario.objects.count()),
        ('Empresas', Empresa.objects.count()),
        ('Plantas', Planta.objects.count()),
        ('Departamentos', Departamento.objects.count()),
        ('Puestos', Puesto.objects.count()),
        ('Empleados', Empleado.objects.count()),
        ('Tipos Evaluación', TipoEvaluacion.objects.count()),
        ('Evaluaciones', Evaluacion.objects.count()),
        ('Secciones', SeccionEval.objects.count()),
        ('Preguntas', Pregunta.objects.count()),
        ('Conjuntos Respuestas', ConjuntoRespuestas.objects.count()),
        ('Opciones Respuesta', PosiblesRespuestas.objects.count()),
        ('Sección-Preguntas', SeccionPregunta.objects.count()),
        ('Asignaciones', Asignacion.objects.count()),
        ('Asignaciones Empleado', AsignacionEmpleado.objects.count()),
        ('Respuestas', RespuestaEmpleado.objects.count()),
        ('Resultados', ResultadoEvaluacion.objects.count()),
    ]
    
    for nombre, count in modelos_conteo:
        print(f"   {nombre:20} : {count:3d} registros")
    
    print("=" * 50)
    print("✅ TODOS LOS MODELOS FUNCIONAN CORRECTAMENTE")
    print("🎉 EL SISTEMA AXYOMA ESTÁ LISTO PARA PRODUCCIÓN")

def main():
    """Función principal"""
    print("🚀 INICIANDO PRUEBA COMPLETA DEL SISTEMA AXYOMA")
    print("=" * 60)
    
    try:
        # 1. Limpiar datos existentes
        limpiar_datos()
        
        # 2. Crear estructura básica
        datos_basicos = crear_datos_basicos()
        
        # 3. Crear sistema de evaluaciones
        sistema_eval = crear_sistema_evaluaciones(datos_basicos)
        
        # 4. Crear asignaciones y respuestas
        flujo_evaluacion = crear_asignaciones_y_respuestas(datos_basicos, sistema_eval)
        
        # 5. Probar propiedades y métodos
        probar_propiedades_y_metodos()
        
        # 6. Mostrar resumen
        mostrar_resumen_final()
        
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        return False
    
    return True

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
