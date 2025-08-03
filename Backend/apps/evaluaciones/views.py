# # -*- coding: utf-8 -*-
# from rest_framework import viewsets, permissions, status
# from rest_framework.decorators import action, api_view, permission_classes
# from rest_framework.response import Response
# from django.utils.decorators import method_decorator
# from django.views.decorators.csrf import csrf_exempt
# from django.db.models import Q, Count, Max
# from django.db import models
# from django.utils import timezone
# from .models import (
#     TipoEvaluacion, Pregunta, EvaluacionCompleta, EvaluacionPregunta,
#     RespuestaEvaluacion, DetalleRespuesta, ResultadoEvaluacion
# )
# from .serializers import (
#     TipoEvaluacionSerializer, PreguntaSerializer, PreguntaCreateSerializer,
#     EvaluacionSerializer, EvaluacionCreateSerializer,
#     RespuestaEvaluacionSerializer, RespuestaEvaluacionCreateSerializer,
#     ResultadoEvaluacionSerializer
# )

# from .models import (
#     TipoEvaluacion, Pregunta, EvaluacionCompleta, EvaluacionPregunta,
#     RespuestaEvaluacion, DetalleRespuesta, ResultadoEvaluacion, SeccionPregunta
# )

# # Importar modelos oficiales para las normas NOM
# from .models_oficiales import (
#     EvaluacionOficial, SeccionOficial, PreguntaOficial,
#     AsignacionEvaluacion, EmpleadoAsignado, RespuestaEmpleado
# )

# @method_decorator(csrf_exempt, name='dispatch')
# class TipoEvaluacionViewSet(viewsets.ModelViewSet):
#     queryset = TipoEvaluacion.objects.filter(activo=True)
#     serializer_class = TipoEvaluacionSerializer
#     permission_classes = [permissions.IsAuthenticated]

# @method_decorator(csrf_exempt, name='dispatch')
# class PreguntaViewSet(viewsets.ModelViewSet):
#     serializer_class = PreguntaSerializer
#     permission_classes = [permissions.IsAuthenticated]

#     def get_queryset(self):
#         user = self.request.user
#         queryset = Pregunta.objects.filter(activa=True)

#         # Filtros por parámetros
#         tipo_evaluacion = self.request.query_params.get('tipo_evaluacion')
#         if tipo_evaluacion:
#             queryset = queryset.filter(tipo_evaluacion__nombre=tipo_evaluacion)

#         # SuperAdmin ve todas las preguntas
#         if hasattr(user, 'perfil') and user.perfil.nivel_usuario == 'superadmin':
#             return queryset

#         # Admin empresa ve preguntas oficiales + las de su empresa
#         if hasattr(user, 'perfil') and user.perfil.nivel_usuario == 'admin-empresa':
#             return queryset.filter(
#                 Q(empresa__isnull=True) |  # Preguntas oficiales
#                 Q(empresa=user.perfil.empresa)  # Preguntas de su empresa
#             )

#         # Otros usuarios solo ven preguntas oficiales
#         return queryset.filter(empresa__isnull=True)

#     def get_serializer_class(self):
#         if self.action in ['create', 'update', 'partial_update']:
#             return PreguntaCreateSerializer
#         return PreguntaSerializer

#     @action(detail=False, methods=['get'])
#     def por_tipo(self, request):
#         """Obtener preguntas agrupadas por tipo de evaluación"""
#         tipo = request.query_params.get('tipo')
#         if not tipo:
#             return Response({'error': 'Tipo de evaluación requerido'}, status=status.HTTP_400_BAD_REQUEST)

#         preguntas = self.get_queryset().filter(tipo_evaluacion__nombre=tipo)
#         serializer = self.get_serializer(preguntas, many=True)

#         return Response({
#             'tipo_evaluacion': tipo,
#             'total_preguntas': preguntas.count(),
#             'preguntas': serializer.data
#         })

#     @action(detail=False, methods=['post'])
#     def crear_oficiales(self, request):
#         """Crear preguntas oficiales (solo superadmin)"""
#         if not (hasattr(request.user, 'perfil') and request.user.perfil.nivel_usuario == 'superadmin'):
#             return Response({'error': 'No tienes permisos para crear preguntas oficiales'},
#                           status=status.HTTP_403_FORBIDDEN)

#         # Crear preguntas predeterminadas
#         preguntas_creadas = self._crear_preguntas_oficiales()

#         return Response({
#             'message': f'Se crearon {preguntas_creadas} preguntas oficiales',
#             'preguntas_creadas': preguntas_creadas
#         })

