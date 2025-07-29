# -*- coding: utf-8 -*-
import csv
import io
from django.http import HttpResponse
from datetime import datetime


class CSVExporter:
    """
    Utilidad para exportar datos a CSV con formato personalizado
    """
    
    def __init__(self):
        self.encoding = 'utf-8'
    
    def exportar_queryset(self, queryset, campos, nombre_archivo=None):
        """
        Exportar un queryset de Django a CSV
        
        Args:
            queryset: QuerySet de Django
            campos: Lista de campos a exportar
            nombre_archivo: Nombre del archivo (opcional)
        
        Returns:
            HttpResponse con el archivo CSV
        """
        if not nombre_archivo:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            nombre_archivo = f'exportacion_{timestamp}.csv'
        
        response = HttpResponse(content_type='text/csv; charset=utf-8')
        response['Content-Disposition'] = f'attachment; filename="{nombre_archivo}"'
        
        # Escribir BOM para compatibilidad con Excel
        response.write('\ufeff')
        
        writer = csv.writer(response)
        
        # Escribir encabezados
        encabezados = [self._formatear_encabezado(campo) for campo in campos]
        writer.writerow(encabezados)
        
        # Escribir datos
        for obj in queryset:
            fila = []
            for campo in campos:
                valor = self._obtener_valor_campo(obj, campo)
                fila.append(str(valor) if valor is not None else '')
            writer.writerow(fila)
        
        return response
    
    def _formatear_encabezado(self, campo):
        """
        Formatear nombre de campo para encabezado
        """
        # Reemplazar guiones bajos con espacios y capitalizar
        return campo.replace('_', ' ').replace('__', ' - ').title()
    
    def _obtener_valor_campo(self, obj, campo):
        """
        Obtener valor de un campo, incluyendo campos relacionados
        """
        try:
            if '__' in campo:
                # Campo relacionado como 'empresa__nombre'
                partes = campo.split('__')
                valor = obj
                for parte in partes:
                    if valor is None:
                        return ''
                    valor = getattr(valor, parte, None)
                return valor
            else:
                return getattr(obj, campo, '')
        except Exception:
            return ''
    
    def crear_csv_en_memoria(self, datos, campos):
        """
        Crear CSV en memoria y retornar como string
        """
        output = io.StringIO()
        writer = csv.writer(output)
        
        # Encabezados
        encabezados = [self._formatear_encabezado(campo) for campo in campos]
        writer.writerow(encabezados)
        
        # Datos
        for fila in datos:
            writer.writerow(fila)
        
        return output.getvalue()
