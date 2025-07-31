#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import django

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.db import connection

cursor = connection.cursor()
cursor.execute("""
    SELECT column_name, data_type, is_nullable
    FROM information_schema.columns 
    WHERE table_name = 'suscripciones'
    ORDER BY ordinal_position;
""")
columns = cursor.fetchall()

print("Columnas en tabla 'suscripciones':")
for col in columns:
    nullable = "NULL" if col[2] == "YES" else "NOT NULL"
    print(f"   - {col[0]} ({col[1]}) {nullable}")

cursor.close()
