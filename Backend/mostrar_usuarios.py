#!/usr/bin/env python
"""
Script para mostrar información detallada de los usuarios del sistema AXYOMA
Extrae datos directamente de la base de datos
"""

import os
import sys
import django
import time
from getpass import getpass

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')
django.setup()

from django.contrib.auth.models import User
from django.db import connection
from django.db.utils import OperationalError

# Intenta importar colorama, pero ofrece una alternativa si no está disponible
try:
    from colorama import init, Fore, Style
    init()  # Inicializar colorama
    COLORAMA_AVAILABLE = True
except ImportError:
    COLORAMA_AVAILABLE = False
    # Creamos clases dummy para simular Fore y Style
    class DummyColors:
        def __getattr__(self, name):
            return ""
    
    Fore = DummyColors()
    Style = DummyColors()
    print("⚠️ La biblioteca 'colorama' no está instalada. Se mostrará sin colores.")
    print("   Para instalar colorama, ejecuta: pip install colorama")
    print()

def mostrar_titulo(texto):
    """Muestra un título con formato colorido"""
    print("\n" + "=" * 70)
    print(f" {texto} ".center(70, "="))
    print("=" * 70 + "\n")

def verificar_conexion_bd():
    """Verificar conexión a la base de datos"""
    print(f"{Fore.YELLOW}🔄 Verificando conexión a la base de datos...{Style.RESET_ALL}")
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            result = cursor.fetchone()
            if result and result[0] == 1:
                print(f"{Fore.GREEN}✅ Conexión a la base de datos exitosa{Style.RESET_ALL}")
                return True
    except OperationalError as e:
        print(f"{Fore.RED}❌ Error al conectar a la base de datos: {e}{Style.RESET_ALL}")
        
        # Sugerir soluciones comunes
        print(f"\n{Fore.YELLOW}Posibles soluciones:{Style.RESET_ALL}")
        print("1. Verifica que el servidor PostgreSQL esté ejecutándose")
        print("2. Revisa que la base de datos 'axyomadb' exista")
        print("3. Confirma que las credenciales en settings/local.py sean correctas")
        
        # Pedir credenciales alternativas
        usar_otras = input("\n¿Deseas intentar con otras credenciales? (s/n): ")
        if usar_otras.lower() == 's':
            user = input("Usuario PostgreSQL [postgres]: ") or "postgres"
            password = getpass("Contraseña PostgreSQL: ")
            database = input("Nombre de base de datos [axyomadb]: ") or "axyomadb"
            
            # Cambiar las credenciales en tiempo de ejecución
            from django.conf import settings
            settings.DATABASES['default']['USER'] = user
            settings.DATABASES['default']['PASSWORD'] = password
            settings.DATABASES['default']['NAME'] = database
            
            # Intentar de nuevo
            try:
                connection.close()
                connection.connect()
                with connection.cursor() as cursor:
                    cursor.execute("SELECT 1")
                    result = cursor.fetchone()
                    if result and result[0] == 1:
                        print(f"{Fore.GREEN}✅ Conexión exitosa con nuevas credenciales{Style.RESET_ALL}")
                        return True
            except Exception as e2:
                print(f"{Fore.RED}❌ Error con nuevas credenciales: {e2}{Style.RESET_ALL}")
        
        return False
    
    except Exception as e:
        print(f"{Fore.RED}❌ Error desconocido: {e}{Style.RESET_ALL}")
        return False

