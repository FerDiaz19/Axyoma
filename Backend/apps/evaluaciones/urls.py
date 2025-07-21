# -*- coding: utf-8 -*-
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    TipoEvaluacionViewSet, PreguntaViewSet, 
    EvaluacionViewSet, RespuestaEvaluacionViewSet,
    AsignacionEvaluacionViewSet, TokenEvaluacionViewSet,
    TokenValidationViewSet
)

router = DefaultRouter()
router.register(r'tipos', TipoEvaluacionViewSet)
router.register(r'preguntas', PreguntaViewSet, basename='pregunta')
router.register(r'evaluaciones', EvaluacionViewSet, basename='evaluacion')
router.register(r'respuestas', RespuestaEvaluacionViewSet, basename='respuesta')
router.register(r'asignaciones', AsignacionEvaluacionViewSet, basename='asignacion')
router.register(r'tokens', TokenEvaluacionViewSet, basename='token')
router.register(r'validar', TokenValidationViewSet, basename='validar')

urlpatterns = [
    path('', include(router.urls)),
]
