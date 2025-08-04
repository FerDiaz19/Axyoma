
# ---------------------------------------------------------------------------- #

from uuid import UUID
# from weasyprint import HTML, CSS

from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.db import transaction
from django.contrib import messages
from django.core.cache import cache

from apps.evaluaciones.models import *
from django.shortcuts import render, redirect, reverse

# ---------------------------------------------------------------------------- #

''' Esta vista se encarga principalmente de validar el acceso. '''
class AccesoEvaluacion(generic.View):
    template_name = 'solaire/access.html'

    # El plan aquí es mostrar la wea del acceso.
    # Sin embargo, si el usuario tiene una evaluación activa, se le redirige.
    def get(self, request, *args, **kwargs):
        if 'asignacion_empleado_id' in request.session:
            return redirect(reverse('AnorLondo:EvaluacionActiva'))

        return render(request, self.template_name)


    # Se valida el token de acceso introducido.
    def post(self, request, *args, **kwargs):
        token_acceso = request.POST.get('token_acceso')

        if not token_acceso: # Vamo' a asegurar que se introduzca un token de acceso.
            messages.error(request, 'Por favor, introduzca un token para continuar.')
            return render(request, self.template_name)

        try: # Vverificamos que tenga el formato de un UUID.
            UUID(token_acceso)
        except ValueError:
            messages.error(request, 'Por favor, introduzca un token de acceso válido.')
            return render(request, self.template_name)

        # -------------------------------------------------------------------- #

        try: # Ahora toca verificar  que el token dado esté realmente asignado.
            asignacion_empleado = AsignacionEmpleado.objects.select_related(
                'asignacion__evaluacion', 'empleado').get(token_acceso=token_acceso)
        except AsignacionEmpleado.DoesNotExist:
            messages.error(request, 'El token de acceso no es válido para ninguna evaluación.')
            return render(request, self.template_name)

        # A continuación, toca verificar el estado de la asignación del empleado.
        if asignacion_empleado.status == 'Completada':
            messages.error(request, 'La evaluación asignada a este token ha sido contestada.')
            return render(request, self.template_name)

        # De no haber sido completada verificamos la expiración de la asignación.e
        asignacion = asignacion_empleado.asignacion
        vordt = timezone.now()

        if not asignacion.status:  # Si la asignación base no está activa.
            messages.error(request, 'La evaluación asignada no se encuentra activa.')
            return render(request, self.template_name)

        if asignacion.fecha_fin and vordt > asignacion.fecha_fin:
            asignacion_empleado.status = 'Expirada'
            asignacion_empleado.save()
            messages.error(request, 'Se ha excedido la fecha máxima para la toma de esta evaluación.')
            return render(request, self.template_name)

        # -------------------------------------------------------------------- #

        # * Toca pasar datillos para la toma de la evaluación.
        evaluacion = asignacion.evaluacion
        empleado = asignacion_empleado.empleado

        # Estos datos los guardamos en la caché para utilizarlos en la otra vista.
        cache.set(f'evaluacion_{token_acceso}', evaluacion)
        cache.set(f'empleado_{token_acceso}', empleado)

        # Guardamos el ID de la asignación en la sesión para controlar el flujo.
        request.session['asignacion_empleado_id'] = asignacion_empleado.asignacion_empleado_id
        return redirect(reverse('AnorLondo:EvaluacionActiva'))

# ---------------------------------------------------------------------------- #

