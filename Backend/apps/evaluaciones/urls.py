# -*- coding: utf-8 -*-
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    TipoEvaluacionViewSet, PreguntaViewSet, 
    EvaluacionViewSet, RespuestaEvaluacionViewSet, preguntas_nom035
)

# Router para el sistema existente de evaluaciones
router = DefaultRouter()
router.register(r'tipos', TipoEvaluacionViewSet)
router.register(r'preguntas', PreguntaViewSet, basename='pregunta')
router.register(r'evaluaciones', EvaluacionViewSet, basename='evaluacion')
router.register(r'respuestas', RespuestaEvaluacionViewSet, basename='respuesta')

urlpatterns = [
    # Sistema existente de evaluaciones
    path('', include(router.urls)),
    path('preguntas-nom035/', preguntas_nom035),
    
    # Sistema oficial de evaluaciones NOM (SuperAdmin)
    path('oficial/', include('apps.evaluaciones.urls_oficiales')),
]
