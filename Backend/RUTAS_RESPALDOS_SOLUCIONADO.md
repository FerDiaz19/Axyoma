# 📁 RUTAS ESTANDARIZADAS DE RESPALDOS - SOLUCIONADO

## 🎯 Problema Resuelto

El error "El sistema no puede encontrar el archivo especificado" se debía a diferencias en las rutas base entre diferentes equipos de desarrollo.

## ✅ Solución Implementada

### **Ruta Estándar Unificada**
Todos los respaldos se guardan ahora en:
```
[PROYECTO_BASE]/Backend/config/backups/
```

**En tu caso específico:**
```
C:\xampp2\htdocs\UTT4B\Axyoma2\Backend\config\backups\
```

**En otros equipos:**
```
[SU_RUTA_BASE]/Backend/config/backups/
```

### **Archivos Modificados**

1. **`Backend/apps/admin_bd/views_respaldos.py`**
   - Ruta: `BACKUP_DIR = os.path.join(settings.BASE_DIR, 'backups')`
   - Función: `get_backup_directory()` para crear directorios automáticamente

2. **`Backend/apps/admin_bd/utils/backup_manager.py`**
   - Ruta: `self.backup_dir = os.path.join(settings.BASE_DIR, 'backups')`

3. **`Backend/apps/admin_bd/views_simple.py`**
   - Ruta: `backup_dir = os.path.join(settings.BASE_DIR, 'backups')`

4. **`Backend/apps/admin_bd/models.py`**
   - Default: `directorio_respaldos = 'config/backups/'`

### **Usuario SuperAdmin Corregido**

- ✅ Usuario Django: `superadmin`
- ✅ Password: `1234`
- ✅ Email: `superadmin@axyoma.com`
- ✅ Nivel: `superadmin`
- ✅ Permisos: `staff=True, superuser=True`

## 🔧 Funcionalidades Verificadas

### **Backend**
- ✅ Directorio de respaldos se crea automáticamente
- ✅ Permisos de escritura correctos
- ✅ Configuración de BD funcionando
- ✅ Usuario SuperAdmin configurado
- ✅ Endpoint de verificación: `/api/admin-bd/respaldos/verificar/`

### **Frontend**
- ✅ Servicio de respaldos actualizado con mejor manejo de errores
- ✅ Componente `GestionRespaldos.tsx` funcional
- ✅ Información detallada de errores para debugging

## 📋 Endpoints Disponibles

```
GET  /api/admin-bd/respaldos/verificar/     - Verificar sistema
POST /api/admin-bd/respaldos/bd-completa/   - Respaldo completo
POST /api/admin-bd/respaldos/tablas/        - Respaldo de tablas
GET  /api/admin-bd/respaldos/listar/        - Listar respaldos
POST /api/admin-bd/respaldos/restaurar/     - Restaurar respaldo
GET  /api/admin-bd/respaldos/info/          - Info del sistema
```

## 🧪 Scripts de Verificación

1. **`Backend/verificar_rutas_simple.py`** - Verificar rutas y directorios
2. **`Backend/probar_django_respaldos.py`** - Probar funcionalidad completa
3. **`Backend/verificar_usuarios.py`** - Listar usuarios del sistema
4. **`Backend/corregir_superadmin.py`** - Configurar usuario superadmin

## 🏆 Para Otros Equipos

### **Configuración Automática**
Ejecutar en el Backend:
```bash
python verificar_rutas_simple.py
python probar_django_respaldos.py
```

### **Si Falta SuperAdmin**
```bash
python corregir_superadmin.py
```

### **Credenciales de Prueba**
- Usuario: `superadmin`
- Password: `1234`
- URL Frontend: `http://localhost:3000`
- URL Backend: `http://localhost:8000`

## 📁 Estructura de Archivos de Respaldo

```
Backend/config/backups/
├── backup_completo_20250729_HHMMSS.sql
├── backup_completo_20250729_HHMMSS_metadata.json
├── backup_tablas_HHMMSS.sql
└── backup_tablas_HHMMSS_metadata.json
```

## ✅ Estado Final

**PROBLEMA RESUELTO** - El sistema de respaldos funcionará en cualquier equipo usando rutas relativas estandarizadas.

**Última verificación:** 29 Julio 2025
**Directorio verificado:** `C:\xampp2\htdocs\UTT4B\Axyoma2\Backend\config\backups`
**Usuario configurado:** `superadmin` / `1234`
**Sistema:** ✅ FUNCIONANDO
