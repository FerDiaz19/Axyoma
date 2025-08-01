# -*- coding: utf-8 -*-
"""
ViewSets para los modelos oficiales de evaluaciones NOM (SuperAdmin)
"""

from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q, Count, Avg, F
from django.utils import timezone
from rest_framework.filters import SearchFilter, OrderingFilter

from .models_oficiales import (
    EvaluacionOficial, SeccionOficial, PreguntaOficial,
    AsignacionEvaluacion, EmpleadoAsignado, RespuestaEmpleado
)
from .serializers_oficiales import (
    EvaluacionOficialSerializer, SeccionOficialSerializer,
    PreguntaOficialSerializer, PreguntaOficialCreateSerializer,
    AsignacionEvaluacionSerializer, AsignacionEvaluacionCreateSerializer,
    EmpleadoAsignadoSerializer, RespuestaEmpleadoSerializer
)
from apps.users.models import Empleado, Empresa, Planta

class SuperAdminOnlyPermission(permissions.BasePermission):
    """Permiso solo para SuperAdmin"""
    
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.user_type == 'SuperAdmin'

class EvaluacionOficialViewSet(viewsets.ModelViewSet):
    """ViewSet para gestión de evaluaciones oficiales (SuperAdmin)"""
    
    queryset = EvaluacionOficial.objects.all()
    serializer_class = EvaluacionOficialSerializer
    permission_classes = [SuperAdminOnlyPermission]
    filter_backends = [SearchFilter, OrderingFilter]
    
    search_fields = ['nombre', 'descripcion']
    ordering_fields = ['fecha_creacion', 'nombre', 'tipo_norma']
    ordering = ['-fecha_creacion']
    
    @action(detail=True, methods=['post'])
    def activar(self, request, pk=None):
        """Activar una evaluación oficial"""
        evaluacion = self.get_object()
        evaluacion.vigente = True
        evaluacion.save()
        return Response({'status': 'Evaluación activada'})
    
    @action(detail=True, methods=['post'])
    def desactivar(self, request, pk=None):
        """Desactivar una evaluación oficial"""
        evaluacion = self.get_object()
        evaluacion.vigente = False
        evaluacion.save()
        return Response({'status': 'Evaluación desactivada'})
    
    @action(detail=True, methods=['get'])
    def estadisticas(self, request, pk=None):
        """Obtener estadísticas de uso de la evaluación"""
        evaluacion = self.get_object()
        
        asignaciones = AsignacionEvaluacion.objects.filter(evaluacion_oficial=evaluacion)
        total_asignaciones = asignaciones.count()
        
        empleados_asignados = EmpleadoAsignado.objects.filter(asignacion__evaluacion_oficial=evaluacion)
        total_empleados = empleados_asignados.count()
        empleados_completados = empleados_asignados.filter(estado='completada').count()
        empleados_en_progreso = empleados_asignados.filter(estado='en_progreso').count()
        
        # Promedio de tiempo de completado
        completadas = empleados_asignados.filter(estado='completada', fecha_finalizacion__isnull=False)
        tiempo_promedio = None
        if completadas.exists():
            tiempos = []
            for emp in completadas:
                if emp.fecha_inicio_empleado:
                    tiempo = (emp.fecha_finalizacion - emp.fecha_inicio_empleado).total_seconds() / 3600  # horas
                    tiempos.append(tiempo)
            if tiempos:
                tiempo_promedio = sum(tiempos) / len(tiempos)
        
        return Response({
            'total_asignaciones': total_asignaciones,
            'total_empleados': total_empleados,
            'empleados_completados': empleados_completados,
            'empleados_en_progreso': empleados_en_progreso,
            'porcentaje_completado': (empleados_completados / total_empleados * 100) if total_empleados > 0 else 0,
            'tiempo_promedio_horas': round(tiempo_promedio, 2) if tiempo_promedio else None,
            'total_secciones': evaluacion.secciones.count(),
            'total_preguntas': PreguntaOficial.objects.filter(seccion__evaluacion_oficial=evaluacion).count()
        })

