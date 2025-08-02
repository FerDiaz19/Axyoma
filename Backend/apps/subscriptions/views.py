from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.exceptions import ValidationError
from django.utils import timezone
from datetime import timedelta, date
from django.db import transaction
import traceback
from apps.users.models import Empresa
from apps.subscriptions.models import PlanSuscripcion, SuscripcionEmpresa, Pago
from apps.subscriptions.utils import SuscripcionManager, requiere_suscripcion_activa

class SubscriptionViewSet(viewsets.ViewSet):
    """
    ViewSet para manejar suscripciones usando PostgreSQL únicamente
    """
    permission_classes = [IsAuthenticated]
    
    def get_permissions(self):
        """
        Permite acceso sin autenticación para algunos endpoints durante debug
        TODO: Implementar verificación de SuperAdmin
        """
        if self.action in ['suscripciones', 'planes']:
            return [AllowAny()]
        return [IsAuthenticated()]
    
    def get_subscription_info(self, empresa):
        """Obtiene información de suscripción de PostgreSQL"""
        try:
            # Buscar suscripción activa de la empresa
            suscripcion = SuscripcionEmpresa.objects.filter(
                empresa=empresa,
                estado='activa'
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
                'plan_nombre': suscripcion.plan.nombre,
                'fecha_inicio': suscripcion.fecha_inicio.isoformat(),
                'fecha_fin': suscripcion.fecha_fin.isoformat() if suscripcion.fecha_fin else None,
                'dias_restantes': suscripcion.dias_restantes,
                'esta_activa': suscripcion.esta_activa,
                'esta_por_vencer': suscripcion.esta_por_vencer,
                'precio': float(suscripcion.plan.precio),
                'duracion': suscripcion.plan.duracion,
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
            # Mostrar TODOS los planes para SuperAdmin
            planes = PlanSuscripcion.objects.all().values(
                'plan_id', 'nombre', 'descripcion', 'precio', 'duracion', 'status'
            )
            return Response(list(planes))
        except Exception as e:
            print(f"❌ Error obteniendo planes: {str(e)}")
            traceback.print_exc()
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
                    status=data.get('status', True)
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
            print(f"❌ Error creando plan: {str(e)}")
            traceback.print_exc()
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
                plan.status = request.data['status']
            
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
            print(f"❌ Error editando plan: {str(e)}")
            traceback.print_exc()
            return Response(
                {'error': f'Error editando plan: {str(e)}'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=False, methods=['get'])
    def suscripciones(self, request):
        """Obtener todas las suscripciones con datos completos"""
        try:
            suscripciones = SuscripcionEmpresa.objects.select_related(
                'empresa', 'plan'
            ).all().order_by('-fecha_inicio')
            
            # Procesar los datos para que coincidan con lo que espera el frontend
            suscripciones_procesadas = []
            for suscripcion in suscripciones:
                # Calcular días restantes
                dias_restantes = (suscripcion.fecha_fin - timezone.now().date()).days
                
                suscripciones_procesadas.append({
                    'suscripcion_id': suscripcion.suscripcion_id,
                    'empresa_id': suscripcion.empresa.empresa_id,
                    'empresa_nombre': suscripcion.empresa.nombre,
                    'plan_id': suscripcion.plan.plan_id,
                    'plan_nombre': suscripcion.plan.nombre,
                    'plan_precio': float(suscripcion.plan.precio),
                    'plan_duracion': suscripcion.plan.duracion,
                    'fecha_inicio': suscripcion.fecha_inicio.isoformat(),
                    'fecha_fin': suscripcion.fecha_fin.isoformat(),
                    'estado': suscripcion.estado,
                    'status': True,  # Asumiendo que está activa si existe
                    'dias_restantes': dias_restantes,
                    'esta_activa': suscripcion.esta_activa,
                    'esta_por_vencer': suscripcion.esta_por_vencer
                })
            
            return Response(suscripciones_procesadas)
        except Exception as e:
            print(f"❌ Error obteniendo suscripciones: {str(e)}")
            traceback.print_exc()
            return Response(
                {'error': f'Error obteniendo suscripciones: {str(e)}'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=False, methods=['post'])
    def crear_suscripcion(self, request):
        """Crear una nueva suscripción"""
        try:
            data = request.data
            empresa_id = data.get('empresa_id')
            plan_id = data.get('plan_id')
            
            if not empresa_id or not plan_id:
                return Response(
                    {'error': 'empresa_id y plan_id son requeridos'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            try:
                empresa = Empresa.objects.get(empresa_id=empresa_id)
            except Empresa.DoesNotExist:
                return Response(
                    {'error': 'Empresa no encontrada'}, 
                    status=status.HTTP_404_NOT_FOUND
                )
            
            try:
                plan = PlanSuscripcion.objects.get(plan_id=plan_id)
            except PlanSuscripcion.DoesNotExist:
                return Response(
                    {'error': 'Plan no encontrado'}, 
                    status=status.HTTP_404_NOT_FOUND
                )
            
            # Verificar si ya existe una suscripción activa
            suscripcion_existente = SuscripcionEmpresa.objects.filter(
                empresa=empresa,
                estado='activa'
            ).first()
            
            if suscripcion_existente:
                return Response(
                    {'error': f'La empresa ya tiene una suscripción activa hasta {suscripcion_existente.fecha_fin}'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            with transaction.atomic():
                # Crear nueva suscripción
                fecha_inicio = timezone.now().date()
                fecha_fin = fecha_inicio + timedelta(days=plan.duracion)
                
                suscripcion = SuscripcionEmpresa.objects.create(
                    empresa=empresa,
                    plan=plan,
                    fecha_inicio=fecha_inicio,
                    fecha_fin=fecha_fin,
                    estado='activa'
                )
                
                # Crear pago automático
                pago = Pago.objects.create(
                    suscripcion=suscripcion,
                    costo=plan.precio,
                    monto_pago=plan.precio,
                    estado_pago='Completado',
                    fecha_pago=timezone.now(),
                    transaccion_id=f"SUB-{suscripcion.suscripcion_id}-{timezone.now().strftime('%Y%m%d%H%M%S')}",
                    usuario=request.user if request.user.is_authenticated else None
                )
            
            return Response({
                'message': f'Suscripción creada exitosamente para {empresa.nombre}',
                'suscripcion_id': suscripcion.suscripcion_id,
                'empresa': empresa.nombre,
                'plan': plan.nombre,
                'fecha_inicio': fecha_inicio.isoformat(),
                'fecha_fin': fecha_fin.isoformat(),
                'precio': float(plan.precio)
            })
            
        except Exception as e:
            print(f"❌ Error creando suscripción: {str(e)}")
            traceback.print_exc()
            return Response(
                {'error': f'Error creando suscripción: {str(e)}'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=False, methods=['get'])
    def pagos(self, request):
        """Obtener todos los pagos"""
        try:
            pagos = Pago.objects.select_related(
                'suscripcion__empresa', 'suscripcion__plan', 'usuario'
            ).all().order_by('-fecha_pago')
            
            pagos_procesados = []
            for pago in pagos:
                pagos_procesados.append({
                    'pago_id': pago.pago_id,
                    'suscripcion_id': pago.suscripcion.suscripcion_id,
                    'empresa_nombre': pago.suscripcion.empresa.nombre,
                    'plan_nombre': pago.suscripcion.plan.nombre,
                    'costo': float(pago.costo),
                    'monto_pago': float(pago.monto_pago),
                    'estado_pago': pago.estado_pago,
                    'fecha_pago': pago.fecha_pago.isoformat(),
                    'fecha_vencimiento': pago.fecha_vencimiento.isoformat() if pago.fecha_vencimiento else None,
                    'transaccion_id': pago.transaccion_id,
                    'usuario': pago.usuario.username if pago.usuario else 'Sistema'
                })
            
            return Response(pagos_procesados)
        except Exception as e:
            print(f"❌ Error obteniendo pagos: {str(e)}")
            traceback.print_exc()
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
            monto_pago = data.get('monto_pago')
            
            if not empresa_id or not plan_id or not monto_pago:
                return Response(
                    {'error': 'empresa_id, plan_id y monto_pago son requeridos'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            try:
                empresa = Empresa.objects.get(empresa_id=empresa_id)
            except Empresa.DoesNotExist:
                return Response(
                    {'error': 'Empresa no encontrada'}, 
                    status=status.HTTP_404_NOT_FOUND
                )
            
            try:
                plan = PlanSuscripcion.objects.get(plan_id=plan_id)
            except PlanSuscripcion.DoesNotExist:
                return Response(
                    {'error': 'Plan no encontrado'}, 
                    status=status.HTTP_404_NOT_FOUND
                )
            
            with transaction.atomic():
                # Buscar suscripción existente o crear nueva
                suscripcion = SuscripcionEmpresa.objects.filter(
                    empresa=empresa,
                    plan=plan
                ).first()
                
                if suscripcion:
                    # Renovar suscripción existente
                    if suscripcion.fecha_fin < timezone.now().date():
                        suscripcion.fecha_inicio = timezone.now().date()
                    suscripcion.fecha_fin = suscripcion.fecha_fin + timedelta(days=plan.duracion)
                    suscripcion.estado = 'activa'
                    suscripcion.save()
                else:
                    # Crear nueva suscripción
                    fecha_inicio = timezone.now().date()
                    fecha_fin = fecha_inicio + timedelta(days=plan.duracion)
                    
                    suscripcion = SuscripcionEmpresa.objects.create(
                        empresa=empresa,
                        plan=plan,
                        fecha_inicio=fecha_inicio,
                        fecha_fin=fecha_fin,
                        estado='activa'
                    )
                
                # Crear registro de pago
                pago = Pago.objects.create(
                    suscripcion=suscripcion,
                    costo=plan.precio,
                    monto_pago=float(monto_pago),
                    estado_pago='Completado',
                    fecha_pago=timezone.now(),
                    transaccion_id=f"PAY-{suscripcion.suscripcion_id}-{timezone.now().strftime('%Y%m%d%H%M%S')}",
                    usuario=request.user if request.user.is_authenticated else None
                )
            
            return Response({
                'message': 'Pago procesado exitosamente',
                'pago_id': pago.pago_id,
                'suscripcion_id': suscripcion.suscripcion_id,
                'nueva_fecha_fin': suscripcion.fecha_fin.isoformat(),
                'monto_pagado': float(monto_pago)
            })
            
        except Exception as e:
            print(f"❌ Error procesando pago: {str(e)}")
            traceback.print_exc()
            return Response(
                {'error': f'Error procesando pago: {str(e)}'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=False, methods=['get'])
    def info_empresa(self, request):
        """Obtener información de suscripción de una empresa específica"""
        try:
            empresa_id = request.GET.get('empresa_id')
            if not empresa_id:
                return Response(
                    {'error': 'empresa_id es requerido'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            empresa = Empresa.objects.get(empresa_id=empresa_id)
            info_suscripcion = self.get_subscription_info(empresa)
            return Response(info_suscripcion)
            
        except Empresa.DoesNotExist:
            return Response(
                {'error': 'Empresa no encontrada'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            print(f"❌ Error obteniendo información de empresa: {str(e)}")
            traceback.print_exc()
            return Response(
                {'error': f'Error obteniendo información de suscripción: {str(e)}'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def mi_suscripcion(self, request):
        """
        Obtiene la información de suscripción del usuario actual
        """
        try:
            perfil = request.user.perfil
            
            # SuperAdmin tiene acceso completo
            if perfil.nivel_usuario == 'superadmin':
                return Response({
                    'tiene_acceso': True,
                    'es_superadmin': True,
                    'mensaje': 'Acceso completo como SuperAdmin'
                })
            
            # Buscar empresa del usuario
            empresa = None
            if perfil.nivel_usuario == 'admin-empresa':
                empresa = Empresa.objects.filter(administrador=perfil).first()
            elif perfil.nivel_usuario == 'admin-planta':
                from apps.users.models import AdminPlanta
                admin_planta = AdminPlanta.objects.filter(usuario=perfil).first()
                if admin_planta:
                    empresa = admin_planta.planta.empresa
            
            if not empresa:
                return Response({
                    'error': 'No se encontró empresa asociada al usuario'
                }, status=status.HTTP_404_NOT_FOUND)
            
            # Usar el nuevo manager
            estado = SuscripcionManager.obtener_estado_suscripcion(empresa)
            return Response(estado)
            
        except Exception as e:
            print(f"❌ Error obteniendo mi suscripción: {str(e)}")
            return Response(
                {'error': f'Error obteniendo suscripción: {str(e)}'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=False, methods=['get'], permission_classes=[AllowAny])
    def planes_disponibles(self, request):
        """
        Obtiene todos los planes disponibles para suscripción
        """
        try:
            planes = SuscripcionManager.obtener_planes_disponibles()
            
            planes_data = []
            for plan in planes:
                planes_data.append({
                    'plan_id': plan.plan_id,
                    'nombre': plan.nombre,
                    'descripcion': plan.descripcion,
                    'precio': float(plan.precio),
                    'duracion_dias': plan.duracion,
                    'duracion_texto': f"{plan.duracion} días",
                    'activo': plan.status
                })
            
            return Response({
                'planes': planes_data,
                'total': len(planes_data)
            })
            
        except Exception as e:
            print(f"❌ Error obteniendo planes: {str(e)}")
            return Response(
                {'error': f'Error obteniendo planes: {str(e)}'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def contratar_plan(self, request):
        """
        Contrata un nuevo plan para la empresa del usuario
        """
        try:
            plan_id = request.data.get('plan_id')
            metodo_pago = request.data.get('metodo_pago', 'tarjeta')
            
            if not plan_id:
                return Response({
                    'error': 'plan_id es requerido'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Verificar que el usuario puede contratar
            perfil = request.user.perfil
            if perfil.nivel_usuario not in ['superadmin', 'admin-empresa']:
                return Response({
                    'error': 'Solo administradores de empresa pueden contratar planes'
                }, status=status.HTTP_403_FORBIDDEN)
            
            # Buscar empresa
            if perfil.nivel_usuario == 'admin-empresa':
                empresa = Empresa.objects.filter(administrador=perfil).first()
            else:  # superadmin puede especificar empresa
                empresa_id = request.data.get('empresa_id')
                empresa = Empresa.objects.get(empresa_id=empresa_id) if empresa_id else None
            
            if not empresa:
                return Response({
                    'error': 'No se encontró empresa para contratar'
                }, status=status.HTTP_404_NOT_FOUND)
            
            # Buscar plan
            plan = PlanSuscripcion.objects.get(plan_id=plan_id, status=True)
            
            # Crear suscripción
            with transaction.atomic():
                suscripcion, pago = SuscripcionManager.crear_suscripcion(
                    empresa=empresa,
                    plan=plan,
                    metodo_pago=metodo_pago
                )
            
            return Response({
                'success': True,
                'mensaje': f'Plan {plan.nombre} contratado exitosamente',
                'suscripcion': {
                    'suscripcion_id': suscripcion.suscripcion_id,
                    'plan': plan.nombre,
                    'precio': float(plan.precio),
                    'fecha_inicio': suscripcion.fecha_inicio,
                    'fecha_fin': suscripcion.fecha_fin,
                    'estado': suscripcion.estado
                },
                'pago': {
                    'pago_id': pago.pago_id,
                    'referencia': pago.referencia_pago,
                    'estado': pago.estado_pago
                }
            })
            
        except PlanSuscripcion.DoesNotExist:
            return Response({
                'error': 'Plan no encontrado o no disponible'
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print(f"❌ Error contratando plan: {str(e)}")
            return Response(
                {'error': f'Error contratando plan: {str(e)}'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def verificar_acceso(self, request):
        """
        Verifica si el usuario actual tiene acceso al sistema
        """
        try:
            tiene_acceso = SuscripcionManager.usuario_tiene_acceso(request.user)
            
            response_data = {
                'tiene_acceso': tiene_acceso
            }
            
            if not tiene_acceso:
                perfil = request.user.perfil
                response_data.update({
                    'mensaje': 'Suscripción requerida para acceder',
                    'accion': 'contratar_plan',
                    'nivel_usuario': perfil.nivel_usuario
                })
            
            return Response(response_data)
            
        except Exception as e:
            print(f"❌ Error verificando acceso: {str(e)}")
            return Response(
                {'error': f'Error verificando acceso: {str(e)}'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
