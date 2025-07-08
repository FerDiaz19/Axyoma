# -*- coding: utf-8 -*-
"""
Archivo para centralizar la importación de modelos
"""

from apps.users.models import PerfilUsuario as Usuario, Empresa, Planta, Departamento, Puesto, Empleado
from apps.subscriptions.models import PlanSuscripcion, SuscripcionEmpresa as Suscripcion

# Importar otros modelos si existen
try:
    from core.models import *
except ImportError:
    pass
