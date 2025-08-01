# 📋 Datos de Prueba - Axyoma

Esta carpeta contiene scripts especializados para cargar datos de prueba en el sistema Axyoma.

## 🎯 Scripts Disponibles

### `cargar_datos_completos.py`
Carga la estructura organizacional completa:
- ✅ **Superadmin**: Usuario administrador principal
- ✅ **2 Empresas**: TechCorp y InnovaSoft  
- ✅ **4 Plantas**: 2 por empresa
- ✅ **28 Departamentos**: Distribución realista
- ✅ **~100 Puestos**: Jerarquía organizacional completa
- ✅ **~200 Empleados**: Asignados a diferentes puestos y departamentos

### `cargar_evaluaciones_nom035.py`
Carga el framework de evaluaciones NOM-035:
- ✅ **Tipos de Evaluación**: Normativa e Interna
- ✅ **Evaluación NOM-035**: Con instrucciones oficiales
- ✅ **14 Secciones**: Todas las áreas de evaluación
- ✅ **Conjuntos de Respuestas**: Escalas y opciones booleanas

### `cargar_todo.py`
Script maestro que ejecuta todos los cargadores en secuencia automáticamente.

## 🚀 Uso Rápido

```powershell
# Cargar todo automáticamente
python datos_prueba/cargar_todo.py

# O cargar individualmente
python datos_prueba/cargar_datos_completos.py
python datos_prueba/cargar_evaluaciones_nom035.py
```

## ⚙️ Características

- **🔄 Transacciones Atómicas**: Si algo falla, todo se revierte
- **🧹 Limpieza Automática**: Elimina datos existentes antes de cargar
- **📊 Reportes Detallados**: Muestra progreso y resultados
- **⚠️ Manejo de Errores**: Rollback automático en caso de problemas
- **💾 Datos Realistas**: Nombres, emails y estructura empresarial verosímil

## 📝 Estructura de Datos

### Empresas y Plantas
```
TechCorp
├── Planta Norte (León, Gto)
└── Planta Sur (Guadalajara, Jal)

InnovaSoft  
├── Centro de Desarrollo (CDMX)
└── Oficina Regional (Monterrey, NL)
```

### Departamentos por Planta
- **Administración**: Finanzas, Recursos Humanos, Legal
- **Operaciones**: Producción, Calidad, Mantenimiento, Logística
- **Tecnología**: Desarrollo, Sistemas, Seguridad Informática
- **Comercial**: Ventas, Marketing, Atención al Cliente

### Puestos Jerárquicos
- **Directivos**: Director, Gerente General
- **Gerencias**: Gerente de área
- **Coordinación**: Coordinador, Supervisor
- **Especialistas**: Analista, Técnico, Especialista
- **Operativos**: Asistente, Auxiliar, Operador

## 🛡️ Seguridad

- **Usuario Superadmin**: `superadmin` / `admin123`
- **Empleados**: Passwords generados automáticamente
- **Transacciones Seguras**: Rollback automático si hay errores

## 📈 Escalabilidad

Los scripts están diseñados para:
- ✅ Ejecutarse múltiples veces sin duplicar datos
- ✅ Manejar grandes volúmenes de información
- ✅ Reportar progreso en tiempo real
- ✅ Facilitar debugging y troubleshooting

---

**💡 Tip**: Ejecuta `cargar_todo.py` para una experiencia completa, o usa los scripts individuales si necesitas cargar datos específicos.
