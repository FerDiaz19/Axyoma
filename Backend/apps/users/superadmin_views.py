# -*- coding: utf-8 -*-
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from django.db.models import Count, Q
from datetime import datetime, timedelta
from .models import Empresa, PerfilUsuario, Planta, Departamento, Puesto, Empleado


class SuperAdminViewSet(viewsets.ViewSet):
    """
    ViewSet para funcionalidades del SuperAdmin
    """
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        """
        Solo usuarios superadmin pueden acceder
        """
        permissions = super().get_permissions()
        return permissions

    @action(detail=False, methods=['get'])
    def estadisticas_sistema(self, request):
        """Obtener estadísticas generales del sistema"""
        try:
            # Estadísticas generales
            total_empresas = Empresa.objects.count()
            empresas_activas = Empresa.objects.filter(status=True).count()
            total_usuarios = PerfilUsuario.objects.count()
            usuarios_activos = PerfilUsuario.objects.filter(status=True).count()
            total_plantas = Planta.objects.count()
            plantas_activas = Planta.objects.filter(status=True).count()
            total_departamentos = Departamento.objects.count()
            departamentos_activos = Departamento.objects.filter(status=True).count()
            total_puestos = Puesto.objects.count()
            puestos_activos = Puesto.objects.filter(status=True).count()
            total_empleados = Empleado.objects.count()
            empleados_activos = Empleado.objects.filter(status=True).count()

            # Estadísticas por nivel de usuario
            usuarios_por_nivel = PerfilUsuario.objects.values('nivel_usuario').annotate(
                count=Count('id')
            ).order_by('nivel_usuario')

            # Empresas recientes (últimos 7 días)
            hace_7_dias = datetime.now() - timedelta(days=7)
            empresas_recientes = Empresa.objects.filter(
                fecha_registro__gte=hace_7_dias
            ).count()

            estadisticas = {
                'totales': {
                    'empresas': total_empresas,
                    'empresas_activas': empresas_activas,
                    'usuarios': total_usuarios,
                    'usuarios_activos': usuarios_activos,
                    'plantas': total_plantas,
                    'plantas_activas': plantas_activas,
                    'departamentos': total_departamentos,
                    'departamentos_activos': departamentos_activos,
                    'puestos': total_puestos,
                    'puestos_activos': puestos_activos,
                    'empleados': total_empleados,
                    'empleados_activos': empleados_activos,
                },
                'usuarios_por_nivel': list(usuarios_por_nivel),
                'empresas_recientes': empresas_recientes,
            }

            return Response(estadisticas, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {'error': f'Error al obtener estadísticas: {str(e)}'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=False, methods=['get'])
    def listar_empresas(self, request):
        """Listar todas las empresas con filtros"""
        try:
            queryset = Empresa.objects.all()
            
            # Filtros
            buscar = request.query_params.get('buscar', '')
            if buscar:
                queryset = queryset.filter(nombre__icontains=buscar)
            
            status_filter = request.query_params.get('status', '')
            if status_filter == 'true':
                queryset = queryset.filter(status=True)
            elif status_filter == 'false':
                queryset = queryset.filter(status=False)

            # Agregar información adicional
            empresas_data = []
            for empresa in queryset:
                try:
                    plantas_count = Planta.objects.filter(empresa=empresa).count()
                    empleados_count = Empleado.objects.filter(puesto__departamento__planta__empresa=empresa).count()
                    
                    empresa_data = {
                        'empresa_id': empresa.empresa_id,
                        'nombre': empresa.nombre,
                        'rfc': empresa.rfc,
                        'direccion': empresa.direccion,
                        'email_contacto': empresa.email_contacto,
                        'telefono_contacto': empresa.telefono_contacto,
                        'fecha_registro': empresa.fecha_registro,
                        'status': empresa.status,
                        'plantas_count': plantas_count,
                        'empleados_count': empleados_count,
                    }
                    empresas_data.append(empresa_data)
                except Exception as e:
                    print(f"Error procesando empresa {empresa.empresa_id}: {e}")
                    continue

            return Response({
                'empresas': empresas_data,
                'total': len(empresas_data)
            }, status=status.HTTP_200_OK)

        except Exception as e:
            print(f"Error general en listar_empresas: {e}")
            return Response(
                {'error': f'Error al listar empresas: {str(e)}'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=False, methods=['get'])
    def listar_usuarios(self, request):
        """Listar todos los usuarios del sistema con filtros"""
        try:
            # Obtener todos los usuarios con perfiles
            queryset = PerfilUsuario.objects.select_related('user').all()
            
            # Filtros
            buscar = request.query_params.get('buscar', '')
            if buscar:
                queryset = queryset.filter(
                    Q(nombre__icontains=buscar) |
                    Q(apellido_paterno__icontains=buscar) |
                    Q(correo__icontains=buscar) |
                    Q(user__username__icontains=buscar)
                )
            
            nivel_filter = request.query_params.get('nivel_usuario', '')
            if nivel_filter:
                queryset = queryset.filter(nivel_usuario=nivel_filter)
            
            status_filter = request.query_params.get('activo', '')
            if status_filter == 'true':
                queryset = queryset.filter(status=True)
            elif status_filter == 'false':
                queryset = queryset.filter(status=False)

            usuarios_data = []
            for perfil in queryset:
                try:
                    # Obtener información adicional según el nivel
                    empresa_info = None
                    planta_info = None
                    
                    if perfil.nivel_usuario == 'admin-empresa':
                        # Buscar empresa donde es administrador
                        try:
                            empresa = Empresa.objects.filter(administrador=perfil).first()
                            if empresa:
                                empresa_info = {
                                    'id': empresa.empresa_id,
                                    'nombre': empresa.nombre
                                }
                        except:
                            pass
                    elif perfil.nivel_usuario == 'admin-planta':
                        # Buscar plantas que administra
                        try:
                            from .models import AdminPlanta
                            admin_plantas = AdminPlanta.objects.filter(usuario=perfil, status=True).select_related('planta')
                            if admin_plantas.exists():
                                planta = admin_plantas.first().planta
                                planta_info = {
                                    'id': planta.planta_id,
                                    'nombre': planta.nombre,
                                    'empresa': planta.empresa.nombre
                                }
                        except:
                            pass
                    
                    usuario_data = {
                        'id': perfil.id,
                        'user_id': perfil.user.id if perfil.user else None,
                        'username': perfil.user.username if perfil.user else '',
                        'email': perfil.correo,
                        'nombre_completo': f"{perfil.nombre} {perfil.apellido_paterno} {perfil.apellido_materno or ''}".strip(),
                        'nombre': perfil.nombre,
                        'apellido_paterno': perfil.apellido_paterno,
                        'apellido_materno': perfil.apellido_materno or '',
                        'nivel_usuario': perfil.nivel_usuario,
                        'fecha_registro': perfil.fecha_registro,
                        'is_active': perfil.status and (perfil.user.is_active if perfil.user else True),
                        'empresa': empresa_info,
                        'planta': planta_info,
                    }
                    usuarios_data.append(usuario_data)
                except Exception as e:
                    print(f"Error procesando usuario {perfil.id}: {e}")
                    continue

            return Response({
                'usuarios': usuarios_data,
                'total': len(usuarios_data)
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {'error': f'Error al listar usuarios: {str(e)}'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=False, methods=['post'])
    def suspender_empresa(self, request):
        """Suspender o activar una empresa y sus elementos relacionados"""
        try:
            empresa_id = request.data.get('empresa_id')
            accion = request.data.get('accion')  # 'suspender' o 'activar'
            
            if not empresa_id or not accion:
                return Response(
                    {'error': 'empresa_id y accion son requeridos'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            empresa = Empresa.objects.get(empresa_id=empresa_id)
            
            nuevo_status = True if accion == 'activar' else False
            
            if accion == 'suspender':
                empresa.status = False
            elif accion == 'activar':
                empresa.status = True
            else:
                return Response(
                    {'error': 'Acción no válida'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            empresa.save()
            
            # Aplicar mismo status a elementos relacionados
            from .models import Planta, Departamento, Puesto, Empleado
            
            plantas_afectadas = Planta.objects.filter(empresa=empresa).update(status=nuevo_status)
            
            # Obtener departamentos de las plantas de esta empresa
            plantas_empresa = Planta.objects.filter(empresa=empresa)
            departamentos_afectados = Departamento.objects.filter(planta__in=plantas_empresa).update(status=nuevo_status)
            
            # Obtener puestos de los departamentos de esta empresa
            departamentos_empresa = Departamento.objects.filter(planta__empresa=empresa)
            puestos_afectados = Puesto.objects.filter(departamento__in=departamentos_empresa).update(status=nuevo_status)
            
            # Obtener empleados a través de puestos de esta empresa
            puestos_empresa = Puesto.objects.filter(departamento__planta__empresa=empresa)
            empleados_afectados = Empleado.objects.filter(puesto__in=puestos_empresa).update(status=nuevo_status)
            
            return Response({
                'message': f'Empresa {accion}da exitosamente',
                'empresa_id': empresa_id,
                'nuevo_status': empresa.status,
                'elementos_afectados': {
                    'plantas': plantas_afectadas,
                    'departamentos': departamentos_afectados,
                    'puestos': puestos_afectados,
                    'empleados': empleados_afectados
                }
            }, status=status.HTTP_200_OK)

        except Empresa.DoesNotExist:
            return Response(
                {'error': 'Empresa no encontrada'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {'error': f'Error al modificar empresa: {str(e)}'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    # ELIMINACIÓN DE EMPRESAS DESHABILITADA - Solo usar suspender/activar
    # @action(detail=False, methods=['delete'])
    # def eliminar_empresa(self, request):
    #     """Eliminar una empresa"""
    #     # Método deshabilitado - usar suspender_empresa en su lugar
    #     return Response(
    #         {'error': 'Eliminación de empresas no permitida. Use suspender/activar.'}, 
    #         status=status.HTTP_405_METHOD_NOT_ALLOWED
    #     )

    @action(detail=False, methods=['put'])
    def editar_empresa(self, request):
        """Editar una empresa"""
        try:
            empresa_id = request.data.get('empresa_id')
            
            if not empresa_id:
                return Response(
                    {'error': 'empresa_id es requerido'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            empresa = Empresa.objects.get(empresa_id=empresa_id)
            
            # Actualizar campos permitidos (telefono removido según solicitud)
            campos_permitidos = ['nombre', 'rfc', 'direccion', 'email_contacto', 'status']
            for campo in campos_permitidos:
                if campo in request.data:
                    setattr(empresa, campo, request.data[campo])
            
            empresa.save()
            
            return Response({
                'message': 'Empresa actualizada exitosamente',
                'empresa_id': empresa_id
            }, status=status.HTTP_200_OK)

        except Empresa.DoesNotExist:
            return Response(
                {'error': 'Empresa no encontrada'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {'error': f'Error al editar empresa: {str(e)}'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    # ==================== PLANTAS ====================
    @action(detail=False, methods=['get'])
    def listar_plantas(self, request):
        """Listar todas las plantas con filtros"""
        try:
            queryset = Planta.objects.select_related('empresa').all()
            
            # Filtros
            buscar = request.query_params.get('buscar', '')
            if buscar:
                queryset = queryset.filter(nombre__icontains=buscar)
            
            status_filter = request.query_params.get('status', '')
            if status_filter == 'true':
                queryset = queryset.filter(status=True)
            elif status_filter == 'false':
                queryset = queryset.filter(status=False)
                
            empresa_filter = request.query_params.get('empresa', '')
            if empresa_filter:
                queryset = queryset.filter(empresa_id=empresa_filter)

            plantas_data = []
            for planta in queryset:
                try:
                    departamentos_count = Departamento.objects.filter(planta=planta).count()
                    empleados_count = Empleado.objects.filter(puesto__departamento__planta=planta).count()
                    
                    planta_data = {
                        'planta_id': planta.planta_id,
                        'nombre': planta.nombre,
                        'direccion': planta.direccion,
                        'fecha_registro': planta.fecha_registro,
                        'status': planta.status,
                        'empresa': {
                            'id': planta.empresa.empresa_id,
                            'nombre': planta.empresa.nombre,
                            'status': planta.empresa.status
                        },
                        'empresa_nombre': planta.empresa.nombre,  # Agregado para compatibilidad frontend
                        'departamentos_count': departamentos_count,
                        'empleados_count': empleados_count,
                    }
                    plantas_data.append(planta_data)
                except Exception as e:
                    print(f"Error procesando planta {planta.planta_id}: {e}")
                    continue

            return Response({
                'plantas': plantas_data,
                'total': len(plantas_data)
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {'error': f'Error al listar plantas: {str(e)}'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=False, methods=['post'])
    def suspender_planta(self, request):
        """Suspender o activar una planta"""
        try:
            planta_id = request.data.get('planta_id')
            accion = request.data.get('accion')
            
            if not planta_id or not accion:
                return Response(
                    {'error': 'planta_id y accion son requeridos'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            planta = Planta.objects.get(planta_id=planta_id)
            
            if accion == 'suspender':
                planta.status = False
            elif accion == 'activar':
                planta.status = True
            else:
                return Response(
                    {'error': 'Acción no válida'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            planta.save()
            
            return Response({
                'message': f'Planta {accion}da exitosamente',
                'planta_id': planta_id,
                'nuevo_status': planta.status
            }, status=status.HTTP_200_OK)

        except Planta.DoesNotExist:
            return Response({'error': 'Planta no encontrada'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': f'Error al modificar planta: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # ELIMINACIÓN DE PLANTAS DESHABILITADA - Solo usar suspender/activar
    # @action(detail=False, methods=['delete'])
    # def eliminar_planta(self, request):
    #     """Eliminar una planta"""
    #     # Método deshabilitado - usar suspender_planta en su lugar
    #     return Response(
    #         {'error': 'Eliminación de plantas no permitida. Use suspender/activar.'}, 
    #         status=status.HTTP_405_METHOD_NOT_ALLOWED
    #     )

    @action(detail=False, methods=['put'])
    def editar_planta(self, request):
        """Editar una planta"""
        try:
            planta_id = request.data.get('planta_id')
            if not planta_id:
                return Response({'error': 'planta_id es requerido'}, status=status.HTTP_400_BAD_REQUEST)
            
            planta = Planta.objects.get(planta_id=planta_id)
            
            campos_permitidos = ['nombre', 'direccion', 'status']
            for campo in campos_permitidos:
                if campo in request.data:
                    setattr(planta, campo, request.data[campo])
            
            planta.save()
            
            return Response({'message': 'Planta actualizada exitosamente', 'planta_id': planta_id}, status=status.HTTP_200_OK)

        except Planta.DoesNotExist:
            return Response({'error': 'Planta no encontrada'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': f'Error al editar planta: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # ==================== DEPARTAMENTOS ====================
    @action(detail=False, methods=['get'])
    def listar_departamentos(self, request):
        """Listar todos los departamentos con filtros"""
        try:
            queryset = Departamento.objects.select_related('planta', 'planta__empresa').all()
            
            buscar = request.query_params.get('buscar', '')
            if buscar:
                queryset = queryset.filter(nombre__icontains=buscar)
            
            status_filter = request.query_params.get('status', '')
            if status_filter == 'true':
                queryset = queryset.filter(status=True)
            elif status_filter == 'false':
                queryset = queryset.filter(status=False)
                
            planta_filter = request.query_params.get('planta', '')
            if planta_filter:
                queryset = queryset.filter(planta_id=planta_filter)

            departamentos_data = []
            for depto in queryset:
                try:
                    puestos_count = Puesto.objects.filter(departamento=depto).count()
                    empleados_count = Empleado.objects.filter(puesto__departamento=depto).count()
                    
                    depto_data = {
                        'departamento_id': depto.departamento_id,
                        'nombre': depto.nombre,
                        'descripcion': depto.descripcion,
                        'fecha_registro': depto.fecha_registro,
                        'status': depto.status,
                        'planta': {
                            'id': depto.planta.planta_id,
                            'nombre': depto.planta.nombre,
                            'status': depto.planta.status
                        },
                        'planta_nombre': depto.planta.nombre,  # Agregado para compatibilidad frontend
                        'empresa': {
                            'id': depto.planta.empresa.empresa_id,
                            'nombre': depto.planta.empresa.nombre,
                            'status': depto.planta.empresa.status
                        },
                        'empresa_nombre': depto.planta.empresa.nombre,  # Agregado para compatibilidad frontend
                        'puestos_count': puestos_count,
                        'empleados_count': empleados_count,
                    }
                    departamentos_data.append(depto_data)
                except Exception as e:
                    print(f"Error procesando departamento {depto.departamento_id}: {e}")
                    continue

            return Response({
                'departamentos': departamentos_data,
                'total': len(departamentos_data)
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': f'Error al listar departamentos: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['post'])
    def suspender_departamento(self, request):
        """Suspender o activar un departamento"""
        try:
            departamento_id = request.data.get('departamento_id')
            accion = request.data.get('accion')
            
            if not departamento_id or not accion:
                return Response({'error': 'departamento_id y accion son requeridos'}, status=status.HTTP_400_BAD_REQUEST)
            
            depto = Departamento.objects.get(departamento_id=departamento_id)
            
            if accion == 'suspender':
                depto.status = False
            elif accion == 'activar':
                depto.status = True
            else:
                return Response({'error': 'Acción no válida'}, status=status.HTTP_400_BAD_REQUEST)
            
            depto.save()
            
            return Response({
                'message': f'Departamento {accion}do exitosamente',
                'departamento_id': departamento_id,
                'nuevo_status': depto.status
            }, status=status.HTTP_200_OK)

        except Departamento.DoesNotExist:
            return Response({'error': 'Departamento no encontrado'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': f'Error al modificar departamento: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # ELIMINACIÓN DE DEPARTAMENTOS DESHABILITADA - Solo usar suspender/activar
    # @action(detail=False, methods=['delete'])
    # def eliminar_departamento(self, request):
    #     """Eliminar un departamento"""
    #     # Método deshabilitado - usar suspender_departamento en su lugar
    #     return Response(
    #         {'error': 'Eliminación de departamentos no permitida. Use suspender/activar.'}, 
    #         status=status.HTTP_405_METHOD_NOT_ALLOWED
    #     )

    @action(detail=False, methods=['put'])
    def editar_departamento(self, request):
        """Editar un departamento"""
        try:
            departamento_id = request.data.get('departamento_id')
            if not departamento_id:
                return Response({'error': 'departamento_id es requerido'}, status=status.HTTP_400_BAD_REQUEST)
            
            depto = Departamento.objects.get(departamento_id=departamento_id)
            
            campos_permitidos = ['nombre', 'descripcion', 'status']
            for campo in campos_permitidos:
                if campo in request.data:
                    setattr(depto, campo, request.data[campo])
            
            depto.save()
            
            return Response({'message': 'Departamento actualizado exitosamente', 'departamento_id': departamento_id}, status=status.HTTP_200_OK)

        except Departamento.DoesNotExist:
            return Response({'error': 'Departamento no encontrado'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': f'Error al editar departamento: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # ==================== PUESTOS ====================
    @action(detail=False, methods=['get'])
    def listar_puestos(self, request):
        """Listar todos los puestos con filtros"""
        try:
            queryset = Puesto.objects.select_related('departamento', 'departamento__planta', 'departamento__planta__empresa').all()
            
            buscar = request.query_params.get('buscar', '')
            if buscar:
                queryset = queryset.filter(nombre__icontains=buscar)
            
            status_filter = request.query_params.get('status', '')
            if status_filter == 'true':
                queryset = queryset.filter(status=True)
            elif status_filter == 'false':
                queryset = queryset.filter(status=False)
                
            departamento_filter = request.query_params.get('departamento', '')
            if departamento_filter:
                queryset = queryset.filter(departamento_id=departamento_filter)

            puestos_data = []
            for puesto in queryset:
                try:
                    empleados_count = Empleado.objects.filter(puesto=puesto).count()
                    
                    puesto_data = {
                        'puesto_id': puesto.puesto_id,
                        'nombre': puesto.nombre,
                        'descripcion': puesto.descripcion,
                        'status': puesto.status,
                        'departamento': {
                            'id': puesto.departamento.departamento_id,
                            'nombre': puesto.departamento.nombre,
                            'status': puesto.departamento.status
                        },
                        'planta': {
                            'id': puesto.departamento.planta.planta_id,
                            'nombre': puesto.departamento.planta.nombre,
                            'status': puesto.departamento.planta.status
                        },
                        'empresa': {
                            'id': puesto.departamento.planta.empresa.empresa_id,
                            'nombre': puesto.departamento.planta.empresa.nombre,
                            'status': puesto.departamento.planta.empresa.status
                        },
                        'empleados_count': empleados_count,
                    }
                    puestos_data.append(puesto_data)
                except Exception as e:
                    print(f"Error procesando puesto {puesto.puesto_id}: {e}")
                    continue

            return Response({
                'puestos': puestos_data,
                'total': len(puestos_data)
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': f'Error al listar puestos: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['post'])
    def suspender_puesto(self, request):
        """Suspender o activar un puesto"""
        try:
            puesto_id = request.data.get('puesto_id')
            accion = request.data.get('accion')
            
            if not puesto_id or not accion:
                return Response({'error': 'puesto_id y accion son requeridos'}, status=status.HTTP_400_BAD_REQUEST)
            
            puesto = Puesto.objects.get(puesto_id=puesto_id)
            
            if accion == 'suspender':
                puesto.status = False
            elif accion == 'activar':
                puesto.status = True
            else:
                return Response({'error': 'Acción no válida'}, status=status.HTTP_400_BAD_REQUEST)
            
            puesto.save()
            
            return Response({
                'message': f'Puesto {accion}do exitosamente',
                'puesto_id': puesto_id,
                'nuevo_status': puesto.status
            }, status=status.HTTP_200_OK)

        except Puesto.DoesNotExist:
            return Response({'error': 'Puesto no encontrado'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': f'Error al modificar puesto: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # ELIMINACIÓN DE PUESTOS DESHABILITADA - Solo usar suspender/activar
    # @action(detail=False, methods=['delete'])
    # def eliminar_puesto(self, request):
    #     """Eliminar un puesto"""
    #     # Método deshabilitado - usar suspender_puesto en su lugar
    #     return Response(
    #         {'error': 'Eliminación de puestos no permitida. Use suspender/activar.'}, 
    #         status=status.HTTP_405_METHOD_NOT_ALLOWED
    #     )

    @action(detail=False, methods=['put'])
    def editar_puesto(self, request):
        """Editar un puesto"""
        try:
            puesto_id = request.data.get('puesto_id')
            if not puesto_id:
                return Response({'error': 'puesto_id es requerido'}, status=status.HTTP_400_BAD_REQUEST)
            
            puesto = Puesto.objects.get(puesto_id=puesto_id)
            
            campos_permitidos = ['nombre', 'descripcion', 'status']
            for campo in campos_permitidos:
                if campo in request.data:
                    setattr(puesto, campo, request.data[campo])
            
            puesto.save()
            
            return Response({'message': 'Puesto actualizado exitosamente', 'puesto_id': puesto_id}, status=status.HTTP_200_OK)

        except Puesto.DoesNotExist:
            return Response({'error': 'Puesto no encontrado'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': f'Error al editar puesto: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # ==================== EMPLEADOS ====================
    @action(detail=False, methods=['get'])
    def listar_empleados(self, request):
        """Listar todos los empleados con filtros"""
        try:
            queryset = Empleado.objects.select_related('puesto', 'puesto__departamento', 'puesto__departamento__planta').all()
            
            buscar = request.query_params.get('buscar', '')
            if buscar:
                queryset = queryset.filter(nombre__icontains=buscar)
            
            status_filter = request.query_params.get('status', '')
            if status_filter == 'true':
                queryset = queryset.filter(status=True)
            elif status_filter == 'false':
                queryset = queryset.filter(status=False)
                
            planta_filter = request.query_params.get('planta', '')
            if planta_filter:
                queryset = queryset.filter(puesto__departamento__planta_id=planta_filter)

            empleados_data = []
            for empleado in queryset:
                try:
                    # Crear nombre completo
                    nombre_completo = f"{empleado.nombre} {empleado.apellido_paterno}"
                    if empleado.apellido_materno:
                        nombre_completo += f" {empleado.apellido_materno}"
                    
                    empleado_data = {
                        'empleado_id': empleado.empleado_id,
                        'nombre': empleado.nombre,
                        'apellido_paterno': empleado.apellido_paterno,
                        'apellido_materno': empleado.apellido_materno or '',
                        'nombre_completo': nombre_completo,  # Agregado para mostrar en frontend
                        'email': empleado.email,
                        # 'telefono': empleado.telefono,  # REMOVIDO según solicitud
                        'fecha_ingreso': empleado.fecha_ingreso,
                        'status': empleado.status,
                    }
                    
                    # Información del puesto (si existe)
                    if empleado.puesto:
                        empleado_data['puesto'] = {
                            'id': empleado.puesto.puesto_id,
                            'nombre': empleado.puesto.nombre,
                            'status': empleado.puesto.status
                        }
                        empleado_data['puesto_nombre'] = empleado.puesto.nombre
                        
                        # Información del departamento (a través del puesto)
                        if empleado.puesto.departamento:
                            empleado_data['departamento'] = {
                                'id': empleado.puesto.departamento.departamento_id,
                                'nombre': empleado.puesto.departamento.nombre,
                                'status': empleado.puesto.departamento.status
                            }
                            empleado_data['departamento_nombre'] = empleado.puesto.departamento.nombre
                            
                            # Información de la planta (a través del departamento)
                            if empleado.puesto.departamento.planta:
                                empleado_data['planta'] = {
                                    'id': empleado.puesto.departamento.planta.planta_id,
                                    'nombre': empleado.puesto.departamento.planta.nombre,
                                    'status': empleado.puesto.departamento.planta.status
                                }
                                empleado_data['planta_nombre'] = empleado.puesto.departamento.planta.nombre
                                
                                # Información de la empresa (a través de la planta)
                                if empleado.puesto.departamento.planta.empresa:
                                    empleado_data['empresa'] = {
                                        'id': empleado.puesto.departamento.planta.empresa.empresa_id,
                                        'nombre': empleado.puesto.departamento.planta.empresa.nombre,
                                        'status': empleado.puesto.departamento.planta.empresa.status
                                    }
                                    empleado_data['empresa_nombre'] = empleado.puesto.departamento.planta.empresa.nombre
                    
                    empleados_data.append(empleado_data)
                except Exception as e:
                    print(f"Error procesando empleado {empleado.empleado_id}: {e}")
                    continue

            return Response({
                'empleados': empleados_data,
                'total': len(empleados_data)
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': f'Error al listar empleados: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['post'])
    def suspender_empleado(self, request):
        """Suspender o activar un empleado"""
        try:
            empleado_id = request.data.get('empleado_id')
            accion = request.data.get('accion')
            
            if not empleado_id or not accion:
                return Response({'error': 'empleado_id y accion son requeridos'}, status=status.HTTP_400_BAD_REQUEST)
            
            empleado = Empleado.objects.get(empleado_id=empleado_id)
            
            if accion == 'suspender':
                empleado.status = False
            elif accion == 'activar':
                empleado.status = True
            else:
                return Response({'error': 'Acción no válida'}, status=status.HTTP_400_BAD_REQUEST)
            
            empleado.save()
            
            return Response({
                'message': f'Empleado {accion}do exitosamente',
                'empleado_id': empleado_id,
                'nuevo_status': empleado.status
            }, status=status.HTTP_200_OK)

        except Empleado.DoesNotExist:
            return Response({'error': 'Empleado no encontrado'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': f'Error al modificar empleado: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['delete'])
    def eliminar_empleado(self, request):
        """Eliminar un empleado"""
        try:
            empleado_id = request.data.get('empleado_id')
            if not empleado_id:
                return Response({'error': 'empleado_id es requerido'}, status=status.HTTP_400_BAD_REQUEST)
            
            empleado = Empleado.objects.get(empleado_id=empleado_id)
            empleado.delete()
            
            return Response({'message': 'Empleado eliminado exitosamente', 'empleado_id': empleado_id}, status=status.HTTP_200_OK)

        except Empleado.DoesNotExist:
            return Response({'error': 'Empleado no encontrado'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': f'Error al eliminar empleado: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['put'])
    def editar_empleado(self, request):
        """Editar un empleado"""
        try:
            empleado_id = request.data.get('empleado_id')
            if not empleado_id:
                return Response({'error': 'empleado_id es requerido'}, status=status.HTTP_400_BAD_REQUEST)
            
            empleado = Empleado.objects.get(empleado_id=empleado_id)
            
            # Campos editables: solo nombres, apellidos y status
            # No se puede editar: telefono, fecha_ingreso (fecha de creación), email (no necesario)
            campos_permitidos = ['nombre', 'apellido_paterno', 'apellido_materno', 'status']
            for campo in campos_permitidos:
                if campo in request.data:
                    setattr(empleado, campo, request.data[campo])
            
            empleado.save()
            
            return Response({'message': 'Empleado actualizado exitosamente', 'empleado_id': empleado_id}, status=status.HTTP_200_OK)

        except Empleado.DoesNotExist:
            return Response({'error': 'Empleado no encontrado'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': f'Error al editar empleado: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # ==================== ALIAS ENDPOINTS (para compatibilidad frontend) ====================
    @action(detail=False, methods=['get'])
    def listar_todas_plantas(self, request):
        """Alias para listar_plantas - para compatibilidad frontend"""
        return self.listar_plantas(request)

    @action(detail=False, methods=['get'])
    def listar_todos_departamentos(self, request):
        """Alias para listar_departamentos - para compatibilidad frontend"""
        return self.listar_departamentos(request)

    @action(detail=False, methods=['get'])
    def listar_todos_puestos(self, request):
        """Alias para listar_puestos - para compatibilidad frontend"""
        return self.listar_puestos(request)

    @action(detail=False, methods=['get'])
    def listar_todos_empleados(self, request):
        """Alias para listar_empleados - para compatibilidad frontend"""
        return self.listar_empleados(request)

    # ==================== CRUD USUARIOS ====================
    @action(detail=False, methods=['put'])
    def editar_usuario(self, request):
        """Editar información de un usuario"""
        try:
            usuario_id = request.data.get('usuario_id')
            
            if not usuario_id:
                return Response(
                    {'error': 'usuario_id es requerido'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            usuario = User.objects.get(id=usuario_id)
            
            # Campos editables (sin incluir rol/nivel_usuario)
            campos_permitidos = ['username', 'email', 'first_name', 'last_name', 'is_active']
            
            for campo in campos_permitidos:
                if campo in request.data:
                    if campo == 'username':
                        # Verificar que el username no exista
                        if User.objects.filter(username=request.data[campo]).exclude(id=usuario_id).exists():
                            return Response(
                                {'error': 'El username ya existe'}, 
                                status=status.HTTP_400_BAD_REQUEST
                            )
                    setattr(usuario, campo, request.data[campo])
            
            usuario.save()
            
            return Response(
                {
                    'message': 'Usuario actualizado exitosamente', 
                    'usuario_id': usuario_id
                }, 
                status=status.HTTP_200_OK
            )

        except User.DoesNotExist:
            return Response(
                {'error': 'Usuario no encontrado'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {'error': f'Error al editar usuario: {str(e)}'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=False, methods=['delete'])
    def eliminar_usuario(self, request):
        """Eliminar un usuario"""
        try:
            usuario_id = request.data.get('usuario_id')
            
            if not usuario_id:
                return Response(
                    {'error': 'usuario_id es requerido'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Primero intentar encontrar por perfil_id (más común)
            try:
                perfil = PerfilUsuario.objects.get(id=usuario_id)
                
                # No permitir eliminar superadmin
                if perfil.nivel_usuario == 'superadmin':
                    return Response(
                        {'error': 'No se puede eliminar el usuario SuperAdmin'}, 
                        status=status.HTTP_403_FORBIDDEN
                    )
                
                # Desactivar perfil
                perfil.status = False
                perfil.save()
                
                # Si tiene usuario Django asociado, también desactivarlo
                if perfil.user:
                    perfil.user.is_active = False
                    perfil.user.save()
                
                return Response(
                    {
                        'message': 'Usuario eliminado (desactivado) exitosamente', 
                        'usuario_id': usuario_id
                    }, 
                    status=status.HTTP_200_OK
                )
                
            except PerfilUsuario.DoesNotExist:
                # Si no se encuentra por perfil_id, intentar por user_id
                try:
                    usuario = User.objects.get(id=usuario_id)
                    
                    # No permitir eliminar superadmin
                    if hasattr(usuario, 'perfil') and usuario.perfil.nivel_usuario == 'superadmin':
                        return Response(
                            {'error': 'No se puede eliminar el usuario SuperAdmin'}, 
                            status=status.HTTP_403_FORBIDDEN
                        )
                    
                    # Desactivar usuario Django
                    usuario.is_active = False
                    usuario.save()
                    
                    # También desactivar perfil si existe
                    if hasattr(usuario, 'perfil'):
                        usuario.perfil.status = False
                        usuario.perfil.save()
                    
                    return Response(
                        {
                            'message': 'Usuario eliminado (desactivado) exitosamente', 
                            'usuario_id': usuario_id
                        }, 
                        status=status.HTTP_200_OK
                    )
                    
                except User.DoesNotExist:
                    return Response(
                        {'error': 'Usuario no encontrado'}, 
                        status=status.HTTP_404_NOT_FOUND
                    )

        except Exception as e:
            return Response(
                {'error': f'Error al eliminar usuario: {str(e)}'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=False, methods=['put'])
    def suspender_usuario(self, request):
        """Suspender/activar un usuario"""
        try:
            usuario_id = request.data.get('usuario_id')
            accion = request.data.get('accion', 'suspender')  # 'suspender' o 'activar'
            
            if not usuario_id:
                return Response(
                    {'error': 'usuario_id es requerido'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            usuario = User.objects.get(id=usuario_id)
            
            # No permitir suspender superadmin
            if hasattr(usuario, 'perfil') and usuario.perfil.nivel_usuario == 'superadmin':
                return Response(
                    {'error': 'No se puede suspender el usuario SuperAdmin'}, 
                    status=status.HTTP_403_FORBIDDEN
                )
            
            if accion == 'suspender':
                usuario.is_active = False
            else:
                usuario.is_active = True
            
            usuario.save()
            
            return Response(
                {
                    'message': f'Usuario {accion}do exitosamente',
                    'usuario_id': usuario_id,
                    'nuevo_status': usuario.is_active
                }, 
                status=status.HTTP_200_OK
            )

        except User.DoesNotExist:
            return Response(
                {'error': 'Usuario no encontrado'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {'error': f'Error al modificar usuario: {str(e)}'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
