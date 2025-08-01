import django
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Backend.settings')
django.setup()

from django.db import connection

def listar_tablas():
    cursor = connection.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    print('=== TABLAS EXISTENTES ===')
    for table in tables:
        print(f'- {table[0]}')
    print('\n')
    
    # Buscar tablas relacionadas con evaluaciones
    evaluation_tables = [t[0] for t in tables if any(keyword in t[0].lower() for keyword in ['eval', 'pregunta', 'respuesta', 'tipo'])]
    if evaluation_tables:
        print('=== TABLAS DE EVALUACIONES EXISTENTES ===')
        for table in evaluation_tables:
            print(f'- {table}')
            cursor.execute(f"PRAGMA table_info({table});")
            columns = cursor.fetchall()
            for col in columns:
                print(f'  └── {col[1]} ({col[2]})')
            print()

if __name__ == '__main__':
    listar_tablas()
