#!/usr/bin/env python
"""
Función para manejar lógica de suscripción en login
"""
import os
import sys
import django
from datetime import datetime, timedelta

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')
django.setup()

from apps.users.models import Empresa, PerfilUsuario
from apps.subscriptions.models import PlanSuscripcion, SuscripcionEmpresa, Pago
from django.utils import timezone
from django.db import transaction

def verificar_o_crear_suscripcion_login(usuario):
    """
    Verifica si el usuario (admin-empresa) tiene suscripción activa
    Si no tiene, no crea una automáticamente (debe seleccionar plan)
    """
    try:
        # Solo para admin-empresa
        if usuario.nivel_usuario != 'admin-empresa':
            return {'tiene_suscripcion': True, 'estado': 'no_aplica'}
        
        # Obtener empresa del usuario
        empresa = Empresa.objects.get(administrador=usuario)
        
        # Buscar suscripción activa
        suscripcion_activa = SuscripcionEmpresa.objects.filter(
            empresa=empresa,
            status=True
        ).first()
        
        if not suscripcion_activa:
            return {
                'tiene_suscripcion': False,
                'estado': 'sin_suscripcion',
                'mensaje': 'No tiene suscripción activa. Seleccione un plan para continuar.',
                'requiere_pago': True,
                'dias_restantes': 0,
                'acceso_reportes': False
            }
        
        # Verificar si está vencida
        if suscripcion_activa.fecha_fin < timezone.now().date():
            # Marcar como vencida
            suscripcion_activa.estado = 'Vencida'
            suscripcion_activa.save()
            
            return {
                'tiene_suscripcion': False,
                'estado': 'vencida',
                'mensaje': 'Su suscripción ha vencido. Renueve para continuar.',
                'requiere_pago': True,
                'dias_restantes': 0,
                'acceso_reportes': False
            }
        
        # Suscripción activa
        dias_restantes = (suscripcion_activa.fecha_fin - timezone.now().date()).days
        
        return {
            'tiene_suscripcion': True,
            'estado': 'activa',
            'plan_nombre': suscripcion_activa.plan_suscripcion.nombre,
            'fecha_inicio': suscripcion_activa.fecha_inicio.isoformat(),
            'fecha_fin': suscripcion_activa.fecha_fin.isoformat(),
            'dias_restantes': dias_restantes,
            'esta_por_vencer': dias_restantes <= 7,
            'precio': float(suscripcion_activa.plan_suscripcion.precio),
            'duracion': suscripcion_activa.plan_suscripcion.duracion,
            'requiere_pago': False,
            'acceso_reportes': True
        }
        
    except Exception as e:
        print(f"Error verificando suscripción: {e}")
        return {
            'tiene_suscripcion': False,
            'estado': 'error',
            'mensaje': f'Error al verificar suscripción: {str(e)}',
            'requiere_pago': True,
            'dias_restantes': 0,
            'acceso_reportes': False
        }

def crear_suscripcion_pago(empresa_id, plan_id, usuario_id):
    """
    Crea una suscripción y procesa el pago
    Solo para admin-empresa
    """
    try:
        with transaction.atomic():
            # Obtener empresa y plan
            empresa = Empresa.objects.get(empresa_id=empresa_id)
            plan = PlanSuscripcion.objects.get(plan_id=plan_id)
            usuario = PerfilUsuario.objects.get(id=usuario_id)
            
            # Verificar que el usuario es admin-empresa de esta empresa
            if usuario.nivel_usuario != 'admin-empresa' or empresa.administrador != usuario:
                raise Exception("Solo el administrador de la empresa puede crear suscripciones")
            
            # Cancelar suscripción anterior si existe
            SuscripcionEmpresa.objects.filter(
                empresa=empresa,
                status=True
            ).update(status=False, estado='Cancelada')
            
            # Crear nueva suscripción
            fecha_inicio = timezone.now().date()
            fecha_fin = fecha_inicio + timedelta(days=plan.duracion)
            
            suscripcion = SuscripcionEmpresa.objects.create(
                empresa=empresa,
                plan_suscripcion=plan,
                fecha_inicio=fecha_inicio,
                fecha_fin=fecha_fin,
                estado='Activa',
                status=True
            )
            
            # Crear pago automático (simulado)
            pago = Pago.objects.create(
                suscripcion=suscripcion,
                costo=plan.precio,
                monto_pago=plan.precio,
                estado_pago='Completado',
                fecha_pago=timezone.now()
            )
            
            return {
                'success': True,
                'suscripcion_id': suscripcion.suscripcion_id,
                'pago_id': pago.pago_id,
                'mensaje': f'Suscripción creada exitosamente. Plan: {plan.nombre}',
                'fecha_fin': fecha_fin.isoformat()
            }
            
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }

if __name__ == '__main__':
    # Test de la función
    print("🧪 Probando lógica de suscripción...")
    
    # Obtener usuario admin-empresa
    admin_empresa = PerfilUsuario.objects.filter(nivel_usuario='admin-empresa').first()
    if admin_empresa:
        print(f"👤 Usuario: {admin_empresa.correo}")
        
        # Verificar suscripción
        info = verificar_o_crear_suscripcion_login(admin_empresa)
        print(f"📊 Estado: {info}")
        
        # Si no tiene suscripción, simular creación
        if not info['tiene_suscripcion']:
            print("💳 Creando suscripción de prueba...")
            
            # Obtener primer plan disponible
            plan = PlanSuscripcion.objects.filter(status=True).first()
            if plan:
                empresa = Empresa.objects.get(administrador=admin_empresa)
                resultado = crear_suscripcion_pago(
                    empresa.empresa_id,
                    plan.plan_id,
                    admin_empresa.id
                )
                print(f"✅ Resultado: {resultado}")
    else:
        print("❌ No se encontró usuario admin-empresa")
