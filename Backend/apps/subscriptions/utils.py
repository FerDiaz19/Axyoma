"""
💳 UTILIDADES DE SUSCRIPCIONES - AXYOMA
=====================================
Funciones para manejar la lógica de suscripciones de empresas
"""

from datetime import date
from apps.subscriptions.models import SuscripcionEmpresa, PlanSuscripcion
from apps.users.models import Empresa, Planta

class SuscripcionManager:
    """Manager para manejar lógica de suscripciones"""
    
    @staticmethod
    def empresa_tiene_suscripcion_activa(empresa):
        """
        Verifica si una empresa tiene una suscripción activa
        """
        return SuscripcionEmpresa.objects.filter(
            empresa=empresa,
            estado='activa',
            fecha_fin__gte=date.today()
        ).exists()
    
    @staticmethod
    def obtener_suscripcion_activa(empresa):
        """
        Obtiene la suscripción activa de una empresa
        """
        return SuscripcionEmpresa.objects.filter(
            empresa=empresa,
            estado='activa',
            fecha_fin__gte=date.today()
        ).first()
    
    @staticmethod
    def planta_tiene_acceso(planta):
        """
        Verifica si una planta tiene acceso (a través de su empresa)
        """
        return SuscripcionManager.empresa_tiene_suscripcion_activa(planta.empresa)
    
    @staticmethod
    def usuario_tiene_acceso(user):
        """
        Verifica si un usuario tiene acceso basado en su empresa
        """
        try:
            perfil = user.perfil  # La relación se llama 'perfil'
            
            # SuperAdmin siempre tiene acceso
            if perfil.nivel_usuario == 'superadmin':
                return True
            
            # Admin empresa: verificar suscripción de su empresa
            if perfil.nivel_usuario == 'admin-empresa':
                empresa = Empresa.objects.filter(administrador=perfil).first()
                if empresa:
                    return SuscripcionManager.empresa_tiene_suscripcion_activa(empresa)
            
            # Admin planta: verificar suscripción de la empresa de su planta
            if perfil.nivel_usuario == 'admin-planta':
                # Buscar planta administrada por este usuario
                from apps.users.models import AdminPlanta
                admin_planta = AdminPlanta.objects.filter(usuario=perfil).first()
                if admin_planta:
                    return SuscripcionManager.planta_tiene_acceso(admin_planta.planta)
            
            return False
            
        except Exception as e:
            print(f"Error verificando acceso de usuario: {e}")
            return False
    
    @staticmethod
    def obtener_planes_disponibles():
        """
        Obtiene todos los planes disponibles para suscripción
        """
        return PlanSuscripcion.objects.filter(status=True).order_by('precio')
    
    @staticmethod
    def crear_suscripcion(empresa, plan, metodo_pago='tarjeta'):
        """
        Crea una nueva suscripción para una empresa
        """
        from datetime import timedelta
        
        # Cancelar suscripciones anteriores
        SuscripcionEmpresa.objects.filter(
            empresa=empresa,
            estado='activa'
        ).update(estado='cancelada')
        
        # Crear nueva suscripción
        suscripcion = SuscripcionEmpresa.objects.create(
            empresa=empresa,
            plan=plan,
            fecha_inicio=date.today(),
            fecha_fin=date.today() + timedelta(days=plan.duracion),
            estado='activa'
        )
        
        # Crear registro de pago (simulado)
        from apps.subscriptions.models import Pago
        pago = Pago.objects.create(
            suscripcion=suscripcion,
            monto=plan.precio,
            metodo_pago=metodo_pago,
            estado_pago='completado',
            referencia_pago=f'TXN_{date.today().strftime("%Y%m%d")}_{suscripcion.suscripcion_id}',
            usuario=empresa.administrador
        )
        
        return suscripcion, pago
    
    @staticmethod
    def obtener_estado_suscripcion(empresa):
        """
        Obtiene el estado detallado de la suscripción de una empresa
        """
        suscripcion = SuscripcionManager.obtener_suscripcion_activa(empresa)
        
        if not suscripcion:
            return {
                'tiene_suscripcion': False,
                'estado': 'sin_suscripcion',
                'mensaje': 'Tu empresa no tiene una suscripción activa',
                'accion_requerida': 'Selecciona un plan para continuar',
                'plantas_incluidas': 0
            }
        
        dias_restantes = (suscripcion.fecha_fin - date.today()).days
        
        return {
            'tiene_suscripcion': True,
            'estado': 'activa',
            'plan': suscripcion.plan.nombre,
            'precio': suscripcion.plan.precio,
            'fecha_fin': suscripcion.fecha_fin,
            'dias_restantes': dias_restantes,
            'plantas_incluidas': empresa.plantas.count(),
            'mensaje': f'Plan {suscripcion.plan.nombre} activo' + 
                      (f' ({dias_restantes} días restantes)' if dias_restantes <= 30 else '')
        }

# Decorador para vistas que requieren suscripción activa
def requiere_suscripcion_activa(view_func):
    """
    Decorador para vistas que requieren suscripción activa
    """
    from functools import wraps
    from django.http import JsonResponse
    
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({
                'error': 'No autenticado',
                'codigo': 'NO_AUTH'
            }, status=401)
        
        if not SuscripcionManager.usuario_tiene_acceso(request.user):
            return JsonResponse({
                'error': 'Suscripción requerida',
                'mensaje': 'Tu empresa necesita una suscripción activa para acceder a esta funcionalidad',
                'codigo': 'NO_SUBSCRIPTION',
                'accion': 'redirect_to_plans'
            }, status=403)
        
        return view_func(request, *args, **kwargs)
    
    return wrapper

# Función helper para templates
def obtener_contexto_suscripcion(user):
    """
    Obtiene contexto de suscripción para usar en templates
    """
    if not user.is_authenticated:
        return {'suscripcion': None}
    
    try:
        perfil = user.perfil
        
        if perfil.nivel_usuario == 'superadmin':
            return {
                'suscripcion': {
                    'tiene_acceso': True,
                    'es_superadmin': True
                }
            }
        
        # Buscar empresa del usuario
        empresa = None
        if perfil.nivel_usuario == 'admin-empresa':
            empresa = Empresa.objects.filter(administrador=perfil).first()
        elif perfil.nivel_usuario == 'admin-planta':
            from apps.users.models import AdminPlanta
            admin_planta = AdminPlanta.objects.filter(usuario=perfil).first()
            if admin_planta:
                empresa = admin_planta.planta.empresa
        
        if empresa:
            estado = SuscripcionManager.obtener_estado_suscripcion(empresa)
            return {'suscripcion': estado}
        
    except:
        pass
    
    return {'suscripcion': None}
