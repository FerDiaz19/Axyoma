# 🛠️ GUÍA PARA NUEVOS DESARROLLADORES

## 🚀 Setup Rápido

### 1. Requisitos Previos
- **Python 3.8+** (para el backend Django)
- **Node.js 16+** (para el frontend React)
- **Git** (para clonar el proyecto)

### 2. Instalación Automática
```bash
# Clonar el proyecto
git clone [repo-url]
cd Axyoma2

# Ejecutar setup automático
setup_project.bat
```

### 3. Iniciar Sistema
```bash
# Opción 1: Sistema completo (recomendado)
start_system.bat

# Opción 2: Servidores por separado
start_backend.bat    # Solo Django en puerto 8000
start_frontend.bat   # Solo React en puerto 3000
```

## 📁 Estructura del Proyecto

```
Axyoma2/
├── 📁 Backend/                 # API Django REST
│   ├── 📁 apps/               # Apps principales
│   │   ├── 📁 users/         # Gestión de usuarios
│   │   ├── 📁 subscriptions/ # Sistema de suscripciones
│   │   ├── 📄 views.py       # Endpoints principales
│   │   └── 📄 mock_storage.py # Sistema de datos mock
│   ├── 📁 config/            # Configuración Django
│   ├── 📄 manage.py          # CLI de Django
│   └── 📄 requirements.txt   # Dependencias Python
├── 📁 frontend/               # App React + TypeScript
│   ├── 📁 src/
│   │   ├── 📁 components/    # Componentes React
│   │   ├── 📁 services/      # Servicios API
│   │   └── 📁 css/          # Estilos
│   ├── 📄 package.json      # Dependencias Node
│   └── 📄 tsconfig.json     # Config TypeScript
├── 📄 AxyomaDB.sql          # Esquema base de datos
├── 📄 setup_project.bat     # Setup automático
├── 📄 start_system.bat      # Iniciar sistema completo
├── 📄 start_backend.bat     # Solo backend
└── 📄 start_frontend.bat    # Solo frontend
```

## 👥 Usuarios de Prueba

| Rol | Usuario | Contraseña | Dashboard |
|-----|---------|------------|-----------|
| SuperAdmin | `superadmin` | `admin123` | Control total del sistema |
| Admin Empresa | `admin` | `admin123` | Gestión de empresa y plantas |
| Admin Planta | `planta1` | `admin123` | Gestión de empleados de planta |

## 🔧 Desarrollo

### Backend (Django)
```bash
cd Backend
python manage.py runserver    # http://localhost:8000
```

**Endpoints principales:**
- `/api/auth/login/` - Autenticación
- `/api/suscripciones/` - Gestión de suscripciones
- `/api/empresas/` - Gestión de empresas
- `/api/empleados/` - Gestión de empleados

### Frontend (React)
```bash
cd frontend
npm start                     # http://localhost:3000
```

**Rutas principales:**
- `/login` - Página de login
- `/superadmin` - Dashboard SuperAdmin
- `/empresa-admin` - Dashboard Admin Empresa
- `/planta-admin` - Dashboard Admin Planta
- `/plan-selection` - Selección de planes

## 💾 Sistema de Datos

### Modo Desarrollo (Mock)
- Los datos se almacenan en `Backend/apps/mock_data.json`
- No requiere configurar PostgreSQL
- Perfecto para desarrollo y testing

### Modo Producción (PostgreSQL)
- Configurar DB en `Backend/config/settings/local.py`
- Ejecutar migraciones: `python manage.py migrate`
- Cargar datos iniciales con fixtures

## 🧪 Testing

### Datos de Prueba Incluidos
- ✅ 3 planes base de suscripción
- ✅ Empresas con diferentes estados
- ✅ Usuarios con roles diferenciados
- ✅ Plantas y empleados de muestra

### Flujo de Testing
1. Login con cualquier usuario de prueba
2. Navegar por el dashboard correspondiente
3. Probar creación/edición de entidades
4. Verificar flujo de suscripciones (Admin Empresa)
5. Probar gestión completa (SuperAdmin)

## 🚨 Solución de Problemas

### Error: "Module not found"
```bash
# Frontend
cd frontend
npm install

# Backend  
cd Backend
pip install -r requirements.txt
```

### Error: "Port already in use"
- Backend: Cambiar puerto en `python manage.py runserver 8001`
- Frontend: Se abrirá automáticamente en otro puerto

### Error: "API connection failed"
- Verificar que el backend esté corriendo en puerto 8000
- Revisar configuración en `frontend/src/api.ts`

## 📝 Notas Importantes

- **Una suscripción activa por empresa** (regla de negocio)
- **Admin Planta hereda estado de la empresa** (no requiere suscripción propia)
- **Flujo automático**: crear suscripción → pagar → activar
- **SuperAdmin ve tiempo restante** de todas las empresas
- **Estados automáticos** tras pagos y vencimientos

## 🤝 Contribución

1. Fork del proyecto
2. Crear rama: `git checkout -b feature/nueva-funcionalidad`
3. Commit: `git commit -am 'Agregar nueva funcionalidad'`
4. Push: `git push origin feature/nueva-funcionalidad`
5. Pull Request

---
**¿Problemas con el setup? Revisa que tengas Python 3.8+ y Node.js 16+ instalados correctamente.**
