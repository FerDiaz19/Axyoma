"""
Script para debuggear la relación entre usuarios, perfiles y empresas
"""
import os
import sys
import django

# Configurar Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'axioma.settings')
django.setup()

from apps.users.models import PerfilUsuario, Empresa, Planta
from django.contrib.auth.models import User

def debug_user_empresa_relation():
    print("=== DEBUG: Relación Usuario-Empresa ===")
    
    # Buscar el usuario Jose Padilal
    user = User.objects.filter(username='axis2').first()
    if not user:
        print("❌ Usuario 'axis2' no encontrado")
        return
    
    print(f"👤 Usuario encontrado: {user.username} (ID: {user.id})")
    
    # Verificar perfil
    if hasattr(user, 'perfil'):
        perfil = user.perfil
        print(f"📋 Perfil: ID={perfil.id}, nivel={perfil.nivel_usuario}, nombre={perfil.nombre_completo}")
        
        # Buscar empresa donde este perfil es administrador
        empresa_admin = Empresa.objects.filter(administrador_id=perfil.id).first()
        if empresa_admin:
            print(f"🏢 Empresa (por administrador): ID={empresa_admin.empresa_id}, nombre={empresa_admin.nombre}")
        else:
            print("❌ No se encontró empresa donde este perfil sea administrador")
        
        # Buscar todas las empresas
        print("\n🔍 Todas las empresas:")
        empresas = Empresa.objects.all()
        for emp in empresas:
            print(f"  - ID={emp.empresa_id}, nombre={emp.nombre}, admin_id={emp.administrador_id}")
        
        # Buscar plantas de la empresa correcta (ID=3 según los datos)
        print(f"\n🏭 Plantas de la empresa ID=3:")
        plantas = Planta.objects.filter(empresa_id=3, status=True)
        for planta in plantas:
            print(f"  - ID={planta.planta_id}, nombre={planta.nombre}, empresa_id={planta.empresa_id}")
    else:
        print("❌ Usuario no tiene perfil")

if __name__ == "__main__":
    debug_user_empresa_relation()
