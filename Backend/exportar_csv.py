#!/usr/bin/env python
"""
Script para exportar datos de tablas a archivos CSV
"""

import os
import sys
import django
import csv
from datetime import datetime

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')
django.setup()

from apps.users.models import Empleado, Puesto, Departamento, Planta, Empresa, PerfilUsuario

def exportar_empleados_csv():
    """Exportar todos los empleados a CSV con datos completos"""
    print("📊 EXPORTANDO EMPLEADOS A CSV")
    print("=" * 50)
    
    try:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"export_empleados_{timestamp}.csv"
        filepath = os.path.join(os.path.dirname(__file__), filename)
        
        empleados = Empleado.objects.select_related(
            'puesto', 
            'puesto__departamento', 
            'puesto__departamento__planta',
            'puesto__departamento__planta__empresa'
        ).all()
        
        with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = [
                'ID', 'Numero_Empleado', 'Nombre', 'Apellido_Paterno', 'Apellido_Materno',
                'Email', 'Telefono', 'Fecha_Ingreso', 'Fecha_Registro', 'Status',
                'Puesto_ID', 'Puesto_Nombre', 'Departamento_ID', 'Departamento_Nombre',
                'Planta_ID', 'Planta_Nombre', 'Empresa_ID', 'Empresa_Nombre'
            ]
            
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            
            for empleado in empleados:
                writer.writerow({
                    'ID': empleado.empleado_id,
                    'Numero_Empleado': f"EMP-{empleado.empleado_id:06d}",
                    'Nombre': empleado.nombre,
                    'Apellido_Paterno': empleado.apellido_paterno,
                    'Apellido_Materno': empleado.apellido_materno or '',
                    'Email': empleado.email or '',
                    'Telefono': empleado.telefono or '',
                    'Fecha_Ingreso': empleado.fecha_ingreso,
                    'Fecha_Registro': empleado.fecha_registro,
                    'Status': 'ACTIVO' if empleado.status else 'INACTIVO',
                    'Puesto_ID': empleado.puesto.puesto_id,
                    'Puesto_Nombre': empleado.puesto.nombre,
                    'Departamento_ID': empleado.puesto.departamento.departamento_id,
                    'Departamento_Nombre': empleado.puesto.departamento.nombre,
                    'Planta_ID': empleado.puesto.departamento.planta.planta_id,
                    'Planta_Nombre': empleado.puesto.departamento.planta.nombre,
                    'Empresa_ID': empleado.puesto.departamento.planta.empresa.empresa_id,
                    'Empresa_Nombre': empleado.puesto.departamento.planta.empresa.nombre
                })
        
        file_size = os.path.getsize(filepath) / 1024  # KB
        print(f"✅ Empleados exportados exitosamente")
        print(f"📁 Archivo: {filename}")
        print(f"📊 Registros: {empleados.count()}")
        print(f"💾 Tamaño: {file_size:.2f} KB")
        
        return filepath
        
    except Exception as e:
        print(f"❌ Error exportando empleados: {e}")
        import traceback
        traceback.print_exc()
        return None

def exportar_estructura_organizacional_csv():
    """Exportar estructura organizacional completa"""
    print("🏢 EXPORTANDO ESTRUCTURA ORGANIZACIONAL A CSV")
    print("=" * 60)
    
    try:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"export_estructura_{timestamp}.csv"
        filepath = os.path.join(os.path.dirname(__file__), filename)
        
        # Obtener todos los puestos con relaciones
        puestos = Puesto.objects.select_related(
            'departamento',
            'departamento__planta',
            'departamento__planta__empresa'
        ).all()
        
        with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = [
                'Empresa_ID', 'Empresa_Nombre', 'Empresa_RFC',
                'Planta_ID', 'Planta_Nombre', 'Planta_Direccion',
                'Departamento_ID', 'Departamento_Nombre', 'Departamento_Descripcion',
                'Puesto_ID', 'Puesto_Nombre', 'Puesto_Descripcion',
                'Total_Empleados_Puesto'
            ]
            
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            
            for puesto in puestos:
                total_empleados = Empleado.objects.filter(puesto=puesto).count()
                
                writer.writerow({
                    'Empresa_ID': puesto.departamento.planta.empresa.empresa_id,
                    'Empresa_Nombre': puesto.departamento.planta.empresa.nombre,
                    'Empresa_RFC': puesto.departamento.planta.empresa.rfc,
                    'Planta_ID': puesto.departamento.planta.planta_id,
                    'Planta_Nombre': puesto.departamento.planta.nombre,
                    'Planta_Direccion': puesto.departamento.planta.direccion or '',
                    'Departamento_ID': puesto.departamento.departamento_id,
                    'Departamento_Nombre': puesto.departamento.nombre,
                    'Departamento_Descripcion': puesto.departamento.descripcion or '',
                    'Puesto_ID': puesto.puesto_id,
                    'Puesto_Nombre': puesto.nombre,
                    'Puesto_Descripcion': puesto.descripcion or '',
                    'Total_Empleados_Puesto': total_empleados
                })
        
        file_size = os.path.getsize(filepath) / 1024  # KB
        print(f"✅ Estructura organizacional exportada exitosamente")
        print(f"📁 Archivo: {filename}")
        print(f"📊 Registros: {puestos.count()}")
        print(f"💾 Tamaño: {file_size:.2f} KB")
        
        return filepath
        
    except Exception as e:
        print(f"❌ Error exportando estructura: {e}")
        return None

