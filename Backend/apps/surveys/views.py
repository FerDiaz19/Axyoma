# -*- coding: utf-8 -*-
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q
from .models import Evaluacion, PreguntaEvaluacion, AplicacionEvaluacion, RespuestaEvaluacion
from .serializers import (
    EvaluacionSerializer, EvaluacionListSerializer, PreguntaEvaluacionSerializer,
    AplicacionEvaluacionSerializer, RespuestaEvaluacionSerializer
)
from apps.users.models import Empleado

class EvaluacionViewSet(viewsets.ModelViewSet):
    """
    ViewSet para manejar el CRUD de evaluaciones con permisos específicos
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """
        Filtrar evaluaciones según el tipo de usuario
        """
        user = self.request.user
        
        if user.is_superuser:
            # SuperAdmin ve todas las evaluaciones
            return Evaluacion.objects.all()
        
        if hasattr(user, 'perfil_usuario'):
            perfil = user.perfil_usuario
            if perfil.es_admin_empresa() or perfil.es_admin_planta():
                # AdminEmpresa/AdminPlanta ven evaluaciones normativas y sus propias internas
                return Evaluacion.objects.filter(
                    Q(tipo='normativa') | 
                    Q(tipo='interna', empresa=perfil.empresa)
                )
        
        return Evaluacion.objects.none()
    
    def get_serializer_class(self):
        """
        Usar serializer diferente para listar vs detalle
        """
        if self.action == 'list':
            return EvaluacionListSerializer
        return EvaluacionSerializer
    
    def perform_create(self, serializer):
        """
        Asignar el usuario creador automáticamente
        """
        user = self.request.user
        
        # Validar permisos de creación
        if serializer.validated_data.get('tipo') == 'normativa':
            if not user.is_superuser:
                raise permissions.PermissionDenied(
                    "Solo los superusuarios pueden crear evaluaciones normativas"
                )
        
        # Asignar usuario creador
        serializer.save(creado_por=user)
    
    def perform_update(self, serializer):
        """
        Validar permisos de edición
        """
        user = self.request.user
        evaluacion = self.get_object()
        
        if not evaluacion.can_user_edit(user):
            raise permissions.PermissionDenied(
                "No tienes permisos para editar esta evaluación"
            )
        
        serializer.save()
    
    def perform_destroy(self, serializer):
        """
        No permitir eliminación, solo desactivación
        """
        raise permissions.PermissionDenied(
            "No se puede eliminar evaluaciones. Use desactivar en su lugar."
        )
    
    @action(detail=True, methods=['post'])
    def desactivar(self, request, pk=None):
        """
        Desactivar una evaluación en lugar de eliminarla
        """
        evaluacion = self.get_object()
        user = request.user
        
        if not evaluacion.can_user_edit(user):
            return Response(
                {'error': 'No tienes permisos para desactivar esta evaluación'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        evaluacion.estado = 'inactiva'
        evaluacion.save()
        
        return Response({'message': 'Evaluación desactivada exitosamente'})
    
    @action(detail=True, methods=['post'])
    def activar(self, request, pk=None):
        """
        Activar una evaluación
        """
        evaluacion = self.get_object()
        user = request.user
        
        if not evaluacion.can_user_edit(user):
            return Response(
                {'error': 'No tienes permisos para activar esta evaluación'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        evaluacion.estado = 'activa'
        evaluacion.save()
        
        return Response({'message': 'Evaluación activada exitosamente'})
    
    @action(detail=False, methods=['get'])
    def normativas(self, request):
        """
        Obtener solo evaluaciones normativas
        """
        evaluaciones = Evaluacion.objects.filter(tipo='normativa', estado='activa')
        serializer = EvaluacionListSerializer(evaluaciones, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def internas(self, request):
        """
        Obtener solo evaluaciones internas de la empresa del usuario
        """
        user = request.user
        
        if not hasattr(user, 'perfil_usuario'):
            return Response(
                {'error': 'Usuario sin perfil válido'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        perfil = user.perfil_usuario
        evaluaciones = Evaluacion.objects.filter(
            tipo='interna', 
            empresa=perfil.empresa,
            estado='activa'
        )
        serializer = EvaluacionListSerializer(evaluaciones, many=True)
        return Response(serializer.data)

class PreguntaEvaluacionViewSet(viewsets.ModelViewSet):
    """
    ViewSet para manejar preguntas de evaluación
    """
    serializer_class = PreguntaEvaluacionSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """
        Filtrar preguntas según la evaluación
        """
        evaluacion_id = self.request.query_params.get('evaluacion_id')
        if evaluacion_id:
            return PreguntaEvaluacion.objects.filter(evaluacion_id=evaluacion_id)
        return PreguntaEvaluacion.objects.all()
    
    def perform_create(self, serializer):
        """
        Validar que el usuario pueda crear preguntas para la evaluación
        """
        evaluacion = serializer.validated_data['evaluacion']
        user = self.request.user
        
        if not evaluacion.can_user_edit(user):
            raise permissions.PermissionDenied(
                "No tienes permisos para crear preguntas en esta evaluación"
            )
        
        serializer.save()
    
    def perform_update(self, serializer):
        """
        Validar que el usuario pueda editar preguntas
        """
        pregunta = self.get_object()
        user = self.request.user
        
        if not pregunta.evaluacion.can_user_edit(user):
            raise permissions.PermissionDenied(
                "No tienes permisos para editar preguntas en esta evaluación"
            )
        
        serializer.save()

class AplicacionEvaluacionViewSet(viewsets.ModelViewSet):
    """
    ViewSet para manejar aplicaciones de evaluación
    """
    serializer_class = AplicacionEvaluacionSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """
        Filtrar aplicaciones según el usuario
        """
        user = self.request.user
        
        if user.is_superuser:
            return AplicacionEvaluacion.objects.all()
        
        if hasattr(user, 'perfil_usuario'):
            perfil = user.perfil_usuario
            if perfil.es_admin_empresa() or perfil.es_admin_planta():
                # Ver aplicaciones de su empresa
                return AplicacionEvaluacion.objects.filter(
                    evaluacion__empresa=perfil.empresa
                )
        
        return AplicacionEvaluacion.objects.none()
    
    def perform_create(self, serializer):
        """
        Asignar el usuario que aplica la evaluación
        """
        serializer.save(aplicada_por=self.request.user)
    
    @action(detail=True, methods=['post'])
    def iniciar(self, request, pk=None):
        """
        Iniciar una aplicación de evaluación
        """
        aplicacion = self.get_object()
        
        if aplicacion.estado != 'programada':
            return Response(
                {'error': 'La aplicación no está en estado programada'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        aplicacion.estado = 'en_progreso'
        aplicacion.fecha_inicio = timezone.now()
        aplicacion.save()
        
        return Response({'message': 'Aplicación iniciada exitosamente'})
    
    @action(detail=True, methods=['post'])
    def finalizar(self, request, pk=None):
        """
        Finalizar una aplicación de evaluación
        """
        aplicacion = self.get_object()
        
        if aplicacion.estado != 'en_progreso':
            return Response(
                {'error': 'La aplicación no está en progreso'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        aplicacion.estado = 'completada'
        aplicacion.fecha_fin = timezone.now()
        aplicacion.save()
        
        return Response({'message': 'Aplicación finalizada exitosamente'})
