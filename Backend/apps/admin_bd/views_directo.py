# -*- coding: utf-8 -*-
"""
SOLUCIÓN DIRECTA PARA EXPORTACIONES CSV
Usa consultas SQL directas para evitar problemas de Django ORM
Solo para SuperAdmin - Garantizado al 100%
"""
import csv
from datetime import datetime
from django.conf import settings
from django.http import HttpResponse
from django.db import connection
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def exportar_tabla_csv_directo(request, tabla_nombre):
    """
    Exportar datos usando consultas SQL directas
    Solo para SuperAdmin - Sin problemas de relaciones
    """
    try:
        user = request.user
        perfil = getattr(user, 'perfil', None)
        
        if not perfil or perfil.nivel_usuario != 'superadmin':
            return Response({'error': 'Solo SuperAdmin puede exportar'}, 
                          status=status.HTTP_403_FORBIDDEN)
        
        # Consultas SQL directas para cada tabla
        consultas_sql = {
            'empleados': {
                'query': """
                    SELECT 
                        e.empleado_id,
                        e.nombre,
                        e.apellido_paterno,
                        e.apellido_materno,
                        e.email,
                        e.telefono,
                        e.fecha_ingreso,
                        e.fecha_registro,
                        CASE WHEN e.status THEN 'Activo' ELSE 'Inactivo' END as status,
                        p.nombre as puesto_nombre
                    FROM empleados e
                    LEFT JOIN puestos p ON e.puesto_id = p.puesto_id
                    ORDER BY e.apellido_paterno, e.nombre
                """,
                'headers': ['ID Empleado', 'Nombre', 'Apellido Paterno', 'Apellido Materno', 'Email', 'Teléfono', 'Fecha Ingreso', 'Fecha Registro', 'Status', 'Puesto']
            },
            'suscripciones': {
                'query': """
                    SELECT 
                        se.suscripcion_id,
                        emp.nombre as empresa_nombre,
                        emp.rfc as empresa_rfc,
                        p.nombre as plan_nombre,
                        p.precio as plan_precio,
                        se.fecha_inicio,
                        se.fecha_fin,
                        se.estado,
                        se.fecha_registro,
                        CASE 
                            WHEN se.fecha_fin < CURRENT_DATE THEN 'Vencida'
                            WHEN se.fecha_fin <= CURRENT_DATE + INTERVAL '7 days' THEN 'Por Vencer'
                            ELSE 'Vigente'
                        END as vigencia
                    FROM suscripciones_empresa se
                    LEFT JOIN empresas emp ON se.empresa = emp.empresa_id
                    LEFT JOIN planes p ON se.plan = p.plan_id
                    ORDER BY emp.nombre, se.fecha_inicio DESC
                """,
                'headers': ['ID Suscripción', 'Empresa', 'RFC Empresa', 'Plan', 'Precio Plan', 'Fecha Inicio', 'Fecha Fin', 'Estado', 'Fecha Registro', 'Vigencia']
            }
        }
        
        if tabla_nombre not in consultas_sql:
            return Response({'error': f'Tabla {tabla_nombre} no disponible'}, 
                          status=status.HTTP_400_BAD_REQUEST)
        
        config = consultas_sql[tabla_nombre]
        
        # Ejecutar consulta SQL directa
        with connection.cursor() as cursor:
            cursor.execute(config['query'])
            datos = cursor.fetchall()
        
        # Crear respuesta CSV
        response = HttpResponse(content_type='text/csv; charset=utf-8')
        response['Content-Disposition'] = f'attachment; filename="{tabla_nombre}_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv"'
        
        # BOM para Excel
        response.write('\ufeff')
        
        writer = csv.writer(response)
        
        # Escribir encabezados
        writer.writerow(config['headers'])
        
        # Escribir datos
        for fila in datos:
            # Convertir cada valor a string, manejando NULLs
            fila_str = [str(valor) if valor is not None else '' for valor in fila]
            writer.writerow(fila_str)
        
        return response
        
    except Exception as e:
        return Response({'error': f'Error al exportar: {str(e)}'}, 
                      status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def listar_tablas_directas(request):
    """
    Listar tablas disponibles para exportación directa
    """
    try:
        user = request.user
        perfil = getattr(user, 'perfil', None)
        
        if not perfil or perfil.nivel_usuario != 'superadmin':
            return Response({'error': 'Solo SuperAdmin puede listar tablas'}, 
                          status=status.HTTP_403_FORBIDDEN)
        
        tablas = [
            {'nombre': 'empleados', 'descripcion': 'Datos de todos los empleados'},
            {'nombre': 'suscripciones', 'descripcion': 'Suscripciones activas y historial'}
        ]
        
        return Response({
            'tablas_disponibles': tablas,
            'nivel_usuario': perfil.nivel_usuario,
            'metodo': 'consulta_directa'
        })
        
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
