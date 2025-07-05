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
    # Test database connection
    with connection.cursor() as cursor:
        cursor.execute("SELECT version();")
        result = cursor.fetchone()
        print(f"✅ Database connection successful")
        print(f"PostgreSQL version: {result[0]}")
        
        # List tables
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
            ORDER BY table_name;
        """)
        tables = cursor.fetchall()
        print(f"\nTables in database: {len(tables)}")
        for table in tables:
            print(f"  - {table[0]}")

except Exception as e:
    print(f"❌ Database connection failed: {e}")
    import traceback
    traceback.print_exc()
