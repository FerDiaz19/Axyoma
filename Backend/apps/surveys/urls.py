# -*- coding: utf-8 -*-
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EvaluacionViewSet, PreguntaEvaluacionViewSet, AplicacionEvaluacionViewSet

router = DefaultRouter()
router.register(r'evaluaciones', EvaluacionViewSet, basename='evaluaciones')
router.register(r'preguntas', PreguntaEvaluacionViewSet, basename='preguntas')
router.register(r'aplicaciones', AplicacionEvaluacionViewSet, basename='aplicaciones')

urlpatterns = [
    path('', include(router.urls)),
]
