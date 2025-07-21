# -*- coding: utf-8 -*-
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q, Count
from django.utils import timezone
from django.shortcuts import get_object_or_404
from .models import (
    TipoEvaluacion, Pregunta, EvaluacionCompleta, EvaluacionPregunta,
    RespuestaEvaluacion, DetalleRespuesta, ResultadoEvaluacion,
    AsignacionEvaluacion, TokenEvaluacion
)
from .serializers import (
    TipoEvaluacionSerializer, PreguntaSerializer, PreguntaCreateSerializer,
    EvaluacionSerializer, EvaluacionCreateSerializer,
    RespuestaEvaluacionSerializer, RespuestaEvaluacionCreateSerializer,
    ResultadoEvaluacionSerializer, AsignacionEvaluacionSerializer,
    TokenEvaluacionSerializer, AsignacionMasivaSerializer,
    FiltroEmpleadosSerializer, EmpleadoEvaluacionSerializer
)
from .utils import crear_token_evaluacion, validar_token
from apps.users.models import Empleado

@method_decorator(csrf_exempt, name='dispatch')
class TipoEvaluacionViewSet(viewsets.ModelViewSet):
    queryset = TipoEvaluacion.objects.filter(activo=True)
    serializer_class = TipoEvaluacionSerializer
    permission_classes = [permissions.IsAuthenticated]

