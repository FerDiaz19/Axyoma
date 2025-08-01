# 📋 DOCUMENTACIÓN COMPLETA DEL SISTEMA AXYOMA

## 🚀 DATOS INICIALES OBLIGATORIOS

### 📦 **Planes de Suscripción (CRÍTICOS)**
Sin planes, el sistema NO funciona. Deben existir desde el inicio:

```sql
-- PLANES OBLIGATORIOS PARA EL SISTEMA
INSERT INTO subscriptions_plansuscripcion VALUES 
(1, 'Plan Básico', 'Funcionalidades básicas para empresas pequeñas', 299.99, 30, true, '2025-01-01 00:00:00'),
(2, 'Plan Estándar', 'Funcionalidades completas para empresas medianas', 599.99, 30, true, '2025-01-01 00:00:00'),
(3, 'Plan Empresarial', 'Todas las funcionalidades para empresas grandes', 999.99, 30, true, '2025-01-01 00:00:00'),
(4, 'Plan de Prueba', 'Plan gratuito por 7 días', 0.00, 7, true, '2025-01-01 00:00:00');
```

**¿Por qué son críticos?**
- El registro de empresas falla si no hay planes disponibles
- La selección de suscripciones no puede mostrar opciones
- Los usuarios no pueden completar el flujo de registro

---

## 🏢 FLUJO COMPLETO DE REGISTRO DE EMPRESA

### **Paso 1: Registro de Empresa**
Cuando un usuario se registra como empresa:

1. **Se crea automáticamente:**
   - ✅ Registro en tabla `Empresa`
   - ✅ Usuario administrador principal
   - ✅ **Planta Principal** (nombre: "Planta Principal")
   - ✅ **7 Departamentos básicos:**
     - Recursos Humanos
     - Finanzas
     - Operaciones
     - Ventas
     - Marketing
     - Tecnología
     - Administración
   - ✅ **15+ Puestos básicos** distribuidos en departamentos
   - ✅ Relación AdminPlanta (usuario → planta principal)

2. **Estructura automática creada:**
```
Empresa "Mi Empresa"
└── Planta Principal
    ├── Recursos Humanos
    │   ├── Director de RRHH
    │   ├── Especialista en RRHH
    │   └── Asistente de RRHH
    ├── Finanzas
    │   ├── Director Financiero
    │   ├── Contador
    │   └── Asistente Contable
    ├── Operaciones
    │   ├── Director de Operaciones
    │   ├── Supervisor de Producción
    │   └── Operario
    └── [5 departamentos más...]
```

### **Paso 2: Selección de Plan**
- El usuario DEBE seleccionar un plan de suscripción
- Se crea registro en `SuscripcionEmpresa` con `estado='activa'`
- Solo entonces puede acceder al dashboard principal

**IMPORTANTE:** El campo `estado` usa valores string, no boolean:
- `'activa'` - Suscripción funcionando
- `'vencida'` - Suscripción expirada
- `'cancelada'` - Suscripción cancelada

---

## 👥 TIPOS DE USUARIOS DEL SISTEMA

### **1. SuperAdmin (Super Usuario)**
- **Acceso:** Panel administrativo global
- **Funciones:**
  - Gestionar todas las empresas del sistema
  - Ver estadísticas globales
  - Crear/editar/suspender planes de suscripción
  - Gestionar usuarios de todas las empresas
  - Acceso a todas las plantas, departamentos y empleados
  - Exportar datos del sistema completo

### **2. Admin Empresa (Usuario Principal)**
- **Acceso:** Dashboard de su empresa
- **Funciones:**
  - Gestionar la estructura de su empresa
  - Crear/editar plantas de su empresa
  - Gestionar departamentos y puestos
  - Administrar empleados
  - Ver reportes de su empresa
  - Gestionar suscripción

### **3. Admin Planta**
- **Acceso:** Dashboard limitado a su planta
- **Funciones:**
  - Ver/gestionar empleados de su planta
  - Gestionar departamentos de su planta
  - Ver reportes de su planta específica
  - NO puede crear otras plantas

---

## 🔄 FLUJO DE DATOS CRÍTICOS

### **Relaciones de Datos:**
```
Empresa
└── SuscripcionEmpresa (estado='activa')
└── Planta(s)
    └── AdminPlanta → Usuario
    └── Departamento(s)
        └── Puesto(s)
            └── Empleado(s)
```

### **Validaciones Importantes:**
- ✅ Una empresa DEBE tener al menos una planta
- ✅ Una planta DEBE tener al menos un administrador
- ✅ Un departamento DEBE pertenecer a una planta
- ✅ Un puesto DEBE pertenecer a un departamento
- ✅ Un empleado DEBE tener un puesto asignado

---

## 🎯 DATOS DE PRUEBA RECOMENDADOS

### **Empresa de Prueba Completa:**
```sql
-- Empresa
INSERT INTO users_empresa VALUES 
(1, 'Axis Development', 'Empresa de desarrollo de software', 'contacto@axis.com', '555-0123', 'Av. Tecnología 123', '2025-01-01 00:00:00');

-- Usuario Admin Empresa
INSERT INTO auth_user VALUES 
(1, 'adminaxis', 'admin@axis.com', 'Admin', 'Axis', true, true, '2025-01-01 00:00:00');

-- Perfil Usuario
INSERT INTO users_perfilusuario VALUES 
(1, 1, 1, 'admin_empresa', '2025-01-01 00:00:00');

-- Suscripción Activa
INSERT INTO subscriptions_suscripcionempresa VALUES 
(1, 1, 2, '2025-01-01', '2025-02-01', 'activa', '2025-01-01 00:00:00');

-- Planta Principal
INSERT INTO users_planta VALUES 
(1, 'Planta Principal', 'Oficinas centrales', 'Centro', 1, true, '2025-01-01 00:00:00');

-- AdminPlanta
INSERT INTO users_adminplanta VALUES 
(1, 1, 1, true, '2025-01-01 00:00:00');
```