#     def _crear_preguntas_oficiales(self):
#         """Crear preguntas oficiales para NOM-035, NOM-030 y 360°"""
#         preguntas_data = [
#             # NOM-035
#             {
#                 'tipo': 'NOM-035',
#                 'preguntas': [
#                     {
#                         'texto': '¿Consideras que tu carga de trabajo es excesiva?',
#                         'tipo_respuesta': 'escala',
#                         'opciones': ['Nunca', 'Casi nunca', 'A veces', 'Casi siempre', 'Siempre']
#                     },
#                     {
#                         'texto': '¿Tienes control sobre tu trabajo?',
#                         'tipo_respuesta': 'escala',
#                         'opciones': ['Nunca', 'Casi nunca', 'A veces', 'Casi siempre', 'Siempre']
#                     },
#                     {
#                         'texto': '¿Recibes apoyo de tus compañeros?',
#                         'tipo_respuesta': 'escala',
#                         'opciones': ['Nunca', 'Casi nunca', 'A veces', 'Casi siempre', 'Siempre']
#                     },
#                     {
#                         'texto': '¿Tu supervisor te brinda apoyo?',
#                         'tipo_respuesta': 'escala',
#                         'opciones': ['Nunca', 'Casi nunca', 'A veces', 'Casi siempre', 'Siempre']
#                     },
#                     {
#                         'texto': '¿Sientes que tu trabajo es reconocido?',
#                         'tipo_respuesta': 'escala',
#                         'opciones': ['Nunca', 'Casi nunca', 'A veces', 'Casi siempre', 'Siempre']
#                     }
#                 ]
#             },
#             # NOM-030
#             {
#                 'tipo': 'NOM-030',
#                 'preguntas': [
#                     {
#                         'texto': '¿Conoces los procedimientos de seguridad de tu área?',
#                         'tipo_respuesta': 'si_no',
#                         'opciones': ['Sí', 'No']
#                     },
#                     {
#                         'texto': '¿Utilizas el equipo de protección personal requerido?',
#                         'tipo_respuesta': 'si_no',
#                         'opciones': ['Sí', 'No']
#                     },
#                     {
#                         'texto': '¿Has recibido capacitación en seguridad en los últimos 6 meses?',
#                         'tipo_respuesta': 'si_no',
#                         'opciones': ['Sí', 'No']
#                     },
#                     {
#                         'texto': '¿Reportas los incidentes de seguridad?',
#                         'tipo_respuesta': 'si_no',
#                         'opciones': ['Sí', 'No']
#                     },
#                     {
#                         'texto': '¿Consideras que tu área de trabajo es segura?',
#                         'tipo_respuesta': 'escala',
#                         'opciones': ['Muy insegura', 'Insegura', 'Regular', 'Segura', 'Muy segura']
#                     }
#                 ]
#             },
#             # 360°
#             {
#                 'tipo': '360',
#                 'preguntas': [
#                     {
#                         'texto': '¿Cómo evalúas la comunicación del empleado?',
#                         'tipo_respuesta': 'escala',
#                         'opciones': ['Deficiente', 'Regular', 'Buena', 'Muy buena', 'Excelente']
#                     },
#                     {
#                         'texto': '¿Cómo evalúas el trabajo en equipo?',
#                         'tipo_respuesta': 'escala',
#                         'opciones': ['Deficiente', 'Regular', 'Buena', 'Muy buena', 'Excelente']
#                     },
#                     {
#                         'texto': '¿Cómo evalúas la iniciativa y proactividad?',
#                         'tipo_respuesta': 'escala',
#                         'opciones': ['Deficiente', 'Regular', 'Buena', 'Muy buena', 'Excelente']
#                     },
#                     {
#                         'texto': '¿Cómo evalúas el cumplimiento de objetivos?',
#                         'tipo_respuesta': 'escala',
#                         'opciones': ['Deficiente', 'Regular', 'Buena', 'Muy buena', 'Excelente']
#                     },
#                     {
#                         'texto': '¿Qué aspectos considera que debe mejorar?',
#                         'tipo_respuesta': 'texto',
#                         'opciones': []
#                     }
#                 ]
#             }
#         ]

#         total_creadas = 0
#         for tipo_data in preguntas_data:
#             tipo_eval, _ = TipoEvaluacion.objects.get_or_create(
#                 nombre=tipo_data['tipo'],
#                 defaults={
#                     'descripcion': f'Evaluación {tipo_data["tipo"]}',
#                     'normativa_oficial': tipo_data['tipo'].startswith('NOM')
#                 }
#             )