@method_decorator(csrf_exempt, name='dispatch')
class PreguntaViewSet(viewsets.ModelViewSet):
    serializer_class = PreguntaSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        queryset = Pregunta.objects.filter(activa=True)
        
        # Filtros por parámetros
        tipo_evaluacion = self.request.query_params.get('tipo_evaluacion')
        if tipo_evaluacion:
            queryset = queryset.filter(tipo_evaluacion__nombre=tipo_evaluacion)
        
        # SuperAdmin ve todas las preguntas
        if hasattr(user, 'perfil') and user.perfil.nivel_usuario == 'superadmin':
            return queryset
        
        # Admin empresa ve preguntas oficiales + las de su empresa
        if hasattr(user, 'perfil') and user.perfil.nivel_usuario == 'admin-empresa':
            return queryset.filter(
                Q(empresa__isnull=True) |  # Preguntas oficiales
                Q(empresa=user.perfil.empresa)  # Preguntas de su empresa
            )
        
        # Otros usuarios solo ven preguntas oficiales
        return queryset.filter(empresa__isnull=True)
    
    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return PreguntaCreateSerializer
        return PreguntaSerializer
    
    @action(detail=False, methods=['get'])
    def por_tipo(self, request):
        """Obtener preguntas agrupadas por tipo de evaluación"""
        tipo = request.query_params.get('tipo')
        if not tipo:
            return Response({'error': 'Tipo de evaluación requerido'}, status=status.HTTP_400_BAD_REQUEST)
        
        preguntas = self.get_queryset().filter(tipo_evaluacion__nombre=tipo)
        serializer = self.get_serializer(preguntas, many=True)
        
        return Response({
            'tipo_evaluacion': tipo,
            'total_preguntas': preguntas.count(),
            'preguntas': serializer.data
        })
    
    @action(detail=False, methods=['post'])
    def crear_oficiales(self, request):
        """Crear preguntas oficiales (solo superadmin)"""
        if not (hasattr(request.user, 'perfil') and request.user.perfil.nivel_usuario == 'superadmin'):
            return Response({'error': 'No tienes permisos para crear preguntas oficiales'}, 
                          status=status.HTTP_403_FORBIDDEN)
        
        # Crear preguntas predeterminadas
        preguntas_creadas = self._crear_preguntas_oficiales()
        
        return Response({
            'message': f'Se crearon {preguntas_creadas} preguntas oficiales',
            'preguntas_creadas': preguntas_creadas
        })
    
    def _crear_preguntas_oficiales(self):
        """Crear preguntas oficiales para NOM-035, NOM-030 y 360°"""
        preguntas_data = [
            # NOM-035
            {
                'tipo': 'NOM-035',
                'preguntas': [
                    {
                        'texto': '¿Consideras que tu carga de trabajo es excesiva?',
                        'tipo_respuesta': 'escala',
                        'opciones': ['Nunca', 'Casi nunca', 'A veces', 'Casi siempre', 'Siempre']
                    },
                    {
                        'texto': '¿Tienes control sobre tu trabajo?',
                        'tipo_respuesta': 'escala',
                        'opciones': ['Nunca', 'Casi nunca', 'A veces', 'Casi siempre', 'Siempre']
                    },
                    {
                        'texto': '¿Recibes apoyo de tus compañeros?',
                        'tipo_respuesta': 'escala',
                        'opciones': ['Nunca', 'Casi nunca', 'A veces', 'Casi siempre', 'Siempre']
                    },
                    {
                        'texto': '¿Tu supervisor te brinda apoyo?',
                        'tipo_respuesta': 'escala',
                        'opciones': ['Nunca', 'Casi nunca', 'A veces', 'Casi siempre', 'Siempre']
                    },
                    {
                        'texto': '¿Sientes que tu trabajo es reconocido?',
                        'tipo_respuesta': 'escala',
                        'opciones': ['Nunca', 'Casi nunca', 'A veces', 'Casi siempre', 'Siempre']
                    }
                ]
            },
            # NOM-030
            {
                'tipo': 'NOM-030',
                'preguntas': [
                    {
                        'texto': '¿Conoces los procedimientos de seguridad de tu área?',
                        'tipo_respuesta': 'si_no',
                        'opciones': ['Sí', 'No']
                    },
                    {
                        'texto': '¿Utilizas el equipo de protección personal requerido?',
                        'tipo_respuesta': 'si_no',
                        'opciones': ['Sí', 'No']
                    },
                    {
                        'texto': '¿Has recibido capacitación en seguridad en los últimos 6 meses?',
                        'tipo_respuesta': 'si_no',
                        'opciones': ['Sí', 'No']
                    },
                    {
                        'texto': '¿Reportas los incidentes de seguridad?',
                        'tipo_respuesta': 'si_no',
                        'opciones': ['Sí', 'No']
                    },
                    {
                        'texto': '¿Consideras que tu área de trabajo es segura?',
                        'tipo_respuesta': 'escala',
                        'opciones': ['Muy insegura', 'Insegura', 'Regular', 'Segura', 'Muy segura']
                    }
                ]
            },
            # 360°
            {
                'tipo': '360',
                'preguntas': [
                    {
                        'texto': '¿Cómo evalúas la comunicación del empleado?',
                        'tipo_respuesta': 'escala',
                        'opciones': ['Deficiente', 'Regular', 'Buena', 'Muy buena', 'Excelente']
                    },
                    {
                        'texto': '¿Cómo evalúas el trabajo en equipo?',
                        'tipo_respuesta': 'escala',
                        'opciones': ['Deficiente', 'Regular', 'Buena', 'Muy buena', 'Excelente']
                    },
                    {
                        'texto': '¿Cómo evalúas la iniciativa y proactividad?',
                        'tipo_respuesta': 'escala',
                        'opciones': ['Deficiente', 'Regular', 'Buena', 'Muy buena', 'Excelente']
                    },
                    {
                        'texto': '¿Cómo evalúas el cumplimiento de objetivos?',
                        'tipo_respuesta': 'escala',
                        'opciones': ['Deficiente', 'Regular', 'Buena', 'Muy buena', 'Excelente']
                    },
                    {
                        'texto': '¿Qué aspectos considera que debe mejorar?',
                        'tipo_respuesta': 'texto',
                        'opciones': []
                    }
                ]
            }
        ]
        
        total_creadas = 0
        for tipo_data in preguntas_data:
            tipo_eval, _ = TipoEvaluacion.objects.get_or_create(
                nombre=tipo_data['tipo'],
                defaults={
                    'descripcion': f'Evaluación {tipo_data["tipo"]}',
                    'normativa_oficial': tipo_data['tipo'].startswith('NOM')
                }
            )
            
            for i, pregunta_data in enumerate(tipo_data['preguntas'], 1):
                pregunta, created = Pregunta.objects.get_or_create(
                    tipo_evaluacion=tipo_eval,
                    texto_pregunta=pregunta_data['texto'],
                    defaults={
                        'tipo_respuesta': pregunta_data['tipo_respuesta'],
                        'opciones_respuesta': pregunta_data['opciones'],
                        'orden': i,
                        'creada_por': self.request.user
                    }
                )
                if created:
                    total_creadas += 1
        
        return total_creadas

