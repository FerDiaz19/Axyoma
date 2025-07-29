from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SubscriptionViewSet

router = DefaultRouter()
router.register(r'', SubscriptionViewSet, basename='subscriptions')

urlpatterns = [
    # Rutas específicas para suscripciones
    path('planes/', SubscriptionViewSet.as_view({'get': 'planes'}), name='planes'),
    path('suscripciones/', SubscriptionViewSet.as_view({'get': 'suscripciones'}), name='listar_suscripciones'),
    path('crear-suscripcion/', SubscriptionViewSet.as_view({'post': 'crear_suscripcion'}), name='crear_suscripcion'),
    path('crear-plan/', SubscriptionViewSet.as_view({'post': 'crear_plan'}), name='crear_plan'),
    path('editar-plan/', SubscriptionViewSet.as_view({'put': 'editar_plan'}), name='editar_plan'),
    path('pagos/', SubscriptionViewSet.as_view({'get': 'pagos'}), name='listar_pagos'),
    path('pago-simple/', SubscriptionViewSet.as_view({'post': 'pago_simple'}), name='pago_simple'),
    path('info-empresa/', SubscriptionViewSet.as_view({'get': 'info_empresa'}), name='info_empresa'),
    
    # Incluir rutas del router
    path('', include(router.urls)),
]
