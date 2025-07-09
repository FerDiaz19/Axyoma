# -*- coding: utf-8 -*-
"""
Archivo para centralizar la importación de modelos
"""

from apps.users.models import PerfilUsuario as Usuario, Empresa, Planta, Departamento, Puesto, Empleado, AdminPlanta
from apps.subscriptions.models import PlanSuscripcion, SuscripcionEmpresa as Suscripcion
from apps.surveys.models import Evaluacion, PreguntaEvaluacion, AplicacionEvaluacion, RespuestaEvaluacion

# Importar otros modelos si existen
try:
    from core.models import *
except ImportError:
    pass