@method_decorator(csrf_exempt, name='dispatch')
class EvaluacionViewSet(viewsets.ModelViewSet):
    serializer_class = EvaluacionSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        
        # SuperAdmin ve todas las evaluaciones
        if hasattr(user, 'perfil') and user.perfil.nivel_usuario == 'superadmin':
            return EvaluacionCompleta.objects.all()
        
        # Inicializar queryset vacío
        queryset = EvaluacionCompleta.objects.none()
        
        # Siempre incluir evaluaciones normativas (NOM-035, NOM-030, 360)
        evaluaciones_normativas = EvaluacionCompleta.objects.filter(empresa__isnull=True)
        
        # Admin empresa ve evaluaciones normativas + las de su empresa
        if hasattr(user, 'perfil') and user.perfil.nivel_usuario == 'admin-empresa':
            try:
                # Buscar empresa administrada por este usuario
                from apps.users.models import Empresa
                empresa = Empresa.objects.get(administrador=user.perfil)
                evaluaciones_empresa = EvaluacionCompleta.objects.filter(empresa=empresa)
                queryset = evaluaciones_normativas.union(evaluaciones_empresa)
            except Empresa.DoesNotExist:
                # Si no administra empresa, solo ve normativas
                queryset = evaluaciones_normativas
        
        # Otros usuarios ven evaluaciones normativas + donde están incluidos
        else:
            evaluaciones_acceso = EvaluacionCompleta.objects.filter(
                Q(plantas__in=user.perfil.plantas.all()) |
                Q(departamentos__in=user.perfil.departamentos.all()) |
                Q(empleados_objetivo__perfil__user=user)
            ).distinct()
            queryset = evaluaciones_normativas.union(evaluaciones_acceso)
        
        return queryset
    
    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return EvaluacionCreateSerializer
        return EvaluacionSerializer
    
    @action(detail=True, methods=['post'])
    def activar(self, request, pk=None):
        """Activar una evaluación"""
        evaluacion = self.get_object()
        
        if evaluacion.estado != 'borrador':
            return Response({'error': 'Solo se pueden activar evaluaciones en borrador'}, 
                          status=status.HTTP_400_BAD_REQUEST)
        
        evaluacion.estado = 'activa'
        evaluacion.save()
        
        return Response({'message': 'Evaluación activada exitosamente'})
    
    @action(detail=True, methods=['get'])
    def resultados(self, request, pk=None):
        """Obtener resultados de una evaluación"""
        evaluacion = self.get_object()
        
        try:
            resultado = ResultadoEvaluacion.objects.get(evaluacion=evaluacion)
            serializer = ResultadoEvaluacionSerializer(resultado)
            return Response(serializer.data)
        except ResultadoEvaluacion.DoesNotExist:
            # Calcular resultados si no existen
            return self._calcular_resultados(evaluacion)
    
    def _calcular_resultados(self, evaluacion):
        """Calcular resultados de una evaluación"""
        respuestas = RespuestaEvaluacion.objects.filter(evaluacion=evaluacion, completada=True)
        total_respuestas = respuestas.count()
        
        if total_respuestas == 0:
            return Response({'error': 'No hay respuestas para calcular resultados'}, 
                          status=status.HTTP_400_BAD_REQUEST)
        
        # Calcular métricas básicas
        total_empleados_objetivo = evaluacion.empleados_objetivo.count()
        if total_empleados_objetivo == 0:
            # Si no hay empleados específicos, contar por plantas/departamentos
            total_empleados_objetivo = 100  # Valor estimado
        
        porcentaje_participacion = (total_respuestas / total_empleados_objetivo) * 100
        
        # Crear o actualizar resultado
        resultado, created = ResultadoEvaluacion.objects.get_or_create(
            evaluacion=evaluacion,
            defaults={
                'total_respuestas': total_respuestas,
                'porcentaje_participacion': porcentaje_participacion,
                'resultados_detallados': {},
                'recomendaciones': 'Resultados calculados automáticamente'
            }
        )
        
        serializer = ResultadoEvaluacionSerializer(resultado)
        return Response(serializer.data)

