#!/usr/bin/env python
import os
import sys
import django

# Setup Django
sys.path.insert(0, 'c:/xampp2/htdocs/UTT4B/Axyoma2/Backend')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')
django.setup()

from django.db import connection

try:
    with connection.cursor() as cursor:
        # Create admin_plantas table manually if needed
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS admin_plantas (
                id SERIAL PRIMARY KEY,
                usuario_id INTEGER NOT NULL REFERENCES usuarios(id) ON DELETE CASCADE,
                planta_id INTEGER NOT NULL REFERENCES plantas(planta_id) ON DELETE CASCADE,
                fecha_asignacion TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
                status BOOLEAN DEFAULT TRUE,
                UNIQUE(usuario_id, planta_id)
            );
        """)
        print("✅ Table admin_plantas created/verified")
        
        # Verify the table exists now
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public' AND table_name = 'admin_plantas';
        """)
        result = cursor.fetchone()
        if result:
            print("✅ admin_plantas table exists")
        else:
            print("❌ admin_plantas table still missing")

except Exception as e:
    print(f"❌ Error creating table: {e}")
    import traceback
    traceback.print_exc()