### **SuperAdmin de Prueba:**
```sql
-- SuperAdmin Usuario
INSERT INTO auth_user VALUES 
(2, 'superadmin', 'super@axyoma.com', 'Super', 'Admin', true, true, '2025-01-01 00:00:00');

-- Perfil SuperAdmin
INSERT INTO users_perfilusuario VALUES 
(2, 2, NULL, 'superadmin', '2025-01-01 00:00:00');
```

---

## 🗄️ COMANDOS SQL PARA RESPALDOS

### **Respaldo Completo del Sistema:**
```sql
-- TABLAS CRÍTICAS EN ORDEN DE DEPENDENCIA

-- 1. Usuarios base
SELECT * FROM auth_user;
SELECT * FROM users_empresa;
SELECT * FROM users_perfilusuario;

-- 2. Planes (CRÍTICO)
SELECT * FROM subscriptions_plansuscripcion;

-- 3. Suscripciones
SELECT * FROM subscriptions_suscripcionempresa;

-- 4. Estructura organizacional
SELECT * FROM users_planta;
SELECT * FROM users_adminplanta;
SELECT * FROM users_departamento;
SELECT * FROM users_puesto;
SELECT * FROM users_empleado;

-- 5. Pagos (opcional)
SELECT * FROM subscriptions_pago;
```

### **Respaldo Solo de Estructura (Sin usuarios):**
```sql
-- Para crear BD limpia con estructura básica
SELECT * FROM subscriptions_plansuscripcion;
-- + Estructura de departamentos y puestos por defecto
```

---

## ⚙️ CONFIGURACIONES IMPORTANTES

### **Variables de Entorno Necesarias:**
- `DEBUG=True` (desarrollo)
- `SECRET_KEY=tu_clave_secreta`
- `DATABASE_URL=postgres://...` (producción)

### **Configuración de CORS:**
```python
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",  # React frontend
    "http://127.0.0.1:3000",
]
```

### **Configuración de Base de Datos:**
- PostgreSQL recomendado para producción
- SQLite para desarrollo local
- Migraciones necesarias: `python manage.py makemigrations && python manage.py migrate`

---

## 🚨 PUNTOS CRÍTICOS DE FUNCIONAMIENTO

### **❌ El sistema NO funciona si:**
1. No existen planes de suscripción activos
2. No hay estructura de departamentos/puestos por defecto
3. El usuario no tiene suscripción activa
4. Las relaciones AdminPlanta están rotas
5. **CRÍTICO:** Constraint de `estado` en tabla suscripciones mal configurado

### **⚠️ Errores Conocidos y Soluciones:**

#### **Error: "violates check constraint suscripciones_estado_check"**
```sql
-- PROBLEMA: El campo 'estado' es CharField con opciones específicas
-- NO usar: estado=True (boolean)
-- SÍ usar: estado='activa' (string)

-- Valores válidos para estado:
-- 'activa'    - Suscripción funcionando
-- 'vencida'   - Suscripción expirada  
-- 'cancelada' - Suscripción cancelada

-- SOLUCIÓN CORREGIDA en código:
SuscripcionEmpresa.objects.create(
    empresa=empresa,
    plan=plan,
    fecha_inicio=fecha_inicio,
    fecha_fin=fecha_fin,
    estado='activa'  # ← CORRECTO
)
```

### **✅ Para funcionamiento óptimo:**
1. Siempre mantener al menos 3-4 planes activos
2. Crear estructura organizacional completa en cada registro
3. Validar suscripciones antes de acceso a funciones
4. Mantener respaldos de la estructura base
5. **Verificar constraints de BD** antes de insertar datos

---

## 📊 FLUJO DE PANTALLAS

### **Usuario Nuevo:**
1. **Landing Page** (`/`) → Información del sistema
2. **Registro** (`/registro`) → Crear empresa + usuario
3. **Selección Plan** (`/plan-selection`) → Elegir suscripción
4. **Dashboard** (`/dashboard`) → Panel principal

### **Usuario Existente:**
1. **Login** (`/login`) → Autenticación
2. **Dashboard** (`/dashboard`) → Según tipo de usuario

### **SuperAdmin:**
1. **Login** → Dashboard con opciones globales
2. **Gestión Empresas** → Ver/editar todas las empresas
3. **Estadísticas** → Métricas del sistema completo

---

## 🔐 CREDENCIALES DE PRUEBA

### **Empresa de Prueba:**
- **Usuario:** `adminaxis`
- **Password:** `admin123`
- **Empresa:** Axis Development
- **Tipo:** Admin Empresa

### **SuperAdmin:**
- **Usuario:** `superadmin`
- **Password:** `super123`
- **Tipo:** Super Administrador

---

## 📝 NOTAS IMPORTANTES

1. **Orden de creación:** Siempre crear planes → empresa → estructura → usuarios
2. **Respaldos:** Incluir todas las tablas relacionales para mantener integridad
3. **Testing:** Usar datos de prueba completos para validar flujos
4. **Producción:** Cambiar credenciales por defecto antes del deploy

---

## 💡 COMANDOS ÚTILES PARA DESARROLLO

### **Resetear BD Completa:**
```bash
# Backend
python resetear_bd_completo.py
python crear_datos_completos.py
```

### **Crear Solo Estructura:**
```bash
python create_initial_data.py
```

### **Ver Estado Actual:**
```bash
python mostrar_usuarios.py
python obtener_tablas.py
```

---

*Este documento es la guía completa para entender, configurar y mantener el sistema Axyoma. ¡Úsalo como referencia para respaldos y restauraciones!* 💪
