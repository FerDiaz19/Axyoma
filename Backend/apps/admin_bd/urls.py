# -*- coding: utf-8 -*-
"""
🗄️ URLS DE ADMINISTRACIÓN DE BASE DE DATOS
==========================================

Configuración de rutas para el sistema de gestión de BD y respaldos.
Incluye endpoints para SuperAdmin y gestión de respaldos.
🚀 Rutas incluidas:
- Sistema de respaldos y restauración
- Exportación directa de tablas
- Gestión de BD (reseteo, datos iniciales)
- Endpoints de SuperAdmin

🔒 Seguridad: Rutas protegidas solo para SuperAdmin
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AdminBDViewSet
from . import views_directo, views_respaldos, views_restauracion

router = DefaultRouter()
router.register(r'', AdminBDViewSet, basename='admin_bd')

urlpatterns = [
    path('', include(router.urls)),
    
    # URLs directas (consultas SQL directas) - SOLUCIÓN GARANTIZADA para tablas problemáticas
    path('directo/exportar/<str:tabla_nombre>/', views_directo.exportar_tabla_csv_directo, name='exportar_tabla_directo'),
    path('directo/tablas/', views_directo.listar_tablas_directas, name='listar_tablas_directas'),
      # URLs para sistema de respaldos y restauración - SOLO SUPERADMIN
    path('respaldos/tablas/', views_respaldos.respaldar_tablas, name='respaldar_tablas'),
    path('respaldos/bd-completa/', views_respaldos.respaldar_bd_completa, name='respaldar_bd_completa'),
    path('respaldos/listar/', views_respaldos.listar_respaldos, name='listar_respaldos'),    path('respaldos/restaurar/', views_respaldos.restaurar_respaldo, name='restaurar_respaldo'),
    path('respaldos/restaurar-forzado/', views_respaldos.restaurar_respaldo_forzado, name='restaurar_respaldo_forzado'),
    path('respaldos/diagnosticar/', views_respaldos.diagnosticar_restauracion, name='diagnosticar_restauracion'),
    path('respaldos/limpiar-tabla/', views_respaldos.limpiar_tabla_para_restaurar, name='limpiar_tabla_restaurar'),
    path('respaldos/eliminar/<str:archivo>/', views_respaldos.eliminar_respaldo, name='eliminar_respaldo'),
    path('respaldos/descargar/<str:archivo>/', views_respaldos.descargar_respaldo, name='descargar_respaldo'),
    path('respaldos/info/', views_respaldos.info_sistema_respaldos, name='info_sistema_respaldos'),
    path('respaldos/verificar/', views_respaldos.verificar_sistema_respaldos, name='verificar_sistema_respaldos'),
    
    # 🚀 NUEVAS RUTAS OPTIMIZADAS PARA BD GRANDES
    path('respaldos/monitorear/', views_respaldos.monitorear_backup_progreso, name='monitorear_backup'),
    path('respaldos/emergencia/', views_respaldos.backup_emergencia_optimizado, name='backup_emergencia'),
      # NUEVAS FUNCIONES SUPERADMIN
    path('respaldos/pgadmin/', views_respaldos.respaldo_limpio_pgadmin, name='respaldo_pgadmin'),
    path('sistema/resetear-bd/', views_respaldos.resetear_bd_completa, name='resetear_bd'),
    path('sistema/datos-iniciales/', views_respaldos.cargar_datos_iniciales, name='cargar_datos_iniciales'),
    path('sistema/estado-inicial/', views_respaldos.restaurar_estado_inicial, name='restaurar_estado_inicial'),
      # 🔧 RUTAS DE RESTAURACIÓN AVANZADA
    path('restauracion/reiniciar-bd/', views_restauracion.reiniciar_bd_cero, name='reiniciar_bd_cero'),
    path('restauracion/cargar-demo/', views_restauracion.cargar_datos_demo, name='cargar_datos_demo'),
    path('restauracion/estado-bd/', views_restauracion.estado_bd_restauracion, name='estado_bd_restauracion'),
    path('restauracion/debug/', views_restauracion.debug_reiniciar_bd, name='debug_reiniciar_bd'),
]
