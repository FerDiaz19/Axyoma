import api from '../api';

// Interfaces para SuperAdmin
export interface SuperAdminEmpresa {
  empresa_id: number;
  nombre: string;
  rfc: string;
  telefono?: string;
  correo?: string;
  direccion?: string;
  fecha_registro: string;
  status: boolean;
  administrador?: {
    id: number;
    username: string;
    email: string;
    nombre_completo: string;
    activo: boolean;
  };
  plantas_count: number;
  empleados_count: number;
}

export interface SuperAdminUsuario {
  user_id: number;
  profile_id: number;
  username: string;
  email: string;
  nombre_completo: string;
  correo: string;
  nivel_usuario: string;
  fecha_registro: string;
  ultimo_login?: string;
  is_active: boolean;
  empresa?: {
    id: number;
    nombre: string;
    status: boolean;
  };
  planta?: {
    id: number;
    nombre: string;
    empresa_nombre: string;
    status: boolean;
  };
}

export interface SuperAdminPlanta {
  planta_id: number;
  nombre: string;
  empresa_id: number;
  empresa_nombre: string;
  telefono?: string;
  correo?: string;
  direccion?: string;
  fecha_registro: string;
  status: boolean;
  username?: string;
  empleados_count: number;
  departamentos_count: number;
}

export interface SuperAdminDepartamento {
  departamento_id: number;
  nombre: string;
  planta_id: number;
  planta_nombre: string;
  empresa_id: number;
  empresa_nombre: string;
  fecha_registro: string;
  status: boolean;
  empleados_count: number;
  puestos_count: number;
}

export interface SuperAdminPuesto {
  puesto_id: number;
  nombre: string;
  descripcion?: string;
  departamento_id: number;
  departamento_nombre: string;
  planta_id: number;
  planta_nombre: string;
  empresa_id: number;
  empresa_nombre: string;
  fecha_registro: string;
  status: boolean;
  empleados_count: number;
}

export interface SuperAdminEmpleado {
  empleado_id: number;
  numero_empleado: string;
  nombre: string;
  apellido: string;
  email?: string;
  telefono?: string;
  puesto_id: number;
  puesto_nombre: string;
  departamento_id: number;
  departamento_nombre: string;
  planta_id: number;
  planta_nombre: string;
  empresa_id: number;
  empresa_nombre: string;
  fecha_registro: string;
  status: boolean;
}

export interface SuperAdminEstadisticas {
  total_empresas: number;
  empresas_activas: number;
  total_usuarios: number;
  usuarios_activos: number;
  total_empleados: number;
  empleados_activos: number;
  total_plantas: number;
  plantas_activas: number;
  total_departamentos: number;
  departamentos_activos: number;
  total_puestos: number;
  puestos_activos: number;
  total_evaluaciones: number;
  total_suscripciones: number;
  suscripciones_activas: number;
  planes_disponibles: number;
}

// Obtener estadísticas del sistema
export const getEstadisticasSistema = async (): Promise<SuperAdminEstadisticas> => {
  const response = await api.get('/empresas/estadisticas/');
  return response.data;
};

// Servicios para empresas
export const getEmpresas = async (params?: {
  buscar?: string;
  status?: string;
}): Promise<{ empresas: SuperAdminEmpresa[]; total: number }> => {
  const response = await api.get('/empresas/', { params });
  return { empresas: response.data, total: response.data.length };
};

// Servicios para usuarios
export const getUsuarios = async (params?: {
  buscar?: string;
  activo?: string;
  nivel_usuario?: string;
}): Promise<{ usuarios: SuperAdminUsuario[]; total: number }> => {
  const response = await api.get('/usuarios/', { params });
  return { usuarios: response.data, total: response.data.length };
};

// Servicios para plantas
export const getPlantas = async (params?: {
  buscar?: string;
  status?: string;
  empresa_id?: string;
}): Promise<{ plantas: SuperAdminPlanta[]; total: number }> => {
  const response = await api.get('/plantas/', { params });
  return { plantas: response.data, total: response.data.length };
};

// Servicios para departamentos
export const getDepartamentos = async (params?: {
  buscar?: string;
  status?: string;
  empresa_id?: string;
}): Promise<{ departamentos: SuperAdminDepartamento[]; total: number }> => {
  const response = await api.get('/departamentos/', { params });
  return { departamentos: response.data, total: response.data.length };
};

// Servicios para puestos
export const getPuestos = async (params?: {
  buscar?: string;
  status?: string;
  empresa_id?: string;
}): Promise<{ puestos: SuperAdminPuesto[]; total: number }> => {
  const response = await api.get('/puestos/', { params });
  return { puestos: response.data, total: response.data.length };
};

