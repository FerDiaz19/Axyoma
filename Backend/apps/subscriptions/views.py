from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.exceptions import ValidationError
from django.utils import timezone
from datetime import timedelta, date
from apps.users.models import Empresa
from apps.subscriptions.models import PlanSuscripcion, SuscripcionEmpresa, Pago
from django.db import transaction

class SubscriptionViewSet(viewsets.ViewSet):
    """
    ViewSet para manejar suscripciones usando PostgreSQL únicamente
    """
    permission_classes = [IsAuthenticated]
    
    def get_subscription_info(self, empresa):
        """Obtiene información de suscripción de PostgreSQL"""
        try:
            # Buscar suscripción activa de la empresa
            suscripcion = SuscripcionEmpresa.objects.filter(
                empresa=empresa,
                status=True
            ).first()
            
            if not suscripcion:
                return {
                    'tiene_suscripcion': False,
                    'estado': 'sin_suscripcion',
                    'mensaje': 'La empresa no tiene una suscripción activa',
                    'requiere_pago': True,
                    'dias_restantes': 0
                }
            
            return {
                'tiene_suscripcion': True,
                'estado': suscripcion.estado.lower(),
                'plan_nombre': suscripcion.plan_suscripcion.nombre,
                'fecha_inicio': suscripcion.fecha_inicio.isoformat(),
                'fecha_fin': suscripcion.fecha_fin.isoformat() if suscripcion.fecha_fin else None,
                'dias_restantes': suscripcion.dias_restantes,
                'esta_activa': suscripcion.esta_activa,
                'esta_por_vencer': suscripcion.esta_por_vencer,
                'precio': float(suscripcion.plan_suscripcion.precio),
                'duracion': suscripcion.plan_suscripcion.duracion,
                'requiere_pago': not suscripcion.esta_activa
            }
            
        except Exception as e:
            print(f"Error getting subscription info: {str(e)}")
            return {
                'tiene_suscripcion': False,
                'estado': 'error',
                'mensaje': f'Error al obtener información de suscripción: {str(e)}',
                'requiere_pago': True,
                'dias_restantes': 0
            }
    
    @action(detail=False, methods=['get'])
    def planes(self, request):
        """Obtener todos los planes disponibles"""
        try:
            # CAMBIO: Mostrar TODOS los planes para SuperAdmin
            planes = PlanSuscripcion.objects.all().values(  # Removido filter(status=True)
                'plan_id', 'nombre', 'descripcion', 'precio', 'duracion', 'status'
            )
            return Response(list(planes))
        except Exception as e:
            return Response(
                {'error': f'Error obteniendo planes: {str(e)}'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=False, methods=['post'])
    def crear_plan(self, request):
        """Crear un nuevo plan de suscripción (Solo SuperAdmin)"""
        try:
            data = request.data
            nombre = data.get('nombre')
            descripcion = data.get('descripcion', '')
            precio = data.get('precio')
            duracion = data.get('duracion')
            
            if not nombre or not precio or not duracion:
                return Response(
                    {'error': 'nombre, precio y duracion son requeridos'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            with transaction.atomic():
                plan = PlanSuscripcion.objects.create(
                    nombre=nombre,
                    descripcion=descripcion,
                    precio=float(precio),
                    duracion=int(duracion),
                    status=True
                )
            
            return Response({
                'message': f'Plan "{plan.nombre}" creado exitosamente',
                'plan': {
                    'plan_id': plan.plan_id,
                    'nombre': plan.nombre,
                    'descripcion': plan.descripcion,
                    'precio': float(plan.precio),
                    'duracion': plan.duracion
                }
            })
            
        except Exception as e:
            return Response(
                {'error': f'Error creando plan: {str(e)}'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=False, methods=['put'])
    def editar_plan(self, request):
        """Editar un plan de suscripción"""
        try:
            plan_id = request.data.get('plan_id')
            if not plan_id:
                return Response(
                    {'error': 'plan_id es requerido'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            plan = PlanSuscripcion.objects.get(plan_id=plan_id)
            
            # Actualizar campos si se proporcionan
            if 'nombre' in request.data:
                plan.nombre = request.data['nombre']
            if 'descripcion' in request.data:
                plan.descripcion = request.data['descripcion']
            if 'precio' in request.data:
                plan.precio = float(request.data['precio'])
            if 'duracion' in request.data:
                plan.duracion = int(request.data['duracion'])
            if 'status' in request.data:
                plan.status = bool(request.data['status'])
            
            plan.save()
            
            return Response({
                'message': f'Plan "{plan.nombre}" actualizado exitosamente',
                'plan': {
                    'plan_id': plan.plan_id,
                    'nombre': plan.nombre,
                    'descripcion': plan.descripcion,
                    'precio': float(plan.precio),
                    'duracion': plan.duracion,
                    'status': plan.status
                }
            })
            
        except PlanSuscripcion.DoesNotExist:
            return Response(
                {'error': 'Plan no encontrado'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {'error': f'Error editando plan: {str(e)}'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=False, methods=['get'])
    def suscripciones(self, request):
        """Obtener todas las suscripciones con datos completos"""
        try:
            suscripciones = SuscripcionEmpresa.objects.select_related(
                'empresa', 'plan_suscripcion'
            ).values(
                'suscripcion_id',
                'empresa__nombre',
                'empresa__empresa_id',
                'plan_suscripcion__nombre',
                'plan_suscripcion__precio',
                'plan_suscripcion__duracion',
                'fecha_inicio',
                'fecha_fin',
                'estado',
                'status'
            ).order_by('-fecha_inicio')
            
            # Procesar los datos para que coincidan con lo que espera el frontend
            suscripciones_procesadas = []
            for suscripcion in suscripciones:
                suscripciones_procesadas.append({
                    'suscripcion_id': suscripcion['suscripcion_id'],
                    'empresa_nombre': suscripcion['empresa__nombre'],
                    'empresa_id': suscripcion['empresa__empresa_id'],
                    'plan_nombre': suscripcion['plan_suscripcion__nombre'],
                    'plan_precio': suscripcion['plan_suscripcion__precio'],
                    'plan_duracion': suscripcion['plan_suscripcion__duracion'],
                    'fecha_inicio': suscripcion['fecha_inicio'],
                    'fecha_fin': suscripcion['fecha_fin'],
                    'estado': suscripcion['estado'],
                    'status': suscripcion['status']
                })
            
            return Response(suscripciones_procesadas)
        except Exception as e:
            return Response(
                {'error': f'Error obteniendo suscripciones: {str(e)}'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=False, methods=['post'])
    def crear_suscripcion(self, request):
        """Crear una nueva suscripción"""
        try:
            empresa_id = request.data.get('empresa_id')
            plan_id = request.data.get('plan_id')
            
            if not empresa_id or not plan_id:
                return Response(
                    {'error': 'empresa_id y plan_id son requeridos'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            empresa = Empresa.objects.get(empresa_id=empresa_id)
            plan = PlanSuscripcion.objects.get(plan_id=plan_id)
            
            # Verificar si ya existe una suscripción activa
            suscripcion_existente = SuscripcionEmpresa.objects.filter(
                empresa=empresa,
                status=True
            ).first()
            
            if suscripcion_existente:
                return Response(
                    {'error': 'La empresa ya tiene una suscripción activa'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            with transaction.atomic():
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
                
                # Crear pago completado
                pago = Pago.objects.create(
                    suscripcion=suscripcion,
                    costo=plan.precio,
                    monto_pago=plan.precio,
                    estado_pago='Completado',
                    fecha_pago=timezone.now(),
                    transaccion_id=f"SUB-{empresa_id}-{timezone.now().strftime('%Y%m%d%H%M%S')}"
                )
            
            return Response({
                'message': f'Suscripción creada exitosamente para {empresa.nombre}',
                'suscripcion': {
                    'suscripcion_id': suscripcion.suscripcion_id,
                    'empresa': empresa.nombre,
                    'plan': plan.nombre,
                    'fecha_inicio': fecha_inicio.isoformat(),
                    'fecha_fin': fecha_fin.isoformat(),
                    'precio': float(plan.precio)
                }
            })
            
        except Empresa.DoesNotExist:
            return Response(
                {'error': 'Empresa no encontrada'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        except PlanSuscripcion.DoesNotExist:
            return Response(
                {'error': 'Plan no encontrado'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {'error': f'Error creando suscripción: {str(e)}'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=False, methods=['get'])
    def pagos(self, request):
        """Obtener todos los pagos"""
        try:
            pagos = Pago.objects.select_related(
                'suscripcion__empresa', 'suscripcion__plan_suscripcion'
            ).values(
                'pago_id',
                'suscripcion__empresa__nombre',
                'suscripcion__plan_suscripcion__nombre',
                'costo',
                'monto_pago',
                'estado_pago',
                'fecha_pago',
                'fecha_vencimiento',
                'transaccion_id',
                'suscripcion__suscripcion_id'
            ).order_by('-fecha_pago')
            
            # Procesar datos para el frontend
            pagos_procesados = []
            for pago in pagos:
                pagos_procesados.append({
                    'pago_id': pago['pago_id'],
                    'empresa_nombre': pago['suscripcion__empresa__nombre'],
                    'plan_nombre': pago['suscripcion__plan_suscripcion__nombre'],
                    'costo': pago['costo'],
                    'monto_pago': pago['monto_pago'],
                    'estado_pago': pago['estado_pago'],
                    'fecha_pago': pago['fecha_pago'],
                    'fecha_vencimiento': pago['fecha_vencimiento'],
                    'transaccion_id': pago['transaccion_id'],
                    'suscripcion_id': pago['suscripcion__suscripcion_id']
                })
            
            return Response(pagos_procesados)
        except Exception as e:
            return Response(
                {'error': f'Error obteniendo pagos: {str(e)}'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=False, methods=['post'])
    def pago_simple(self, request):
        """Procesar pago simple para renovar/activar suscripción"""
        try:
            data = request.data
            empresa_id = data.get('empresa_id')
            plan_id = data.get('plan_id')
            metodo_pago = data.get('metodo_pago', 'Transferencia')
            referencia_pago = data.get('referencia_pago', '')
            
            if not empresa_id or not plan_id:
                return Response(
                    {'error': 'empresa_id y plan_id son requeridos'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            empresa = Empresa.objects.get(empresa_id=empresa_id)
            plan = PlanSuscripcion.objects.get(plan_id=plan_id)
            
            with transaction.atomic():
                # Verificar suscripción existente
                suscripcion = SuscripcionEmpresa.objects.filter(
                    empresa=empresa,
                    status=True
                ).first()
                
                if suscripcion:
                    # Renovar suscripción existente
                    suscripcion.renovar_suscripcion()
                else:
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
                
                # Crear pago automáticamente completado
                pago = Pago.objects.create(
                    suscripcion=suscripcion,
                    costo=plan.precio,
                    monto_pago=plan.precio,
                    estado_pago='Completado',
                    fecha_pago=timezone.now(),
                    transaccion_id=f"PAY-{empresa_id}-{timezone.now().strftime('%Y%m%d%H%M%S')}"
                )
            
            return Response({
                'message': 'Pago procesado exitosamente',
                'suscripcion_activa': True,
                'fecha_fin': suscripcion.fecha_fin.isoformat(),
                'pago_id': pago.pago_id
            })
            
        except Empresa.DoesNotExist:
            return Response(
                {'error': 'Empresa no encontrada'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        except PlanSuscripcion.DoesNotExist:
            return Response(
                {'error': 'Plan no encontrado'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {'error': f'Error procesando pago: {str(e)}'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
