"""
Obtener usuarios reales del sistema
"""

from apps.users.models import *
from django.contrib.auth.models import User

print("🔍 USUARIOS DE DJANGO EN EL SISTEMA")
print("=" * 50)

usuarios = User.objects.all()
for user in usuarios:
    print(f"\n👤 Usuario Django: {user.username}")
    print(f"   📧 Email: {user.email}")
    print(f"   ✅ Activo: {user.is_active}")
    
    if hasattr(user, 'perfil'):
        perfil = user.perfil
        print(f"   🏷️ Nivel: {perfil.nivel_usuario}")
        print(f"   📛 Nombre: {perfil.nombre_completo}")
        print(f"   📧 Correo Perfil: {perfil.correo}")
        
        if perfil.nivel_usuario == 'admin-empresa':
            try:
                empresa = Empresa.objects.get(administrador=perfil)
                print(f"   🏢 Empresa: {empresa.nombre}")
            except:
                print(f"   ❌ Sin empresa asignada")
    else:
        print(f"   ❌ Sin perfil asociado")

print("\n" + "=" * 50)
print("TOTAL USUARIOS:", usuarios.count())
