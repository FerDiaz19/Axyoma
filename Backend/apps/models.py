
''' Centralización de importación de modelos. '''

# Importar modelos de usuarios
from apps.users.models import PerfilUsuario as Usuario, Empresa, Planta, Departamento, Puesto, Empleado, AdminPlanta

# Importar modelos de suscripciones
from apps.subscriptions.models import PlanSuscripcion as Plan, SuscripcionEmpresa as Suscripcion, Pago