''' Esta vista se encarga de mostrar la evaluación al empleado. '''
class EvaluacionActiva(generic.View):
    template_name = 'solaire/appraisal.html'

    # El punto es mostrar los datillos e la evaluación al usuario.
    def get(self, request, *args, **kwargs):
        asignacionSesion = request.session.get('asignacion_empleado_id')

        # ! Cosita importante:
        # Vamo' a verificar que exista una evaluación activa en la sesión.
        # Además de los datillos que se han de haber guardado en caché.
        if not asignacionSesion:
            messages.error(request, 'No se posee una evaluación activa. Por favor, ingrese con un token válido.')
            return redirect(reverse('AnorLondo:AccesoEvaluacion'))

        try: # Toca realizar un par de verificaciones para poder mandar lo buneo al context.
            asignacion_empleado = AsignacionEmpleado.objects.get(asignacion_empleado_id=asignacionSesion)
            token_acceso = str(asignacion_empleado.token_acceso)

            # Recuperamos los datillos que se encuentran en la caché.
            evaluacion = cache.get(f'evaluacion_{token_acceso}')
            empleado = cache.get(f'empleado_{token_acceso}')

            # Si no se encuentran datos en la caché, redirecciona a la vista de acceso.
            if not evaluacion or not empleado:
                del request.session[ 'asignacion_empleado_id' ] # Este lo eliminamos para evitar un buclé de redirecciones.
                messages.error(request, 'La sesión ha expirado. Por favor, intente nuevamente.')
                return redirect(reverse('AnorLondo:AccesoEvaluacion'))

            # ---------------------------------------------------------------- #

            # Procedemos a consultar los datos completos de la evaluación a tomar.
            secciones = SeccionEval.objects.filter(evaluacion=evaluacion).prefetch_related(
                'preguntas_seccion__pregunta',
                'preguntas_seccion__conjunto_respuestas__opciones'
            ).order_by('numero_orden')

            context = { 'empleado': empleado, 'evaluacion': evaluacion, 'secciones': secciones }

            return render(request, self.template_name, context)

        except AsignacionEmpleado.DoesNotExist:
            if 'asignacion_empleado_id' in request.session:
                del request.session[ 'asignacion_empleado_id' ]
            messages.error(request, 'El token actual no es válido...')
            return redirect(reverse('AnorLondo:AccesoEvaluacion'))


        # Si por alguna razón la asignación ha sido eliminada, redireccionamos.
        except AsignacionEmpleado.DoesNotExist:
            if 'asignacion_empleado_id' in request.session:
                del request.session[ 'asignacion_empleado_id' ]
            messages.error(request, 'El token actual no es válido...')
            return redirect(reverse('AnorLondo:AccesoEvaluacion'))


    # Cuando el empleado termina la evaluación guardamos sus respuestas.
    # Buah! Se vienen muchas inserciones y cálculos.
    def post(self, request, *args, **kwargs):
        asignacion_empleado_id = request.session.get('asignacion_empleado_id')

        # * Antes de hacer las inserciones vamo' a hacer validaciones simples.
        if not asignacion_empleado_id:
            messages.error(request, 'No se posee una evaluación activa. Por favor, ingrese con un token válido.')
            return redirect(reverse('AnorLondo:AccesoEvaluacion'))

        try:
            asignacion_empleado = AsignacionEmpleado.objects.get(pk=asignacion_empleado_id)
        except AsignacionEmpleado.DoesNotExist:
            messages.error(request, 'La asignación actual no es válida para esta evaluación.')
            return redirect(reverse('AnorLondo:AccesoEvaluacion'))

        if asignacion_empleado.status == 'Completada':
            messages.error(request, 'Esta evaluación ha sido completada anteriormente.')
            return redirect(reverse('AnorLondo:EvaluacionCompletada'))

        # -------------------------------------------------------------------- #

        with transaction.atomic():
            preguntas_evaluables_con_respuesta_correcta = 0
            respuestas_correctas_dadas = 0

            # Iniciamos con un recorrido de los datos del formulario:
            for key, value in request.POST.items():
                if key.startswith('pregunta_'):
                    pregunta_id = key.split('_')[1]

                    try: # * Ahora sí, toca hacer las inserciones.
                        seccion_pregunta = SeccionPregunta.objects.get(
                            seccion__evaluacion__pk=asignacion_empleado.asignacion.evaluacion.pk,
                            pregunta__pk=pregunta_id
                        )

                        pregunta = seccion_pregunta.pregunta
                        seccion = seccion_pregunta.seccion

                        # Creamos una nueva instancia de RespuestaEmpleado.
                        respuesta = RespuestaEmpleado(
                            asignacion_empleado=asignacion_empleado,
                            seccion_pregunta=seccion_pregunta
                        )

                        respuesta.es_correcta = False

                        # ? Para preguntas de tipo 'Abierta', guardamos el texto introducido.
                        if pregunta.tipo_pregunta == 'Abierta':
                            respuesta.respuesta_texto = value

                        # ? En caso de que sean 'Múltiple', 'Escala' o 'Bool'.
                        elif pregunta.tipo_pregunta in [ 'Múltiple', 'Escala', 'Bool' ]:

                            try:
                                opcion_seleccionada = PosiblesRespuestas.objects.get(pk=int(value))
                                respuesta.opcion_seleccionada = opcion_seleccionada

                                # Dependiendo del tipo de valor, veremos qué guardamos.
                                if opcion_seleccionada.valor_numerico is not None:
                                    respuesta.respuesta_valor_numerico = opcion_seleccionada.valor_numerico
                                if opcion_seleccionada.valor_booleano is not None:
                                    respuesta.respuesta_valor_booleano = opcion_seleccionada.valor_booleano
                                if opcion_seleccionada.valor_decimal is not None:
                                    respuesta.respuesta_valor_decimal = opcion_seleccionada.valor_decimal

                            except (ValueError, PosiblesRespuestas.DoesNotExist):
                                messages.error(request, f'El valor de la respuesta para la pregunta {pregunta.texto_pregunta[:50]}... no es válido.')
                                transaction.set_rollback(True) # Deshacemos la transacción para no guardar datos innecesarios.
                                return redirect(reverse('AnorLondo:EvaluacionActiva'))

                            # Verificamos si la respuesta es correcta (si aplica).
                            # Para las secciones evaluables con 'respuestas correctas'.
                            if seccion.es_evaluable and seccion_pregunta.respuesta_correcta:
                                preguntas_evaluables_con_respuesta_correcta += 1

                                if respuesta.opcion_seleccionada == seccion_pregunta.respuesta_correcta:
                                    respuesta.es_correcta = True
                                    respuestas_correctas_dadas += 1

                        respuesta.save()

                    except SeccionPregunta.DoesNotExist:
                        pass # Ignoramos las preguntas que no se encuentren.

                    except Exception as error:
                        print('ERROR: ', error)
                        messages.error(request, f'Ha ocurrido un error inesperado al procesar las respuestas. :(')
                        transaction.set_rollback(True)
                        return redirect(reverse('AnorLondo:EvaluacionActiva'))

            # Tras guardar cada una de las respuestas, procedemos a cambiar el estado de la asignación.
            asignacion_empleado.status = 'Completada'
            asignacion_empleado.fecha_completado = timezone.now()
            asignacion_empleado.save()


            # Calculamos el resultado de la evaluación.
            if preguntas_evaluables_con_respuesta_correcta > 0:
                porcentaje_correctas = (respuestas_correctas_dadas / preguntas_evaluables_con_respuesta_correcta) * 100
            else:
                porcentaje_correctas = 0.0

            aprobado = None
            if asignacion_empleado.asignacion.evaluacion.umbral_aprobacion is not None:
                aprobado = porcentaje_correctas >= asignacion_empleado.asignacion.evaluacion.umbral_aprobacion


            # Por si acaso, eliminamos cualquier resultado previamente guardado para esta asignación.
            ResultadoEvaluacion.objects.filter(asignacion_empleado=asignacion_empleado).delete()

            ResultadoEval = ResultadoEvaluacion.objects.create(
                puntaje_total=porcentaje_correctas,
                num_respuestas_correctas=respuestas_correctas_dadas,
                num_preguntas_evaluables=preguntas_evaluables_con_respuesta_correcta,
                porcentaje_correctas=porcentaje_correctas,
                aprobado=aprobado,
                asignacion_empleado=asignacion_empleado
            )


            resultadoEvaluacionID = ResultadoEval.pk
            cache.set(f'resultado', resultadoEvaluacionID)

        # Dado que hemos concluido con la toma de la evaluación, limpiamos la sesión.
        del request.session[ 'asignacion_empleado_id' ]

        messages.success(request, 'Tus respuestas han sido grabadas en las cenizas del tiempo, que la llama guíe tu destino...')
        return redirect(reverse('AnorLondo:EvaluacionCompletada'))

# ---------------------------------------------------------------------------- #

''' Esta vista se encarga de mostrar al usuario los resultados de su evaluación. '''
class EvaluacionCompletada(generic.View):
    template_name = 'solaire/certificate.html'
    context = { }

    def get(self, request, *args, **kwargs):
        resultado = cache.get(f'resultado') # ID de la entidad: ResultadoEvaluacion

        if not resultado:
            return redirect(reverse('AnorLondo:AccesoEvaluacion'))

        return render(request, self.template_name, self.context)

# ---------------------------------------------------------------------------- #
