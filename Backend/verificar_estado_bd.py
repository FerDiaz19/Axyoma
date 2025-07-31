#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Verificador de estado de la base de datos
"""

import os
import sys
import django

# Configurar Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.db import connection

def verificar_tablas():
    """Verifica qué tablas existen en la base de datos"""
    print("🔍 VERIFICANDO ESTADO DE LA BASE DE DATOS")
    print("=" * 50)
    
    try:
        cursor = connection.cursor()
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public' 
            ORDER BY table_name;
        """)
        tables = cursor.fetchall()
        
        print(f"📊 Total de tablas encontradas: {len(tables)}")
        print("\n📋 Lista de tablas:")
        for table in tables:
            print(f"   ✅ {table[0]}")
        
        # Verificar tablas específicas que necesitamos
        tablas_necesarias = [
            'usuarios', 'empresas', 'plantas', 'departamentos', 'puestos', 'empleados',
            'planes', 'suscripciones',
            'tipos_evaluacion', 'evaluaciones', 'secciones_eval', 'preguntas'
        ]
        
        tablas_existentes = [t[0] for t in tables]
        
        print(f"\n🎯 Verificando tablas necesarias:")
        for tabla in tablas_necesarias:
            if tabla in tablas_existentes:
                print(f"   ✅ {tabla} - Existe")
            else:
                print(f"   ❌ {tabla} - No existe")
        
        cursor.close()
        return True
        
    except Exception as e:
        print(f"❌ Error verificando BD: {str(e)}")
        return False

def probar_importaciones():
    """Prueba importar los modelos"""
    print(f"\n🧪 PROBANDO IMPORTACIONES DE MODELOS")
    print("=" * 50)
    
    try:
        # Importar modelos de users
        from apps.users.models import (
            PerfilUsuario, Empresa, Planta, Departamento, Puesto, Empleado,
            TipoEvaluacion, Evaluacion, SeccionEval, Pregunta
        )
        print("✅ Modelos de users importados correctamente")
        
        # Importar modelos de subscriptions
        from apps.subscriptions.models import PlanSuscripcion, SuscripcionEmpresa
        print("✅ Modelos de subscriptions importados correctamente")
        
        return True
        
    except Exception as e:
        print(f"❌ Error importando modelos: {str(e)}")
        return False

def verificar_estructura_planes():
    """Verifica la estructura de la tabla planes"""
    print(f"\n🔍 VERIFICANDO ESTRUCTURA DE TABLA PLANES")
    print("=" * 50)
    
    try:
        cursor = connection.cursor()
        cursor.execute("""
            SELECT column_name, data_type, is_nullable
            FROM information_schema.columns 
            WHERE table_name = 'planes'
            ORDER BY ordinal_position;
        """)
        columns = cursor.fetchall()
        
        print("Columnas en tabla 'planes':")
        for col in columns:
            print(f"   - {col[0]} ({col[1]}) {'NULL' if col[2] == 'YES' else 'NOT NULL'}")
        
        cursor.close()
        return True
        
    except Exception as e:
        print(f"❌ Error verificando estructura: {str(e)}")
        return False

def contar_registros():
    """Cuenta registros existentes"""
    print(f"\n📊 CONTANDO REGISTROS EXISTENTES")
    print("=" * 50)
    
    try:
        from apps.users.models import PerfilUsuario, Empresa, Empleado
        from apps.subscriptions.models import PlanSuscripcion
        
        conteos = [
            ('Perfiles Usuario', PerfilUsuario.objects.count()),
            ('Empresas', Empresa.objects.count()),
            ('Empleados', Empleado.objects.count()),
            ('Planes Suscripción', PlanSuscripcion.objects.count()),
        ]
        
        for nombre, count in conteos:
            print(f"   {nombre:20} : {count:4d}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error contando registros: {str(e)}")
        return False

def main():
    """Función principal"""
    try:
        # 1. Verificar tablas
        if not verificar_tablas():
            return False
        
        # 2. Probar importaciones
        if not probar_importaciones():
            return False
        
        # 3. Verificar estructura
        if not verificar_estructura_planes():
            return False
        
        # 4. Contar registros
        if not contar_registros():
            return False
        
        print(f"\n🎉 SISTEMA VERIFICADO CORRECTAMENTE")
        return True
        
    except Exception as e:
        print(f"❌ ERROR CRÍTICO: {str(e)}")
        return False

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
