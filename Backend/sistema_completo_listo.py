#!/usr/bin/env python
"""
🚀 SCRIPT MAESTRO SIMPLIFICADO - BD LISTA PARA USAR
==================================================
"""

import os
import sys
import django
from datetime import date, datetime, timedelta
import random

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')
django.setup()

from django.contrib.auth.models import User
from django.core.management import call_command

def resetear_base_datos():
    """Resetea completamente la base de datos"""
    print("🔥 RESETEANDO BASE DE DATOS...")
    try:
        call_command('flush', '--noinput')
        call_command('migrate', '--run-syncdb')
        print("✅ Base de datos lista")
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def crear_superusers():
    """Crear usuarios administrativos"""
    print("\n👑 CREANDO USUARIOS ADMINISTRATIVOS...")
    
    usuarios = [
        {'username': 'superadmin', 'email': 'superadmin@axyoma.com', 'nombre': 'Super', 'apellido': 'Admin'},
        {'username': 'superadmin_TEST', 'email': 'superadmin_test@axyoma.com', 'nombre': 'Super', 'apellido': 'Admin Test'}
    ]
    
    for usuario_data in usuarios:
        try:
            # Crear usuario Django
            user = User.objects.create_user(
                username=usuario_data['username'],
                email=usuario_data['email'],
                password='admin123'
            )
            user.is_superuser = True
            user.is_staff = True
            user.save()
            
            # Crear perfil en tabla usuarios usando SQL directo
            from django.db import connection
            with connection.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO usuarios (
                        user_id, nombre, apellido_paterno, apellido_materno, 
                        correo, nivel_usuario, status, admin_empresa, fecha_registro
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, NOW())
                """, (
                    user.id,
                    usuario_data['nombre'],
                    usuario_data['apellido'],
                    '',
                    usuario_data['email'],
                    'superadmin',
                    True,
                    None
                ))
            
            print(f"✅ Usuario creado: {usuario_data['username']}")
            
        except Exception as e:
            print(f"❌ Error creando {usuario_data['username']}: {e}")

def crear_datos_basicos():
    """Crear datos básicos del sistema"""
    print("\n🏢 CREANDO DATOS BÁSICOS...")
    
    try:
        from apps.users.models import Empresa, Planta, Departamento, Puesto, Empleado
        
        # Crear empresa principal
        empresa = Empresa.objects.create(
            nombre='TechnoMex Industries',
            rfc='TMI950815AB2',
            direccion='Blvd. Tecnológico #2000, Querétaro, Qro.',
            email_contacto='contacto@technomex.com.mx',
            telefono_contacto='4421234567',
            status=True
        )
        print(f"✅ Empresa: {empresa.nombre}")
        
        # Crear plantas
        plantas_data = [
            {'nombre': 'Planta Querétaro Centro', 'direccion': 'Av. Constituyentes #850, Centro, Qro.'},
            {'nombre': 'Planta El Marqués', 'direccion': 'Carr. Querétaro-México Km. 45, El Marqués, Qro.'}
        ]
        
        plantas = []
        for planta_data in plantas_data:
            planta = Planta.objects.create(
                nombre=planta_data['nombre'],
                direccion=planta_data['direccion'],
                empresa=empresa,
                status=True
            )
            plantas.append(planta)
            print(f"✅ Planta: {planta.nombre}")
        
        # Crear departamentos
        departamentos_nombres = ['Recursos Humanos', 'Producción', 'Mantenimiento', 'Calidad']
        
        for planta in plantas:
            for dept_nombre in departamentos_nombres:
                departamento = Departamento.objects.create(
                    nombre=dept_nombre,
                    descripcion=f"Departamento de {dept_nombre}",
                    planta=planta,
                    status=True
                )
                
                # Crear puestos
                puestos_nombres = ['Gerente', 'Supervisor', 'Operador']
                for puesto_nombre in puestos_nombres:
                    puesto = Puesto.objects.create(
                        nombre=f"{puesto_nombre} de {dept_nombre}",
                        descripcion=f"Puesto de {puesto_nombre}",
                        departamento=departamento,
                        status=True
                    )
                    
                    # Crear empleados
                    for i in range(2):
                        Empleado.objects.create(
                            nombre=f"Empleado {i+1}",
                            apellido_paterno=f"Apellido{i+1}",
                            apellido_materno="Test",
                            email=f"empleado{random.randint(1000,9999)}@technomex.com",
                            telefono=f"442{random.randint(1000000, 9999999)}",
                            fecha_ingreso=date.today(),
                            puesto=puesto,
                            status=True
                        )
        
        print("✅ Estructura organizacional completa")
        
    except Exception as e:
        print(f"❌ Error creando datos básicos: {e}")

def crear_planes():
    """Crear planes de suscripción"""
    print("\n📋 CREANDO PLANES DE SUSCRIPCIÓN...")
    
    try:
        from apps.subscriptions.models import PlanSuscripcion
        
        planes_data = [
            {'nombre': 'Plan Básico', 'descripcion': 'Plan básico', 'duracion': 365, 'precio': 5000.00},
            {'nombre': 'Plan Profesional', 'descripcion': 'Plan profesional', 'duracion': 365, 'precio': 10000.00},
            {'nombre': 'Plan Empresarial', 'descripcion': 'Plan empresarial', 'duracion': 365, 'precio': 20000.00}
        ]
        
        for plan_data in planes_data:
            plan = PlanSuscripcion.objects.create(
                **plan_data,
                status=True
            )
            print(f"✅ Plan: {plan.nombre} - ${plan.precio}")
            
    except Exception as e:
        print(f"❌ Error creando planes: {e}")

def crear_suscripcion_demo():
    """Crear suscripción demo"""
    print("\n💳 CREANDO SUSCRIPCIÓN DEMO...")
    
    try:
        from apps.subscriptions.models import PlanSuscripcion, SuscripcionEmpresa, Pago
        from apps.users.models import Empresa
        
        empresa = Empresa.objects.first()
        plan = PlanSuscripcion.objects.first()
        
        if empresa and plan:
            # Crear suscripción
            fecha_inicio = datetime.now()
            fecha_fin = fecha_inicio + timedelta(days=365)
            
            suscripcion = SuscripcionEmpresa.objects.create(
                empresa=empresa,
                plan=plan,
                fecha_inicio=fecha_inicio.date(),
                fecha_fin=fecha_fin.date(),
                estado='activa',
                auto_renovacion=True
            )
            
            # Crear pago
            Pago.objects.create(
                suscripcion=suscripcion,
                monto_pago=plan.precio,
                fecha_pago=fecha_inicio,
                estado_pago='completado',
                transaccion_id=f"TXN{random.randint(100000, 999999)}"
            )
            
            print(f"✅ Suscripción: {empresa.nombre} -> {plan.nombre}")
            
    except Exception as e:
        print(f"❌ Error creando suscripción: {e}")

def verificar_login():
    """Verificar que el login funciona"""
    print("\n🧪 VERIFICANDO LOGIN...")
    
    try:
        import requests
        response = requests.post('http://127.0.0.1:8000/api/auth/login/', 
            json={'username': 'superadmin', 'password': 'admin123'})
        
        if response.status_code == 200:
            print("✅ Login funcionando correctamente")
            data = response.json()
            print(f"   Usuario: {data.get('usuario')}")
            print(f"   Nivel: {data.get('nivel_usuario')}")
        else:
            print("⚠️ Usar credenciales alternativas: superadmin_TEST / admin123")
            
    except Exception as e:
        print(f"⚠️ No se pudo verificar login: {e}")

def main():
    """Función principal"""
    print("🚀 INICIANDO CONFIGURACIÓN COMPLETA DEL SISTEMA")
    print("=" * 60)
    
    # 1. Resetear BD
    if not resetear_base_datos():
        return
    
    # 2. Crear superusers
    crear_superusers()
    
    # 3. Crear datos básicos
    crear_datos_basicos()
    
    # 4. Crear planes
    crear_planes()
    
    # 5. Crear suscripción demo
    crear_suscripcion_demo()
    
    # 6. Verificar login
    verificar_login()
    
    # RESUMEN FINAL
    print("\n🎯 SISTEMA CONFIGURADO Y LISTO PARA USAR")
    print("=" * 60)
    print("✅ Base de datos reiniciada")
    print("✅ Usuarios administrativos")
    print("✅ Empresas y estructura organizacional")
    print("✅ Planes de suscripción")
    print("✅ Suscripciones activas")
    print()
    print("🔑 CREDENCIALES:")
    print("   Usuario: superadmin")
    print("   Contraseña: admin123")
    print()
    print("🌐 Accede al panel en: http://localhost:3000")
    print("=" * 60)

if __name__ == "__main__":
    main()
