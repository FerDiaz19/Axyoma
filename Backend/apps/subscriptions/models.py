from django.db import models
from django.utils import timezone
from datetime import datetime, timedelta
from django.contrib.auth.models import User
from apps.users.models import Empresa

class PlanSuscripcion(models.Model):
    """
    Modelo para tabla PLANES existente
    """
    plan_id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    duracion = models.IntegerField(help_text="Duración en días")
    fecha_registro = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=True)

    class Meta:
        db_table = 'planes'
        managed = False  # No dejar que Django gestione esta tabla

    def __str__(self):
        return f"{self.nombre} - ${self.precio}"

class SuscripcionEmpresa(models.Model):
    """
    Modelo para tabla SUSCRIPCIONES_EMPRESA existente
    """
    suscripcion_id = models.AutoField(primary_key=True)
    empresa = models.IntegerField()  # FK simple como integer
    plan = models.IntegerField()     # FK simple como integer
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    estado = models.CharField(max_length=20)
    fecha_registro = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'suscripciones_empresa'
        managed = False  # No dejar que Django gestione esta tabla

    def __str__(self):
        return f"Suscripción {self.suscripcion_id}"

    # Propiedades para obtener objetos relacionados
    def get_empresa(self):
        try:
            return Empresa.objects.get(empresa_id=self.empresa)
        except Empresa.DoesNotExist:
            return None
    
    def get_plan(self):
        try:
            return PlanSuscripcion.objects.get(plan_id=self.plan)
        except PlanSuscripcion.DoesNotExist:
            return None
        self.save()

class Pago(models.Model):
    """
    Modelo para PAGOS según el SQL original
    """
    ESTADO_PAGO_CHOICES = [
        ('Completado', 'Completado'),
        ('Pendiente', 'Pendiente'),
        ('Cancelado', 'Cancelado'),
        ('Fallido', 'Fallido'),
    ]
    
    pago_id = models.AutoField(primary_key=True)
    suscripcion = models.ForeignKey(
        SuscripcionEmpresa, 
        on_delete=models.CASCADE,
        db_column='suscripcion_id',
        verbose_name="Suscripción"
    )
    costo = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Costo")
    monto_pago = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Monto Pagado")
    estado_pago = models.CharField(max_length=20, choices=ESTADO_PAGO_CHOICES, default='Pendiente', verbose_name="Estado del Pago")
    fecha_pago = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Pago")
    fecha_vencimiento = models.DateField(null=True, blank=True, verbose_name="Fecha de Vencimiento")
    transaccion_id = models.CharField(max_length=50, blank=True, null=True, verbose_name="ID de Transacción")
    comprobante = models.CharField(max_length=255, blank=True, null=True, verbose_name="Comprobante de Pago")
    usuario = models.ForeignKey(
        'auth.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Usuario que realizó el pago"
    )

    class Meta:
        db_table = 'pagos'
        verbose_name = "Pago"
        verbose_name_plural = "Pagos"
        ordering = ['-fecha_pago']

    def __str__(self):
        usuario_info = f" - {self.usuario.username}" if self.usuario else ""
        return f"Pago ${self.monto_pago} - {self.suscripcion.empresa.nombre}{usuario_info}"