#             for i, pregunta_data in enumerate(tipo_data['preguntas'], 1):
#                 pregunta, created = Pregunta.objects.get_or_create(
#                     tipo_evaluacion=tipo_eval,
#                     texto_pregunta=pregunta_data['texto'],
#                     defaults={
#                         'tipo_respuesta': pregunta_data['tipo_respuesta'],
#                         'opciones_respuesta': pregunta_data['opciones'],
#                         'orden': i,
#                         'creada_por': self.request.user
#                     }
#                 )
#                 if created:
#                     total_creadas += 1

#         return total_creadas

# @method_decorator(csrf_exempt, name='dispatch')
# class EvaluacionViewSet(viewsets.ModelViewSet):
#     serializer_class = EvaluacionSerializer
#     permission_classes = [permissions.IsAuthenticated]

#     def get_queryset(self):
#         user = self.request.user

#         # SuperAdmin ve todas las evaluaciones
#         if hasattr(user, 'perfil') and user.perfil.nivel_usuario == 'superadmin':
#             return EvaluacionCompleta.objects.all()

#         # Admin empresa ve solo las de su empresa
#         if hasattr(user, 'perfil') and user.perfil.nivel_usuario == 'admin-empresa':
#             return EvaluacionCompleta.objects.filter(empresa=user.perfil.empresa)

#         # Otros usuarios ven evaluaciones donde están incluidos
#         perfil = getattr(user, 'perfil', None)
#         query = Q()
#         # Solo agrega los filtros si existen los atributos
#         if perfil:
#             if hasattr(perfil, 'plantas'):
#                 query |= Q(plantas__in=perfil.plantas.all())
#             if hasattr(perfil, 'departamentos'):
#                 query |= Q(departamentos__in=perfil.departamentos.all())
#         query |= Q(empleados_objetivo__perfil__user=user)
#         return EvaluacionCompleta.objects.filter(query).distinct()

#     def get_serializer_class(self):
#         if self.action in ['create', 'update', 'partial_update']:
#             return EvaluacionCreateSerializer
#         return EvaluacionSerializer

#     @action(detail=True, methods=['post'])
#     def activar(self, request, pk=None):
#         """Activar una evaluación"""
#         evaluacion = self.get_object()

#         if evaluacion.estado != 'borrador':
#             return Response({'error': 'Solo se pueden activar evaluaciones en borrador'},
#                           status=status.HTTP_400_BAD_REQUEST)

#         evaluacion.estado = 'activa'
#         evaluacion.save()

#         return Response({'message': 'Evaluación activada exitosamente'})

#     @action(detail=True, methods=['get'])
#     def resultados(self, request, pk=None):
#         """Obtener resultados de una evaluación"""
#         evaluacion = self.get_object()

#         try:
#             resultado = ResultadoEvaluacion.objects.get(evaluacion=evaluacion)
#             serializer = ResultadoEvaluacionSerializer(resultado)
#             return Response(serializer.data)
#         except ResultadoEvaluacion.DoesNotExist:
#             # Calcular resultados si no existen
#             return self._calcular_resultados(evaluacion)

#     def _calcular_resultados(self, evaluacion):
#         """Calcular resultados de una evaluación"""
#         respuestas = RespuestaEvaluacion.objects.filter(evaluacion=evaluacion, completada=True)
#         total_respuestas = respuestas.count()

#         if total_respuestas == 0:
#             return Response({'error': 'No hay respuestas para calcular resultados'},
#                           status=status.HTTP_400_BAD_REQUEST)

#         # Calcular métricas básicas
#         total_empleados_objetivo = evaluacion.empleados_objetivo.count()
#         if total_empleados_objetivo == 0:
#             # Si no hay empleados específicos, contar por plantas/departamentos
#             total_empleados_objetivo = 100  # Valor estimado

#         porcentaje_participacion = (total_respuestas / total_empleados_objetivo) * 100

#         # Crear o actualizar resultado
#         resultado, created = ResultadoEvaluacion.objects.get_or_create(
#             evaluacion=evaluacion,
#             defaults={
#                 'total_respuestas': total_respuestas,
#                 'porcentaje_participacion': porcentaje_participacion,
#                 'resultados_detallados': {},
#                 'recomendaciones': 'Resultados calculados automáticamente'
#             }
#         )

#         serializer = ResultadoEvaluacionSerializer(resultado)
#         return Response(serializer.data)

