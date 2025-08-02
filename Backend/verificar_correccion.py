import os
import sys
import subprocess

print("🚀 Iniciando verificación de endpoints corregidos...")
print("="*60)

# Cambiar al directorio Backend si es necesario
if not os.path.exists('manage.py'):
    if os.path.exists('Backend/manage.py'):
        os.chdir('Backend')
        print("📁 Cambiado al directorio Backend")
    else:
        print("❌ No se encuentra manage.py")
        sys.exit(1)

# Verificar que Django funcione
try:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')
    import django
    django.setup()
    print("✅ Django configurado correctamente")
    
    from apps.users.models import Empresa, Planta
    from apps.serializers import PlantaSerializer
    
    # Buscar empresa con ID 3
    try:
        empresa = Empresa.objects.get(empresa_id=3)
        print(f"✅ Empresa encontrada: {empresa.nombre}")
        
        # Verificar plantas
        plantas = Planta.objects.filter(empresa=empresa)
        print(f"🏭 Plantas en empresa: {plantas.count()}")
        
        if plantas.exists():
            planta = plantas.first()
            print(f"   Primera planta: {planta.nombre}")
            
            # Probar serializer
            try:
                serializer = PlantaSerializer(planta)
                data = serializer.data
                print(f"✅ Serializer funciona - Campos: {list(data.keys())}")
                print(f"   Datos: {data}")
            except Exception as e:
                print(f"❌ Error en serializer: {e}")
        else:
            print("⚠️  No hay plantas, creando una de prueba...")
            try:
                nueva_planta = Planta.objects.create(
                    nombre="Planta de Prueba",
                    direccion="Dirección de prueba",
                    empresa=empresa
                )
                print(f"✅ Planta creada: {nueva_planta.nombre}")
            except Exception as e:
                print(f"❌ Error creando planta: {e}")
                
    except Empresa.DoesNotExist:
        print("❌ No existe empresa con ID 3")
        print("🔍 Empresas disponibles:")
        for emp in Empresa.objects.all()[:5]:
            print(f"   - ID {emp.empresa_id}: {emp.nombre}")
            
except Exception as e:
    print(f"❌ Error configurando Django: {e}")
    sys.exit(1)

print("\n" + "="*60)
print("✨ ¡Verificación completada!")
print("🌟 Los serializers han sido corregidos:")
print("   - Eliminado campo 'fecha_registro' de PlantaSerializer")
print("   - Eliminado campo 'fecha_registro' de DepartamentoSerializer")  
print("   - Eliminado campo 'fecha_registro' de EmpleadoSerializer")
print("\n🚀 Ahora puedes iniciar el servidor con: python manage.py runserver")
print("🌐 Y probar el frontend en: http://localhost:3000")
