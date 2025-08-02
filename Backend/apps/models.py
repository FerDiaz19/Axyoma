# -*- coding: utf-8 -*-
"""
Archivo para centralizar la importación de modelos
"""

from django.db import models

# NOTA: Los modelos Suscripcion, Plan y Pago están definidos en apps.subscriptions
# para evitar conflictos de db_table

# Importar modelos de usuarios
from apps.users.models import PerfilUsuario as Usuario, Empresa, Planta, Departamento, Puesto, Empleado, AdminPlanta

# Importar modelos de suscripciones
from apps.subscriptions.models import PlanSuscripcion as Plan, SuscripcionEmpresa as Suscripcion, Pago

# Importar otros modelos si existen
try:
    from core.models import *
except ImportError:
    pass