# @method_decorator(csrf_exempt, name='dispatch')
# class RespuestaEvaluacionViewSet(viewsets.ModelViewSet):
#     serializer_class = RespuestaEvaluacionSerializer
#     permission_classes = [permissions.IsAuthenticated]

#     def get_queryset(self):
#         user = self.request.user

#         # SuperAdmin ve todas las respuestas
#         if hasattr(user, 'perfil') and user.perfil.nivel_usuario == 'superadmin':
#             return RespuestaEvaluacion.objects.all()

#         # Admin empresa ve respuestas de su empresa
#         if hasattr(user, 'perfil') and user.perfil.nivel_usuario == 'admin-empresa':
#             return RespuestaEvaluacion.objects.filter(evaluacion__empresa=user.perfil.empresa)

#         # Empleados ven solo sus respuestas
#         return RespuestaEvaluacion.objects.filter(empleado__perfil__user=user)

#     def get_serializer_class(self):
#         if self.action in ['create']:
#             return RespuestaEvaluacionCreateSerializer
#         return RespuestaEvaluacionSerializer

#     @action(detail=False, methods=['get'])
#     def mis_evaluaciones(self, request):
#         """Obtener evaluaciones disponibles para el usuario actual"""
#         user = request.user

#         if not hasattr(user, 'perfil'):
#             return Response({'error': 'Usuario sin perfil'}, status=status.HTTP_400_BAD_REQUEST)

#         # Buscar evaluaciones donde el usuario está incluido
#         evaluaciones = EvaluacionCompleta.objects.filter(
#             estado='activa',
#             fecha_inicio__lte=timezone.now(),
#             fecha_fin__gte=timezone.now()
#         ).filter(
#             Q(empleados_objetivo__perfil__user=user) |
#             Q(departamentos__in=user.perfil.departamentos.all()) |
#             Q(plantas__in=user.perfil.plantas.all())
#         ).distinct()

#         # Filtrar las que no ha respondido
#         evaluaciones_sin_responder = []
#         for evaluacion in evaluaciones:
#             if not RespuestaEvaluacion.objects.filter(evaluacion=evaluacion, empleado__perfil__user=user).exists():
#                 evaluaciones_sin_responder.append(evaluacion)

#         serializer = EvaluacionSerializer(evaluaciones_sin_responder, many=True)
#         return Response(serializer.data)


# @api_view(['GET'])
# def preguntas_nom035(request):
#     # El ID de la evaluación NOM-035 es 1
#     preguntas = SeccionPregunta.objects.filter(
#         seccion__evaluacion__id=1
#     ).select_related('pregunta')
#     data = []
#     for sp in preguntas:
#         data.append({
#             'id': sp.pregunta.id,
#             'texto_pregunta': sp.pregunta.texto_pregunta,
#             # ...otros campos que quieras mostrar...
#         })
#     return Response({'total': len(data), 'preguntas': data})


# # ===== EVALUACIONES OFICIALES =====
# from .models_oficiales import EvaluacionOficial, SeccionOficial, PreguntaOficial

# @method_decorator(csrf_exempt, name='dispatch')
# class EvaluacionOficialViewSet(viewsets.ModelViewSet):
#     """ViewSet para evaluaciones oficiales NOM-030 y NOM-035"""
#     queryset = EvaluacionOficial.objects.filter(activa=True)
#     permission_classes = [permissions.AllowAny]  # Permitir acceso sin autenticación temporalmente

#     def get_serializer_class(self):
#         from .serializers_oficiales import EvaluacionOficialSerializer
#         return EvaluacionOficialSerializer

#     @action(detail=True, methods=['get'])
#     def preguntas(self, request, pk=None):
#         """Obtener todas las preguntas de una evaluación oficial"""
#         evaluacion = self.get_object()
#         secciones = evaluacion.secciones.all().order_by('numero_orden')

#         data = []
#         for seccion in secciones:
#             preguntas = seccion.preguntas.all().order_by('numero_orden')
#             for pregunta in preguntas:
#                 data.append({
#                     'id': pregunta.id,
#                     'numero_orden': pregunta.numero_orden,
#                     'texto': pregunta.texto_pregunta,
#                     'tipo': pregunta.tipo_pregunta.lower(),
#                     'opciones': pregunta.opciones_respuesta,
#                     'obligatoria': pregunta.es_obligatoria,
#                     'normativa': evaluacion.tipo_norma.lower().replace('-', '_'),
#                     'seccion': {
#                         'id': seccion.id,
#                         'nombre': seccion.nombre,
#                         'numero_orden': seccion.numero_orden
#                     }
#                 })