@method_decorator(csrf_exempt, name='dispatch')
class RespuestaEvaluacionViewSet(viewsets.ModelViewSet):
    serializer_class = RespuestaEvaluacionSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        
        # SuperAdmin ve todas las respuestas
        if hasattr(user, 'perfil') and user.perfil.nivel_usuario == 'superadmin':
            return RespuestaEvaluacion.objects.all()
        
        # Admin empresa ve respuestas de su empresa
        if hasattr(user, 'perfil') and user.perfil.nivel_usuario == 'admin-empresa':
            return RespuestaEvaluacion.objects.filter(evaluacion__empresa=user.perfil.empresa)
        
        # Empleados ven solo sus respuestas
        return RespuestaEvaluacion.objects.filter(empleado__perfil__user=user)
    
    def get_serializer_class(self):
        if self.action in ['create']:
            return RespuestaEvaluacionCreateSerializer
        return RespuestaEvaluacionSerializer
    
    @action(detail=False, methods=['get'])
    def mis_evaluaciones(self, request):
        """Obtener evaluaciones disponibles para el usuario actual"""
        user = request.user
        
        if not hasattr(user, 'perfil'):
            return Response({'error': 'Usuario sin perfil'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Buscar evaluaciones donde el usuario está incluido
        evaluaciones = EvaluacionCompleta.objects.filter(
            estado='activa',
            fecha_inicio__lte=timezone.now(),
            fecha_fin__gte=timezone.now()
        ).filter(
            Q(empleados_objetivo__perfil__user=user) |
            Q(departamentos__in=user.perfil.departamentos.all()) |
            Q(plantas__in=user.perfil.plantas.all())
        ).distinct()
        
        # Filtrar las que no ha respondido
        evaluaciones_sin_responder = []
        for evaluacion in evaluaciones:
            if not RespuestaEvaluacion.objects.filter(evaluacion=evaluacion, empleado__perfil__user=user).exists():
                evaluaciones_sin_responder.append(evaluacion)
        
        serializer = EvaluacionSerializer(evaluaciones_sin_responder, many=True)
        return Response(serializer.data)

@method_decorator(csrf_exempt, name='dispatch')
class AsignacionEvaluacionViewSet(viewsets.ModelViewSet):
    serializer_class = AsignacionEvaluacionSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        
        # SuperAdmin ve todas las asignaciones
        if hasattr(user, 'perfil') and user.perfil.nivel_usuario == 'superadmin':
            return AsignacionEvaluacion.objects.all()
        
        # Admin empresa ve asignaciones de su empresa
        if hasattr(user, 'perfil') and user.perfil.nivel_usuario == 'admin-empresa':
            return AsignacionEvaluacion.objects.filter(evaluacion__empresa=user.perfil.empresa)
        
        # Admin planta ve asignaciones de sus plantas
        if hasattr(user, 'perfil') and user.perfil.nivel_usuario == 'admin-planta':
            return AsignacionEvaluacion.objects.filter(empleado__planta__in=user.perfil.plantas.all())
        
        # Empleados ven solo sus asignaciones
        return AsignacionEvaluacion.objects.filter(empleado__perfil__user=user)
    
    @action(detail=False, methods=['post'])
    def activar_evaluacion(self, request):
        """Activar evaluación y permitir selección de empleados"""
        evaluacion_id = request.data.get('evaluacion_id')
        
        try:
            evaluacion = EvaluacionCompleta.objects.get(id=evaluacion_id)
            
            # Verificar permisos
            if not self._tiene_permiso_evaluacion(request.user, evaluacion):
                return Response({'error': 'Sin permisos para esta evaluación'}, 
                              status=status.HTTP_403_FORBIDDEN)
            
            # Cambiar estado a activa
            evaluacion.estado = 'activa'
            evaluacion.save()
            
            return Response({'message': 'Evaluación activada correctamente'})
            
        except EvaluacionCompleta.DoesNotExist:
            return Response({'error': 'Evaluación no encontrada'}, 
                          status=status.HTTP_404_NOT_FOUND)
    
    @action(detail=True, methods=['get'])
    def empleados_asignados(self, request, pk=None):
        """Obtener empleados asignados a una evaluación específica"""
        try:
            evaluacion = EvaluacionCompleta.objects.get(pk=pk)
            
            # Verificar permisos
            if not self._tiene_permiso_evaluacion(request.user, evaluacion):
                return Response({'error': 'Sin permisos para esta evaluación'}, 
                              status=status.HTTP_403_FORBIDDEN)
            
            # Obtener asignaciones de esta evaluación
            asignaciones = AsignacionEvaluacion.objects.filter(evaluacion=evaluacion).select_related(
                'empleado', 'empleado__departamento', 'empleado__planta'
            )
            
            empleados_data = []
            for asignacion in asignaciones:
                empleado_info = {
                    'asignacion_id': asignacion.id,
                    'empleado_id': asignacion.empleado.empleado_id,
                    'nombre': asignacion.empleado.nombre,
                    'apellido': asignacion.empleado.apellido,
                    'numero_empleado': asignacion.empleado.numero_empleado,
                    'email': asignacion.empleado.email,
                    'puesto': asignacion.empleado.puesto,
                    'departamento': asignacion.empleado.departamento.nombre if asignacion.empleado.departamento else None,
                    'planta': asignacion.empleado.planta.nombre if asignacion.empleado.planta else None,
                    'estado_asignacion': asignacion.estado,
                    'fecha_asignacion': asignacion.fecha_asignacion,
                    'fecha_inicio': asignacion.fecha_inicio,
                    'fecha_fin': asignacion.fecha_fin,
                    'fecha_completado': asignacion.fecha_completado,
                    'duracion_dias': asignacion.duracion_dias,
                    'duracion_horas': asignacion.duracion_horas,
                    'dias_restantes': asignacion.dias_restantes,
                    'porcentaje_tiempo_usado': asignacion.porcentaje_tiempo_usado,
                    'intentos_acceso': asignacion.intentos_acceso,
                    'fecha_ultimo_acceso': asignacion.fecha_ultimo_acceso,
                    'token_activo': hasattr(asignacion, 'token') and asignacion.token.activo if hasattr(asignacion, 'token') else False
                }
                empleados_data.append(empleado_info)
            
            # Estadísticas resumen
            total_empleados = len(empleados_data)
            por_estado = {}
            for asignacion in asignaciones:
                estado = asignacion.estado
                por_estado[estado] = por_estado.get(estado, 0) + 1
            
            response_data = {
                'evaluacion_id': evaluacion.id,
                'evaluacion_titulo': evaluacion.titulo,
                'evaluacion_tipo': evaluacion.tipo_evaluacion.nombre,
                'total_empleados_asignados': total_empleados,
                'resumen_estados': por_estado,
                'empleados': empleados_data
            }
            
            return Response(response_data)
            
        except EvaluacionCompleta.DoesNotExist:
            return Response({'error': 'Evaluación no encontrada'}, 
                          status=status.HTTP_404_NOT_FOUND)

    @action(detail=False, methods=['post'])
    def obtener_empleados_filtrados(self, request):
        """Obtener empleados filtrados para asignación"""
        serializer = FiltroEmpleadosSerializer(data=request.data)
        
        if serializer.is_valid():
            filtros = serializer.validated_data
            queryset = Empleado.objects.all()
            
            # Filtrar por empresa del usuario
            if hasattr(request.user, 'perfil'):
                queryset = queryset.filter(empresa=request.user.perfil.empresa)
            
            # Aplicar filtros
            if filtros.get('planta_id'):
                queryset = queryset.filter(planta_id=filtros['planta_id'])
            
            if filtros.get('departamento_id'):
                queryset = queryset.filter(departamento_id=filtros['departamento_id'])
            
            if filtros.get('empleados_ids'):
                queryset = queryset.filter(id__in=filtros['empleados_ids'])
            
            serializer_empleados = EmpleadoEvaluacionSerializer(queryset, many=True)
            return Response(serializer_empleados.data)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['post'])
    def asignar_masivo(self, request):
        """Asignar evaluación a múltiples empleados"""
        serializer = AsignacionMasivaSerializer(data=request.data)
        
        if serializer.is_valid():
            data = serializer.validated_data
            
            try:
                evaluacion = EvaluacionCompleta.objects.get(id=data['evaluacion_id'])
                
                # Verificar permisos
                if not self._tiene_permiso_evaluacion(request.user, evaluacion):
                    return Response({'error': 'Sin permisos para esta evaluación'}, 
                                  status=status.HTTP_403_FORBIDDEN)
                
                # Crear asignaciones
                asignaciones_creadas = []
                tokens_creados = []
                
                for empleado_id in data['empleados_ids']:
                    try:
                        empleado = Empleado.objects.get(empleado_id=empleado_id)
                        
                        # Verificar si ya tiene una evaluación activa
                        evaluacion_activa = AsignacionEvaluacion.objects.filter(
                            empleado=empleado,
                            estado__in=['pendiente', 'en_progreso']
                        ).first()
                        
                        if evaluacion_activa:
                            continue  # Saltar este empleado si ya tiene una evaluación activa
                        
                        # Crear asignación
                        defaults = {
                            'fecha_inicio': data['fecha_inicio'],
                            'fecha_fin': data['fecha_fin'],
                            'asignado_por': request.user,
                            'estado': 'pendiente'
                        }
                        
                        # Agregar nuevos campos si están presentes
                        if 'duracion_dias' in data:
                            defaults['duracion_dias'] = data['duracion_dias']
                        if 'duracion_horas' in data:
                            defaults['duracion_horas'] = data['duracion_horas']
                        if 'instrucciones_especiales' in data:
                            defaults['instrucciones_especiales'] = data['instrucciones_especiales']
                        
                        asignacion, created = AsignacionEvaluacion.objects.get_or_create(
                            evaluacion=evaluacion,
                            empleado=empleado,
                            defaults=defaults
                        )
                        
                        if created:
                            asignaciones_creadas.append(asignacion)
                            
                            # Crear token
                            token = crear_token_evaluacion(asignacion)
                            tokens_creados.append(token)
                    
                    except Empleado.DoesNotExist:
                        continue
                
                return Response({
                    'message': f'Se crearon {len(asignaciones_creadas)} asignaciones',
                    'asignaciones': AsignacionEvaluacionSerializer(asignaciones_creadas, many=True).data,
                    'tokens': TokenEvaluacionSerializer(tokens_creados, many=True).data
                })
                
            except EvaluacionCompleta.DoesNotExist:
                return Response({'error': 'Evaluación no encontrada'}, 
                              status=status.HTTP_404_NOT_FOUND)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['get'])
    def evaluaciones_activas(self, request):
        """Obtener evaluaciones activas con sus asignaciones y tokens"""
        user = request.user
        
        if not hasattr(user, 'perfil'):
            return Response({'error': 'Usuario sin perfil'}, 
                          status=status.HTTP_403_FORBIDDEN)
        
        perfil = user.perfil
        
        # Filtrar asignaciones según el tipo de usuario
        if perfil.nivel_usuario == 'superadmin':
            asignaciones = AsignacionEvaluacion.objects.filter(
                estado__in=['pendiente', 'en_progreso']
            ).select_related('evaluacion', 'empleado', 'empleado__departamento', 'empleado__puesto')
        elif perfil.nivel_usuario == 'admin-empresa':
            asignaciones = AsignacionEvaluacion.objects.filter(
                evaluacion__empresa=perfil.empresa,
                estado__in=['pendiente', 'en_progreso']
            ).select_related('evaluacion', 'empleado', 'empleado__departamento', 'empleado__puesto')
        else:
            return Response({'error': 'Sin permisos'}, 
                          status=status.HTTP_403_FORBIDDEN)
        
        # Agrupar por evaluación
        evaluaciones_data = {}
        
        for asignacion in asignaciones:
            evaluacion_id = asignacion.evaluacion.id
            
            if evaluacion_id not in evaluaciones_data:
                # Calcular tiempo restante
                from django.utils import timezone
                tiempo_restante = None
                if asignacion.fecha_fin:
                    diff = asignacion.fecha_fin - timezone.now()
                    if diff.total_seconds() > 0:
                        dias = diff.days
                        horas = diff.seconds // 3600
                        tiempo_restante = f"{dias} días, {horas} horas"
                    else:
                        tiempo_restante = "Expirada"
                
                evaluaciones_data[evaluacion_id] = {
                    'evaluacion': {
                        'id': asignacion.evaluacion.id,
                        'titulo': asignacion.evaluacion.titulo,
                        'descripcion': asignacion.evaluacion.descripcion,
                        'estado': asignacion.evaluacion.estado,
                        'fecha_inicio': asignacion.fecha_inicio,
                        'fecha_fin': asignacion.fecha_fin,
                        'tiempo_restante': tiempo_restante
                    },
                    'asignaciones': [],
                    'total_empleados': 0,
                    'completadas': 0,
                    'pendientes': 0
                }
            
            # Obtener token de esta asignación
            try:
                token = TokenEvaluacion.objects.get(asignacion=asignacion)
                token_data = {
                    'token': token.token,
                    'activo': token.activo,
                    'usado': token.usado,
                    'fecha_expiracion': token.fecha_expiracion
                }
            except TokenEvaluacion.DoesNotExist:
                token_data = None
            
            # Agregar asignación
            asignacion_data = {
                'id': asignacion.id,
                'empleado': {
                    'id': asignacion.empleado.empleado_id,
                    'nombre': f"{asignacion.empleado.nombre} {asignacion.empleado.apellido_paterno}",
                    'departamento': asignacion.empleado.departamento.nombre if asignacion.empleado.departamento else 'N/A',
                    'puesto': asignacion.empleado.puesto.nombre if asignacion.empleado.puesto else 'N/A'
                },
                'estado': asignacion.estado,
                'fecha_asignacion': asignacion.fecha_creacion if hasattr(asignacion, 'fecha_creacion') else None,
                'token': token_data
            }
            
            evaluaciones_data[evaluacion_id]['asignaciones'].append(asignacion_data)
            evaluaciones_data[evaluacion_id]['total_empleados'] += 1
            
            if asignacion.estado == 'completada':
                evaluaciones_data[evaluacion_id]['completadas'] += 1
            else:
                evaluaciones_data[evaluacion_id]['pendientes'] += 1
        
        return Response({
            'evaluaciones_activas': list(evaluaciones_data.values()),
            'total_evaluaciones': len(evaluaciones_data)
        })
    
    def _tiene_permiso_evaluacion(self, user, evaluacion):
        """Verificar si el usuario tiene permisos sobre la evaluación"""
        if not hasattr(user, 'perfil'):
            return False
        
        perfil = user.perfil
        
        # SuperAdmin tiene todos los permisos
        if perfil.nivel_usuario == 'superadmin':
            return True
        
        # Admin empresa debe ser de la misma empresa
        if perfil.nivel_usuario == 'admin-empresa':
            return evaluacion.empresa == perfil.empresa
        
        # Admin planta debe tener plantas relacionadas
        if perfil.nivel_usuario == 'admin-planta':
            return evaluacion.plantas.filter(id__in=perfil.plantas.all()).exists()
        
        return False