def mostrar_usuarios():
    """Mostrar información detallada de todos los usuarios"""
    mostrar_titulo("📋 USUARIOS DEL SISTEMA AXYOMA")
    
    try:
        # Primero verificamos qué tablas existen
        tablas_existentes = []
        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT table_name 
                    FROM information_schema.tables 
                    WHERE table_schema = 'public'
                """)
                tablas_existentes = [row[0] for row in cursor.fetchall()]
                print(f"{Fore.CYAN}Tablas detectadas: {', '.join(tablas_existentes)}{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}❌ No se pudo verificar las tablas existentes: {e}{Style.RESET_ALL}")
        
        # Consulta SQL simplificada sin tablas que podrían no existir
        sql = """
            SELECT 
                au.id, 
                au.username, 
                au.email,
                au.is_active,
                au.is_staff,
                au.is_superuser,
                u.nombre, 
                u.apellido_paterno, 
                u.apellido_materno, 
                u.nivel_usuario
            FROM 
                auth_user au
            LEFT JOIN 
                usuarios u ON u.user_id = au.id
            ORDER BY 
                au.username
        """
        
        # Si existen las tablas adicionales, usamos una consulta más completa
        if 'usuarios' in tablas_existentes and 'empresas' in tablas_existentes:
            # Consulta más completa con información de empresa
            sql = """
                SELECT 
                    au.id, 
                    au.username, 
                    au.email,
                    au.is_active,
                    au.is_staff,
                    au.is_superuser,
                    u.nombre, 
                    u.apellido_paterno, 
                    u.apellido_materno, 
                    u.nivel_usuario,
                    e.nombre AS empresa_nombre,
                    NULL AS planta_nombre
                FROM 
                    auth_user au
                LEFT JOIN 
                    usuarios u ON u.user_id = au.id
                LEFT JOIN 
                    empresas e ON e.administrador = u.id
            """
            
            # Si también existe la tabla plantas
            if 'plantas' in tablas_existentes:
                print(f"{Fore.GREEN}✅ Tablas de empresas y plantas detectadas. Mostrando información completa.{Style.RESET_ALL}")
            else:
                print(f"{Fore.YELLOW}⚠️ Tabla 'plantas' no encontrada. Información de plantas no disponible.{Style.RESET_ALL}")
        else:
            print(f"{Fore.YELLOW}⚠️ Tablas de estructura organizacional no encontradas.{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}⚠️ Mostrando solo información básica de usuarios.{Style.RESET_ALL}")
        
        with connection.cursor() as cursor:
            cursor.execute(sql)
            columns = [col[0] for col in cursor.description]
            usuarios = [dict(zip(columns, row)) for row in cursor.fetchall()]
        
        if not usuarios:
            print(f"{Fore.YELLOW}⚠️ No se encontraron usuarios en el sistema{Style.RESET_ALL}")
            return
        
        print(f"{Fore.GREEN}✅ Se encontraron {len(usuarios)} usuarios{Style.RESET_ALL}\n")
        
        # Obtener contraseñas para usuarios de prueba
        usuarios_prueba = {
            "superadmin": "1234",
            "admin": "1234",
            "admin_empresa": "1234",
            "admin_planta": "1234",
            "superadmin@axyoma.com": "1234",
            "testuser": "testpass123"
        }
        
        # Mostrar información agrupada por nivel de usuario si la columna existe
        nivel_usuario_col = 'nivel_usuario' if 'nivel_usuario' in columns else None
        
        if nivel_usuario_col:
            # Agrupar por nivel
            niveles = {}
            for usuario in usuarios:
                nivel = usuario[nivel_usuario_col] if usuario[nivel_usuario_col] else 'sin_asignar'
                if nivel not in niveles:
                    niveles[nivel] = []
                niveles[nivel].append(usuario)
            
            for nivel, usuarios_nivel in niveles.items():
                print(f"\n{Fore.CYAN}{Style.BRIGHT}== {nivel.upper()} ==\n{Style.RESET_ALL}")
                mostrar_usuarios_grupo(usuarios_nivel, columns, usuarios_prueba)
        else:
            # Mostrar todos sin agrupación
            print(f"\n{Fore.CYAN}{Style.BRIGHT}== TODOS LOS USUARIOS ==\n{Style.RESET_ALL}")
            mostrar_usuarios_grupo(usuarios, columns, usuarios_prueba)
        
        # Verificar usuarios de Django sin perfil
        if 'usuarios' in tablas_existentes:
            print(f"\n{Fore.YELLOW}Buscando usuarios sin perfil asociado...{Style.RESET_ALL}")
            try:
                with connection.cursor() as cursor:
                    cursor.execute("""
                        SELECT au.id, au.username, au.email
                        FROM auth_user au
                        LEFT JOIN usuarios u ON u.user_id = au.id
                        WHERE u.id IS NULL
                    """)
                    sin_perfil = [dict(zip(['id', 'username', 'email'], row)) for row in cursor.fetchall()]
                    
                if sin_perfil:
                    print(f"{Fore.RED}⚠️ Encontrados {len(sin_perfil)} usuarios sin perfil:{Style.RESET_ALL}")
                    for usuario in sin_perfil:
                        print(f"  - {usuario['username']} ({usuario['email']})")
                else:
                    print(f"{Fore.GREEN}✅ Todos los usuarios tienen perfil asociado{Style.RESET_ALL}")
            except Exception as e:
                print(f"{Fore.RED}❌ Error al buscar usuarios sin perfil: {e}{Style.RESET_ALL}")
    
    except Exception as e:
        print(f"{Fore.RED}❌ Error al obtener usuarios: {e}{Style.RESET_ALL}")
        import traceback
        traceback.print_exc()

def mostrar_usuarios_grupo(usuarios, columns, usuarios_prueba):
    """Muestra un grupo de usuarios formateado"""
    for usuario in usuarios:
        # Color según estado
        color = Fore.GREEN if usuario['is_active'] else Fore.RED
        
        # Buscar si es un usuario de prueba conocido
        password = None
        for test_user, test_pass in usuarios_prueba.items():
            if usuario['username'] == test_user or usuario['email'] == test_user:
                password = test_pass
                break
        
        # Verificar contraseña mediante Django
        if password is None:
            # Verificar si tiene contraseña "1234"
            try:
                user_obj = User.objects.get(id=usuario['id'])
                if user_obj.check_password("1234"):
                    password = "1234"
                elif user_obj.check_password("admin123"):
                    password = "admin123"
                elif user_obj.check_password("password"):
                    password = "password"
                else:
                    password = "desconocida"
            except Exception:
                password = "desconocida"
        
        # Mostrar datos de usuario con formato colorido
        print(f"{color}{Style.BRIGHT}{usuario['username']}{Style.RESET_ALL} ({usuario['email']})")
        
        # Mostrar nombre completo si hay información
        if 'nombre' in columns and usuario['nombre']:
            apellido_paterno = usuario.get('apellido_paterno', '')
            apellido_materno = usuario.get('apellido_materno', '')
            nombre_completo = f"{usuario['nombre']} {apellido_paterno} {apellido_materno}".strip()
            print(f"  📝 Nombre: {nombre_completo}")
        
        print(f"  🔑 Contraseña: {Fore.YELLOW}{password}{Style.RESET_ALL}")
        
        # Mostrar nivel si existe
        if 'nivel_usuario' in columns and usuario['nivel_usuario']:
            print(f"  👤 Nivel: {usuario['nivel_usuario']}")
            
        print(f"  🟢 Activo: {'Sí' if usuario['is_active'] else 'No'}")
        
        # Mostrar empresa/planta si aplica
        if 'empresa_nombre' in columns and usuario['empresa_nombre']:
            print(f"  🏢 Empresa: {usuario['empresa_nombre']}")
        if 'planta_nombre' in columns and usuario['planta_nombre']:
            print(f"  🏭 Planta: {usuario['planta_nombre']}")
        
        print("")  # Línea en blanco para separar usuarios

def crear_usuarios_prueba():
    """Crear usuarios de prueba con credenciales conocidas"""
    mostrar_titulo("🛠️ CREANDO USUARIOS DE PRUEBA")
    
    usuarios_test = [
        {
            "username": "superadmin",
            "email": "superadmin@axyoma.com",
            "password": "1234",
            "nombre": "Super",
            "apellido": "Admin",
            "nivel": "superadmin"
        },
        {
            "username": "admin_empresa",
            "email": "admin@empresa.com",
            "password": "1234",
            "nombre": "Admin",
            "apellido": "Empresa",
            "nivel": "admin-empresa"
        },
        {
            "username": "admin_planta",
            "email": "admin@planta.com",
            "password": "1234",
            "nombre": "Admin",
            "apellido": "Planta",
            "nivel": "admin-planta"
        }
    ]
    
    try:
        from django.contrib.auth.models import User
        from apps.users.models import PerfilUsuario
        
        for usuario in usuarios_test:
            username = usuario["username"]
            
            # Verificar si ya existe
            if User.objects.filter(username=username).exists():
                user = User.objects.get(username=username)
                print(f"{Fore.YELLOW}⚠️ Usuario {username} ya existe, actualizando contraseña...{Style.RESET_ALL}")
                user.set_password(usuario["password"])
                user.save()
                
                # Asegurar que el perfil exista
                if not hasattr(user, 'perfil'):
                    print(f"{Fore.YELLOW}⚠️ Creando perfil para {username}...{Style.RESET_ALL}")
                    PerfilUsuario.objects.create(
                        user=user,
                        nombre=usuario["nombre"],
                        apellido_paterno=usuario["apellido"],
                        correo=usuario["email"],
                        nivel_usuario=usuario["nivel"]
                    )
            else:
                # Crear nuevo usuario
                print(f"{Fore.GREEN}✅ Creando usuario {username}...{Style.RESET_ALL}")
                user = User.objects.create_user(
                    username=username,
                    email=usuario["email"],
                    password=usuario["password"]
                )
                
                PerfilUsuario.objects.create(
                    user=user,
                    nombre=usuario["nombre"],
                    apellido_paterno=usuario["apellido"],
                    correo=usuario["email"],
                    nivel_usuario=usuario["nivel"]
                )
        
        print(f"{Fore.GREEN}✅ Usuarios de prueba creados/actualizados exitosamente{Style.RESET_ALL}")
        
    except Exception as e:
        print(f"{Fore.RED}❌ Error creando usuarios de prueba: {e}{Style.RESET_ALL}")
        import traceback
        traceback.print_exc()

def main():
    """Función principal"""
    os.system('cls' if os.name == 'nt' else 'clear')  # Limpiar terminal
    
    print(f"{Fore.CYAN}{Style.BRIGHT}")
    print("╔══════════════════════════════════════════════════════════════╗")
    print("║           INFORMACIÓN DE USUARIOS AXYOMA API                 ║")
    print("╚══════════════════════════════════════════════════════════════╝")
    print(f"{Style.RESET_ALL}")
    
    # 1. Verificar conexión a la base de datos
    if not verificar_conexion_bd():
        print(f"{Fore.RED}⚠️ No se pudo conectar a la base de datos. Abortando...{Style.RESET_ALL}")
        return
    
    while True:
        print(f"\n{Fore.CYAN}{Style.BRIGHT}MENÚ:{Style.RESET_ALL}")
        print("1. Mostrar usuarios existentes")
        print("2. Crear usuarios de prueba")
        print("3. Salir")
        
        opcion = input(f"\n{Fore.YELLOW}Selecciona una opción (1-3): {Style.RESET_ALL}")
        
        if opcion == '1':
            mostrar_usuarios()
        elif opcion == '2':
            crear_usuarios_prueba()
        elif opcion == '3':
            break
        else:
            print(f"{Fore.RED}Opción inválida. Por favor, intenta de nuevo.{Style.RESET_ALL}")
    
    print(f"\n{Fore.CYAN}{Style.BRIGHT}¡Gracias por usar el verificador de usuarios de AXYOMA!{Style.RESET_ALL}")

if __name__ == "__main__":
    main()