def exportar_empresas_csv():
    """Exportar información de empresas"""
    print("🏢 EXPORTANDO EMPRESAS A CSV")
    print("=" * 40)
    
    try:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"export_empresas_{timestamp}.csv"
        filepath = os.path.join(os.path.dirname(__file__), filename)
        
        empresas = Empresa.objects.select_related('administrador').all()
        
        with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = [
                'ID', 'Nombre', 'RFC', 'Direccion', 'Email_Contacto', 'Telefono_Contacto',
                'Fecha_Registro', 'Status', 'Administrador_Nombre', 'Administrador_Email',
                'Total_Plantas', 'Total_Empleados'
            ]
            
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            
            for empresa in empresas:
                total_plantas = Planta.objects.filter(empresa=empresa).count()
                total_empleados = Empleado.objects.filter(
                    puesto__departamento__planta__empresa=empresa
                ).count()
                
                writer.writerow({
                    'ID': empresa.empresa_id,
                    'Nombre': empresa.nombre,
                    'RFC': empresa.rfc,
                    'Direccion': empresa.direccion or '',
                    'Email_Contacto': empresa.email_contacto or '',
                    'Telefono_Contacto': empresa.telefono_contacto or '',
                    'Fecha_Registro': empresa.fecha_registro,
                    'Status': 'ACTIVA' if empresa.status else 'INACTIVA',
                    'Administrador_Nombre': f"{empresa.administrador.nombre} {empresa.administrador.apellido_paterno}",
                    'Administrador_Email': empresa.administrador.correo,
                    'Total_Plantas': total_plantas,
                    'Total_Empleados': total_empleados
                })
        
        file_size = os.path.getsize(filepath) / 1024  # KB
        print(f"✅ Empresas exportadas exitosamente")
        print(f"📁 Archivo: {filename}")
        print(f"📊 Registros: {empresas.count()}")
        print(f"💾 Tamaño: {file_size:.2f} KB")
        
        return filepath
        
    except Exception as e:
        print(f"❌ Error exportando empresas: {e}")
        return None

def exportar_resumen_estadistico_csv():
    """Exportar resumen estadístico del sistema"""
    print("📊 EXPORTANDO RESUMEN ESTADÍSTICO A CSV")
    print("=" * 50)
    
    try:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"export_resumen_estadistico_{timestamp}.csv"
        filepath = os.path.join(os.path.dirname(__file__), filename)
        
        with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = [
                'Planta_Nombre', 'Departamento_Nombre', 'Total_Puestos', 'Total_Empleados',
                'Empleados_Activos', 'Empleados_Inactivos'
            ]
            
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            
            plantas = Planta.objects.all()
            
            for planta in plantas:
                departamentos = Departamento.objects.filter(planta=planta)
                
                for departamento in departamentos:
                    total_puestos = Puesto.objects.filter(departamento=departamento).count()
                    total_empleados = Empleado.objects.filter(puesto__departamento=departamento).count()
                    empleados_activos = Empleado.objects.filter(
                        puesto__departamento=departamento, status=True
                    ).count()
                    empleados_inactivos = total_empleados - empleados_activos
                    
                    writer.writerow({
                        'Planta_Nombre': planta.nombre,
                        'Departamento_Nombre': departamento.nombre,
                        'Total_Puestos': total_puestos,
                        'Total_Empleados': total_empleados,
                        'Empleados_Activos': empleados_activos,
                        'Empleados_Inactivos': empleados_inactivos
                    })
        
        file_size = os.path.getsize(filepath) / 1024  # KB
        print(f"✅ Resumen estadístico exportado exitosamente")
        print(f"📁 Archivo: {filename}")
        print(f"💾 Tamaño: {file_size:.2f} KB")
        
        return filepath
        
    except Exception as e:
        print(f"❌ Error exportando resumen: {e}")
        return None

def menu_exportacion():
    """Menú principal para exportaciones CSV"""
    while True:
        print("\n📊 SISTEMA DE EXPORTACIÓN CSV")
        print("=" * 40)
        print("1. Exportar empleados (detallado)")
        print("2. Exportar estructura organizacional")
        print("3. Exportar empresas")
        print("4. Exportar resumen estadístico")
        print("5. Exportar todo (todos los archivos)")
        print("6. Salir")
        print("=" * 40)
        
        opcion = input("Selecciona una opción (1-6): ").strip()
        
        if opcion == '1':
            exportar_empleados_csv()
            
        elif opcion == '2':
            exportar_estructura_organizacional_csv()
            
        elif opcion == '3':
            exportar_empresas_csv()
            
        elif opcion == '4':
            exportar_resumen_estadistico_csv()
            
        elif opcion == '5':
            print("📦 EXPORTANDO TODOS LOS ARCHIVOS...")
            exportar_empleados_csv()
            exportar_estructura_organizacional_csv()
            exportar_empresas_csv()
            exportar_resumen_estadistico_csv()
            print("✅ Todas las exportaciones completadas")
            
        elif opcion == '6':
            print("👋 ¡Hasta luego!")
            break
            
        else:
            print("❌ Opción inválida")

if __name__ == "__main__":
    menu_exportacion()
