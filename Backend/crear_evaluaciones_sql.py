#!/usr/bin/env python3
import psycopg2

def crear_datos_evaluaciones_sql():
    """Crea datos de evaluaciones directamente con SQL - RÁPIDO Y FUNCIONAL"""
    
    try:
        # Conexión a la base de datos
        conn = psycopg2.connect(
            host="localhost",
            database="axyoma",
            user="postgres",
            password="12345678"
        )
        
        cur = conn.cursor()
        
        print("🚀 CREANDO EVALUACIONES NOM-030 Y NOM-035 CON SQL DIRECTO")
        print("=" * 60)
        
        # 1. TIPOS DE EVALUACIÓN
        print("📋 Insertando tipos de evaluación...")
        cur.execute("""
            INSERT INTO tipos_evaluacion (tipo_evaluacion_id, nombre, descripcion) 
            VALUES 
                (1, 'NOM-030', 'Factores de riesgo psicosocial en el trabajo'),
                (2, 'NOM-035', 'Factores de riesgo psicosocial en el trabajo - Identificación y prevención')
            ON CONFLICT (tipo_evaluacion_id) DO NOTHING;
        """)
        print("   ✅ Tipos NOM-030 y NOM-035 creados")
        
        # 2. CONJUNTOS DE OPCIONES
        print("📝 Creando conjuntos de opciones...")
        cur.execute("""
            INSERT INTO conjuntos_opciones (conjunto_id, nombre, descripcion, predefinido) 
            VALUES 
                (1, 'Likert 5 puntos', 'Escala Likert de 5 opciones', true),
                (2, 'Likert 4 puntos', 'Escala Likert de 4 opciones', true),
                (3, 'Sí/No', 'Respuestas binarias', true)
            ON CONFLICT (conjunto_id) DO NOTHING;
        """)
        
        # 3. OPCIONES PARA LIKERT 5 PUNTOS
        cur.execute("""
            INSERT INTO opciones_conjunto (opcion_conjunto_id, texto_opcion, valor_numerico, numero_orden, conjunto_opciones) 
            VALUES 
                (1, 'Nunca', 0, 1, 1),
                (2, 'Pocas veces', 1, 2, 1),
                (3, 'Algunas veces', 2, 3, 1),
                (4, 'Muchas veces', 3, 4, 1),
                (5, 'Siempre', 4, 5, 1)
            ON CONFLICT (opcion_conjunto_id) DO NOTHING;
        """)
        
        # 4. OPCIONES PARA LIKERT 4 PUNTOS
        cur.execute("""
            INSERT INTO opciones_conjunto (opcion_conjunto_id, texto_opcion, valor_numerico, numero_orden, conjunto_opciones) 
            VALUES 
                (6, 'Nunca', 0, 1, 2),
                (7, 'Pocas veces', 1, 2, 2),
                (8, 'Algunas veces', 2, 3, 2),
                (9, 'Siempre', 3, 4, 2)
            ON CONFLICT (opcion_conjunto_id) DO NOTHING;
        """)
        
        # 5. OPCIONES SÍ/NO
        cur.execute("""
            INSERT INTO opciones_conjunto (opcion_conjunto_id, texto_opcion, valor_booleano, numero_orden, conjunto_opciones) 
            VALUES 
                (10, 'Sí', true, 1, 3),
                (11, 'No', false, 2, 3)
            ON CONFLICT (opcion_conjunto_id) DO NOTHING;
        """)
        print("   ✅ Conjuntos de opciones creados")
        
        # 6. EVALUACIONES
        print("📊 Creando evaluaciones...")
        cur.execute("""
            INSERT INTO evaluaciones (evaluacion_id, nombre, descripcion, instrucciones, tiempo_limite, umbral_aprobacion, tipo_evaluacion_id, empresa_id, creado_por_id) 
            VALUES 
                (1, 'NOM-030-STPS-2009 - Factores de Riesgo Psicosocial', 
                 'Evaluación de los factores de riesgo psicosocial en el trabajo que pueden provocar trastornos en la salud, afectar la productividad y propiciar accidentes y fatiga laboral.',
                 'A continuación se presentan las preguntas sobre las condiciones en las que realizas tu trabajo. Deberás seleccionar UNA respuesta por cada pregunta.',
                 45, NULL, 1, NULL, NULL),
                (2, 'NOM-035-STPS-2018 - Entorno Organizacional Favorable',
                 'Evaluación del entorno organizacional favorable y factores de riesgo psicosocial para la identificación, análisis y prevención.',
                 'Esta evaluación te ayudará a identificar factores del entorno organizacional. Responde con honestidad todas las preguntas.',
                 60, NULL, 2, NULL, NULL)
            ON CONFLICT (evaluacion_id) DO NOTHING;
        """)
        print("   ✅ Evaluaciones NOM-030 y NOM-035 creadas")
        
        # 7. VERIFICAR RESULTADOS
        print("\n🔍 Verificando datos creados...")
        
        # Contar tipos
        cur.execute("SELECT COUNT(*) FROM tipos_evaluacion;")
        tipos_count = cur.fetchone()[0]
        print(f"   📋 Tipos de evaluación: {tipos_count}")
        
        # Contar conjuntos
        cur.execute("SELECT COUNT(*) FROM conjuntos_opciones;")
        conjuntos_count = cur.fetchone()[0]
        print(f"   📝 Conjuntos de opciones: {conjuntos_count}")
        
        # Contar opciones
        cur.execute("SELECT COUNT(*) FROM opciones_conjunto;")
        opciones_count = cur.fetchone()[0]
        print(f"   🔘 Opciones totales: {opciones_count}")
        
        # Contar evaluaciones
        cur.execute("SELECT COUNT(*) FROM evaluaciones;")
        evaluaciones_count = cur.fetchone()[0]
        print(f"   📊 Evaluaciones: {evaluaciones_count}")
        
        # Confirmar cambios
        conn.commit()
        cur.close()
        conn.close()
        
        print("\n🎉 ¡SISTEMA DE EVALUACIONES CREADO EXITOSAMENTE!")
        print("✅ Base de datos lista para funcionar")
        print("✅ Datos insertados correctamente")
        print("✅ Sistema listo para respaldos y restauraciones")
        
    except Exception as e:
        print(f"❌ ERROR: {e}")
        if 'conn' in locals():
            conn.rollback()
            conn.close()

if __name__ == "__main__":
    crear_datos_evaluaciones_sql()
