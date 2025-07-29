-- Respaldo generado por AXYOMA usando Django ORM
-- Fecha: 2025-07-28T21:57:25.463904
-- Usuario: admin


-- Datos de empresas
-- 19 registros
-- Tabla: empresas
-- Campos: ['empresa_id', 'nombre', 'rfc', 'direccion', 'logotipo', 'email_contacto', 'telefono_contacto', 'fecha_registro', 'status', 'administrador']

-- Datos de usuarios
-- 38 registros
-- Tabla: usuarios
-- Campos: ['id', 'nombre', 'apellido_paterno', 'apellido_materno', 'correo', 'fecha_registro', 'nivel_usuario', 'status', 'admin_empresa', 'user']

-- Datos de plantas
-- 25 registros
-- Tabla: plantas
-- Campos: ['planta_id', 'nombre', 'direccion', 'fecha_registro', 'status', 'empresa']

-- Datos de departamentos
-- 136 registros
-- Tabla: departamentos
-- Campos: ['departamento_id', 'nombre', 'descripcion', 'fecha_registro', 'status', 'planta']

-- Datos de puestos
-- 603 registros
-- Tabla: puestos
-- Campos: ['puesto_id', 'nombre', 'descripcion', 'status', 'departamento']

-- Datos de empleados
-- 27 registros
-- Tabla: empleados
-- Campos: ['empleado_id', 'nombre', 'apellido_paterno', 'apellido_materno', 'genero', 'antiguedad', 'status', 'puesto', 'departamento', 'planta']

-- Datos de planes_suscripcion
-- Error al procesar subscriptions.PlanSuscripcion: no existe la relación «planes_suscripcion»
LINE 1: SELECT 1 AS "a" FROM "planes_suscripcion" LIMIT 1
                             ^


-- Datos de suscripciones_empresa
-- Error al procesar subscriptions.SuscripcionEmpresa: transacción abortada, las órdenes serán ignoradas hasta el fin de bloque de transacción

-- Error al procesar evaluaciones.Evaluacion: App 'evaluaciones' doesn't have a 'Evaluacion' model.
-- Error al procesar surveys.Encuesta: App 'surveys' doesn't have a 'Encuesta' model.

-- Datos de admin_bd_logrespaldo
-- Error al procesar admin_bd.LogRespaldo: transacción abortada, las órdenes serán ignoradas hasta el fin de bloque de transacción


-- Datos de admin_bd_configuracionbd
-- Error al procesar admin_bd.ConfiguracionBD: transacción abortada, las órdenes serán ignoradas hasta el fin de bloque de transacción


-- Respaldo completado: 848 registros procesados
