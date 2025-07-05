# Sistema Axyoma - Gestión Empresarial

Sistema web completo desarrollado con Django (Backend) y React (Frontend) para la gestión de empresas, plantas, departamentos y empleados con diferentes niveles de administración.

## 🚀 Configuración Rápida

### Requisitos Previos
- Python 3.8+
- Node.js 14+
- PostgreSQL 12+
- Git

### Instalación Automática

1. **Clonar el repositorio**
```bash
git clone <url-repositorio>
cd Axyoma2
```

2. **Ejecutar configuración automática**
```bash
setup_proyecto_completo.bat
```

Este script hará todo automáticamente:
- Instalar dependencias del backend
- Configurar la base de datos
- Insertar datos de prueba
- Instalar dependencias del frontend

### Configuración Manual (si es necesario)

#### Backend (Django)
```bash
cd Backend
pip install -r requirements.txt
python manage.py migrate
python manage.py insertar_datos
```

#### Frontend (React)
```bash
cd frontend
npm install
```

## 🎯 Ejecutar el Proyecto

### Opción 1: Scripts Automáticos
```bash
# Terminal 1 - Backend
start-backend.bat

# Terminal 2 - Frontend  
start-frontend.bat
```

### Opción 2: Manual
```bash
# Backend (Puerto 8000)
cd Backend
python manage.py runserver

# Frontend (Puerto 3000)
cd frontend
npm start
```

## 👥 Usuarios de Prueba

| Email | Contraseña | Rol | Dashboard |
|-------|------------|-----|-----------|
| ed-rubio@axyoma.com | 1234 | Super Admin | Gestión completa del sistema |
| juan.perez@codewave.com | 1234 | Admin Empresa | Gestión de su empresa |
| maria.gomez@codewave.com | 1234 | Admin Planta | Gestión de plantas asignadas |

## 🗄️ Base de Datos

### Configuración PostgreSQL
1. Crear base de datos: `axyoma`
2. Usuario: `postgres`
3. Contraseña: `123456789`
4. Puerto: `5432`

**Nota:** Modificar `Backend/config/settings/local.py` si usa diferentes credenciales.

### Estructura de la Base de Datos
- **usuarios**: Perfiles de usuario con niveles de acceso
- **empresas**: Información de empresas registradas
- **plantas**: Plantas asociadas a empresas
- **admin_plantas**: Relación entre admins y plantas
- **departamentos**: Departamentos por planta
- **puestos**: Puestos por departamento
- **empleados**: Empleados por puesto/departamento/planta

## 🛠️ Comandos de Gestión

```bash
# Limpiar todos los datos
python manage.py limpiar_datos

# Insertar datos de prueba
python manage.py insertar_datos

# Verificar datos y autenticación
python manage.py verificar_datos
```

## 🌐 URLs de Acceso

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000/api/
- **Admin Django**: http://localhost:8000/admin/

## 📋 Funcionalidades

### Dashboard SuperAdmin
- Gestión completa de empresas
- Registro de nuevas empresas
- Vista global del sistema

### Dashboard Admin Empresa
- Gestión de empleados de su empresa
- Gestión de estructura organizacional
- Vista de plantas y departamentos

### Dashboard Admin Planta
- Gestión de empleados de plantas asignadas
- Vista de departamentos de su planta

## 🔧 Solución de Problemas

### Error de Credenciales Inválidas
```bash
# Verificar datos de prueba
python manage.py verificar_datos

# Recrear datos si es necesario
python manage.py limpiar_datos
python manage.py insertar_datos
```

### Error de Base de Datos
```bash
# Recrear migraciones
python manage.py makemigrations
python manage.py migrate
```

### Error de CORS
Verificar que `CORS_ALLOWED_ORIGINS` en `settings/local.py` incluya el puerto del frontend.

## 📁 Estructura del Proyecto

```
Axyoma2/
├── Backend/                 # Django Backend
│   ├── apps/               # Aplicaciones Django
│   │   ├── users/         # Modelos de usuario
│   │   ├── management/    # Comandos personalizados
│   │   └── ...
│   ├── config/            # Configuración Django
│   └── requirements.txt   # Dependencias Python
├── frontend/              # React Frontend
│   ├── src/              # Código fuente React
│   │   ├── components/   # Componentes React
│   │   ├── services/     # Servicios API
│   │   └── ...
│   └── package.json      # Dependencias Node.js
├── setup_proyecto_completo.bat  # Configuración automática
├── start-backend.bat            # Iniciar backend
├── start-frontend.bat           # Iniciar frontend
└── README.md                    # Esta documentación
```

## 🤝 Contribución

1. Fork el proyecto
2. Crear rama feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit cambios (`git commit -am 'Agregar nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Crear Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE.md](LICENSE.md) para detalles.
