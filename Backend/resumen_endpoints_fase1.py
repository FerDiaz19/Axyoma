# -*- coding: utf-8 -*-
"""
Script para listar todos los endpoints de evaluaciones disponibles
"""

print("🚀 SISTEMA DE EVALUACIONES AXYOMA - ENDPOINTS DISPONIBLES")
print("=" * 80)

print("\n📊 SISTEMA EXISTENTE DE EVALUACIONES (Funcional):")
print("   GET  /api/evaluaciones/tipos/                   - Tipos de evaluaciones")
print("   GET  /api/evaluaciones/preguntas/               - Preguntas personalizadas") 
print("   GET  /api/evaluaciones/evaluaciones/            - Evaluaciones personalizadas")
print("   GET  /api/evaluaciones/respuestas/              - Respuestas de evaluaciones")
print("   GET  /api/evaluaciones/preguntas-nom035/        - Preguntas NOM-035 desde SQL")

print("\n🔐 SISTEMA OFICIAL NOM (SuperAdmin) - FASE 1 COMPLETADA:")
print("   ⚡ Gestión de Evaluaciones Oficiales:")
print("   GET    /api/evaluaciones/oficial/superadmin/evaluaciones-oficiales/")
print("   POST   /api/evaluaciones/oficial/superadmin/evaluaciones-oficiales/")
print("   GET    /api/evaluaciones/oficial/superadmin/evaluaciones-oficiales/{id}/")
print("   PUT    /api/evaluaciones/oficial/superadmin/evaluaciones-oficiales/{id}/")
print("   DELETE /api/evaluaciones/oficial/superadmin/evaluaciones-oficiales/{id}/")
print("   POST   /api/evaluaciones/oficial/superadmin/evaluaciones-oficiales/{id}/activar/")
print("   POST   /api/evaluaciones/oficial/superadmin/evaluaciones-oficiales/{id}/desactivar/")
print("   GET    /api/evaluaciones/oficial/superadmin/evaluaciones-oficiales/{id}/estadisticas/")

print("\n   ⚡ Gestión de Secciones Oficiales:")
print("   GET    /api/evaluaciones/oficial/superadmin/secciones-oficiales/")
print("   POST   /api/evaluaciones/oficial/superadmin/secciones-oficiales/")
print("   GET    /api/evaluaciones/oficial/superadmin/secciones-oficiales/{id}/")
print("   PUT    /api/evaluaciones/oficial/superadmin/secciones-oficiales/{id}/")
print("   DELETE /api/evaluaciones/oficial/superadmin/secciones-oficiales/{id}/")

print("\n   ⚡ Gestión de Preguntas Oficiales:")
print("   GET    /api/evaluaciones/oficial/superadmin/preguntas-oficiales/")
print("   POST   /api/evaluaciones/oficial/superadmin/preguntas-oficiales/")
print("   GET    /api/evaluaciones/oficial/superadmin/preguntas-oficiales/{id}/")
print("   PUT    /api/evaluaciones/oficial/superadmin/preguntas-oficiales/{id}/")
print("   DELETE /api/evaluaciones/oficial/superadmin/preguntas-oficiales/{id}/")
print("   GET    /api/evaluaciones/oficial/superadmin/preguntas-oficiales/por_evaluacion/?evaluacion_id={id}")
print("   POST   /api/evaluaciones/oficial/superadmin/preguntas-oficiales/{id}/duplicar/")

print("\n   ⚡ Gestión de Asignaciones de Evaluación:")
print("   GET    /api/evaluaciones/oficial/superadmin/asignaciones/")
print("   POST   /api/evaluaciones/oficial/superadmin/asignaciones/")
print("   GET    /api/evaluaciones/oficial/superadmin/asignaciones/{id}/")
print("   PUT    /api/evaluaciones/oficial/superadmin/asignaciones/{id}/")
print("   DELETE /api/evaluaciones/oficial/superadmin/asignaciones/{id}/")
print("   GET    /api/evaluaciones/oficial/superadmin/asignaciones/dashboard/")
print("   GET    /api/evaluaciones/oficial/superadmin/asignaciones/{id}/progreso_detallado/")
print("   POST   /api/evaluaciones/oficial/superadmin/asignaciones/{id}/finalizar/")

print("\n   ⚡ Monitoreo de Empleados Asignados:")
print("   GET    /api/evaluaciones/oficial/superadmin/empleados-asignados/")
print("   GET    /api/evaluaciones/oficial/superadmin/empleados-asignados/{id}/")
print("   GET    /api/evaluaciones/oficial/superadmin/empleados-asignados/{id}/respuestas/")

print("\n   ⚡ Análisis de Respuestas:")
print("   GET    /api/evaluaciones/oficial/superadmin/respuestas/")
print("   GET    /api/evaluaciones/oficial/superadmin/respuestas/{id}/")
print("   GET    /api/evaluaciones/oficial/superadmin/respuestas/estadisticas_pregunta/?pregunta_id={id}")

print("\n🔒 AUTENTICACIÓN REQUERIDA:")
print("   - Todas las APIs oficiales requieren token JWT")
print("   - Solo usuarios con user_type='SuperAdmin' pueden acceder")
print("   - Obtener token: POST /api/auth/login/ con email y password")

print("\n📋 CREDENCIALES DE PRUEBA:")
print("   Email: superadmin@axyoma.com")
print("   Password: superadmin123")

print("\n🎯 PRÓXIMAS FASES:")
print("   Fase 2: Interface de Usuario para SuperAdmin")
print("   Fase 3: Sistema de Tokens para Empleados")
print("   Fase 4: Dashboard de Resultados y Reportes")

print("\n✅ ESTADO ACTUAL:")
print("   ✅ Base de datos: Modelos creados y migrados")
print("   ✅ Backend APIs: ViewSets y Serializers funcionales")
print("   ✅ Autenticación: Protección SuperAdmin implementada")
print("   ✅ Endpoints: 30+ endpoints disponibles")
print("   ⏳ Frontend: Pendiente para Fase 2")

print("\n🚀 PARA PROBAR:")
print("   1. Abrir: http://127.0.0.1:8000/api/evaluaciones/oficial/superadmin/")
print("   2. Autenticarse como SuperAdmin")
print("   3. Explorar los endpoints disponibles")

print("\n" + "=" * 80)
print("🎉 FASE 1 DEL SISTEMA DE EVALUACIONES COMPLETADA!")
print("=" * 80)
