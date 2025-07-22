# -*- coding: utf-8 -*-
from django.urls import path, include
from rest_framework.routers import DefaultRouter

# Import viewsets que realmente existen
from apps.users.views import (
    AuthViewSet, UserViewSet, EmpresaViewSet, EmpleadoViewSet,
    PlantaViewSet, DepartamentoViewSet, PuestoViewSet
)
from apps.users.superadmin_views import SuperAdminViewSet
from apps.evaluaciones.views import (
    EvaluacionViewSet, AsignacionEvaluacionViewSet, 
    RespuestaEvaluacionViewSet, TokenEvaluacionViewSet
)
from apps.subscriptions.views import SubscriptionViewSet

# Create router
router = DefaultRouter()

# Register viewsets
router.register(r'auth', AuthViewSet, basename='auth')
router.register(r'users', UserViewSet, basename='user')
router.register(r'superadmin', SuperAdminViewSet, basename='superadmin')
router.register(r'empresas', EmpresaViewSet, basename='empresa')
router.register(r'empleados', EmpleadoViewSet, basename='empleado')
router.register(r'plantas', PlantaViewSet, basename='planta')
router.register(r'departamentos', DepartamentoViewSet, basename='departamento')
router.register(r'puestos', PuestoViewSet, basename='puesto')
router.register(r'evaluaciones', EvaluacionViewSet, basename='evaluacion')
router.register(r'asignaciones', AsignacionEvaluacionViewSet, basename='asignacion')
router.register(r'respuestas', RespuestaEvaluacionViewSet, basename='respuesta')
router.register(r'tokens', TokenEvaluacionViewSet, basename='token')
router.register(r'subscriptions', SubscriptionViewSet, basename='subscription')

urlpatterns = [
    path('', include(router.urls)),
    # Include evaluaciones app URLs
    path('evaluaciones/', include('apps.evaluaciones.urls')),
]
