# 🏢 SISTEMA AXYOMA - GESTIÓN DE BASE DE DATOS

## 📋 Descripción

Sistema completo de gestión empresarial con funcionalidades avanzadas de base de datos:
- ✅ Respaldos completos y parciales
- ✅ Restauración de datos
- ✅ Exportación a CSV
- ✅ Gestión de usuarios y roles
- ✅ Estructura organizacional completa
- ✅ Reseteo y reinicialización

## 🚀 Instalación y Configuración

### 1. Instalación Automática
```bash
# Ejecutar el script principal
.\exportar_bd_axyoma.bat
```

### 2. Instalación Manual
```bash
# 1. Activar entorno virtual
cd Backend
.\env\Scripts\activate.bat

# 2. Aplicar migraciones
python manage.py migrate

# 3. Crear usuarios y datos
python crear_superadmin.py
python crear_usuarios_prueba.py
python crear_datos_completos.py
```

## 🔑 Credenciales de Acceso

| Usuario | Contraseña | Nivel | Descripción |
|---------|------------|-------|-------------|
| `superadmin` | `1234` | SuperAdmin | Acceso completo al sistema |
| `admin_empresa` | `admin123` | Admin Empresa | Gestión de empresa |
| `admin_planta` | `admin123` | Admin Planta | Gestión de planta específica |

## 🌐 URLs del Sistema

- **Frontend:** http://localhost:3000
- **Backend API:** http://localhost:8000/api/
- **Admin Django:** http://localhost:8000/admin/

## 🛠️ Scripts Disponibles

### 📋 Menú Principal
```bash
cd Backend
python menu_maestro.py
```

### 🔧 Scripts Individuales

#### Gestión de Usuarios
- `crear_superadmin.py` - Crear/corregir superadmin
- `crear_usuarios_prueba.py` - Crear usuarios de prueba
- `corregir_password_superadmin.py` - Corregir contraseña superadmin

#### Gestión de Datos
- `crear_datos_completos.py` - Crear estructura empresarial completa
- `inicializar_sistema_completo.py` - Proceso completo de inicialización
- `resetear_bd_completo.py` - ⚠️ RESETEO COMPLETO (borra todo)

#### Respaldos y Exportación
- `sistema_respaldos.py` - Sistema de respaldos completos/parciales
- `exportar_csv.py` - Exportar datos a CSV
- `verificar_enlaces_empleados.py` - Verificar integridad de datos

## 💾 Sistema de Respaldos

### Respaldo Completo
```bash
python sistema_respaldos.py
# Opción 1: Crear respaldo completo
```

### Respaldo Parcial
```bash
python sistema_respaldos.py
# Opción 2: Seleccionar tablas específicas
```

### Restauración
```bash
# Usando psql
psql -U postgres -d axyoma_bd < backups/respaldo_completo_YYYYMMDD_HHMMSS.sql

# O usando pgAdmin
# 1. Abrir pgAdmin
# 2. Click derecho en base de datos
# 3. Restore > Seleccionar archivo .sql
```

## 📊 Exportación a CSV

### Exportaciones Disponibles
1. **Empleados completos** - Todos los empleados con estructura organizacional
2. **Estructura organizacional** - Empresas, plantas, departamentos, puestos
3. **Empresas** - Información completa de empresas
4. **Resumen estadístico** - Estadísticas por planta y departamento

### Ejecutar Exportaciones
```bash
python exportar_csv.py
```

## 🏢 Estructura de Datos Creada

### Empresa: TechnoMex Industries
```
🏢 TechnoMex Industries
├── 🏭 Planta Querétaro Centro
│   ├── 📋 Recursos Humanos (5 puestos, ~35 empleados)
│   ├── 📋 Producción (5 puestos, ~65 empleados)
│   ├── 📋 Mantenimiento (4 puestos, ~24 empleados)
│   ├── 📋 Calidad (3 puestos, ~18 empleados)
│   ├── 📋 Almacén (3 puestos, ~21 empleados)
│   ├── 📋 Administración (4 puestos, ~20 empleados)
│   └── 📋 Sistemas (3 puestos, ~18 empleados)
├── 🏭 Planta El Marqués
│   └── [Misma estructura]
└── 🏭 Planta San Juan del Río
    └── [Misma estructura]
```

