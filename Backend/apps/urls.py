from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    AuthViewSet, EmpresaViewSet, PlantaViewSet, 
    DepartamentoViewSet, PuestoViewSet, EmpleadoViewSet,
    EstructuraViewSet, SuperAdminViewSet, SuscripcionViewSet
)

# Crear router para las vistas
router = DefaultRouter()
router.register(r'superadmin', SuperAdminViewSet, basename='superadmin')
router.register(r'empresas', EmpresaViewSet, basename='empresas')
router.register(r'plantas', PlantaViewSet, basename='plantas')
router.register(r'departamentos', DepartamentoViewSet, basename='departamentos')
router.register(r'puestos', PuestoViewSet, basename='puestos')
router.register(r'empleados', EmpleadoViewSet, basename='empleados')
router.register(r'estructura', EstructuraViewSet, basename='estructura')
router.register(r'suscripciones', SuscripcionViewSet, basename='suscripciones')

urlpatterns = [
    path('', include(router.urls)),
]
urlpatterns = [
    # Rutas de autenticación
    path('auth/login/', AuthViewSet.as_view({'post': 'login'})),
    path('auth/test-login/', AuthViewSet.as_view({'post': 'test_login'})),
    path('auth/test-users/', AuthViewSet.as_view({'get': 'test_users'})),
    
    # Rutas de empresas
    path('empresas/registro/', EmpresaViewSet.as_view({'post': 'registro'})),
    
    # Rutas específicas con DetailView
    path('estructura/mi_estructura/', EstructuraViewSet.as_view({'get': 'mi_estructura'})),
    path('estructura/usuarios_planta/', EstructuraViewSet.as_view({'get': 'usuarios_planta'})),
    
    # Rutas de SuperAdmin
    path('superadmin/listar_empresas/', SuperAdminViewSet.as_view({'get': 'listar_empresas'})),
    path('superadmin/listar_usuarios/', SuperAdminViewSet.as_view({'get': 'listar_usuarios'})),
    path('superadmin/listar_todas_plantas/', SuperAdminViewSet.as_view({'get': 'listar_todas_plantas'})),
    path('superadmin/listar_todos_departamentos/', SuperAdminViewSet.as_view({'get': 'listar_todos_departamentos'})),
    path('superadmin/listar_todos_puestos/', SuperAdminViewSet.as_view({'get': 'listar_todos_puestos'})),
    path('superadmin/listar_todos_empleados/', SuperAdminViewSet.as_view({'get': 'listar_todos_empleados'})),
    path('superadmin/estadisticas_sistema/', SuperAdminViewSet.as_view({'get': 'estadisticas_sistema'})),
    
    # Incluir rutas automáticas del router
    path('', include(router.urls)),
]