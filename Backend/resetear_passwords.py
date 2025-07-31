"""
Resetear contraseñas de usuarios específicos
"""

from django.contrib.auth.models import User

# Resetear contraseña del superadmin
print("🔑 Reseteando contraseñas...")

usuarios_a_resetear = [
    ('superadmin', 'admin123'),
    ('admin_axis', 'admin123'),
    ('admin_mdn', 'admin123'),
    ('admin_techcorp', 'admin123'),
    ('admin_planta_1_1', 'admin123'),
    ('admin_planta_2_1', 'admin123'),
]

for username, nueva_password in usuarios_a_resetear:
    try:
        user = User.objects.get(username=username)
        user.set_password(nueva_password)
        user.save()
        print(f"✅ {username}: contraseña actualizada")
    except User.DoesNotExist:
        print(f"❌ {username}: usuario no encontrado")

print("🎉 Contraseñas actualizadas")