### Total: 138+ empleados distribuidos realísticamente

## 🔄 Operaciones de Base de Datos

### 4. Respaldo Completo
- Genera archivo SQL con toda la estructura y datos
- Incluye metadatos de respaldo
- Ubicación: `backups/respaldo_completo_YYYYMMDD_HHMMSS.sql`

### 5. Respaldo Parcial
- Selección de tablas específicas
- Útil para respaldos temáticos
- Ejemplos: solo empleados, solo estructura organizacional

### 6. Restaurar al Estado Inicial
```bash
python resetear_bd_completo.py
```
⚠️ **PELIGRO:** Elimina TODOS los datos

### 7. Restaurar Respaldo Parcial
```bash
# Restaurar tablas específicas
psql -U postgres -d axyoma_bd < backups/respaldo_parcial_empleados_YYYYMMDD_HHMMSS.sql
```

### 8. Exportar a CSV
Exportación de cualquier tabla a formato CSV para análisis externo

### 9. Usuarios y Roles de BD

#### Usuarios de PostgreSQL (configurar según necesidad):
1. **postgres** (superusuario)
2. **axyoma_admin** (administrador de aplicación)
3. **axyoma_read** (solo lectura)

#### Roles sugeridos:
1. **db_admin** - Administración completa
2. **db_app_user** - Operaciones de aplicación
3. **db_readonly** - Solo consultas

### 10. Reindexado (Opcional)
```sql
-- Reindexar toda la base de datos
REINDEX DATABASE axyoma_bd;

-- Reindexar tabla específica
REINDEX TABLE empleados;
```

## 📁 Estructura de Archivos

```
Backend/
├── menu_maestro.py                    # 🎯 MENÚ PRINCIPAL
├── inicializar_sistema_completo.py    # 🚀 Inicialización completa
├── resetear_bd_completo.py           # 🧹 Reseteo completo
├── sistema_respaldos.py              # 💾 Sistema de respaldos
├── exportar_csv.py                   # 📊 Exportación CSV
├── crear_superadmin.py               # 👑 Crear superadmin
├── crear_usuarios_prueba.py          # 👥 Usuarios de prueba
├── crear_datos_completos.py          # 🏢 Datos empresariales
├── verificar_enlaces_empleados.py    # 🔍 Verificar integridad
└── corregir_password_superadmin.py   # 🔧 Corregir contraseñas

../backups/                           # 📁 Respaldos
├── respaldo_completo_*.sql
├── respaldo_parcial_*.sql
└── *_metadata.json

./                                    # 📁 Exportaciones CSV
├── export_empleados_*.csv
├── export_estructura_*.csv
├── export_empresas_*.csv
└── export_resumen_estadistico_*.csv
```

## 🚨 Comandos de Emergencia

### Resetear Solo Contraseñas
```bash
python corregir_password_superadmin.py
```

### Verificar Estado del Sistema
```bash
python verificar_enlaces_empleados.py
```

### Acceso Directo a Base de Datos
```bash
# PostgreSQL
psql -U postgres -d axyoma_bd

# Ver tablas
\dt

# Ver empleados
SELECT e.nombre, p.nombre as puesto, d.nombre as departamento 
FROM empleados e 
JOIN puestos p ON e.puesto_id = p.puesto_id 
JOIN departamentos d ON p.departamento = d.departamento_id 
LIMIT 10;
```

## 📞 Soporte y Documentación

- **Logs del sistema:** Revisar consola de Django
- **Errores de BD:** Verificar conexión PostgreSQL
- **Frontend:** Verificar que el servidor React esté corriendo
- **Backend:** Verificar que Django esté corriendo en puerto 8000

## 🎯 Funcionalidades del Proyecto

✅ **11. Funcionalidad completa** - Sistema empresarial real con:
- Gestión de empleados multi-nivel
- Estructura organizacional completa
- Evaluaciones y asignaciones
- Sistema de usuarios y permisos
- Gestión de suscripciones
- API REST completa
- Frontend React funcional
