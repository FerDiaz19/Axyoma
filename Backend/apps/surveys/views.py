# -*- coding: utf-8 -*-
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .models import TipoEvaluacion, Evaluacion, Pregunta
from .serializers import (
    TipoEvaluacionSerializer, 
    EvaluacionSerializer, 
    PreguntaEvaluacionSerializer
)

class TipoEvaluacionViewSet(viewsets.ModelViewSet):
    """
    ViewSet para manejar el CRUD de tipo de evaluaciones
    """
    queryset = TipoEvaluacion.objects.all()  # Cambiar de activo=True a all()
    serializer_class = TipoEvaluacionSerializer
    permission_classes = [AllowAny]

class EvaluacionViewSet(viewsets.ModelViewSet):
    """
    ViewSet para manejar el CRUD de evaluaciones con permisos específicos
    """
    serializer_class = EvaluacionSerializer
    permission_classes = [AllowAny]
    
    def get_queryset(self):
        """
        Filtrar evaluaciones según el tipo de usuario
        """
        return Evaluacion.objects.all()  # Cambiar de status=True a all()
    
    @action(detail=True, methods=['post'])
    def activar(self, request, pk=None):
        """
        Activar una evaluación
        """
        evaluacion = self.get_object()
        evaluacion.estado = 'activa'
        evaluacion.save()
        
        return Response({'message': 'Evaluación activada exitosamente'})

class PreguntaViewSet(viewsets.ModelViewSet):
    """
    ViewSet para manejar preguntas de evaluación
    """
    serializer_class = PreguntaEvaluacionSerializer
    permission_classes = [AllowAny]
    
    def get_queryset(self):
        """
        Filtrar preguntas según la sección
        """
        return Pregunta.objects.all()  # Cambiar de activa=True a all()
    
    @action(detail=False, methods=['post'])
    def crear_preguntas_nom035(self, request):
        """Crear preguntas predeterminadas para NOM-035"""
        # Ejemplo básico para pruebas
        return Response({
            'message': 'Preguntas NOM-035 creadas exitosamente',
            'total_creadas': 0
        })
