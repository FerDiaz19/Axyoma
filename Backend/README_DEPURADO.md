# BACKEND AXYOMA - ESTRUCTURA DEPURADA

## 📁 Estructura del Proyecto

```
Backend/
├── manage.py                    # Comando principal de Django
├── requirements.txt             # Dependencias del proyecto
├── config/                      # Configuración de Django
│   ├── settings/               # Configuraciones por ambiente
│   ├── urls.py                 # URLs principales
│   └── wsgi.py / asgi.py       # Configuración de servidor
├── core/                       # App principal/común
├── apps/                       # Aplicaciones del sistema
│   ├── users/                  # Gestión de usuarios, empresas, empleados
│   ├── evaluaciones/           # Sistema de evaluaciones y asignaciones
│   ├── subscriptions/          # Gestión de suscripciones
│   └── surveys/               # Encuestas y cuestionarios
├── scripts_utiles/            # Scripts útiles mantenidos
│   ├── create_initial_data.py  # Crear datos iniciales
│   ├── inicializar_sistema.py  # Inicializar sistema completo
│   ├── mostrar_credenciales.py # Mostrar usuarios disponibles
│   ├── registrar_empresa.py    # Registrar nueva empresa
│   ├── fix_all_users_final.py  # Arreglar usuarios sin empresa
│   ├── test_api_directo.py     # Probar APIs principales
│   ├── test_api_mejorada.py    # Probar APIs mejoradas
│   └── test_evaluaciones_nuevas.py # Crear evaluaciones de prueba
├── env/                       # Entorno virtual de Python
└── Scripts/                   # Scripts de Django
```

## 🚀 Scripts Útiles Disponibles

### Inicialización del Sistema
```bash
python scripts_utiles/inicializar_sistema.py    # Configurar sistema completo
python scripts_utiles/create_initial_data.py    # Crear datos base
```

### Gestión de Usuarios
```bash
python scripts_utiles/mostrar_credenciales.py   # Ver usuarios disponibles
python scripts_utiles/fix_all_users_final.py    # Arreglar usuarios sin empresa
python scripts_utiles/registrar_empresa.py      # Registrar nueva empresa
```

### Testing y Desarrollo
```bash
python scripts_utiles/test_api_directo.py       # Probar APIs principales
python scripts_utiles/test_api_mejorada.py      # Probar funcionalidades mejoradas
python scripts_utiles/test_evaluaciones_nuevas.py # Crear evaluaciones de prueba
```

## 🛠️ Comandos Principales

### Servidor de Desarrollo
```bash
python manage.py runserver
```

### Migraciones
```bash
python manage.py makemigrations
python manage.py migrate
```

### Usuario Administrador
```bash
python manage.py createsuperuser
```

## 📋 Archivos Eliminados en la Depuración

### Scripts Temporales Eliminados:
- `asignar_empresa_evaluaciones.py`
- `check_*.py` (varios archivos de verificación)
- `configurar_login.py`
- `create_test_user.py`
- `debug_permisos.py`
- `fix_all_users.py` y `fix_all_users_new.py`
- `fix_superadmin.py`, `fix_user_empresa.py`
- `limpiar_*.py` (varios archivos de limpieza)
- `sincronizar_usuarios.py`
- `test_*.py` (múltiples archivos de testing temporales)
- `verificar_*.py` (varios archivos de verificación)

### Archivos Duplicados Eliminados:
- `apps/apps.py`, `apps/models.py`, `apps/serializers.py`, `apps/urls.py`, `apps/views.py`
- `apps/mock_storage.py`

### Archivos de Caché Eliminados:
- Todos los archivos `.pyc`
- Todos los directorios `__pycache__/`

## ✅ Estado Actual

El proyecto ha sido depurado y organizado. Solo se mantienen:
- **Archivos esenciales** del framework Django
- **Código fuente** de las aplicaciones principales
- **Scripts útiles** organizados en `scripts_utiles/`
- **Configuraciones** necesarias para el funcionamiento

El sistema está optimizado y más rápido sin archivos innecesarios.
