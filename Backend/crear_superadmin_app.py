#!/usr/bin/env python
import os
import sys
import django
from django.db import transaction

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')
django.setup()

from django.contrib.auth.models import User
from apps.users.models import PerfilUsuario, Empresa, Planta, Departamento, Puesto, Empleado
from apps.subscriptions.models import PlanSuscripcion, SuscripcionEmpresa, Pago
from datetime import date, timedelta
from django.utils import timezone

def crear_superadmin_completo():
    """
    Crear superadmin completo para login de la aplicación web
    """
    print("🚀 Creando SuperAdmin para la APLICACIÓN WEB...")
    
    # Credenciales
    USERNAME = "superadmin"
    PASSWORD = "1234"
    EMAIL = "superadmin@axyoma.com"
    
    try:
        with transaction.atomic():
            # 1. Eliminar usuario existente si existe
            if User.objects.filter(username=USERNAME).exists():
                print(f"⚠️ Usuario '{USERNAME}' ya existe. Eliminando...")
                User.objects.filter(username=USERNAME).delete()
            
            # 2. Crear usuario Django
            user = User.objects.create_user(
                username=USERNAME,
                email=EMAIL,
                password=PASSWORD,
                first_name="Super",
                last_name="Admin",
                is_staff=True,
                is_superuser=True
            )
            print(f"✅ Usuario Django creado: {user.username}")
            
            # 3. Crear perfil SuperAdmin
            perfil = PerfilUsuario.objects.create(
                user_id=user,
                nombre="Super",
                apellido_paterno="Admin",
                apellido_materno="Sistema",
                correo=EMAIL,
                nivel_usuario="superadmin",
                status=True,
                admin_empresa=None  # SuperAdmin no tiene admin_empresa
            )
            print(f"✅ Perfil SuperAdmin creado: {perfil.nombre_completo}")
            
            # 4. Crear plan de suscripción si no existe
            plan, created = PlanSuscripcion.objects.get_or_create(
                nombre="Plan Premium",
                defaults={
                    'descripcion': 'Plan completo con todas las funcionalidades',
                    'precio': 999.99,
                    'duracion': 365,  # 1 año
                    'status': True
                }
            )
            if created:
                print(f"✅ Plan de suscripción creado: {plan.nombre}")
            else:
                print(f"✅ Plan existente encontrado: {plan.nombre}")
            
            # 5. Crear admin empresa para demostración
            admin_empresa_user = User.objects.create_user(
                username="admin_empresa",
                email="admin@empresa.com",
                password="1234",
                first_name="Admin",
                last_name="Empresa"
            )
            
            admin_empresa_perfil = PerfilUsuario.objects.create(
                user_id=admin_empresa_user,
                nombre="Admin",
                apellido_paterno="Empresa",
                correo="admin@empresa.com",
                nivel_usuario="admin-empresa",
                status=True
            )
            print(f"✅ Admin empresa creado: {admin_empresa_perfil.nombre_completo}")
            
            # 6. Crear empresa demo
            empresa = Empresa.objects.create(
                nombre="Empresa Demo",
                rfc="DEMO123456789",
                direccion="Calle Demo 123, Ciudad Demo",
                email_contacto="contacto@empresademo.com",
                telefono_contacto="4421234567",
                administrador=admin_empresa_perfil,
                status=True
            )
            print(f"✅ Empresa creada: {empresa.nombre}")
            
            # 7. Crear suscripción activa
            fecha_inicio = timezone.now().date()
            fecha_fin = fecha_inicio + timedelta(days=365)
            
            suscripcion = SuscripcionEmpresa.objects.create(
                empresa=empresa,
                plan=plan,
                fecha_fin=fecha_fin,
                estado='activa'
            )
            print(f"✅ Suscripción activa creada hasta: {fecha_fin}")
            
            # 8. Crear registro de pago
            pago = Pago.objects.create(
                suscripcion=suscripcion,
                monto_pago=plan.precio,
                estado_pago='Completado',
                metodo_pago='Pago online',
                transaccion_id=f"DEMO-{timezone.now().strftime('%Y%m%d%H%M%S')}",
                usuario=admin_empresa_user
            )
            print(f"✅ Pago registrado: ${pago.monto_pago}")
            
            # 9. Crear estructura organizacional básica
            planta = Planta.objects.create(
                nombre="Planta Principal",
                direccion="Av. Principal 456",
                empresa=empresa,
                status=True
            )
            print(f"✅ Planta creada: {planta.nombre}")
            
            departamento = Departamento.objects.create(
                nombre="Departamento IT",
                descripcion="Departamento de Tecnología",
                planta=planta,
                status=True
            )
            print(f"✅ Departamento creado: {departamento.nombre}")
            
            puesto = Puesto.objects.create(
                nombre="Desarrollador Senior",
                descripcion="Desarrollador de software senior",
                departamento=departamento,
                status=True
            )
            print(f"✅ Puesto creado: {puesto.nombre}")
            
            empleado = Empleado.objects.create(
                nombre="Juan",
                apellido_paterno="Pérez",
                apellido_materno="García",
                email="juan.perez@empresademo.com",
                telefono="4421111111",
                puesto=puesto,
                status=True
            )
            print(f"✅ Empleado creado: {empleado.nombre_completo}")
            
            # Mostrar credenciales finales
            print("\n" + "="*60)
            print("🎉 SUPERADMIN Y SISTEMA COMPLETO CREADO")
            print("="*60)
            print("\n🔑 CREDENCIALES SUPERADMIN:")
            print(f"   👤 Usuario: {USERNAME}")
            print(f"   🔑 Contraseña: {PASSWORD}")
            print(f"   📧 Email: {EMAIL}")
            print(f"   🎯 Nivel: {perfil.nivel_usuario}")
            
            print("\n🏢 CREDENCIALES ADMIN EMPRESA:")
            print(f"   👤 Usuario: admin_empresa")
            print(f"   🔑 Contraseña: 1234")
            print(f"   📧 Email: admin@empresa.com")
            print(f"   🎯 Nivel: admin-empresa")
            
            print("\n🌐 URLS DE ACCESO:")
            print("   • Frontend Login: http://localhost:3000/login")
            print("   • API Login: http://127.0.0.1:8000/api/auth/login/")
            print("   • Admin Django: http://127.0.0.1:8000/admin/")
            
            print("\n📊 DATOS CREADOS:")
            print(f"   • 1 Empresa: {empresa.nombre}")
            print(f"   • 1 Planta: {planta.nombre}")
            print(f"   • 1 Departamento: {departamento.nombre}")
            print(f"   • 1 Puesto: {puesto.nombre}")
            print(f"   • 1 Empleado: {empleado.nombre_completo}")
            print(f"   • Suscripción activa hasta: {fecha_fin}")
            
            print("\n🚀 ¡Ya puedes hacer login en la aplicación web!")
            print("="*60)
            
            return True
            
    except Exception as e:
        print(f"❌ Error creando sistema completo: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_login_api():
    """
    Probar login via API
    """
    print("\n🧪 PROBANDO LOGIN VIA API...")
    
    import requests
    
    try:
        # Datos de login
        login_data = {
            "username": "superadmin",
            "password": "1234"
        }
        
        # Hacer request de login
        response = requests.post(
            "http://127.0.0.1:8000/api/auth/login/",
            json=login_data,
            headers={'Content-Type': 'application/json'}
        )
        
        if response.status_code == 200:
            data = response.json()
            print("✅ LOGIN API EXITOSO")
            print(f"   Token: {data.get('token', 'N/A')[:20]}...")
            print(f"   Tipo Dashboard: {data.get('tipo_dashboard', 'N/A')}")
            print(f"   Nombre: {data.get('nombre_completo', 'N/A')}")
            return True
        else:
            print(f"❌ Login falló: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"⚠️ No se pudo probar API (servidor no corriendo): {str(e)}")
        return False

if __name__ == "__main__":
    print("🚀 SCRIPT CREAR SUPERADMIN PARA APLICACIÓN WEB")
    print("-" * 50)
    
    success = crear_superadmin_completo()
    
    if success:
        print("\n✅ Sistema completo creado exitosamente")
        
        # Verificar login Django
        from django.contrib.auth import authenticate
        user = authenticate(username="superadmin", password="1234")
        if user:
            print("✅ Login Django verificado")
        else:
            print("⚠️ Error verificando login Django")
        
        # Probar login API si el servidor está corriendo
        test_login_api()
        
    else:
        print("\n❌ Proceso falló")
