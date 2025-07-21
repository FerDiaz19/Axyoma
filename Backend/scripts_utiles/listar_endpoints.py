#!/usr/bin/env python
"""
Script para listar todos los endpoints de la API de Axyoma
"""

def print_endpoints():
    print("="*80)
    print("            ENDPOINTS DE LA API AXYOMA")
    print("="*80)
    print()
    
    # Base URL
    base_url = "http://localhost:8000"
    
    print("🔧 DOCUMENTACIÓN:")
    print(f"   📋 Swagger UI:  {base_url}/swagger/")
    print(f"   📖 ReDoc:       {base_url}/redoc/")
    print(f"   🔧 Admin:       {base_url}/admin/")
    print()
    
    print("🔐 AUTENTICACIÓN:")
    print(f"   POST   {base_url}/api/auth/login/")
    print(f"   POST   {base_url}/api/auth/register/")
    print(f"   POST   {base_url}/api/auth/logout/")
    print()
    
    print("🏢 GESTIÓN DE EMPRESAS:")
    print(f"   GET    {base_url}/api/empresas/                    # Listar empresas")
    print(f"   POST   {base_url}/api/empresas/                    # Crear empresa")
    print(f"   GET    {base_url}/api/empresas/{{id}}/              # Obtener empresa")
    print(f"   PUT    {base_url}/api/empresas/{{id}}/              # Actualizar empresa")
    print(f"   DELETE {base_url}/api/empresas/{{id}}/              # Eliminar empresa")
    print()
    
    print("👥 GESTIÓN DE EMPLEADOS:")
    print(f"   GET    {base_url}/api/empleados/                   # Listar empleados")
    print(f"   POST   {base_url}/api/empleados/                   # Crear empleado")
    print(f"   GET    {base_url}/api/empleados/{{id}}/             # Obtener empleado")
    print(f"   PUT    {base_url}/api/empleados/{{id}}/             # Actualizar empleado")
    print(f"   DELETE {base_url}/api/empleados/{{id}}/             # Eliminar empleado")
    print()
    
    print("🏭 GESTIÓN DE PLANTAS:")
    print(f"   GET    {base_url}/api/plantas/                     # Listar plantas")
    print(f"   POST   {base_url}/api/plantas/                     # Crear planta")
    print(f"   GET    {base_url}/api/plantas/{{id}}/               # Obtener planta")
    print(f"   PUT    {base_url}/api/plantas/{{id}}/               # Actualizar planta")
    print(f"   DELETE {base_url}/api/plantas/{{id}}/               # Eliminar planta")
    print()
    
    print("🏛️ GESTIÓN DE DEPARTAMENTOS:")
    print(f"   GET    {base_url}/api/departamentos/               # Listar departamentos")
    print(f"   POST   {base_url}/api/departamentos/               # Crear departamento")
    print(f"   GET    {base_url}/api/departamentos/{{id}}/         # Obtener departamento")
    print(f"   PUT    {base_url}/api/departamentos/{{id}}/         # Actualizar departamento")
    print(f"   DELETE {base_url}/api/departamentos/{{id}}/         # Eliminar departamento")
    print()
    
    print("💼 GESTIÓN DE PUESTOS:")
    print(f"   GET    {base_url}/api/puestos/                     # Listar puestos")
    print(f"   POST   {base_url}/api/puestos/                     # Crear puesto")
    print(f"   GET    {base_url}/api/puestos/{{id}}/               # Obtener puesto")
    print(f"   PUT    {base_url}/api/puestos/{{id}}/               # Actualizar puesto")
    print(f"   DELETE {base_url}/api/puestos/{{id}}/               # Eliminar puesto")
    print()
    
    print("🏗️ ESTRUCTURA ORGANIZACIONAL:")
    print(f"   GET    {base_url}/api/estructura/                  # Ver estructura completa")
    print(f"   POST   {base_url}/api/estructura/crear_estructura/ # Crear estructura")
    print()
    
    print("🔧 SUPER ADMINISTRADOR:")
    print(f"   GET    {base_url}/api/superadmin/empresas/         # Gestionar todas las empresas")
    print(f"   POST   {base_url}/api/superadmin/suspender_empresa/")
    print(f"   POST   {base_url}/api/superadmin/reactivar_empresa/")
    print()
    
    print("💳 SUSCRIPCIONES:")
    print(f"   GET    {base_url}/api/suscripciones/               # Listar suscripciones")
    print(f"   POST   {base_url}/api/suscripciones/               # Crear suscripción")
    print(f"   GET    {base_url}/api/suscripciones/{{id}}/         # Obtener suscripción")
    print(f"   PUT    {base_url}/api/suscripciones/{{id}}/         # Actualizar suscripción")
    print()
    
    print("💰 SUBSCRIPTIONS (GESTIÓN AVANZADA):")
    print(f"   GET    {base_url}/api/subscriptions/               # Listar subscriptions")
    print(f"   POST   {base_url}/api/subscriptions/               # Crear subscription")
    print(f"   GET    {base_url}/api/subscriptions/{{id}}/         # Obtener subscription")
    print(f"   PUT    {base_url}/api/subscriptions/{{id}}/         # Actualizar subscription")
    print()
    
    print("📊 EVALUACIONES:")
    print(f"   GET    {base_url}/api/surveys/evaluaciones/        # Listar evaluaciones")
    print(f"   POST   {base_url}/api/surveys/evaluaciones/        # Crear evaluación")
    print(f"   GET    {base_url}/api/surveys/evaluaciones/{{id}}/  # Obtener evaluación")
    print(f"   PUT    {base_url}/api/surveys/evaluaciones/{{id}}/  # Actualizar evaluación")
    print(f"   DELETE {base_url}/api/surveys/evaluaciones/{{id}}/  # Eliminar evaluación")
    print()
    
    print("❓ PREGUNTAS DE EVALUACIÓN:")
    print(f"   GET    {base_url}/api/surveys/preguntas/           # Listar preguntas")
    print(f"   POST   {base_url}/api/surveys/preguntas/           # Crear pregunta")
    print(f"   GET    {base_url}/api/surveys/preguntas/{{id}}/     # Obtener pregunta")
    print(f"   PUT    {base_url}/api/surveys/preguntas/{{id}}/     # Actualizar pregunta")
    print(f"   DELETE {base_url}/api/surveys/preguntas/{{id}}/     # Eliminar pregunta")
    print()
    
    print("🎯 APLICACIONES DE EVALUACIÓN:")
    print(f"   GET    {base_url}/api/surveys/aplicaciones/        # Listar aplicaciones")
    print(f"   POST   {base_url}/api/surveys/aplicaciones/        # Crear aplicación")
    print(f"   GET    {base_url}/api/surveys/aplicaciones/{{id}}/  # Obtener aplicación")
    print(f"   PUT    {base_url}/api/surveys/aplicaciones/{{id}}/  # Actualizar aplicación")
    print(f"   DELETE {base_url}/api/surveys/aplicaciones/{{id}}/  # Eliminar aplicación")
    print()
    
    print("="*80)
    print("🔑 AUTENTICACIÓN:")
    print("   - Todas las rutas (excepto login/register) requieren token de autenticación")
    print("   - Incluir en headers: Authorization: Token <your-token>")
    print()
    print("📝 NOTAS:")
    print("   - {{id}} representa el ID numérico del recurso")
    print("   - Todos los endpoints soportan JSON como formato de datos")
    print("   - Los métodos POST/PUT requieren Content-Type: application/json")
    print("="*80)

if __name__ == "__main__":
    print_endpoints()
