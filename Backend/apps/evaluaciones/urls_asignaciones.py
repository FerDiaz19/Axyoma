# -*- coding: utf-8 -*-
"""
URLs adicionales para el sistema de asignación con tokens (Fase 2)
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views_oficiales import (
    EmpleadosAsignacionViewSet, 
    AsignacionTokenViewSet,
    EvaluacionTokenViewSet
)

# Router para asignaciones con tokens
router_asignacion = DefaultRouter()
router_asignacion.register(r'empleados', EmpleadosAsignacionViewSet, basename='empleados-asignacion')
router_asignacion.register(r'asignaciones', AsignacionTokenViewSet, basename='asignaciones-token')
router_asignacion.register(r'publico', EvaluacionTokenViewSet, basename='evaluacion-token-publico')

urlpatterns = [
    # Endpoints para asignación con filtros y tokens
    path('', include(router_asignacion.urls)),
]
