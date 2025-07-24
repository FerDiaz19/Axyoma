#!/usr/bin/env python
"""
Script para verificar que los modelos de Django correspondan con las tablas de la base de datos
"""

import os
import sys
import django
from django.db import connection

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')
django.setup()

# Importar todos los modelos
from apps.users.models import PerfilUsuario, Empresa, Planta, AdminPlanta, Departamento, Puesto, Empleado
from apps.subscriptions.models import PlanSuscripcion, SuscripcionEmpresa, Pago
from apps.surveys.models import TipoEvaluacion, Evaluacion, SeccionEval, ConjuntoOpciones, OpcionConjunto, Pregunta

def check_table_exists(table_name):
    """Verificar si una tabla existe en la base de datos"""
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_name = %s
            );
        """, [table_name])
        return cursor.fetchone()[0]

def check_column_exists(table_name, column_name):
    """Verificar si una columna existe en una tabla"""
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT EXISTS (
                SELECT FROM information_schema.columns 
                WHERE table_name = %s AND column_name = %s
            );
        """, [table_name, column_name])
        return cursor.fetchone()[0]

def check_model(model):
    """Verificar que un modelo tenga su tabla y columnas correspondientes"""
    table_name = model._meta.db_table
    print(f"\n🔍 Verificando modelo {model.__name__} (tabla: {table_name})")
    
    # Verificar si la tabla existe
    if not check_table_exists(table_name):
        print(f"❌ La tabla {table_name} no existe en la base de datos")
        return False
    
    print(f"✅ Tabla {table_name} encontrada")
    
    # Verificar campos, especialmente foreign keys
    errors = 0
    for field in model._meta.fields:
        if field.is_relation and field.remote_field.model != model:
            # Es una relación a otro modelo
            related_name = field.name
            db_column = field.db_column or f"{related_name}_id"
            
            if check_column_exists(table_name, db_column):
                print(f"✅ Columna de relación {db_column} encontrada")
            else:
                print(f"❌ Columna de relación {db_column} NO encontrada en {table_name}")
                errors += 1
                
                # Sugerir posibles nombres alternativos
                alternatives = [related_name, f"{related_name}_id"]
                for alt in alternatives:
                    if check_column_exists(table_name, alt):
                        print(f"   💡 Se encontró una columna alternativa: {alt}")
                        print(f"   💡 Sugerencia: usar db_column='{alt}' en el modelo")
    
    return errors == 0

def main():
    print("\n🔍 VERIFICANDO MODELOS DJANGO vs ESTRUCTURA DE BASE DE DATOS")
    print("=" * 70)
    
    # Lista de todos los modelos a verificar
    models = [
        PerfilUsuario, Empresa, Planta, AdminPlanta, Departamento, Puesto, Empleado,
        PlanSuscripcion, SuscripcionEmpresa, Pago,
        TipoEvaluacion, Evaluacion, SeccionEval, ConjuntoOpciones, OpcionConjunto, Pregunta
    ]
    
    # Verificar cada modelo
    errors = 0
    for model in models:
        if not check_model(model):
            errors += 1
    
    # Mostrar resultado final
    if errors == 0:
        print("\n✅ TODOS LOS MODELOS ESTÁN CORRECTAMENTE MAPEADOS A LA BASE DE DATOS")
    else:
        print(f"\n⚠️ SE ENCONTRARON {errors} ERRORES EN LOS MODELOS")
        print("   Revisa los mensajes anteriores y corrige los modelos.")
    
if __name__ == "__main__":
    main()