@method_decorator(csrf_exempt, name='dispatch')
class TokenEvaluacionViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = TokenEvaluacionSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        
        # SuperAdmin ve todos los tokens
        if hasattr(user, 'perfil') and user.perfil.nivel_usuario == 'superadmin':
            return TokenEvaluacion.objects.all()
        
        # Admin empresa ve tokens de su empresa
        if hasattr(user, 'perfil') and user.perfil.nivel_usuario == 'admin-empresa':
            return TokenEvaluacion.objects.filter(asignacion__evaluacion__empresa=user.perfil.empresa)
        
        # Admin planta ve tokens de sus plantas
        if hasattr(user, 'perfil') and user.perfil.nivel_usuario == 'admin-planta':
            return TokenEvaluacion.objects.filter(asignacion__empleado__planta__in=user.perfil.plantas.all())
        
        return TokenEvaluacion.objects.none()
    
    @action(detail=False, methods=['post'])
    def validar_token(self, request):
        """Validar un token de evaluación"""
        token = request.data.get('token')
        
        if not token:
            return Response({'error': 'Token requerido'}, status=status.HTTP_400_BAD_REQUEST)
        
        asignacion = validar_token(token)
        
        if asignacion:
            return Response({
                'valid': True,
                'empleado': {
                    'id': asignacion.empleado.id,
                    'nombre': asignacion.empleado.nombre,
                    'apellido': asignacion.empleado.apellido,
                    'numero_empleado': asignacion.empleado.numero_empleado,
                    'departamento': asignacion.empleado.departamento.nombre if asignacion.empleado.departamento else None,
                    'planta': asignacion.empleado.planta.nombre if asignacion.empleado.planta else None,
                },
                'evaluacion': {
                    'id': asignacion.evaluacion.id,
                    'titulo': asignacion.evaluacion.titulo,
                    'descripcion': asignacion.evaluacion.descripcion,
                    'fecha_fin': asignacion.fecha_fin,
                },
                'asignacion': {
                    'id': asignacion.id,
                    'estado': asignacion.estado,
                    'fecha_inicio': asignacion.fecha_inicio,
                    'fecha_fin': asignacion.fecha_fin,
                }
            })
        else:
            return Response({'valid': False, 'error': 'Token inválido o expirado'}, 
                          status=status.HTTP_400_BAD_REQUEST)


