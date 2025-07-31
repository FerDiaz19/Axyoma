#!/usr/bin/env python3
import psycopg2
from psycopg2 import sql

def recrear_tablas_evaluaciones():
    """Borra y recrea todas las tablas de evaluaciones"""
    
    try:
        # Conexión a la base de datos
        conn = psycopg2.connect(
            host="localhost",
            database="axyoma",
            user="postgres",
            password="12345678"
        )
        
        cur = conn.cursor()
        
        print("🗑️  BORRANDO TABLAS EXISTENTES...")
        
        # Lista de tablas a borrar (en orden para evitar problemas de FK)
        tablas_a_borrar = [
            'resultados_evaluacion',
            'respuestas_empleado', 
            'asignaciones_empleado',
            'asignaciones',
            'seccion_preguntas',
            'opciones_conjunto',
            'conjuntos_opciones',
            'secciones_eval',
            'preguntas',
            'evaluaciones',
            'tipos_evaluacion'
        ]
        
        for tabla in tablas_a_borrar:
            try:
                cur.execute(f"DROP TABLE IF EXISTS {tabla} CASCADE;")
                print(f"   ✅ Borrada: {tabla}")
            except Exception as e:
                print(f"   ⚠️  {tabla}: {e}")
        
        print("\n🔧 CREANDO TABLAS NUEVAS...")
        
        # 1. TIPOS DE EVALUACIÓN
        cur.execute("""
            CREATE TABLE tipos_evaluacion (
                tipo_evaluacion_id SERIAL PRIMARY KEY,
                nombre VARCHAR(32) NOT NULL UNIQUE,
                descripcion TEXT
            );
        """)
        print("   ✅ tipos_evaluacion")
        
        # 2. EVALUACIONES (sin foreign keys por ahora)
        cur.execute("""
            CREATE TABLE evaluaciones (
                evaluacion_id SERIAL PRIMARY KEY,
                nombre VARCHAR(128) NOT NULL,
                descripcion TEXT,
                instrucciones TEXT,
                tiempo_limite INTEGER,
                umbral_aprobacion INTEGER,
                status BOOLEAN DEFAULT TRUE,
                fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                tipo_evaluacion_id INTEGER REFERENCES tipos_evaluacion(tipo_evaluacion_id) ON DELETE RESTRICT,
                empresa_id INTEGER,
                creado_por_id INTEGER
            );
        """)
        print("   ✅ evaluaciones")
        
        # 3. PREGUNTAS
        cur.execute("""
            CREATE TABLE preguntas (
                pregunta_id SERIAL PRIMARY KEY,
                texto_pregunta TEXT NOT NULL,
                tipo_pregunta VARCHAR(20) CHECK (tipo_pregunta IN ('Abierta', 'Múltiple', 'Escala', 'Bool')),
                es_obligatoria BOOLEAN DEFAULT TRUE,
                pregunta_padre INTEGER REFERENCES preguntas(pregunta_id) ON DELETE CASCADE,
                activador_padre VARCHAR(255)
            );
        """)
        print("   ✅ preguntas")
        
        # 4. SECCIONES EVALUACIÓN
        cur.execute("""
            CREATE TABLE secciones_eval (
                seccion_id SERIAL PRIMARY KEY,
                nombre VARCHAR(64) NOT NULL,
                descripcion TEXT,
                numero_orden INTEGER NOT NULL,
                es_evaluable BOOLEAN DEFAULT TRUE,
                evaluacion_id INTEGER REFERENCES evaluaciones(evaluacion_id) ON DELETE CASCADE,
                UNIQUE(evaluacion_id, numero_orden)
            );
        """)
        print("   ✅ secciones_eval")
        
        # 5. CONJUNTOS DE OPCIONES
        cur.execute("""
            CREATE TABLE conjuntos_opciones (
                conjunto_id SERIAL PRIMARY KEY,
                nombre VARCHAR(64) NOT NULL UNIQUE,
                descripcion TEXT,
                predefinido BOOLEAN DEFAULT FALSE
            );
        """)
        print("   ✅ conjuntos_opciones")
        
        # 6. OPCIONES CONJUNTO
        cur.execute("""
            CREATE TABLE opciones_conjunto (
                opcion_conjunto_id SERIAL PRIMARY KEY,
                texto_opcion VARCHAR(256) NOT NULL,
                valor_booleano BOOLEAN,
                valor_numerico INTEGER,
                puntuaje_escala DECIMAL(16,2),
                numero_orden INTEGER NOT NULL,
                conjunto_opciones INTEGER REFERENCES conjuntos_opciones(conjunto_id) ON DELETE CASCADE,
                UNIQUE(conjunto_opciones, numero_orden)
            );
        """)
        print("   ✅ opciones_conjunto")
        
        # 7. SECCIÓN PREGUNTAS
        cur.execute("""
            CREATE TABLE seccion_preguntas (
                seccion_pregunta_id SERIAL PRIMARY KEY,
                seccion_id INTEGER REFERENCES secciones_eval(seccion_id) ON DELETE CASCADE,
                pregunta_id INTEGER REFERENCES preguntas(pregunta_id) ON DELETE CASCADE,
                conjunto_respuestas_id INTEGER REFERENCES conjuntos_opciones(conjunto_id) ON DELETE SET NULL,
                respuesta_correcta_id INTEGER REFERENCES opciones_conjunto(opcion_conjunto_id) ON DELETE SET NULL,
                numero_orden INTEGER NOT NULL,
                UNIQUE(seccion_id, pregunta_id),
                UNIQUE(seccion_id, numero_orden)
            );
        """)
        print("   ✅ seccion_preguntas")
        
        # 8. ASIGNACIONES (sin algunas foreign keys por ahora)
        cur.execute("""
            CREATE TABLE asignaciones (
                asignacion_id SERIAL PRIMARY KEY,
                evaluacion_id INTEGER REFERENCES evaluaciones(evaluacion_id) ON DELETE RESTRICT,
                fecha_inicio TIMESTAMP NOT NULL,
                fecha_fin TIMESTAMP NOT NULL,
                status BOOLEAN DEFAULT TRUE,
                fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                empleado_evaluado_id INTEGER,
                puesto VARCHAR(64),
                departamento VARCHAR(64)
            );
        """)
        print("   ✅ asignaciones")
        
        # 9. ASIGNACIONES EMPLEADO (sin foreign key a empleados por ahora)
        cur.execute("""
            CREATE TABLE asignaciones_empleado (
                asignacion_empleado_id SERIAL PRIMARY KEY,
                asignacion_id INTEGER REFERENCES asignaciones(asignacion_id) ON DELETE CASCADE,
                empleado_id INTEGER,
                token_acceso UUID DEFAULT gen_random_uuid() UNIQUE,
                status VARCHAR(16) CHECK (status IN ('Expirada', 'Pendiente', 'Completada')) DEFAULT 'Pendiente',
                fecha_asignacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                fecha_completado TIMESTAMP,
                UNIQUE(asignacion_id, empleado_id)
            );
        """)
        print("   ✅ asignaciones_empleado")
        
        # 10. RESPUESTAS EMPLEADO
        cur.execute("""
            CREATE TABLE respuestas_empleado (
                respuesta_empleado_id SERIAL PRIMARY KEY,
                asignacion_empleado_id INTEGER REFERENCES asignaciones_empleado(asignacion_empleado_id) ON DELETE CASCADE,
                seccion_pregunta_id INTEGER REFERENCES seccion_preguntas(seccion_pregunta_id) ON DELETE CASCADE,
                opcion_seleccionada_id INTEGER REFERENCES opciones_conjunto(opcion_conjunto_id) ON DELETE SET NULL,
                respuesta_texto TEXT,
                respuesta_valor_numerico INTEGER,
                respuesta_valor_decimal DECIMAL(16,2),
                es_correcta BOOLEAN DEFAULT FALSE,
                fecha_respuesta TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(asignacion_empleado_id, seccion_pregunta_id)
            );
        """)
        print("   ✅ respuestas_empleado")
        
        # 11. RESULTADOS EVALUACIÓN
        cur.execute("""
            CREATE TABLE resultados_evaluacion (
                resultado_id SERIAL PRIMARY KEY,
                asignacion_empleado_id INTEGER REFERENCES asignaciones_empleado(asignacion_empleado_id) ON DELETE CASCADE UNIQUE,
                puntaje_total DECIMAL(6,2),
                num_respuestas_correctas INTEGER DEFAULT 0,
                num_preguntas_evaluables INTEGER DEFAULT 0,
                porcentaje_correctas DECIMAL(5,2),
                fecha_calculo TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                aprobado BOOLEAN
            );
        """)
        print("   ✅ resultados_evaluacion")
        
        # Crear índices para performance
        print("\n📊 CREANDO ÍNDICES...")
        indices = [
            "CREATE INDEX idx_evaluaciones_tipo ON evaluaciones(tipo_evaluacion_id);",
            "CREATE INDEX idx_evaluaciones_empresa ON evaluaciones(empresa_id);",
            "CREATE INDEX idx_secciones_evaluacion ON secciones_eval(evaluacion_id);",
            "CREATE INDEX idx_opciones_conjunto ON opciones_conjunto(conjunto_opciones);",
            "CREATE INDEX idx_asignaciones_evaluacion ON asignaciones(evaluacion_id);",
            "CREATE INDEX idx_asignaciones_emp_asignacion ON asignaciones_empleado(asignacion_id);",
            "CREATE INDEX idx_respuestas_asignacion ON respuestas_empleado(asignacion_empleado_id);"
        ]
        
        for indice in indices:
            cur.execute(indice)
        print("   ✅ Índices creados")
        
        # Confirmar cambios
        conn.commit()
        cur.close()
        conn.close()
        
        print("\n🎉 ¡TABLAS RECREADAS EXITOSAMENTE!")
        print("✅ Todas las tablas de evaluaciones están listas")
        print("✅ Estructura compatible con los modelos")
        print("✅ Relaciones e índices configurados")
        
    except Exception as e:
        print(f"❌ ERROR: {e}")
        if 'conn' in locals():
            conn.rollback()
            conn.close()

if __name__ == "__main__":
    recrear_tablas_evaluaciones()
