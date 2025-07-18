# -*- coding: utf-8 -*-
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    TipoEvaluacionViewSet, PreguntaViewSet, 
    EvaluacionViewSet, RespuestaEvaluacionViewSet
)

router = DefaultRouter()
router.register(r'tipos', TipoEvaluacionViewSet)
router.register(r'preguntas', PreguntaViewSet, basename='pregunta')
router.register(r'evaluaciones', EvaluacionViewSet, basename='evaluacion')
router.register(r'respuestas', RespuestaEvaluacionViewSet, basename='respuesta')

urlpatterns = [
    path('', include(router.urls)),
]