// Servicios para empleados
export const getEmpleados = async (params?: {
  buscar?: string;
  status?: string;
  empresa_id?: string;
}): Promise<{ empleados: SuperAdminEmpleado[]; total: number }> => {
  const response = await api.get('/empleados/', { params });
  return { empleados: response.data, total: response.data.length };
};

// Funciones de suspender/activar (pendientes de implementación)
export const suspenderEmpresa = async (empresaId: number, accion: 'suspender' | 'activar'): Promise<void> => {
  console.log('⚠️ Función suspenderEmpresa pendiente de implementación');
  throw new Error('Función no implementada');
};

export const suspenderUsuario = async (userId: number, accion: 'suspender' | 'activar'): Promise<void> => {
  console.log('⚠️ Función suspenderUsuario pendiente de implementación');
  throw new Error('Función no implementada');
};

export const suspenderPlanta = async (plantaId: number, accion: 'suspender' | 'activar'): Promise<void> => {
  console.log('⚠️ Función suspenderPlanta pendiente de implementación');
  throw new Error('Función no implementada');
};

export const suspenderDepartamento = async (depId: number, accion: 'suspender' | 'activar'): Promise<void> => {
  console.log('⚠️ Función suspenderDepartamento pendiente de implementación');
  throw new Error('Función no implementada');
};

export const suspenderPuesto = async (puestoId: number, accion: 'suspender' | 'activar'): Promise<void> => {
  console.log('⚠️ Función suspenderPuesto pendiente de implementación');
  throw new Error('Función no implementada');
};

export const suspenderEmpleado = async (empleadoId: number, accion: 'suspender' | 'activar'): Promise<void> => {
  console.log('⚠️ Función suspenderEmpleado pendiente de implementación');
  throw new Error('Función no implementada');
};

// Funciones de eliminar (pendientes de implementación)
export const eliminarEmpresa = async (empresaId: number): Promise<void> => {
  console.log('⚠️ Función eliminarEmpresa pendiente de implementación');
  throw new Error('Función no implementada');
};

export const eliminarUsuario = async (userId: number): Promise<void> => {
  console.log('⚠️ Función eliminarUsuario pendiente de implementación');
  throw new Error('Función no implementada');
};

export const eliminarPlanta = async (plantaId: number): Promise<void> => {
  console.log('⚠️ Función eliminarPlanta pendiente de implementación');
  throw new Error('Función no implementada');
};

export const eliminarDepartamento = async (depId: number): Promise<void> => {
  console.log('⚠️ Función eliminarDepartamento pendiente de implementación');
  throw new Error('Función no implementada');
};

export const eliminarPuesto = async (puestoId: number): Promise<void> => {
  console.log('⚠️ Función eliminarPuesto pendiente de implementación');
  throw new Error('Función no implementada');
};

export const eliminarEmpleado = async (empleadoId: number): Promise<void> => {
  console.log('⚠️ Función eliminarEmpleado pendiente de implementación');
  throw new Error('Función no implementada');
};

// Funciones de editar (pendientes de implementación)
export const editarEmpresa = async (id: number, data: Partial<SuperAdminEmpresa>) => {
  console.log('⚠️ Función editarEmpresa pendiente de implementación');
  throw new Error('Función no implementada');
};

export const editarUsuario = async (id: number, data: Partial<SuperAdminUsuario>) => {
  console.log('⚠️ Función editarUsuario pendiente de implementación');
  throw new Error('Función no implementada');
};

export const editarPlanta = async (id: number, data: Partial<SuperAdminPlanta>) => {
  console.log('⚠️ Función editarPlanta pendiente de implementación');
  throw new Error('Función no implementada');
};

export const editarDepartamento = async (id: number, data: Partial<SuperAdminDepartamento>) => {
  console.log('⚠️ Función editarDepartamento pendiente de implementación');
  throw new Error('Función no implementada');
};

export const editarPuesto = async (id: number, data: Partial<SuperAdminPuesto>) => {
  console.log('⚠️ Función editarPuesto pendiente de implementación');
  throw new Error('Función no implementada');
};

export const editarEmpleado = async (id: number, data: Partial<SuperAdminEmpleado>) => {
  console.log('⚠️ Función editarEmpleado pendiente de implementación');
  throw new Error('Función no implementada');
};

// Función para crear usuarios SuperAdmin
export const crearUsuario = async (userData: {
  username: string;
  email: string;
  password: string;
  first_name?: string;
  last_name?: string;
}): Promise<any> => {
  console.log('⚠️ Función crearUsuario pendiente de implementación');
  throw new Error('Función no implementada');
};
