# 🛠️ GUÍA PARA DESARROLLADORES - AXYOMA

## 🚀 Setup Inicial (Solo la primera vez)

### 1. Requisitos del Sistema
```bash
# Verificar que estén instalados:
python --version    # Python 3.8+
node --version      # Node.js 16+
psql --version      # PostgreSQL 12+
```

### 2. Setup Automático
```bash
# Ejecutar una sola vez:
setup_project.bat
```

### 3. Configurar PostgreSQL
1. Crear base de datos: `axyomadb`
2. Usuario: `postgres`
3. Password: `123456789`
4. Puerto: `5432`

## 🏃‍♂️ Desarrollo Diario

### Iniciar Sistema Completo
```bash
start.bat
```

Esto automáticamente:
- ✅ Verifica requisitos
- ✅ Activa entorno virtual Python
- ✅ Ejecuta migraciones
- ✅ Crea planes básicos
- ✅ Configura usuarios originales
- ✅ Verifica sistema PostgreSQL
- ✅ Inicia Backend (puerto 8000)
- ✅ Inicia Frontend (puerto 3000)

## 🏗️ Arquitectura PostgreSQL

### Modelos Principales
```
apps/users/models.py:
├── PerfilUsuario (usuarios)
├── Empresa (empresas)  
├── Planta (plantas)
├── Departamento (departamentos)
├── Puesto (puestos)
└── Empleado (empleados)

apps/subscriptions/models.py:
├── PlanSuscripcion (planes_suscripcion)
├── SuscripcionEmpresa (suscripcion_empresa)
└── Pago (pagos)
```

### APIs REST Disponibles
```
/api/auth/              # Login y autenticación
/api/empresas/          # CRUD empresas
/api/plantas/           # CRUD plantas
/api/empleados/         # CRUD empleados
/api/suscripciones/     # Sistema de suscripciones (legacy)
/api/subscriptions/     # Sistema de suscripciones (PostgreSQL)
```

## 🔄 Flujo de Suscripciones PostgreSQL

### 1. Planes Base (Auto-creados)
- **Plan Mensual**: $299.00 (30 días)
- **Plan Trimestral**: $799.00 (90 días)  
- **Plan Anual**: $2999.00 (365 días)

### 2. Lógica de Negocio
```python
# Una sola suscripción activa por empresa
empresa.tiene_suscripcion_activa  # Property
empresa.dias_restantes_suscripcion  # Property
empresa.estado_suscripcion  # Property

# Estados automáticos
suscripcion.esta_activa  # Verifica fechas y estado
suscripcion.esta_por_vencer  # 7 días o menos
suscripcion.dias_restantes  # Cálculo automático
```

### 3. Gestión de Pagos
```python
# Crear pago automáticamente activa suscripción
pago = Pago.objects.create(
    suscripcion=suscripcion,
    monto_pago=plan.precio,
    estado_pago='Completado'
)
```

## 👥 Usuarios por Defecto

```
SuperAdmin:     ed-rubio@axyoma.com / 1234
Admin Empresa:  juan.perez@codewave.com / 1234  
Admin Planta:   maria.gomez@codewave.com / 1234
```

## 🧪 Testing y Verificación

### Verificar Sistema
```bash
cd Backend
python verificacion_final_postgresql.py
```

### Testing Manual de APIs
```bash
# Login
POST /api/auth/login/
{"username": "ed-rubio@axyoma.com", "password": "1234"}

# Listar planes
GET /api/subscriptions/planes/

# Crear suscripción
POST /api/subscriptions/crear_suscripcion/
{"empresa_id": 1, "plan_id": 1}

# Procesar pago
POST /api/suscripciones/procesar_pago/
{"suscripcion_id": 1, "monto_pago": 299.00}
```

## 🛠️ Comandos de Desarrollo

### Backend (Django)
```bash
cd Backend
call env\Scripts\activate.bat

# Migraciones
python manage.py makemigrations
python manage.py migrate

# Crear superusuario
python manage.py createsuperuser

# Shell Django
python manage.py shell

# Servidor
python manage.py runserver
```

### Frontend (React)
```bash
cd frontend

# Instalar dependencias
npm install

# Desarrollo
npm start

# Build producción
npm run build
```

## 📁 Estructura de Archivos Esenciales

```
Axyoma2/
├── start.bat                           # ⭐ Script principal
├── setup_project.bat                   # ⭐ Setup inicial
├── cleanup.bat                         # Limpieza opcional
├── README.md                           # Documentación
├── DEVELOPER_GUIDE.md                  # Esta guía
├── Backend/
│   ├── manage.py                       # ⭐ Django management
│   ├── create_base_plans.py            # ⭐ Crear planes básicos
│   ├── verificacion_final_postgresql.py # ⭐ Verificación
│   ├── requirements.txt                # Dependencias Python
│   ├── config/settings/                # Configuración Django
│   ├── apps/
│   │   ├── views.py                    # ⭐ APIs principales
│   │   ├── urls.py                     # URLs
│   │   ├── users/models.py             # ⭐ Modelos usuarios
│   │   └── subscriptions/
│   │       ├── models.py               # ⭐ Modelos suscripciones
│   │       └── views.py                # ⭐ APIs PostgreSQL
│   └── env/                            # Entorno virtual
└── frontend/
    ├── package.json                    # Dependencias Node
    ├── src/
    │   ├── components/                 # Componentes React
    │   ├── services/                   # Servicios API
    │   └── routes.tsx                  # Rutas
    └── build/                          # Build producción
```

## ❌ Lo que YA NO se usa

- ❌ `mock_storage.py` (eliminado)
- ❌ `mock_data.json` (eliminado)
- ❌ SQLite (nunca se usa)
- ❌ `start_system.bat` (usar `start.bat`)
- ❌ Scripts de testing viejos

## 🔧 Solución de Problemas

### Error: "No module named 'psycopg2'"
```bash
pip install psycopg2-binary
```

### Error: "database does not exist"
```sql
-- En PostgreSQL:
CREATE DATABASE axyomadb;
```

### Error: Frontend no inicia
```bash
cd frontend
npm install
npm start
```

### Limpiar sistema completamente
```bash
cleanup.bat
setup_project.bat
start.bat
```

---

## 📝 Notas de Desarrollo

- **Una sola suscripción activa por empresa** (constraint en modelo)
- **Pagos automáticamente activan suscripciones**
- **Estados calculados dinámicamente** (properties en modelos)
- **Migraciones automáticas** en cada inicio
- **Sistema 100% PostgreSQL** (sin dependencias mock)

**¡El sistema está listo para desarrollo productivo!** 🚀