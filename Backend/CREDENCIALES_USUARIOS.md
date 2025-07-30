# 🔑 CREDENCIALES DEL SISTEMA AXYOMA

## 🎯 USUARIOS PRINCIPALES

### 🔥 SUPERADMIN (Acceso Total)
- **Usuario:** `superadmin`
- **Contraseña:** `1234`
- **Nivel:** SuperAdmin
- **Puede:** Todo (resetear BD, cargar datos, respaldos, etc.)

### 🏢 ADMIN EMPRESA 
- **Usuario:** `admin_empresa`
- **Contraseña:** `1234`
- **Nivel:** Admin Empresa
- **Puede:** Gestionar su empresa y todas sus plantas

### 🏭 ADMIN PLANTA
- **Usuario:** `admin_planta`  
- **Contraseña:** `1234`
- **Nivel:** Admin Planta
- **Puede:** Gestionar solo su planta asignada

## 👥 EMPLEADOS (Si existen)
- **Patrón de contraseñas:** `empleado123`
- **Nombres:** Depende de los datos cargados
- **Ejemplos:**
  - sergio.perez / empleado123
  - maria.martinez / empleado123
  - francisco.romero / empleado123

## 🌐 ACCESO AL SISTEMA

### URLs Importantes:
- **Panel Admin:** http://127.0.0.1:8000/admin/
- **API Root:** http://127.0.0.1:8000/api/
- **Login API:** http://127.0.0.1:8000/api/auth/login/

### 🔥 RECOMENDACIÓN:
**USA SIEMPRE:** `superadmin` / `1234`

Este usuario tiene acceso a TODO:
- ✅ Panel de administración completo
- ✅ Botones para resetear BD
- ✅ Botones para cargar datos
- ✅ Sistema de respaldos
- ✅ Exportaciones CSV
- ✅ Gestión de todos los usuarios

## 🛠️ SI OLVIDAS CONTRASEÑAS:

1. **Ejecuta:** `python corregir_password_superadmin.py`
2. **O resetea todo:** Botón "Resetear BD" en admin
3. **O carga datos:** Botón "Cargar Datos" en admin

---
🎉 **¡Con superadmin/1234 puedes hacer TODO!**
