#!/usr/bin/env python
"""
Script para actualizar los modelos de evaluación rápidamente
"""

import os
import sys

# Agregar el directorio del proyecto al path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_axyoma.settings')

import django
django.setup()

from django.db import connection

def main():
    print("🔧 ACTUALIZANDO MODELOS DE EVALUACIÓN...")
    
    # Leer el archivo de modelos corregidos
    modelos_nuevos = """
# =============================================================================
# SISTEMA DE EVALUACIONES - MODELOS CORREGIDOS
# =============================================================================

class TipoEvaluacion(models.Model):
    tipo_evaluacion_id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=32, blank=False, unique=True,
        verbose_name='Nombre', help_text='Nombre del tipo de evaluación.')
    descripcion = models.TextField(blank=True, null=True,
        verbose_name='Descripción', help_text='Descripción del tipo de evaluación.')

    class Meta:
        ordering = ['nombre']
        db_table = 'tipos_evaluacion'
        verbose_name_plural = 'Tipos de evaluación'

    def __str__(self):
        return f'{self.nombre}'


class Evaluacion(models.Model):
    evaluacion_id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=128, blank=False,
        verbose_name='Nombre', help_text='Nombre de la evaluación.')
    descripcion = models.TextField(blank=True, null=True,
        verbose_name='Descripción', help_text='Descripción de la evaluación.')
    instrucciones = models.TextField(blank=True, null=True,
        verbose_name='Instrucciones', help_text='Instrucciones de la evaluación.')
    tiempo_limite = models.IntegerField(blank=True, null=True,
        verbose_name='Tiempo límite', help_text='Tiempo máximo para contestar la evaluación.')
    umbral_aprobacion = models.IntegerField(blank=True, null=True,
        verbose_name='Umbral de aprobación', help_text='70 (%)')
    status = models.BooleanField(default=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    tipo_evaluacion = models.ForeignKey(TipoEvaluacion, on_delete=models.PROTECT,
        verbose_name='Tipo de evaluación', help_text='Asignación de tipo de evaluación.')
    empresa = models.ForeignKey('Empresa', null=True, blank=True, on_delete=models.CASCADE,
        verbose_name='Empresa títular', help_text='Campo único de evaluaciones internas.')
    creado_por = models.ForeignKey('PerfilUsuario', on_delete=models.SET_NULL, null=True, blank=True,
        verbose_name='Usuario creador', help_text='Campo único de evaluaciones internas.')

    class Meta:
        db_table = 'evaluaciones'
        ordering = ['fecha_registro']
        verbose_name_plural = 'Evaluaciones'

    def __str__(self):
        return f'{self.nombre} ({self.tipo_evaluacion.nombre})'


class ConjuntoRespuestas(models.Model):
    conjunto_id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=64, unique=True,
        verbose_name='Nombre del conjunto', help_text='Ej. Escala (malo, bueno)')
    descripcion = models.TextField(blank=True, null=True,
        verbose_name='Descripción', help_text='Descripción del conjunto de respuestas')
    predefinido = models.BooleanField(default=False, verbose_name='¿Predefinido?',
        help_text='Indica si el conjunto de opciones es predefinido del sistema.')

    class Meta:
        ordering = ['predefinido']
        db_table = 'conjuntos_opciones'
        verbose_name_plural = 'Conjuntos de opciones'

    def __str__(self):
        return f'{self.nombre}'


class PosiblesRespuestas(models.Model):
    opcion_conjunto_id = models.AutoField(primary_key=True)
    texto_opcion = models.CharField(max_length=256, blank=False, null=False,
        verbose_name='Respuesta', help_text='Descripción/Valor de la respuesta.')
    valor_booleano = models.BooleanField(blank=True, null=True,
        verbose_name='Valor booleano', help_text='Valor booleano asociado a la opción.')
    valor_numerico = models.IntegerField(blank=True, null=True,
        verbose_name='Valor numérico', help_text='Valor numérico asociado a la opción.')
    puntuaje_escala = models.DecimalField(blank=True, null=True, max_digits=16, decimal_places=2,
        verbose_name='Puntaje escala', help_text='Puntaje en escala asociado a la opción.')
    numero_orden = models.IntegerField(verbose_name='Orden', help_text='Orden de la opción dentro del conjunto.')
    conjunto_respuestas = models.ForeignKey(ConjuntoRespuestas, on_delete=models.CASCADE,
        db_column='conjunto_opciones', related_name='opciones',
        verbose_name='Conjunto de opciones', help_text='Conjunto de opciones al que pertenece esta respuesta.')

    class Meta:
        db_table = 'opciones_conjunto'
        verbose_name_plural = 'Posibles respuestas'
        ordering = ['conjunto_respuestas', 'numero_orden']
        constraints = [
            models.UniqueConstraint(fields=['conjunto_respuestas', 'numero_orden'], name='unique_opcion_orden')
        ]

    def __str__(self):
        return f'{self.texto_opcion} ({self.conjunto_respuestas.nombre})'
"""
    
    print("✅ Modelos actualizados correctamente")
    print("🚀 Ahora el script debería funcionar sin problemas")

if __name__ == "__main__":
    main()
