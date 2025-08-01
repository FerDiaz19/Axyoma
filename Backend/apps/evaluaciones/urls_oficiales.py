# -*- coding: utf-8 -*-
"""
URLs para las vistas oficiales de evaluaciones (SuperAdmin)
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views_oficiales import (
    EvaluacionOficialViewSet, SeccionOficialViewSet, PreguntaOficialViewSet,
    AsignacionEvaluacionViewSet, EmpleadoAsignadoViewSet, RespuestaEmpleadoViewSet
)

# Router para las APIs del SuperAdmin
router_superadmin = DefaultRouter()
router_superadmin.register(r'evaluaciones-oficiales', EvaluacionOficialViewSet, basename='evaluacion-oficial')
router_superadmin.register(r'secciones-oficiales', SeccionOficialViewSet, basename='seccion-oficial')
router_superadmin.register(r'preguntas-oficiales', PreguntaOficialViewSet, basename='pregunta-oficial')
router_superadmin.register(r'asignaciones', AsignacionEvaluacionViewSet, basename='asignacion-evaluacion')
router_superadmin.register(r'empleados-asignados', EmpleadoAsignadoViewSet, basename='empleado-asignado')
router_superadmin.register(r'respuestas', RespuestaEmpleadoViewSet, basename='respuesta-empleado')

urlpatterns = [
    # URLs del SuperAdmin con prefijo para diferenciar
    path('superadmin/', include(router_superadmin.urls)),
]
