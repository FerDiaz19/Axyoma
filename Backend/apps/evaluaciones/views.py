# -*- coding: utf-8 -*-
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q, Count
from django.utils import timezone
from .models import (
    TipoEvaluacion, Pregunta, EvaluacionCompleta, EvaluacionPregunta,
    RespuestaEvaluacion, DetalleRespuesta, ResultadoEvaluacion
)
from .serializers import (
    TipoEvaluacionSerializer, PreguntaSerializer, PreguntaCreateSerializer,
    EvaluacionSerializer, EvaluacionCreateSerializer,
    RespuestaEvaluacionSerializer, RespuestaEvaluacionCreateSerializer,
    ResultadoEvaluacionSerializer
)

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
        
        # Admin empresa ve solo las de su empresa
        if hasattr(user, 'perfil') and user.perfil.nivel_usuario == 'admin-empresa':
            return EvaluacionCompleta.objects.filter(empresa=user.perfil.empresa)
        
        # Otros usuarios ven evaluaciones donde están incluidos
        return EvaluacionCompleta.objects.filter(
            Q(plantas__in=user.perfil.plantas.all()) |
            Q(departamentos__in=user.perfil.departamentos.all()) |
            Q(empleados_objetivo__perfil__user=user)
        ).distinct()
    
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
