# -*- coding: utf-8 -*-
from django.urls import path, include
from rest_framework.routers import DefaultRouter

# Import viewsets que realmente existen
from apps.users.views import (
    UserViewSet, EmpresaViewSet, EmpleadoViewSet
)
from apps.evaluaciones.views import (
    EvaluacionViewSet, AsignacionEvaluacionViewSet, 
    RespuestaEvaluacionViewSet, TokenEvaluacionViewSet
)
from apps.subscriptions.views import SubscriptionViewSet

# Create router
router = DefaultRouter()

# Register viewsets
router.register(r'users', UserViewSet, basename='user')
router.register(r'usuarios', UserViewSet, basename='usuarios')  # Agregamos ambos endpoints
router.register(r'empresas', EmpresaViewSet, basename='empresa')
router.register(r'empleados', EmpleadoViewSet, basename='empleado')
router.register(r'evaluaciones', EvaluacionViewSet, basename='evaluacion')
router.register(r'asignaciones', AsignacionEvaluacionViewSet, basename='asignacion')
router.register(r'respuestas', RespuestaEvaluacionViewSet, basename='respuesta')
router.register(r'tokens', TokenEvaluacionViewSet, basename='token')
router.register(r'subscriptions', SubscriptionViewSet, basename='subscription')
router.register(r'suscripciones', SubscriptionViewSet, basename='suscripciones')  # Agregamos ambos endpoints

urlpatterns = [
    path('', include(router.urls)),
    # Include evaluaciones app URLs
    path('evaluaciones/', include('apps.evaluaciones.urls')),
]
