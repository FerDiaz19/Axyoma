from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SubscriptionViewSet

router = DefaultRouter()
router.register(r'', SubscriptionViewSet, basename='subscriptions')

urlpatterns = [
    # Endpoints específicos
    path('planes/', SubscriptionViewSet.as_view({'get': 'planes'})),
    path('suscripciones/', SubscriptionViewSet.as_view({'get': 'suscripciones'})),
    path('listar/', SubscriptionViewSet.as_view({'get': 'suscripciones'})),  # Alias para compatibilidad
    path('crear_suscripcion/', SubscriptionViewSet.as_view({'post': 'crear_suscripcion'})),
    path('pagos/', SubscriptionViewSet.as_view({'get': 'pagos'})),
    path('pago_simple/', SubscriptionViewSet.as_view({'post': 'pago_simple'})),
    path('crear_plan/', SubscriptionViewSet.as_view({'post': 'crear_plan'})),
    path('editar_plan/', SubscriptionViewSet.as_view({'put': 'editar_plan'})),
    
    # Router automático
    path('', include(router.urls)),
]
