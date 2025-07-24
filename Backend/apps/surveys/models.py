from django.db import models
from apps.users.models import Empresa, PerfilUsuario

class TipoEvaluacion(models.Model):
    tipo_evaluacion_id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=64, unique=True)
    descripcion = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'tipos_evaluacion'

class Evaluacion(models.Model):
    evaluacion_id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=128)
    descripcion = models.TextField(blank=True, null=True)
    instrucciones = models.TextField(blank=True, null=True)
    tiempo_limite = models.IntegerField(blank=True, null=True)  # Tiempo límite en minutos
    status = models.BooleanField(default=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    
    # Relaciones
    tipo_evaluacion = models.ForeignKey(
        TipoEvaluacion, 
        on_delete=models.PROTECT,
        db_column='tipo_evaluacion'
    )
    empresa = models.ForeignKey(
        Empresa, 
        null=True, 
        blank=True, 
        on_delete=models.SET_NULL,
        db_column='empresa'
    )  # NULL para evaluaciones normativas
    creado_por = models.ForeignKey(
        PerfilUsuario, 
        on_delete=models.PROTECT,
        db_column='creado_por'
    )

    class Meta:
        db_table = 'evaluaciones'

class SeccionEval(models.Model):
    seccion_id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField(blank=True, null=True)
    numero_orden = models.IntegerField()
    evaluacion = models.ForeignKey(
        Evaluacion, 
        on_delete=models.CASCADE,
        db_column='evaluacion'
    )

    class Meta:
        db_table = 'secciones_eval'

class ConjuntoOpciones(models.Model):
    conjunto_id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=64, unique=True)
    descripcion = models.TextField(blank=True, null=True)
    predefinido = models.BooleanField(default=False)

    class Meta:
        db_table = 'conjuntos_opciones'

class OpcionConjunto(models.Model):
    opcion_conjunto_id = models.AutoField(primary_key=True)
    texto_opcion = models.CharField(max_length=256)
    valor_booleano = models.BooleanField(blank=True, null=True)
    valor_numerico = models.IntegerField(blank=True, null=True)
    puntuaje_escala = models.IntegerField(blank=True, null=True)
    numero_orden = models.IntegerField()
    conjunto_opciones = models.ForeignKey(
        ConjuntoOpciones, 
        on_delete=models.CASCADE,
        db_column='conjunto_opciones'
    )

    class Meta:
        db_table = 'opciones_conjunto'

class Pregunta(models.Model):
    TIPO_CHOICES = (
        ('Abierta', 'Abierta'),
        ('Múltiple', 'Múltiple'),
        ('Escala', 'Escala'),
        ('Bool', 'Bool'),
    )
    
    pregunta_id = models.AutoField(primary_key=True)
    texto_pregunta = models.TextField()
    tipo_pregunta = models.CharField(max_length=20, choices=TIPO_CHOICES)
    es_obligatoria = models.BooleanField(default=True)
    pregunta_padre = models.ForeignKey(
        'self', 
        blank=True, 
        null=True, 
        on_delete=models.CASCADE,
        db_column='pregunta_padre'
    )
    activador_padre = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'preguntas'

class SeccionPregunta(models.Model):
    id = models.AutoField(primary_key=True)  # Django necesita una clave primaria
    seccion = models.ForeignKey(
        SeccionEval, 
        on_delete=models.CASCADE,
        db_column='seccion'
    )
    pregunta = models.ForeignKey(
        Pregunta, 
        on_delete=models.CASCADE,
        db_column='pregunta'
    )
    conjunto_opciones = models.ForeignKey(
        ConjuntoOpciones, 
        blank=True, 
        null=True, 
        on_delete=models.SET_NULL,
        db_column='conjunto_opciones'
    )

    class Meta:
        db_table = 'seccion_preguntas'
        constraints = [
            models.UniqueConstraint(fields=['seccion', 'pregunta'], name='unique_seccion_pregunta')
        ]