class SeccionOficialViewSet(viewsets.ModelViewSet):
    """ViewSet para gestión de secciones oficiales (SuperAdmin)"""
    
    queryset = SeccionOficial.objects.all()
    serializer_class = SeccionOficialSerializer
    permission_classes = [SuperAdminOnlyPermission]
    filter_backends = [SearchFilter, OrderingFilter]
    
    search_fields = ['nombre', 'descripcion']
    ordering_fields = ['numero_orden', 'nombre']
    ordering = ['numero_orden']

class PreguntaOficialViewSet(viewsets.ModelViewSet):
    """ViewSet para gestión de preguntas oficiales (SuperAdmin)"""
    
    queryset = PreguntaOficial.objects.all()
    permission_classes = [SuperAdminOnlyPermission]
    filter_backends = [SearchFilter, OrderingFilter]
    
    search_fields = ['texto_pregunta']
    ordering_fields = ['numero_orden', 'seccion__numero_orden']
    ordering = ['seccion__numero_orden', 'numero_orden']
    
    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return PreguntaOficialCreateSerializer
        return PreguntaOficialSerializer
    
    @action(detail=False, methods=['get'])
    def por_evaluacion(self, request):
        """Obtener preguntas agrupadas por evaluación"""
        evaluacion_id = request.query_params.get('evaluacion_id')
        
        if not evaluacion_id:
            return Response({'error': 'Se requiere evaluacion_id'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            evaluacion = EvaluacionOficial.objects.get(id=evaluacion_id)
        except EvaluacionOficial.DoesNotExist:
            return Response({'error': 'Evaluación no encontrada'}, status=status.HTTP_404_NOT_FOUND)
        
        secciones = SeccionOficial.objects.filter(evaluacion_oficial=evaluacion).order_by('numero_orden')
        
        resultado = []
        for seccion in secciones:
            preguntas = PreguntaOficial.objects.filter(seccion=seccion).order_by('numero_orden')
            seccion_data = SeccionOficialSerializer(seccion).data
            seccion_data['preguntas'] = PreguntaOficialSerializer(preguntas, many=True).data
            resultado.append(seccion_data)
        
        return Response({
            'evaluacion': EvaluacionOficialSerializer(evaluacion).data,
            'secciones': resultado
        })
    
    @action(detail=True, methods=['post'])
    def duplicar(self, request, pk=None):
        """Duplicar una pregunta"""
        pregunta = self.get_object()
        
        nueva_pregunta = PreguntaOficial.objects.create(
            seccion=pregunta.seccion,
            texto_pregunta=f"Copia de: {pregunta.texto_pregunta}",
            tipo_pregunta=pregunta.tipo_pregunta,
            opciones_respuesta=pregunta.opciones_respuesta,
            es_obligatoria=pregunta.es_obligatoria,
            numero_orden=pregunta.numero_orden + 1,
            pregunta_padre=pregunta.pregunta_padre,
            activador_padre=pregunta.activador_padre
        )
        
        # Actualizar números de orden de preguntas posteriores
        PreguntaOficial.objects.filter(
            seccion=pregunta.seccion,
            numero_orden__gt=pregunta.numero_orden
        ).exclude(id=nueva_pregunta.id).update(numero_orden=F('numero_orden') + 1)
        
        return Response(PreguntaOficialSerializer(nueva_pregunta).data)

class AsignacionEvaluacionViewSet(viewsets.ModelViewSet):
    """ViewSet para gestión de asignaciones de evaluación (SuperAdmin)"""
    
    queryset = AsignacionEvaluacion.objects.all()
    permission_classes = [SuperAdminOnlyPermission]
    filter_backends = [SearchFilter, OrderingFilter]
    
    search_fields = ['empresa__nombre', 'planta__nombre', 'token_sesion']
    ordering_fields = ['fecha_creacion', 'fecha_inicio', 'fecha_fin']
    ordering = ['-fecha_creacion']
    
    def get_serializer_class(self):
        if self.action == 'create':
            return AsignacionEvaluacionCreateSerializer
        return AsignacionEvaluacionSerializer
    
    @action(detail=False, methods=['get'])
    def dashboard(self, request):
        """Dashboard con estadísticas generales de asignaciones"""
        # Filtros por fechas si se proporcionan
        fecha_desde = request.query_params.get('fecha_desde')
        fecha_hasta = request.query_params.get('fecha_hasta')
        
        queryset = self.get_queryset()
        
        if fecha_desde:
            queryset = queryset.filter(fecha_creacion__gte=fecha_desde)
        if fecha_hasta:
            queryset = queryset.filter(fecha_creacion__lte=fecha_hasta)
        
        total_asignaciones = queryset.count()
        asignaciones_activas = queryset.filter(estado='activa').count()
        asignaciones_completadas = queryset.filter(estado='completada').count()
        
        # Estadísticas de empleados
        empleados_asignados = EmpleadoAsignado.objects.filter(asignacion__in=queryset)
        total_empleados = empleados_asignados.count()
        empleados_completados = empleados_asignados.filter(estado='completada').count()
        empleados_en_progreso = empleados_asignados.filter(estado='en_progreso').count()
        
        # Top empresas por asignaciones
        top_empresas = queryset.values('empresa__nombre').annotate(
            total=Count('id')
        ).order_by('-total')[:10]
        
        # Evaluaciones más utilizadas
        top_evaluaciones = queryset.values('evaluacion_oficial__nombre', 'evaluacion_oficial__tipo_norma').annotate(
            total=Count('id')
        ).order_by('-total')[:10]
        
        return Response({
            'resumen_general': {
                'total_asignaciones': total_asignaciones,
                'asignaciones_activas': asignaciones_activas,
                'asignaciones_completadas': asignaciones_completadas,
                'total_empleados': total_empleados,
                'empleados_completados': empleados_completados,
                'empleados_en_progreso': empleados_en_progreso,
                'porcentaje_completado': (empleados_completados / total_empleados * 100) if total_empleados > 0 else 0
            },
            'top_empresas': list(top_empresas),
            'top_evaluaciones': list(top_evaluaciones)
        })
    
    @action(detail=True, methods=['get'])
    def progreso_detallado(self, request, pk=None):
        """Obtener progreso detallado de una asignación"""
        asignacion = self.get_object()
        
        empleados = EmpleadoAsignado.objects.filter(asignacion=asignacion).select_related('empleado')
        
        empleados_data = []
        for emp_asig in empleados:
            respuestas_completadas = RespuestaEmpleado.objects.filter(empleado_asignado=emp_asig).count()
            total_preguntas = PreguntaOficial.objects.filter(
                seccion__evaluacion_oficial=asignacion.evaluacion_oficial
            ).count()
            
            empleados_data.append({
                'id': emp_asig.id,
                'empleado': {
                    'id': emp_asig.empleado.id,
                    'nombre': emp_asig.empleado.nombre,
                    'email': emp_asig.empleado.email,
                    'puesto': emp_asig.empleado.puesto.nombre if emp_asig.empleado.puesto else None
                },
                'estado': emp_asig.estado,
                'progreso_porcentaje': emp_asig.progreso_porcentaje,
                'respuestas_completadas': respuestas_completadas,
                'total_preguntas': total_preguntas,
                'fecha_asignacion': emp_asig.fecha_asignacion,
                'fecha_inicio': emp_asig.fecha_inicio_empleado,
                'fecha_finalizacion': emp_asig.fecha_finalizacion,
                'ultimo_acceso': emp_asig.ultimo_acceso
            })
        
        return Response({
            'asignacion': AsignacionEvaluacionSerializer(asignacion).data,
            'empleados': empleados_data
        })
    
    @action(detail=True, methods=['post'])
    def finalizar(self, request, pk=None):
        """Finalizar una asignación antes de tiempo"""
        asignacion = self.get_object()
        
        if asignacion.estado == 'completada':
            return Response({'error': 'La asignación ya está completada'}, status=status.HTTP_400_BAD_REQUEST)
        
        asignacion.estado = 'completada'
        asignacion.fecha_fin = timezone.now().date()
        asignacion.save()
        
        # Marcar empleados pendientes como no completados
        EmpleadoAsignado.objects.filter(
            asignacion=asignacion,
            estado='pendiente'
        ).update(estado='no_completada')
        
        return Response({'status': 'Asignación finalizada'})

class EmpleadoAsignadoViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet de solo lectura para empleados asignados (SuperAdmin)"""
    
    queryset = EmpleadoAsignado.objects.all()
    serializer_class = EmpleadoAsignadoSerializer
    permission_classes = [SuperAdminOnlyPermission]
    filter_backends = [SearchFilter, OrderingFilter]
    
    search_fields = ['empleado__nombre', 'empleado__email', 'token_empleado']
    ordering_fields = ['fecha_asignacion', 'progreso_porcentaje', 'fecha_finalizacion']
    ordering = ['-fecha_asignacion']
    
    @action(detail=True, methods=['get'])
    def respuestas(self, request, pk=None):
        """Obtener todas las respuestas de un empleado"""
        empleado_asignado = self.get_object()
        
        respuestas = RespuestaEmpleado.objects.filter(
            empleado_asignado=empleado_asignado
        ).select_related('pregunta_oficial', 'pregunta_oficial__seccion')
        
        return Response(RespuestaEmpleadoSerializer(respuestas, many=True).data)

class RespuestaEmpleadoViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet de solo lectura para respuestas de empleados (SuperAdmin)"""
    
    queryset = RespuestaEmpleado.objects.all()
    serializer_class = RespuestaEmpleadoSerializer
    permission_classes = [SuperAdminOnlyPermission]
    filter_backends = [SearchFilter, OrderingFilter]
    
    search_fields = ['respuesta_texto', 'empleado_asignado__empleado__nombre']
    ordering_fields = ['fecha_respuesta', 'tiempo_respuesta_segundos']
    ordering = ['-fecha_respuesta']
    
    @action(detail=False, methods=['get'])
    def estadisticas_pregunta(self, request):
        """Estadísticas de respuestas por pregunta"""
        pregunta_id = request.query_params.get('pregunta_id')
        
        if not pregunta_id:
            return Response({'error': 'Se requiere pregunta_id'}, status=status.HTTP_400_BAD_REQUEST)
        
        respuestas = self.get_queryset().filter(pregunta_oficial_id=pregunta_id)
        
        estadisticas = {
            'total_respuestas': respuestas.count(),
            'tiempo_promedio_segundos': respuestas.aggregate(Avg('tiempo_respuesta_segundos'))['tiempo_respuesta_segundos__avg'],
        }
        
        # Estadísticas específicas por tipo de pregunta
        if respuestas.exists():
            primera_respuesta = respuestas.first()
            tipo_pregunta = primera_respuesta.pregunta_oficial.tipo_pregunta
            
            if tipo_pregunta == 'Múltiple':
                # Conteo de opciones seleccionadas
                opciones_count = {}
                for resp in respuestas.filter(respuesta_multiple__isnull=False):
                    opcion = resp.respuesta_multiple
                    opciones_count[opcion] = opciones_count.get(opcion, 0) + 1
                estadisticas['distribución_opciones'] = opciones_count
                
            elif tipo_pregunta == 'Escala':
                # Promedio y distribución de valores numéricos
                valores = respuestas.filter(respuesta_numerica__isnull=False).values_list('respuesta_numerica', flat=True)
                if valores:
                    estadisticas['promedio_escala'] = sum(valores) / len(valores)
                    estadisticas['distribución_escala'] = dict(zip(*zip(*[(v, list(valores).count(v)) for v in set(valores)])))
                    
            elif tipo_pregunta == 'Si/No':
                # Conteo de respuestas booleanas
                si_count = respuestas.filter(respuesta_booleana=True).count()
                no_count = respuestas.filter(respuesta_booleana=False).count()
                estadisticas['respuestas_si'] = si_count
                estadisticas['respuestas_no'] = no_count
        
        return Response(estadisticas)
