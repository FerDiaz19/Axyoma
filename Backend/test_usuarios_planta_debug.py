#!/usr/bin/env python
"""
Test específico para el endpoint usuarios-planta
"""
import os
import sys
import django

# Configurar Django
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

def test_usuarios_planta_logic():
    """
    Emular la lógica del endpoint usuarios_planta línea por línea
    """
    print("🧪 Testing usuarios-planta logic step by step...")
    
    from apps.users.models import Empresa, Planta, AdminPlanta
    
    try:
        # Paso 1: Obtener empresa
        empresa_id = 10
        empresa = Empresa.objects.filter(empresa_id=empresa_id).first()
        print(f"✅ Empresa encontrada: {empresa.nombre if empresa else 'None'}")
        
        if not empresa:
            print("❌ Empresa no encontrada")
            return
        
        # Paso 2: Obtener plantas (excluyendo Planta Principal)
        plantas = Planta.objects.filter(empresa=empresa, status=True).exclude(nombre='Planta Principal')
        print(f"✅ Plantas encontradas (sin Planta Principal): {plantas.count()}")
        
        for planta in plantas:
            print(f"  - {planta.nombre} (ID: {planta.planta_id})")
        
        # Paso 3: Obtener AdminPlanta records
        admin_plantas = AdminPlanta.objects.filter(planta__in=plantas).select_related('usuario__user_id', 'planta')
        print(f"✅ AdminPlanta records encontrados: {admin_plantas.count()}")
        
        # Paso 4: Procesar cada AdminPlanta (aquí puede estar el error)
        usuarios_data = []
        for i, admin_planta in enumerate(admin_plantas):
            print(f"\n🔍 Procesando AdminPlanta {i+1}:")
            print(f"  - Planta: {admin_planta.planta.nombre}")
            print(f"  - Usuario perfil: {admin_planta.usuario}")
            
            # AQUÍ PUEDE ESTAR EL ERROR
            try:
                usuario_user = admin_planta.usuario.user_id
                print(f"  - Usuario Django: {usuario_user}")
                
                if usuario_user:
                    print(f"    - ID: {usuario_user.id}")
                    print(f"    - Username: {usuario_user.username}")
                    print(f"    - Email: {usuario_user.email}")
                    print(f"    - First name: {usuario_user.first_name}")
                    print(f"    - Last name: {usuario_user.last_name}")
                    print(f"    - Is active: {usuario_user.is_active}")
                    print(f"    - Date joined: {usuario_user.date_joined}")
                    
                    # Crear el objeto de datos tal como lo hace el endpoint
                    usuario_data = {
                        'usuario_id': usuario_user.id,
                        'username': usuario_user.username,
                        'email': usuario_user.email,
                        'first_name': usuario_user.first_name,
                        'last_name': usuario_user.last_name,
                        'is_active': usuario_user.is_active,
                        'planta_id': admin_planta.planta.planta_id,
                        'planta_nombre': admin_planta.planta.nombre,
                        'fecha_creacion': usuario_user.date_joined.isoformat() if usuario_user.date_joined else None
                    }
                    usuarios_data.append(usuario_data)
                    print(f"  ✅ Usuario procesado correctamente")
                else:
                    print(f"  ❌ admin_planta.usuario.user_id es None!")
                    
            except AttributeError as e:
                print(f"  ❌ AttributeError: {e}")
            except Exception as e:
                print(f"  ❌ Error inesperado: {e}")
                import traceback
                traceback.print_exc()
        
        print(f"\n✅ Total usuarios procesados: {len(usuarios_data)}")
        
        # Paso 5: Agregar información adicional
        plantas_sin_usuarios = Planta.objects.filter(
            empresa=empresa, 
            status=True,
            nombre='Planta Principal'
        ).exclude(
            planta_id__in=admin_plantas.values_list('planta__planta_id', flat=True)
        )
        
        info_adicional = {
            'total_plantas_empresa': Planta.objects.filter(empresa=empresa, status=True).count(),
            'plantas_con_usuarios': len(usuarios_data),
            'planta_principal_sin_usuario': plantas_sin_usuarios.exists(),
            'mensaje': 'La Planta Principal no requiere usuario específico, es administrada por el admin de empresa.'
        }
        
        print(f"\n📊 Info adicional:")
        print(f"  - Total plantas empresa: {info_adicional['total_plantas_empresa']}")
        print(f"  - Plantas con usuarios: {info_adicional['plantas_con_usuarios']}")
        print(f"  - Planta principal sin usuario: {info_adicional['planta_principal_sin_usuario']}")
        
        # Paso 6: Crear respuesta final
        response_data = {
            'usuarios': usuarios_data,
            'info': info_adicional
        }
        
        print(f"\n✅ Response data generado exitosamente")
        print(f"Usuarios en respuesta: {len(response_data['usuarios'])}")
        
    except Exception as e:
        print(f"❌ Error general: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_usuarios_planta_logic()