#         return Response({
#             'evaluacion': {
#                 'id': evaluacion.id,
#                 'tipo_norma': evaluacion.tipo_norma,
#                 'nombre': evaluacion.nombre,
#                 'descripcion': evaluacion.descripcion
#             },
#             'total_preguntas': len(data),
#             'preguntas': data
#         })

# @method_decorator(csrf_exempt, name='dispatch')
# class PreguntaOficialViewSet(viewsets.ModelViewSet):
#     """ViewSet para preguntas oficiales"""
#     serializer_class = PreguntaSerializer  # Usamos el serializer existente temporalmente
#     permission_classes = [permissions.AllowAny]  # Permitir acceso sin autenticación temporalmente

#     def get_queryset(self):
#         queryset = PreguntaOficial.objects.all()

#         # Filtrar por normativa si se especifica
#         normativa = self.request.query_params.get('normativa')
#         if normativa:
#             # Convertir nom_030 -> NOM-030
#             tipo_norma = normativa.upper().replace('_', '-')
#             queryset = queryset.filter(seccion__evaluacion_oficial__tipo_norma=tipo_norma)

#         return queryset.order_by('seccion__numero_orden', 'numero_orden')

#     def create(self, request, *args, **kwargs):
#         """Crear nueva pregunta oficial"""
#         try:
#             data = request.data

#             # Determinar la normativa (del request o parámetro)
#             normativa = data.get('normativa', 'nom_035')  # Por defecto NOM-035
#             tipo_norma = normativa.upper().replace('_', '-')

#             # Buscar la evaluación oficial correspondiente
#             evaluacion = EvaluacionOficial.objects.get(tipo_norma=tipo_norma, activa=True)

#             # Buscar una sección apropiada o usar la primera disponible
#             seccion = evaluacion.secciones.first()
#             if not seccion:
#                 return Response(
#                     {'error': f'No hay secciones disponibles para {tipo_norma}'},
#                     status=status.HTTP_400_BAD_REQUEST
#                 )

#             # Determinar el próximo número de orden
#             ultimo_numero = PreguntaOficial.objects.filter(
#                 seccion__evaluacion_oficial=evaluacion
#             ).aggregate(max_orden=Max('numero_orden'))['max_orden'] or 0

#             # Crear la pregunta
#             pregunta = PreguntaOficial.objects.create(
#                 texto_pregunta=data.get('texto', ''),
#                 tipo_pregunta=data.get('tipo', 'multiple').capitalize(),
#                 opciones_respuesta=data.get('opciones', []),
#                 es_obligatoria=data.get('obligatoria', True),
#                 numero_orden=data.get('numero_orden', ultimo_numero + 1),
#                 seccion=seccion
#             )

#             # Respuesta en formato esperado por el frontend
#             return Response({
#                 'id': pregunta.id,
#                 'numero_orden': pregunta.numero_orden,
#                 'texto': pregunta.texto_pregunta,
#                 'tipo': pregunta.tipo_pregunta.lower(),
#                 'opciones': pregunta.opciones_respuesta,
#                 'obligatoria': pregunta.es_obligatoria,
#                 'normativa': normativa,
#                 'seccion': {
#                     'id': seccion.id,
#                     'nombre': seccion.nombre,
#                     'numero_orden': seccion.numero_orden
#                 }
#             }, status=status.HTTP_201_CREATED)

#         except EvaluacionOficial.DoesNotExist:
#             return Response(
#                 {'error': f'No se encontró la evaluación oficial para {normativa}'},
#                 status=status.HTTP_404_NOT_FOUND
#             )
#         except Exception as e:
#             return Response(
#                 {'error': f'Error al crear pregunta: {str(e)}'},
#                 status=status.HTTP_400_BAD_REQUEST
#             )

#     def update(self, request, *args, **kwargs):
#         """Actualizar pregunta oficial existente"""
#         try:
#             pregunta = self.get_object()
#             data = request.data

#             # Actualizar campos
#             if 'texto' in data:
#                 pregunta.texto_pregunta = data['texto']
#             if 'tipo' in data:
#                 pregunta.tipo_pregunta = data['tipo'].capitalize()
#             if 'opciones' in data:
#                 pregunta.opciones_respuesta = data['opciones']
#             if 'obligatoria' in data:
#                 pregunta.es_obligatoria = data['obligatoria']
#             if 'numero_orden' in data:
#                 pregunta.numero_orden = data['numero_orden']

