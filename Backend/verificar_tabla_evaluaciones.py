import psycopg2

try:
    conn = psycopg2.connect(
        host="localhost",
        database="axyoma",
        user="postgres",
        password="12345678"
    )
    
    cur = conn.cursor()
    
    # Verificar estructura de la tabla evaluaciones
    cur.execute("""
        SELECT column_name, data_type, is_nullable, column_default
        FROM information_schema.columns 
        WHERE table_name = 'evaluaciones'
        ORDER BY ordinal_position;
    """)
    
    print("=== ESTRUCTURA TABLA EVALUACIONES ===")
    columns = cur.fetchall()
    for col in columns:
        print(f"Columna: {col[0]}, Tipo: {col[1]}, Nulo: {col[2]}, Default: {col[3]}")
    
    cur.close()
    conn.close()
    
except Exception as e:
    print(f"Error: {e}")
