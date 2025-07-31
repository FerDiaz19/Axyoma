import psycopg2

try:
    conn = psycopg2.connect(
        host="localhost",
        database="axyoma",
        user="postgres",
        password="12345678"
    )
    
    cur = conn.cursor()
    
    # Obtener todas las tablas
    cur.execute("""
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_schema = 'public'
        ORDER BY table_name;
    """)
    
    print("=== TODAS LAS TABLAS ===")
    tables = cur.fetchall()
    for table in tables:
        print(f"- {table[0]}")
    
    cur.close()
    conn.close()
    
except Exception as e:
    print(f"Error: {e}")