#             pregunta.save()

#             # Respuesta en formato esperado por el frontend
#             normativa = pregunta.seccion.evaluacion_oficial.tipo_norma.lower().replace('-', '_')
#             return Response({
#                 'id': pregunta.id,
#                 'numero_orden': pregunta.numero_orden,
#                 'texto': pregunta.texto_pregunta,
#                 'tipo': pregunta.tipo_pregunta.lower(),
#                 'opciones': pregunta.opciones_respuesta,
#                 'obligatoria': pregunta.es_obligatoria,
#                 'normativa': normativa,
#                 'seccion': {
#                     'id': pregunta.seccion.id,
#                     'nombre': pregunta.seccion.nombre,
#                     'numero_orden': pregunta.seccion.numero_orden
#                 }
#             })

#         except Exception as e:
#             return Response(
#                 {'error': f'Error al actualizar pregunta: {str(e)}'},
#                 status=status.HTTP_400_BAD_REQUEST
#             )

#     def list(self, request, *args, **kwargs):
#         """Listar preguntas oficiales con formato específico"""
#         queryset = self.get_queryset()

#         # Agrupar por normativa
#         data = {}
#         for pregunta in queryset:
#             normativa = pregunta.seccion.evaluacion_oficial.tipo_norma.lower().replace('-', '_')

#             if normativa not in data:
#                 data[normativa] = {
#                     'id': pregunta.seccion.evaluacion_oficial.id,
#                     'tipo_norma': pregunta.seccion.evaluacion_oficial.tipo_norma,
#                     'nombre': pregunta.seccion.evaluacion_oficial.nombre,
#                     'descripcion': pregunta.seccion.evaluacion_oficial.descripcion,
#                     'preguntas': []
#                 }

#             data[normativa]['preguntas'].append({
#                 'id': pregunta.id,
#                 'numero_orden': pregunta.numero_orden,
#                 'texto': pregunta.texto_pregunta,
#                 'tipo': pregunta.tipo_pregunta.lower(),
#                 'opciones': pregunta.opciones_respuesta,
#                 'obligatoria': pregunta.es_obligatoria,
#                 'normativa': normativa,
#                 'seccion': {
#                     'id': pregunta.seccion.id,
#                     'nombre': pregunta.seccion.nombre,
#                     'numero_orden': pregunta.seccion.numero_orden
#                 }
#             })

#         return Response({
#             'total_normativas': len(data),
#             'normativas': data
#         })

# @api_view(['GET'])
# @permission_classes([permissions.AllowAny])  # Permitir acceso sin autenticación temporalmente
# def preguntas_por_normativa(request, normativa):
#     """Endpoint específico para obtener preguntas por normativa - SuperAdmin y usuarios autenticados"""
#     try:
#         # Convertir nom_030 -> NOM-030
#         tipo_norma = normativa.upper().replace('_', '-')

#         evaluacion = EvaluacionOficial.objects.get(tipo_norma=tipo_norma, activa=True)
#         secciones = evaluacion.secciones.all().order_by('numero_orden')

#         preguntas = []
#         for seccion in secciones:
#             preguntas_seccion = seccion.preguntas.all().order_by('numero_orden')
#             for pregunta in preguntas_seccion:
#                 preguntas.append({
#                     'id': pregunta.id,
#                     'numero_orden': pregunta.numero_orden,
#                     'texto': pregunta.texto_pregunta,
#                     'tipo': pregunta.tipo_pregunta.lower(),
#                     'opciones': pregunta.opciones_respuesta,
#                     'obligatoria': pregunta.es_obligatoria,
#                     'normativa': normativa,
#                     'seccion': {
#                         'id': seccion.id,
#                         'nombre': seccion.nombre,
#                         'numero_orden': seccion.numero_orden
#                     }
#                 })

#         return Response({
#             'evaluacion': {
#                 'id': evaluacion.id,
#                 'tipo_norma': evaluacion.tipo_norma,
#                 'nombre': evaluacion.nombre,
#                 'descripcion': evaluacion.descripcion,
#                 'tiempo_limite': evaluacion.tiempo_limite
#             },
#             'total_preguntas': len(preguntas),
#             'preguntas': preguntas
#         })

#     except EvaluacionOficial.DoesNotExist:
#         return Response(
#             {'error': f'No se encontró la evaluación oficial para {normativa}'},
#             status=status.HTTP_404_NOT_FOUND
#         )

