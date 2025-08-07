import os, sys, django
sys.path.insert(0, 'Backend')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.evaluaciones.models import *
from apps.users.models import *

print("=== Verificando estructura de datos ===")

try:
    # Verificar evaluación ID 1
    evaluacion = Evaluacion.objects.get(evaluacion_id=1)
    print(f"Evaluación: {evaluacion.titulo}")
    print(f"Estado: {evaluacion.estado}")
    print(f"Empresa ID: {evaluacion.empresa.empresa_id if evaluacion.empresa else 'None'}")
    print(f"Creado por ID: {evaluacion.creado_por.user_id if evaluacion.creado_por else 'None'}")
    print(f"Tipo evaluación ID: {evaluacion.tipo_evaluacion.tipo_evaluacion_id}")
    
    # Verificar secciones
    secciones = evaluacion.secciones.all()
    print(f"Secciones: {len(secciones)}")
    
    for seccion in secciones:
        print(f"  - Sección: {seccion.nombre} (ID: {seccion.seccion_id})")
        preguntas = seccion.preguntas_seccion.all()
        print(f"    Preguntas: {len(preguntas)}")
        
        for pregunta_seccion in preguntas:
            print(f"    - Pregunta: {pregunta_seccion.pregunta.texto_pregunta[:50]}...")
            if pregunta_seccion.conjunto_respuestas:
                print(f"      Conjunto: {pregunta_seccion.conjunto_respuestas.nombre}")
            if pregunta_seccion.respuesta_correcta:
                print(f"      Respuesta correcta: {pregunta_seccion.respuesta_correcta.texto_opcion}")

except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
