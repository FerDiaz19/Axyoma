# ---------------------------------------------------------------------------- #

''' Vistas para las entidades relacionadas a las evaluaciones (Ed Rubio) '''


from .models import *
from .serializers import *
from apps.users.models import Empleado

from django.utils import timezone
from django.db import transaction
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

# ---------------------------------------------------------------------------- #

class TipoEvaluacionViewSet(viewsets.ModelViewSet):
    queryset = TipoEvaluacion.objects.all()
    serializer_class = TipoEvaluacionSerializer
    permission_classes = [ IsAuthenticated ]

# ---------------------------------------------------------------------------- #

class EvaluacionViewSet(viewsets.ModelViewSet):
    queryset = Evaluacion.objects.all()
    serializer_class = EvaluacionSerializer
    permission_classes = [ IsAuthenticated ]

    # ------------------------------------------------------------------------ #

    @action(detail=True, methods=['patch'])
    def desactivar(self, request, pk=None):
        try:
            evaluacion = self.get_object()

            with transaction.atomic():
                evaluacion.estado = False
                evaluacion.save() # Se desactiva la evaluación.

                # Y, una cosita que había olvidado, era el desactivar las asignaciones dadas.
                asignaciones_relacionadas = Asignacion.objects.filter(evaluacion=evaluacion, status=True)

                for asignacion in asignaciones_relacionadas:
                    asignacion.status = False
                    asignacion.save()

                    AsignacionEmpleado.objects.filter(asignacion=asignacion).update(status='Desactivada')

            return Response({'status': 'La evaluación ha sido desactivada.'}, status=status.HTTP_200_OK)
        except Evaluacion.DoesNotExist:
            return Response({'error': 'Owh, parece que la evaluación no se encuentra más en la base de datos.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as error:
            return Response({'error': f'Ha ocurrido un error al desactivar la evaluación: {str(error)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # ------------------------------------------------------------------------ #

    @action(detail=True, methods=['patch'])
    def activar(self, request, pk=None):
        try:
            evaluacion = self.get_object()

            with transaction.atomic():
                evaluacion.estado = True
                evaluacion.save() # Activamo' la evaluación.

                # Junto a las asignaciones relacionadas.
                asignaciones_relacionadas = Asignacion.objects.filter(evaluacion=evaluacion, status=False)

                for asignacion in asignaciones_relacionadas:

                    # Solo reactiva si la fecha de término no ha sido excedida.
                    if asignacion.fecha_fin >= timezone.now():
                        asignacion.status = True
                        asignacion.save()

                        AsignacionEmpleado.objects.filter(
                            asignacion=asignacion,
                            status__in=['Desactivada', 'Expirada']
                        ).update(status='Pendiente')

            return Response({'status': 'La evaluación y sus asignaciones relacionadas han sido activadas.'}, status=status.HTTP_200_OK)
        except Evaluacion.DoesNotExist:
            return Response({'error': 'Owh, parece que la evaluación no se encuentra más en la base de datos.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as error:
            return Response({'error': f'Ha ocurrido un error al activar la evaluación: {str(error)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# ---------------------------------------------------------------------------- #

class PreguntaViewSet(viewsets.ModelViewSet):
    queryset = Pregunta.objects.all()
    serializer_class = PreguntaSerializer
    permission_classes = [ IsAuthenticated ]

# ---------------------------------------------------------------------------- #

class ConjuntoRespuestasViewSet(viewsets.ModelViewSet):
    queryset = ConjuntoRespuestas.objects.all()
    serializer_class = ConjuntoRespuestasSerializer
    permission_classes = [ IsAuthenticated ]

# ---------------------------------------------------------------------------- #

class AsignacionViewSet(viewsets.ModelViewSet):
    queryset = Asignacion.objects.all()
    serializer_class = AsignacionSerializer
    permission_classes = [ IsAuthenticated ]

    # ------------------------------------------------------------------------ #

    @action(detail=True, methods=['post'])
    def asignar_empleados(self, request, pk=None):
        asignacion = self.get_object()

        '''
            A mi parecer, la manera más agradable de realizar las asignaciones sería, no uno a uno,
            sino más bien por conjuntos, sea de empleados, plantas, departamentos o puestos.
        '''

        evaluacion_relacionada = asignacion.evaluacion
        if not evaluacion_relacionada.estado:
            return Response({ 'error':
                'Dado el estado inactivo de la evaluación, no se ha podidod llevar a cabo el proceso de asgnación.'},
                    status=status.HTTP_400_BAD_REQUEST)


        empleado_ids = request.data.get('empleado_ids', [])
        planta_ids = request.data.get('planta_ids', [])
        puesto_ids = request.data.get('puesto_ids', [])
        departamento_ids = request.data.get('departamento_ids', [])

        # En caso de que no se obtengan los IDs de los asignados.
        if not any([empleado_ids, planta_ids, puesto_ids, departamento_ids]):
            return Response({ 'error': 'No ha seleccionado a ningún empleado para la asignación de esta evaluación.'},
                status=status.HTTP_400_BAD_REQUEST)

        # Toca inicializar la variable sin nigún empleado.
        empleados_a_asignar = Empleado.objects.none()

        # * 01: En caso de haber proporcionado un conjunto de empleados.
        if empleado_ids:
            empleados_a_asignar |= Empleado.objects.filter(empleado_id__in=empleado_ids)

        # * 02: En caso de haber proporcionado a todos los empleados de una planta.
        if planta_ids:
            empleados_a_asignar |= Empleado.objects.filter(puesto__departamento__planta__planta_id__in=planta_ids)


        # * 03: En caso de haber proporcionado a todos los empleados de un puesto.
        if puesto_ids:
            empleados_a_asignar |= Empleado.objects.filter(puesto__puesto_id__in=puesto_ids)

        # * 04: En caso de haber proporcionado a todos los empleados de un departamento.
        if departamento_ids:
            empleados_a_asignar |= Empleado.objects.filter(puesto__departamento__departamento_id__in=departamento_ids)


        # Solamente por si acaaso, eliminamos los duplicados.
        empleados_a_asignar = empleados_a_asignar.distinct()

        if not empleados_a_asignar.exists():
            return Response({ 'error': 'Ningundo de los empleados proporcionados ha sido encontrado.'},
                status=status.HTTP_404_NOT_FOUND)

        # Let the sun shine upon this Lord of Cinder!
        with transaction.atomic():
            nuevas_asignaciones = []

            for empleado in empleados_a_asignar:

                # Una cosilla bien importante es el asegurar la existencia de duplicaados.
                # Pues estaría bien feillo andar haciendo asignaciones extra.
                asignacion_existente = AsignacionEmpleado.objects.filter(
                    asignacion=asignacion, empleado=empleado
                ).first()

                if not asignacion_existente:
                    nuevas_asignaciones.append(AsignacionEmpleado(
                        asignacion=asignacion, empleado=empleado ))

            # Ahora sí, a crear todas de a golpe, hehe.
            if nuevas_asignaciones:
                AsignacionEmpleado.objects.bulk_create(nuevas_asignaciones)

        return Response({ 'status': 'Las asignaciones han sido registradas con éxito.'},
            status=status.HTTP_201_CREATED)

    # ------------------------------------------------------------------------ #

    @action(detail=True, methods=['patch'])
    def desactivar_asignacion(self, request, pk=None):
        asignacion = self.get_object()

        with transaction.atomic():
            # Obviamente, primero desactivamos la asignación base.
            asignacion.status = False
            asignacion.save()

            # Pero, las asignaciones a los empleados también han de ser desactivadas.
            # De lo contrario todo el sistema estaría bien raro.
            AsignacionEmpleado.objects.filter(asignacion=asignacion).update(status='Desactivada')

        return Response({ 'status': 'La asignacion ha sido completamente desactivada.' },
            status=status.HTTP_200_OK)

    # ------------------------------------------------------------------------ #

    @action(detail=True, methods=['patch'])
    def activar_asignacion(self, request, pk=None):
        asignacion = self.get_object()

        evaluacion_relacionada = asignacion.evaluacion
        if not evaluacion_relacionada.estado:
            return Response({ 'error':
                'Dado el estado inactivo de la evaluación, no se ha podidod llevar a cabo el proceso de asgnación.'},
                    status=status.HTTP_400_BAD_REQUEST)


        # Mucho cuida'o con intentar reactivar una asignación que se encuentra 'expirada'.
        if asignacion.fecha_fin < timezone.now():
            return Response({ 'error': 'La asignación no ha podido ser reactivada debido a que su fecha de término ha sido excedida.' },
                status=status.HTTP_400_BAD_REQUEST)

        with transaction.atomic():
            # Tal como en el caso de la desactivación, iniciamos por la asignación base.
            asignacion.status = True
            asignacion.save()

            # Las asignaciones a los empleados también son reactivadas, siempre que no fuesen completadas con anterioridad.
            AsignacionEmpleado.objects.filter(asignacion=asignacion,
                status__in=[ 'Desactivada', 'Expirada' ]).update(status='Pendiente')

        return Response({ 'status': 'La asignación ha sido reactivada con éxito.' },
            status=status.HTTP_200_OK)

class AsignacionEmpleadoViewSet(viewsets.ModelViewSet):
    queryset = AsignacionEmpleado.objects.all()
    serializer_class = AsignacionEmpleadoSerializer
    permission_classes = [ IsAuthenticated ]

    # ------------------------------------------------------------------------ #

    @action(detail=True, methods=['patch'])
    def desactivar(self, request, pk=None):
        asignacion_empleado = self.get_object()

        if asignacion_empleado.status == 'Completada':
            return Response({ 'error': 'La asignación ha sido contestada.' },
                status=status.HTTP_400_BAD_REQUEST)

        with transaction.atomic():
            asignacion_empleado.status = 'Desactivada'
            asignacion_empleado.save()

        return Response({ 'status': 'La asignacion del empleado ha sido desactivada.' },
            status=status.HTTP_200_OK)

    # ------------------------------------------------------------------------ #

    @action(detail=True, methods=['patch'])
    def activar(self, request, pk=None):
        asignacion_empleado = self.get_object()
        asignacion_base = asignacion_empleado.asignacion
        evaluacion_relacionada = asignacion_base.evaluacion

        if not evaluacion_relacionada.estado:
            return Response({ 'error':
                'Dado el estado inactivo de la evaluación, no se ha podidod llevar a cabo el proceso de asgnación.'},
                    status=status.HTTP_400_BAD_REQUEST)

        if asignacion_base.fecha_fin < timezone.now():
            return Response({ 'error': 'La asignación no ha podido ser reactivada debido a que su fecha de término ha sido excedida.' },
                status=status.HTTP_400_BAD_REQUEST)

        if asignacion_empleado.status == 'Expirada':
            return Response({ 'error': 'La asignación no ha podido ser reactivada debido a que su fecha de término ha sido excedida.' },
                status=status.HTTP_400_BAD_REQUEST)

        with transaction.atomic():
            asignacion_empleado.status = 'Pendiente'
            asignacion_empleado.save()

        return Response({ 'status': 'La asignacion del empleado ha sido reactivada con éxito.' },
            status=status.HTTP_200_OK)

# ---------------------------------------------------------------------------- #

class RespuestaEmpleadoViewSet(viewsets.ModelViewSet):
    queryset = RespuestaEmpleado.objects.all()
    serializer_class = RespuestaEmpleadoSerializer
    permission_classes = [ IsAuthenticated ]

# ---------------------------------------------------------------------------- #

class ResultadoEvaluacionViewSet(viewsets.ModelViewSet):
    queryset = ResultadoEvaluacion.objects.all()
    serializer_class = ResultadoEvaluacionSerializer
    permission_classes = [ IsAuthenticated ]

# ---------------------------------------------------------------------------- #
