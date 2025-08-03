
# ---------------------------------------------------------------------------- #

from .views import *

from django.urls import path, include
from rest_framework.routers import DefaultRouter

# ---------------------------------------------------------------------------- #

router = DefaultRouter()
router.register(r'superadmin', SuperAdminViewSet, basename='superadmin')
router.register(r'admin-bd', AdminBDViewSet, basename='admin-bd')
router.register(r'empresas', EmpresaViewSet, basename='empresas')
router.register(r'plantas', PlantaViewSet, basename='plantas')
router.register(r'departamentos', DepartamentoViewSet, basename='departamentos')
router.register(r'puestos', PuestoViewSet, basename='puestos')
router.register(r'empleados', EmpleadoViewSet, basename='empleados')
router.register(r'estructura', EstructuraViewSet, basename='estructura')
router.register(r'suscripciones', SuscripcionViewSet, basename='suscripciones')

# ---------------------------------------------------------------------------- #

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
    path('superadmin/listar_planes_admin/', SuperAdminViewSet.as_view({'get': 'listar_planes_admin'})),
    path('superadmin/suspender_plan/<int:plan_id>/', SuperAdminViewSet.as_view({'post': 'suspender_plan'})),

    # Rutas de suscripciones - AGREGAMOS LA RUTA FALTANTE
    path('suscripciones/planes/', SuscripcionViewSet.as_view({'get': 'planes'})),
    path('suscripciones/crear_suscripcion/', crear_suscripcion_publica, name='crear_suscripcion_publica'),
    path('suscripciones/info_empresa/', SuscripcionViewSet.as_view({'get': 'info_empresa'})),
    path('suscripciones/actual/', SuscripcionViewSet.as_view({'get': 'actual'})),  # ← NUEVA RUTA AGREGADA

    # Rutas de Admin BD - Agregar estas líneas
    path('admin-bd/exportar/<str:tabla>/', AdminBDViewSet.as_view({'get': 'exportar_tabla'})),
    path('admin-bd/estadisticas/', AdminBDViewSet.as_view({'get': 'estadisticas_bd'})),

    # Incluir rutas automáticas del router
    path('', include(router.urls)),
]