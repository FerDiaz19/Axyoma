# -*- coding: utf-8 -*-
"""
ViewSets para los modelos oficiales de evaluaciones NOM (SuperAdmin)
"""

from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q, Count, Avg, F, Max
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
    permission_classes = [permissions.AllowAny]  # Permitir acceso sin autenticación temporalmente
    filter_backends = [SearchFilter, OrderingFilter]
    
    search_fields = ['texto_pregunta']
    ordering_fields = ['numero_orden', 'seccion__numero_orden']
    ordering = ['seccion__numero_orden', 'numero_orden']
    
    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return PreguntaOficialCreateSerializer
        return PreguntaOficialSerializer
    
    def create(self, request, *args, **kwargs):
        """Crear nueva pregunta oficial"""
        try:
            data = request.data.copy()
            
            # Mapear tipos de frontend a backend
            tipo_map = {
                'multiple': 'Múltiple',
                'si_no': 'Si/No', 
                'escala': 'Escala',
                'texto': 'Abierta'
            }
            
            if 'tipo_pregunta' in data:
                data['tipo_pregunta'] = tipo_map.get(data['tipo_pregunta'], data['tipo_pregunta'])
            
            # Asignar sección por defecto basándose en normativa
            normativa = request.query_params.get('normativa', 'nom_035')
            evaluacion = EvaluacionOficial.objects.filter(
                tipo_norma=normativa.upper().replace('_', '-')
            ).first()
            
            if evaluacion:
                seccion = SeccionOficial.objects.filter(evaluacion_oficial=evaluacion).first()
                if seccion:
                    data['seccion'] = seccion.id
            
            # Asignar número de orden automáticamente
            if 'numero_orden' not in data and 'seccion' in data:
                ultimo_orden = PreguntaOficial.objects.filter(
                    seccion_id=data['seccion']
                ).aggregate(max_orden=Max('numero_orden'))['max_orden'] or 0
                data['numero_orden'] = ultimo_orden + 1
            
            serializer = self.get_serializer(data=data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            
            return Response(serializer.data, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    def update(self, request, *args, **kwargs):
        """Actualizar pregunta oficial"""
        try:
            partial = kwargs.pop('partial', False)
            instance = self.get_object()
            data = request.data.copy()
            
            # Mapear tipos de frontend a backend
            tipo_map = {
                'multiple': 'Múltiple',
                'si_no': 'Si/No',
                'escala': 'Escala', 
                'texto': 'Abierta'
            }
            
            if 'tipo_pregunta' in data:
                data['tipo_pregunta'] = tipo_map.get(data['tipo_pregunta'], data['tipo_pregunta'])
            
            serializer = self.get_serializer(instance, data=data, partial=partial)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            
            return Response(serializer.data)
            
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
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


# ===== NUEVOS VIEWSETS PARA FASE 2: ASIGNACIÓN CON TOKENS =====

import secrets
import string
from django.db import transaction
from apps.users.models import Departamento, Puesto

class EmpleadosAsignacionViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet para obtener empleados filtrados por empresa/planta para asignación"""
    
    serializer_class = EmpleadoAsignadoSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [SearchFilter, OrderingFilter]
    
    search_fields = ['nombre', 'apellido', 'numero_empleado']
    ordering_fields = ['nombre', 'apellido', 'fecha_ingreso']
    ordering = ['nombre', 'apellido']
    
    def get_queryset(self):
        """Filtrar empleados según el usuario logueado"""
        user = self.request.user
        
        # SuperAdmin ve todos los empleados
        if hasattr(user, 'perfil') and user.perfil.nivel_usuario == 'superadmin':
            return Empleado.objects.all()
        
        # Admin Empresa ve empleados de su empresa
        elif hasattr(user, 'perfil') and user.perfil.nivel_usuario == 'admin-empresa':
            try:
                empresa = Empresa.objects.get(administrador=user.perfil)
                return Empleado.objects.filter(empresa=empresa)
            except Empresa.DoesNotExist:
                return Empleado.objects.none()
        
        # Admin Planta ve empleados de su planta
        elif hasattr(user, 'perfil') and user.perfil.nivel_usuario == 'admin-planta':
            try:
                from apps.users.models import AdminPlanta
                admin_planta = AdminPlanta.objects.get(usuario=user.perfil, status=True)
                return Empleado.objects.filter(planta=admin_planta.planta)
            except:
                return Empleado.objects.none()
        
        return Empleado.objects.none()
    
    @action(detail=False, methods=['get'])
    def filtros_disponibles(self, request):
        """Obtener opciones de filtros disponibles"""
        queryset = self.get_queryset()
        
        # Departamentos únicos
        departamentos = Departamento.objects.filter(
            id__in=queryset.values_list('departamento_id', flat=True).distinct()
        ).values('id', 'nombre')
        
        # Puestos únicos
        puestos = Puesto.objects.filter(
            id__in=queryset.values_list('puesto_id', flat=True).distinct()
        ).values('id', 'nombre')
        
        # Plantas únicas (si aplica)
        plantas = []
        if hasattr(self.request.user, 'perfil') and self.request.user.perfil.nivel_usuario in ['superadmin', 'admin-empresa']:
            plantas = queryset.values_list('planta__id', 'planta__nombre').distinct()
            plantas = [{'id': p[0], 'nombre': p[1]} for p in plantas if p[0]]
        
        return Response({
            'departamentos': list(departamentos),
            'puestos': list(puestos),
            'plantas': plantas,
            'total_empleados': queryset.count()
        })
    
    @action(detail=False, methods=['get'])
    def por_departamento(self, request):
        """Filtrar empleados por departamento"""
        departamento_id = request.query_params.get('departamento_id')
        
        if not departamento_id:
            return Response({'error': 'Se requiere departamento_id'}, status=status.HTTP_400_BAD_REQUEST)
        
        queryset = self.get_queryset().filter(departamento_id=departamento_id)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def por_puesto(self, request):
        """Filtrar empleados por puesto"""
        puesto_id = request.query_params.get('puesto_id')
        
        if not puesto_id:
            return Response({'error': 'Se requiere puesto_id'}, status=status.HTTP_400_BAD_REQUEST)
        
        queryset = self.get_queryset().filter(puesto_id=puesto_id)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class AsignacionTokenViewSet(viewsets.ModelViewSet):
    """ViewSet para gestionar asignaciones de evaluaciones con tokens"""
    
    queryset = AsignacionEvaluacion.objects.all()
    serializer_class = AsignacionEvaluacionSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [SearchFilter, OrderingFilter]
    
    search_fields = ['nombre_asignacion', 'evaluacion_oficial__nombre']
    ordering_fields = ['fecha_creacion', 'fecha_inicio', 'fecha_fin']
    ordering = ['-fecha_creacion']
    
    def get_queryset(self):
        """Filtrar asignaciones según el usuario"""
        user = self.request.user
        
        if hasattr(user, 'perfil') and user.perfil.nivel_usuario == 'superadmin':
            return AsignacionEvaluacion.objects.all()
        elif hasattr(user, 'perfil') and user.perfil.nivel_usuario == 'admin-empresa':
            try:
                empresa = Empresa.objects.get(administrador=user.perfil)
                return AsignacionEvaluacion.objects.filter(empresa=empresa)
            except Empresa.DoesNotExist:
                return AsignacionEvaluacion.objects.none()
        elif hasattr(user, 'perfil') and user.perfil.nivel_usuario == 'admin-planta':
            try:
                from apps.users.models import AdminPlanta
                admin_planta = AdminPlanta.objects.get(usuario=user.perfil, status=True)
                return AsignacionEvaluacion.objects.filter(planta=admin_planta.planta)
            except:
                return AsignacionEvaluacion.objects.none()
        
        return AsignacionEvaluacion.objects.none()
    
    def generar_token_unico(self):
        """Generar token único de 8 caracteres"""
        while True:
            token = ''.join(secrets.choice(string.ascii_uppercase + string.digits) for _ in range(8))
            if not EmpleadoAsignado.objects.filter(token_acceso=token).exists():
                return token
    
    @action(detail=False, methods=['post'])
    def crear_asignacion(self, request):
        """Crear nueva asignación con empleados y tokens"""
        try:
            with transaction.atomic():
                # Validar datos requeridos
                evaluacion_id = request.data.get('evaluacion_id')
                empleados_ids = request.data.get('empleados_ids', [])
                duracion_dias = request.data.get('duracion_dias', 7)
                nombre_asignacion = request.data.get('nombre_asignacion', f'Evaluación {timezone.now().strftime("%d/%m/%Y")}')
                
                if not evaluacion_id or not empleados_ids:
                    return Response({
                        'error': 'Se requiere evaluacion_id y empleados_ids'
                    }, status=status.HTTP_400_BAD_REQUEST)
                
                # Obtener evaluación oficial
                try:
                    evaluacion = EvaluacionOficial.objects.get(id=evaluacion_id)
                except EvaluacionOficial.DoesNotExist:
                    return Response({
                        'error': 'Evaluación no encontrada'
                    }, status=status.HTTP_404_NOT_FOUND)
                
                # Validar empleados pertenecen al usuario
                empleados_validos = self.get_empleados_validos(empleados_ids)
                if not empleados_validos:
                    return Response({
                        'error': 'No se encontraron empleados válidos'
                    }, status=status.HTTP_400_BAD_REQUEST)
                
                # Obtener empresa y planta del usuario
                empresa, planta = self.get_empresa_planta_usuario()
                
                # Crear asignación
                fecha_inicio = timezone.now()
                fecha_fin = fecha_inicio + timezone.timedelta(days=duracion_dias)
                
                asignacion = AsignacionEvaluacion.objects.create(
                    evaluacion_oficial=evaluacion,
                    empresa=empresa,
                    planta=planta,
                    administrador_asignador=request.user.perfil,
                    nombre_asignacion=nombre_asignacion,
                    fecha_inicio=fecha_inicio,
                    fecha_fin=fecha_fin,
                    duracion_dias=duracion_dias,
                    estado='activa'
                )
                
                # Crear empleados asignados con tokens
                empleados_con_tokens = []
                for empleado in empleados_validos:
                    token = self.generar_token_unico()
                    
                    empleado_asignado = EmpleadoAsignado.objects.create(
                        asignacion=asignacion,
                        empleado=empleado,
                        token_acceso=token,
                        fecha_asignacion=timezone.now(),
                        estado='pendiente'
                    )
                    
                    empleados_con_tokens.append({
                        'empleado_id': empleado.id,
                        'nombre_completo': f"{empleado.nombre} {empleado.apellido}",
                        'token': token,
                        'numero_empleado': empleado.numero_empleado if hasattr(empleado, 'numero_empleado') else None
                    })
                
                return Response({
                    'success': True,
                    'message': f'Asignación creada exitosamente para {len(empleados_con_tokens)} empleados',
                    'asignacion_id': asignacion.id,
                    'nombre_asignacion': asignacion.nombre_asignacion,
                    'evaluacion': evaluacion.nombre,
                    'tipo_norma': evaluacion.tipo_norma,
                    'fecha_inicio': asignacion.fecha_inicio,
                    'fecha_fin': asignacion.fecha_fin,
                    'empleados_asignados': empleados_con_tokens,
                    'total_empleados': len(empleados_con_tokens)
                }, status=status.HTTP_201_CREATED)
                
        except Exception as e:
            return Response({
                'error': f'Error al crear asignación: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def get_empleados_validos(self, empleados_ids):
        """Obtener empleados válidos según permisos del usuario"""
        user = self.request.user
        
        if hasattr(user, 'perfil') and user.perfil.nivel_usuario == 'admin-empresa':
            try:
                empresa = Empresa.objects.get(administrador=user.perfil)
                return Empleado.objects.filter(id__in=empleados_ids, empresa=empresa)
            except Empresa.DoesNotExist:
                return Empleado.objects.none()
                
        elif hasattr(user, 'perfil') and user.perfil.nivel_usuario == 'admin-planta':
            try:
                from apps.users.models import AdminPlanta
                admin_planta = AdminPlanta.objects.get(usuario=user.perfil, status=True)
                return Empleado.objects.filter(id__in=empleados_ids, planta=admin_planta.planta)
            except:
                return Empleado.objects.none()
        
        # SuperAdmin puede asignar a cualquier empleado
        elif hasattr(user, 'perfil') and user.perfil.nivel_usuario == 'superadmin':
            return Empleado.objects.filter(id__in=empleados_ids)
        
        return Empleado.objects.none()
    
    def get_empresa_planta_usuario(self):
        """Obtener empresa y planta del usuario logueado"""
        user = self.request.user
        
        if hasattr(user, 'perfil') and user.perfil.nivel_usuario == 'admin-empresa':
            try:
                empresa = Empresa.objects.get(administrador=user.perfil)
                return empresa, None
            except Empresa.DoesNotExist:
                return None, None
                
        elif hasattr(user, 'perfil') and user.perfil.nivel_usuario == 'admin-planta':
            try:
                from apps.users.models import AdminPlanta
                admin_planta = AdminPlanta.objects.get(usuario=user.perfil, status=True)
                return admin_planta.planta.empresa, admin_planta.planta
            except:
                return None, None
        
        return None, None
    
    @action(detail=True, methods=['get'])
    def empleados_asignados(self, request, pk=None):
        """Ver empleados asignados con sus tokens"""
        asignacion = self.get_object()
        empleados = EmpleadoAsignado.objects.filter(asignacion=asignacion)
        
        datos_empleados = []
        for emp_asignado in empleados:
            datos_empleados.append({
                'id': emp_asignado.id,
                'empleado_id': emp_asignado.empleado.id,
                'nombre_completo': f"{emp_asignado.empleado.nombre} {emp_asignado.empleado.apellido}",
                'numero_empleado': emp_asignado.empleado.numero_empleado if hasattr(emp_asignado.empleado, 'numero_empleado') else None,
                'departamento': emp_asignado.empleado.departamento.nombre if emp_asignado.empleado.departamento else None,
                'puesto': emp_asignado.empleado.puesto.nombre if emp_asignado.empleado.puesto else None,
                'token_acceso': emp_asignado.token_acceso,
                'estado': emp_asignado.estado,
                'fecha_asignacion': emp_asignado.fecha_asignacion,
                'fecha_inicio_evaluacion': emp_asignado.fecha_inicio_evaluacion,
                'fecha_completado': emp_asignado.fecha_completado,
                'progreso_porcentaje': emp_asignado.progreso_porcentaje
            })
        
        return Response({
            'asignacion_id': asignacion.id,
            'nombre_asignacion': asignacion.nombre_asignacion,
            'evaluacion': asignacion.evaluacion_oficial.nombre,
            'estado': asignacion.estado,
            'total_empleados': len(datos_empleados),
            'empleados': datos_empleados
        })
    
    @action(detail=False, methods=['get'])
    def activas(self, request):
        """Obtener asignaciones activas"""
        asignaciones_activas = self.get_queryset().filter(
            estado='activa',
            fecha_fin__gt=timezone.now()
        )
        
        datos = []
        for asignacion in asignaciones_activas:
            empleados_count = EmpleadoAsignado.objects.filter(asignacion=asignacion).count()
            completados_count = EmpleadoAsignado.objects.filter(
                asignacion=asignacion, 
                estado='completado'
            ).count()
            
            datos.append({
                'id': asignacion.id,
                'nombre_asignacion': asignacion.nombre_asignacion,
                'evaluacion': asignacion.evaluacion_oficial.nombre,
                'tipo_norma': asignacion.evaluacion_oficial.tipo_norma,
                'fecha_inicio': asignacion.fecha_inicio,
                'fecha_fin': asignacion.fecha_fin,
                'dias_restantes': (asignacion.fecha_fin.date() - timezone.now().date()).days,
                'total_empleados': empleados_count,
                'completados': completados_count,
                'pendientes': empleados_count - completados_count,
                'progreso_porcentaje': (completados_count / empleados_count * 100) if empleados_count > 0 else 0
            })
        
        return Response({
            'asignaciones_activas': datos,
            'total': len(datos)
        })


# ===== ENDPOINT PÚBLICO PARA EMPLEADOS CON TOKEN =====

class EvaluacionTokenViewSet(viewsets.ViewSet):
    """ViewSet público para que empleados accedan con token"""
    
    permission_classes = [permissions.AllowAny]  # Acceso público con token
    
    @action(detail=False, methods=['post'])
    def validar_token(self, request):
        """Validar token de empleado y devolver datos de evaluación"""
        token = request.data.get('token', '').upper().strip()
        
        if not token:
            return Response({
                'error': 'Token requerido'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            # Buscar empleado asignado con el token
            empleado_asignado = EmpleadoAsignado.objects.select_related(
                'asignacion__evaluacion_oficial',
                'empleado'
            ).get(token_acceso=token)
            
            # Validar que la asignación esté activa
            if empleado_asignado.asignacion.estado != 'activa':
                return Response({
                    'error': 'La evaluación ya no está activa'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Validar que no haya expirado
            if empleado_asignado.asignacion.fecha_fin < timezone.now():
                return Response({
                    'error': 'La evaluación ha expirado'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Validar que el empleado no haya completado ya
            if empleado_asignado.estado == 'completado':
                return Response({
                    'error': 'Ya has completado esta evaluación'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Marcar como iniciado si está pendiente
            if empleado_asignado.estado == 'pendiente':
                empleado_asignado.estado = 'en_progreso'
                empleado_asignado.fecha_inicio_evaluacion = timezone.now()
                empleado_asignado.save()
            
            # Obtener preguntas de la evaluación
            evaluacion = empleado_asignado.asignacion.evaluacion_oficial
            preguntas = PreguntaOficial.objects.filter(
                evaluacion_oficial=evaluacion
            ).order_by('numero_orden')
            
            return Response({
                'success': True,
                'empleado': {
                    'nombre': empleado_asignado.empleado.nombre,
                    'apellido': empleado_asignado.empleado.apellido,
                    'id': empleado_asignado.empleado.id
                },
                'evaluacion': {
                    'id': evaluacion.id,
                    'nombre': evaluacion.nombre,
                    'descripcion': evaluacion.descripcion,
                    'tipo_norma': evaluacion.tipo_norma,
                    'instrucciones': evaluacion.instrucciones,
                    'tiempo_limite_minutos': evaluacion.tiempo_limite_minutos,
                    'total_preguntas': preguntas.count()
                },
                'asignacion': {
                    'id': empleado_asignado.asignacion.id,
                    'fecha_fin': empleado_asignado.asignacion.fecha_fin,
                    'dias_restantes': (empleado_asignado.asignacion.fecha_fin.date() - timezone.now().date()).days
                },
                'token_session': token,  # Para mantener la sesión
                'progreso_actual': empleado_asignado.progreso_porcentaje
            }, status=status.HTTP_200_OK)
            
        except EmpleadoAsignado.DoesNotExist:
            return Response({
                'error': 'Token inválido'
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({
                'error': f'Error interno: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @action(detail=False, methods=['get'])
    def obtener_preguntas(self, request):
        """Obtener preguntas de la evaluación con token"""
        token = request.query_params.get('token', '').upper().strip()
        
        if not token:
            return Response({
                'error': 'Token requerido'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            empleado_asignado = EmpleadoAsignado.objects.select_related(
                'asignacion__evaluacion_oficial'
            ).get(token_acceso=token)
            
            # Validaciones básicas
            if empleado_asignado.estado == 'completado':
                return Response({
                    'error': 'Evaluación ya completada'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Obtener preguntas
            evaluacion = empleado_asignado.asignacion.evaluacion_oficial
            preguntas = PreguntaOficial.objects.filter(
                evaluacion_oficial=evaluacion
            ).order_by('numero_orden')
            
            preguntas_data = []
            for pregunta in preguntas:
                pregunta_data = {
                    'id': pregunta.id,
                    'numero_orden': pregunta.numero_orden,
                    'texto_pregunta': pregunta.texto_pregunta,
                    'tipo_pregunta': pregunta.tipo_pregunta,
                    'es_obligatoria': pregunta.es_obligatoria,
                    'seccion': pregunta.seccion_oficial.nombre if pregunta.seccion_oficial else None
                }
                
                # Agregar opciones según el tipo
                if pregunta.tipo_pregunta == 'Múltiple' and pregunta.opciones_multiple:
                    pregunta_data['opciones'] = pregunta.opciones_multiple
                elif pregunta.tipo_pregunta == 'Escala':
                    pregunta_data['escala_min'] = pregunta.escala_min
                    pregunta_data['escala_max'] = pregunta.escala_max
                    pregunta_data['etiquetas_escala'] = pregunta.etiquetas_escala
                
                preguntas_data.append(pregunta_data)
            
            return Response({
                'preguntas': preguntas_data,
                'total': len(preguntas_data),
                'evaluacion': evaluacion.nombre
            })
            
        except EmpleadoAsignado.DoesNotExist:
            return Response({
                'error': 'Token inválido'
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({
                'error': f'Error: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
