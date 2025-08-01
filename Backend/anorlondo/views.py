
# ---------------------------------------------------------------------------- #

from uuid import UUID
from django.urls import reverse
from django.views import generic
from django.utils import timezone
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
            messages.error(request, 'El token introducido ha sido utilizado con anterioridad.')
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





        # ------------------------------------------------------------------------ #


        # ------------------------------------------------------------------------ #




















            # Y guardamos toda la info' relacionada a la evaluación a tomar.
            # evaluacion = asignacion.evaluacion

            # secciones = SeccionEval.objects.filter(evaluacion=evaluacion
            # ).prefetch_related(
            #     'preguntas_seccion__pregunta',
            #     'preguntas_seccion__conjunto_respuestas__opciones'
            # ).order_by('numero_orden')

            # for seccion in secciones:
            #     seccion.preguntas = [ps.pregunta for ps in seccion.preguntas_seccion.all()]

            # evaluacion_data = { 'info': evaluacion, 'secciones': list(secciones) }
            # cache.set(f'evaluacion_{token_acceso}', evaluacion_data)

            # Ya por último, aseguramos el flujillo de la toma de la evaluación.
            request.session['asignacion_empleado_id'] = asignacion_empleado.asignacion_empleado_id

            return redirect(reverse('AnorLondo:EvaluacionActiva'))

        # -------------------------------------------------------------------- #

        # * Toca pasar datillos para la toma de la evaluación.
        evaluacion = asignacion.evaluacion
        empleado = asignacion_empleado.empleado

        # Estos datos los guardamos en la caché para utilizarlos en la otra vista.
        cache.set(f'evaluacion_{token_acceso}', evaluacion)
        cache.set(f'empleado_{token_acceso}', empleado)

        # Guardamos el ID de la asignación en la sesión para controlar el flujo.
        request.session[ 'asignacion_empleado_id' ] = asignacion_empleado.asignacion_empleado_id
        return redirect(reverse('AnorLondo:EvaluacionActiva'))

# ---------------------------------------------------------------------------- #

''' Esta vista se encarga de mostrar la evaluación al empleado. '''
class EvaluacionActiva(generic.View):
    template_name = 'solaire/appraisal.html'

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
                del request.session['asignacion_empleado_id'] # Este lo eliminamos para evitar un buclé de redirecciones.
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
                del request.session['asignacion_empleado_id']
            messages.error(request, 'El token actual no es válido...')
            return redirect(reverse('AnorLondo:AccesoEvaluacion'))


        # Si por alguna razón la asignación ha sido eliminada, redireccionamos.
        except AsignacionEmpleado.DoesNotExist:
            if 'asignacion_empleado_id' in request.session:
                del request.session['asignacion_empleado_id']
            messages.error(request, 'El token actual no es válido...')
            return redirect(reverse('AnorLondo:AccesoEvaluacion'))


    # TODO: Aquí ahorita pondré cuando manda las respuestas pa' guardarlas en la BD.
    # def post(self, request, *args, **kwargs):
    #     return redirect(reverse('AnorLondo:EvaluacionCompletada'))

# ---------------------------------------------------------------------------- #

class EvaluacionCompletada(generic.View):
    template_name = 'solaire/certificate.html'

    # Lo planea'o es que, tras completar una evaluación, al empleado...
    # ...se le permita descargar una constancia en PDF (generado por DJANGO).
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

# ---------------------------------------------------------------------------- #
