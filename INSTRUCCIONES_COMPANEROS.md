# 🔧 INSTRUCCIONES PARA COMPAÑEROS - SISTEMA DE RESPALDOS

## 🎯 Problema Solucionado
El error "archivo especificado no encontrado" se debía a diferencias en nombres de directorios:
- **Tu equipo:** `Axyoma2`
- **Otros equipos:** `axyoma`

## ✅ Solución Universal Implementada

El sistema ahora funciona **automáticamente** independientemente del nombre del directorio del proyecto.

## 🚀 PASOS PARA COMPAÑEROS

### 1️⃣ Configuración Automática (SOLO UNA VEZ)
En el directorio Backend, ejecutar:
```bash
cd Backend
python configurar_para_companeros.py
```

Este script:
- ✅ Detecta automáticamente el nombre del proyecto (`axyoma`, `Axyoma2`, etc.)
- ✅ Crea el directorio `Backend/config/backups/`
- ✅ Configura el usuario `superadmin` / `1234`
- ✅ Verifica permisos y funcionamiento
- ✅ Confirma que todo esté listo

### 2️⃣ Verificación (Opcional)
Para confirmar que todo funciona:
```bash
python verificar_rutas_universales.py
```

## 📁 Estructura Universal
El sistema ahora usa **rutas relativas** que funcionan en cualquier equipo:

```
[CUALQUIER_NOMBRE_PROYECTO]/
├── Backend/
│   ├── config/
│   │   ├── backups/          ← Respaldos aquí (se crea automáticamente)
│   │   │   ├── backup_completo_*.sql
│   │   │   ├── backup_completo_*_metadata.json
│   │   │   └── configuracion_completada.txt
│   │   └── settings/
│   ├── apps/
│   └── manage.py
└── frontend/
```

## 🔑 Credenciales
- **Usuario:** `superadmin`
- **Password:** `1234`
- **Nivel:** SuperAdmin (acceso completo a respaldos)

## 🌐 URLs
- **Frontend:** http://localhost:3000
- **Backend:** http://localhost:8000
- **Respaldos:** SuperAdmin Dashboard → Gestión de BD → Respaldos

## 🧪 Pruebas
1. **Login:** Usar `superadmin` / `1234`
2. **Crear respaldo:** Ir a SuperAdmin → Gestión BD → Crear respaldo completo
3. **Verificar archivo:** Debe aparecer en `Backend/config/backups/`

## ❗ Si Hay Problemas

### Error de usuario SuperAdmin:
```bash
python corregir_superadmin.py
```

### Error de rutas:
```bash
python verificar_rutas_universales.py
```

### Error de permisos:
Verificar que el directorio `Backend/config/backups/` tenga permisos de escritura.

## 🎉 Confirmación
Si el script `configurar_para_companeros.py` termina con:
```
✅ EL SISTEMA ESTÁ LISTO PARA USAR
```

**El sistema de respaldos funcionará correctamente** sin importar el nombre del directorio del proyecto.

## 📧 En Caso de Dudas
Si persisten problemas, enviar:
1. Salida del comando `python verificar_rutas_universales.py`
2. Nombre del directorio del proyecto
3. Sistema operativo

---
**Actualizado:** 29 Julio 2025  
**Estado:** ✅ FUNCIONANDO UNIVERSALMENTE
