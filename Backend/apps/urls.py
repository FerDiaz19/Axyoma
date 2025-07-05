from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AuthViewSet, EmpresaViewSet, EmpleadoViewSet, PlantaViewSet, DepartamentoViewSet, PuestoViewSet, EstructuraViewSet

router = DefaultRouter()
router.register(r'auth', AuthViewSet, basename='auth')
router.register(r'empresas', EmpresaViewSet, basename='empresas')
router.register(r'empleados', EmpleadoViewSet)
router.register(r'plantas', PlantaViewSet)
router.register(r'departamentos', DepartamentoViewSet)
router.register(r'puestos', PuestoViewSet)
router.register(r'estructura', EstructuraViewSet, basename='estructura')

urlpatterns = [
    path('', include(router.urls)),
]