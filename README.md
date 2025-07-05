# Sistema Axyoma - Gestión Empresarial

Sistema web completo desarrollado con **Django (Backend)** y **React (Frontend)** para la gestión de empresas, plantas, departamentos y empleados con diferentes niveles de administración.

## 🚀 Para Nuevos Desarrolladores

### Instalación (Solo 2 pasos)

1. **Configuración automática:**
```bash
setup_proyecto_completo.bat
```

2. **Ejecutar el sistema:**
```bash
# Terminal 1 - Backend
start-backend.bat

# Terminal 2 - Frontend  
start-frontend.bat
```

**¡Eso es todo!** El sistema estará en http://localhost:3000

### Requisitos Previos
- **Python 3.8+** 
- **Node.js 14+**
- **PostgreSQL 12+**

## 👥 Usuarios de Prueba

| Email | Contraseña | Rol |
|-------|------------|-----|
| ed-rubio@axyoma.com | 1234 | Super Admin |
| juan.perez@codewave.com | 1234 | Admin Empresa |
| maria.gomez@codewave.com | 1234 | Admin Planta |

## ✨ Funcionalidades

- 🏢 **Registro de empresas** con administrador automático
- 📊 **Dashboards por rol** (SuperAdmin, Admin Empresa, Admin Planta)
- 🏭 **Gestión organizacional** (Plantas → Departamentos → Puestos → Empleados)
- 🔐 **Seguridad por empresa** (cada empresa solo ve sus datos)

## �️ Si algo falla

### Error de Base de Datos
```bash
cd Backend
python manage.py migrate
```

### Error de Dependencias
```bash
# Volver a ejecutar la configuración
setup_proyecto_completo.bat
```

## 📁 Estructura

```
Axyoma2/
├── Backend/          # Django API
├── frontend/         # React App
├── setup_proyecto_completo.bat  # ⭐ Configuración automática
├── start-backend.bat            # ⭐ Iniciar servidor
├── start-frontend.bat           # ⭐ Iniciar app
└── README.md                    # Esta documentación
```

## � Licencia

MIT License
