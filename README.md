# Sistema Axyoma - Gestión Empresarial

Sistema web completo desarrollado con **Django (Backend)** y **React (Frontend)** para la gestión de empresas, plantas, departamentos y empleados con diferentes niveles de administración.

## 🚀 Configuración Rápida

### Requisitos Previos
- **Python 3.8+** 
- **Node.js 14+**
- **PostgreSQL 12+**
- **Git**

### Instalación en 3 Pasos

1. **Clonar el repositorio**
```bash
git clone <url-repositorio>
cd Axyoma2
```

2. **Configuración automática completa**
```bash
setup_proyecto_completo.bat
```

Este script configura todo automáticamente:
- ✅ Verifica/Crea la base de datos PostgreSQL
- ✅ Instala dependencias del backend (Django)
- ✅ Ejecuta migraciones y configura la base de datos
- ✅ Inserta datos de prueba y usuarios
- ✅ Instala dependencias del frontend (React)

3. **Ejecutar el sistema**
```bash
# Terminal 1 - Backend Django
start-backend.bat

# Terminal 2 - Frontend React  
start-frontend.bat
```

## 🌐 Acceso al Sistema

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000/api/
- **Admin Django**: http://localhost:8000/admin/

## 👥 Usuarios de Prueba

| Email | Contraseña | Rol | Descripción |
|-------|------------|-----|-------------|
| ed-rubio@axyoma.com | 1234 | Super Admin | Gestión completa del sistema |
| juan.perez@codewave.com | 1234 | Admin Empresa | Gestión de empleados de CodeWave |
| maria.gomez@codewave.com | 1234 | Admin Planta | Gestión de plantas asignadas |

## ✨ Funcionalidades Principales

### 🏢 Registro de Empresas
- Registro completo de nuevas empresas
- Creación automática de usuario administrador
- Validación de datos únicos (RFC, usuario)

### 📊 Dashboard por Rol
- **SuperAdmin**: Vista global del sistema, gestión de todas las empresas
- **Admin Empresa**: Gestión completa de su empresa (plantas, empleados)
- **Admin Planta**: Gestión de empleados de plantas asignadas

### 🏭 Gestión Organizacional
- **Plantas**: Hasta 5 plantas por empresa
- **Departamentos**: Organizados por planta
- **Puestos**: Definidos por departamento
- **Empleados**: Asignados a puesto/departamento/planta

### 🔐 Seguridad y Aislamiento
- **Filtrado por empresa**: Cada empresa solo ve sus datos
- **Autenticación por token**: Seguridad en todas las APIs
- **Niveles de acceso**: Permisos diferenciados por rol

## 🗄️ Base de Datos

### Configuración PostgreSQL
```
Base de datos: axyoma
Usuario: postgres
Contraseña: 123456789
Puerto: 5432
```

**Nota**: Modificar `Backend/config/settings/local.py` para usar diferentes credenciales.

### Estructura Principal
```
usuarios → empresas → plantas → departamentos → puestos → empleados
```

## 🛠️ Comandos de Gestión

```bash
cd Backend

# Limpiar todos los datos
python manage.py limpiar_datos

# Insertar datos de prueba
python manage.py insertar_datos

# Crear tokens de autenticación
python manage.py crear_tokens

# Verificar configuración
python manage.py verificar_datos
```

## 🔧 Solución de Problemas

### Error de Base de Datos
```bash
cd Backend
python manage.py makemigrations
python manage.py migrate
python setup_database.py
```

### Error de Dependencias
```bash
# Backend
cd Backend
pip install -r requirements.txt

# Frontend
cd frontend
npm install
```

### Error de CORS
Verificar que `CORS_ALLOWED_ORIGINS` en `Backend/config/settings/local.py` incluya:
```python
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]
```

## 📁 Estructura del Proyecto

```
Axyoma2/
├── Backend/                     # Django Backend
│   ├── apps/                   # Aplicación principal
│   │   ├── users/              # Modelos de usuario y empresa
│   │   ├── management/         # Comandos personalizados
│   │   ├── views.py           # Vistas de la API
│   │   ├── serializers.py     # Serializers de la API
│   │   └── urls.py            # URLs de la API
│   ├── config/                 # Configuración Django
│   │   ├── settings/          # Settings por ambiente
│   │   └── urls.py            # URLs principales
│   ├── requirements.txt        # Dependencias Python
│   └── setup_database.py       # Script de configuración DB
├── frontend/                    # React Frontend
│   ├── src/                    # Código fuente
│   │   ├── components/         # Componentes React
│   │   ├── services/          # Servicios API
│   │   └── css/               # Estilos
│   ├── package.json           # Dependencias Node.js
│   └── tsconfig.json          # Configuración TypeScript
├── setup_proyecto_completo.bat # Configuración inicial
├── start-backend.bat           # Iniciar Django
├── start-frontend.bat          # Iniciar React
├── AxyomaDB.sql               # Esquema de base de datos
└── README.md                  # Esta documentación
```

## 🚀 Flujo de Uso

1. **Configuración inicial**: `setup_proyecto_completo.bat`
2. **Iniciar backend**: `start-backend.bat` 
3. **Iniciar frontend**: `start-frontend.bat`
4. **Acceder**: http://localhost:3000
5. **Login** con usuarios de prueba o registrar nueva empresa
6. **Gestionar** plantas, departamentos y empleados según tu rol

## 🤝 Desarrollo

### Agregar nuevas funcionalidades
1. Backend: Agregar modelos en `Backend/apps/users/models.py`
2. Crear serializers en `Backend/apps/serializers.py`
3. Agregar vistas en `Backend/apps/views.py`
4. Frontend: Crear componentes en `frontend/src/components/`
5. Agregar servicios en `frontend/src/services/`

### Comandos útiles
```bash
# Crear nuevas migraciones
python manage.py makemigrations

# Aplicar migraciones
python manage.py migrate

# Compilar frontend para producción
cd frontend && npm run build
```

## 📄 Licencia

Este proyecto está bajo la Licencia MIT.