class TokenValidationViewSet(viewsets.ViewSet):
    """ViewSet para validación de tokens de empleados"""
    permission_classes = [permissions.AllowAny]  # No requiere autenticación
    
    @action(detail=False, methods=['post'])
    def validar_token(self, request):
        """Validar token de empleado y devolver información de la evaluación"""
        token_value = request.data.get('token')
        
        if not token_value:
            return Response({'error': 'Token requerido'}, 
                          status=status.HTTP_400_BAD_REQUEST)
        
        try:
            token = TokenEvaluacion.objects.get(
                token=token_value,
                activo=True,
                usado=False,
                fecha_expiracion__gt=timezone.now()
            )
            
            asignacion = token.asignacion
            empleado = asignacion.empleado
            evaluacion = asignacion.evaluacion
            
            return Response({
                'valido': True,
                'empleado': {
                    'id': empleado.empleado_id,
                    'nombre': empleado.nombre,
                    'apellido_paterno': empleado.apellido_paterno,
                    'apellido_materno': empleado.apellido_materno,
                    'departamento': empleado.departamento.nombre if empleado.departamento else '',
                    'puesto': empleado.puesto.nombre if empleado.puesto else '',
                },
                'evaluacion': {
                    'id': evaluacion.id,
                    'titulo': evaluacion.titulo,
                    'descripcion': evaluacion.descripcion,
                    'fecha_inicio': asignacion.fecha_inicio,
                    'fecha_fin': asignacion.fecha_fin,
                },
                'token_info': {
                    'id': token.id,
                    'fecha_expiracion': token.fecha_expiracion,
                }
            })
            
        except TokenEvaluacion.DoesNotExist:
            return Response({'valido': False, 'error': 'Token inválido o expirado'}, 
                          status=status.HTTP_404_NOT_FOUND)
