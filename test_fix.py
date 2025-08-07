import os, sys, django
sys.path.insert(0, 'Backend')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.evaluaciones.models import Evaluacion
from apps.evaluaciones.serializers import EvaluacionSerializer

print("=== Testeo de actualización de evaluación ===")

try:
    # Obtener evaluación 1
    evaluacion = Evaluacion.objects.get(evaluacion_id=1)
    print(f"✅ Evaluación encontrada: {evaluacion.titulo}")
    print(f"   Creado por: {evaluacion.creado_por.user_id if evaluacion.creado_por else 'None'}")
    
    # Simular los datos que enviaría el frontend corregido
    update_data = {
        'titulo': evaluacion.titulo,
        'descripcion': evaluacion.descripcion or '',
        'instrucciones': evaluacion.instrucciones or '',
        'contenido_informativo': evaluacion.contenido_informativo or '',
        'tiempo_limite': evaluacion.tiempo_limite,
        'umbral_aprobacion': evaluacion.umbral_aprobacion,
        'estado': evaluacion.estado,
        'tipo_evaluacion_id': evaluacion.tipo_evaluacion.tipo_evaluacion_id,
        'empresa_id': evaluacion.empresa.empresa_id if evaluacion.empresa else None,
        'creado_por_id': evaluacion.creado_por.user_id if evaluacion.creado_por else None,  # MANTENER EL ORIGINAL
        'secciones': []
    }
    
    print(f"📤 Datos de prueba:")
    print(f"   creado_por_id: {update_data['creado_por_id']}")
    print(f"   tipo_evaluacion_id: {update_data['tipo_evaluacion_id']}")
    print(f"   empresa_id: {update_data['empresa_id']}")
    
    # Validar con serializer
    serializer = EvaluacionSerializer(evaluacion, data=update_data)
    
    if serializer.is_valid():
        print("✅ Validación exitosa - El problema está resuelto")
        print("   Los datos se pueden actualizar sin errores")
    else:
        print("❌ Errores de validación:")
        for field, errors in serializer.errors.items():
            print(f"   {field}: {errors}")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
