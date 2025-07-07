# 🏭 AXYOMA - Sistema de Gestión de Empleados

Sistema completo de gestión de empleados con arquitectura de suscripciones para empresas industriales.

## � Requisitos del Sistema

### Obligatorios
- **Python 3.8+** (con pip)
- **Node.js 16+** (con npm)
- **PostgreSQL 12+** (usuario: postgres, password: 123456789)

### Verificar Instalación
```bash
python --version    # o py --version
node --version
npm --version
psql --version
```

## �🚀 Inicio Rápido

### Para Usuarios
```bash
# Iniciar sistema completo
start_system.bat
```

### Para Nuevos Desarrolladores
```bash
# Setup completo (primera vez)
setup_project.bat

# Después usar
start_system.bat
```

📖 **Guía completa**: Ver [DEVELOPER_GUIDE.md](DEVELOPER_GUIDE.md)

## 🏗️ Arquitectura

- **Backend**: Django + PostgreSQL
- **Frontend**: React + TypeScript
- **Autenticación**: Token-based
- **Suscripciones**: Sistema automatizado de pagos
- **Base de Datos**: PostgreSQL (axyomadb)

## 👥 Tipos de Usuario

### 🔧 SuperAdmin
- Gestión de planes de suscripción
- Vista global de todas las empresas
- Control de estados de suscripción
- Administración del sistema

### 🏢 Admin Empresa  
- Gestión de plantas propias
- Gestión de empleados
- Control de suscripción (debe pagar para activar)
- Reportes y estadísticas

### 🏭 Admin Planta
- Gestión de empleados de su planta
- **Depende de la suscripción de la empresa**
- No requiere suscripción propia

## 💳 Sistema de Suscripciones

### Planes Base (configurables por SuperAdmin)
- **Plan Básico**: 1 mes - $299 MXN
- **Plan Profesional**: 3 meses - $799 MXN  
- **Plan Anual**: 1 año - $2,999 MXN

### Flujo Automático
1. **Sin suscripción** → Empresa suspendida
2. **Crear suscripción** → Estado: pendiente_pago
3. **Pagar** → Estado: activa (automático)
4. **Vencimiento** → Estado: vencida (automático)

### Reglas de Negocio
- ✅ **Una suscripción activa por empresa**
- ✅ **Admin Planta hereda estado de la empresa**
- ✅ **Activación automática tras pago**
- ✅ **SuperAdmin ve tiempo restante de todas las empresas**

## 🗂️ Estructura del Proyecto

```
Axyoma2/
├── Backend/                 # API Django
│   ├── apps/               # Aplicaciones principales
│   │   ├── users/         # Gestión de usuarios
│   │   ├── subscriptions/ # Sistema de suscripciones
│   │   ├── views.py       # Endpoints principales
│   │   └── mock_storage.py # Datos simulados
│   ├── config/            # Configuración Django
│   └── manage.py
├── frontend/              # Aplicación React
│   ├── src/
│   │   ├── components/    # Componentes React
│   │   ├── services/      # Servicios API
│   │   └── css/          # Estilos
│   └── package.json
├── AxyomaDB.sql          # Esquema de base de datos
├── setup_project.bat     # Setup para desarrolladores
├── start_system.bat      # Iniciar sistema completo
├── start_backend.bat     # Solo backend
└── start_frontend.bat    # Solo frontend
```

## 📊 Estado de Implementación

### ✅ Completado (85%)
- [x] Sistema de autenticación
- [x] Gestión de usuarios (SuperAdmin, Admin Empresa, Admin Planta)
- [x] Sistema de suscripciones completo
- [x] Flujo automático de pagos
- [x] Dashboards diferenciados por rol
- [x] Sistema de plantas y departamentos
- [x] Gestión básica de empleados
- [x] Estados de suscripción en tiempo real
- [x] Mock storage para desarrollo

### 🔄 En Desarrollo (10%)
- [ ] Módulo de evaluaciones
- [ ] Reportes avanzados
- [ ] Integración con DB PostgreSQL

### 📋 Pendiente (5%)
- [ ] Notificaciones por email
- [ ] Exportación de reportes
- [ ] Dashboard de métricas avanzadas

## 🧪 Testing

El sistema incluye datos mock para desarrollo y testing sin necesidad de configurar base de datos.

### Usuarios de Prueba
- **SuperAdmin**: `superadmin` / `admin123`
- **Admin Empresa**: `admin` / `admin123`
- **Admin Planta**: `planta1` / `admin123`

## 📝 Notas de Desarrollo

- Los admin planta **NO** requieren suscripción propia
- El sistema garantiza **una sola suscripción activa por empresa**
- Los estados se actualizan automáticamente tras pagos
- El SuperAdmin puede ver el tiempo restante de cada empresa
- Los datos se persisten en `Backend/apps/mock_data.json`

---

**Desarrollado para UTT4B - Sistema de gestión empresarial con suscripciones**
