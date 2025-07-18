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
  direccion?: string;
  telefono?: string;
  status: boolean;
  empresa: {
    id: number;
    nombre: string;
    status: boolean;
  };
  administrador?: {
    id: number;
    username: string;
    email: string;
    nombre_completo: string;
    activo: boolean;
  };
  departamentos_count: number;
  empleados_count: number;
}

export interface SuperAdminDepartamento {
  departamento_id: number;
  nombre: string;
  descripcion?: string;
  status: boolean;
  planta: {
    id: number;
    nombre: string;
    status: boolean;
  };
  empresa: {
    id: number;
    nombre: string;
    status: boolean;
  };
  puestos_count: number;
  empleados_count: number;
}

export interface SuperAdminPuesto {
  puesto_id: number;
  nombre: string;
  descripcion?: string;
  status: boolean;
  departamento: {
    id: number;
    nombre: string;
    status: boolean;
  };
  planta: {
    id: number;
    nombre: string;
    status: boolean;
  };
  empresa: {
    id: number;
    nombre: string;
    status: boolean;
  };
  empleados_count: number;
}

export interface SuperAdminEmpleado {
  empleado_id: number;
  numero_empleado: string;
  nombre: string;
  apellido_paterno: string;
  apellido_materno?: string;
  nombre_completo: string;
  correo?: string;
  telefono?: string;
  fecha_ingreso?: string;
  salario?: number;
  status: boolean;
  empresa: {
    id: number;
    nombre: string;
    status: boolean;
  };
  planta: {
    id: number;
    nombre: string;
    status: boolean;
  };
  departamento: {
    id: number;
    nombre: string;
    status: boolean;
  };
  puesto: {
    id: number;
    nombre: string;
    status: boolean;
  };
}

export interface SuperAdminEstadisticas {
  total_empresas: number;
  empresas_activas: number;
  total_plantas: number;
  plantas_activas: number;
  total_departamentos: number;
  departamentos_activos: number;
  total_puestos: number;
  puestos_activos: number;
  total_empleados: number;
  empleados_activos: number;
  total_usuarios: number;
  usuarios_por_nivel: {
    superadmin: number;
    'admin-empresa': number;
    'admin-planta': number;
    empleado: number;
  };
}

const API_BASE = 'superadmin';

// Obtener estadísticas del sistema
export const getEstadisticasSistema = async (): Promise<SuperAdminEstadisticas> => {
  const response = await api.get(`${API_BASE}/estadisticas_sistema/`);
  return response.data;
};

// Servicios para empresas
export const getEmpresas = async (params?: {
  buscar?: string;
  status?: string;
}): Promise<{ empresas: SuperAdminEmpresa[]; total: number }> => {
  const response = await api.get(`${API_BASE}/listar_empresas/`, { params });
  return response.data;
};

export const suspenderEmpresa = async (empresaId: number, accion: 'suspender' | 'activar'): Promise<void> => {
  await api.post(`${API_BASE}/suspender_empresa/`, {
    empresa_id: empresaId,
    accion
  });
};

export const eliminarEmpresa = async (empresaId: number): Promise<void> => {
  await api.delete(`${API_BASE}/eliminar_empresa/`, {
    data: { empresa_id: empresaId }
  });
};

// Funciones de edición
export const editarEmpresa = async (id: number, data: Partial<SuperAdminEmpresa>) => {
  try {
    console.log(`🔧 SuperAdmin: Editando empresa ${id}...`, data);
    const response = await api.put(`${API_BASE}/editar_empresa/`, {
      empresa_id: id,
      ...data
    });
    console.log('✅ SuperAdmin: Empresa editada exitosamente');
    return response.data;
  } catch (error) {
    console.error('❌ SuperAdmin: Error editando empresa:', error);
    throw error;
  }
};

// Servicios para usuarios
export const getUsuarios = async (params?: {
  buscar?: string;
  nivel_usuario?: string;
  activo?: string;
}): Promise<{ usuarios: SuperAdminUsuario[]; total: number }> => {
  const response = await api.get(`${API_BASE}/listar_usuarios/`, { params });
  return response.data;
};

export const suspenderUsuario = async (userId: number, accion: 'suspender' | 'activar'): Promise<void> => {
  await api.post(`${API_BASE}/suspender_usuario/`, {
    user_id: userId,
    accion
  });
};

export const eliminarUsuario = async (userId: number): Promise<void> => {
  await api.delete(`${API_BASE}/eliminar_usuario/`, {
    data: { user_id: userId }
  });
};

// Funciones de edición
export const editarUsuario = async (id: number, data: Partial<SuperAdminUsuario>) => {
  try {
    console.log(`🔧 SuperAdmin: Editando usuario ${id}...`, data);
    const response = await api.put(`${API_BASE}/editar_usuario/`, {
      user_id: id,
      ...data
    });
    console.log('✅ SuperAdmin: Usuario editado exitosamente');
    return response.data;
  } catch (error) {
    console.error('❌ SuperAdmin: Error editando usuario:', error);
    throw error;
  }
};

// Función para crear usuarios SuperAdmin
export const crearUsuario = async (data: {
  username: string;
  email: string;
  nombre: string;
  apellido_paterno: string;
  apellido_materno?: string;
  password?: string;
  is_active?: boolean;
}) => {
  try {
    console.log('🔧 SuperAdmin: Creando nuevo usuario SuperAdmin...', data);
    const response = await api.post(`${API_BASE}/crear_usuario/`, {
      ...data,
      nivel_usuario: 'superadmin' // Solo permitir crear SuperAdmin
    });
    console.log('✅ SuperAdmin: Usuario SuperAdmin creado exitosamente');
    return response.data;
  } catch (error) {
    console.error('❌ SuperAdmin: Error creando usuario:', error);
    throw error;
  }
};

// Servicios para plantas
export const getPlantas = async (params?: {
  buscar?: string;
  empresa_id?: string;
  status?: string;
}): Promise<{ plantas: SuperAdminPlanta[]; total: number }> => {
  const response = await api.get(`${API_BASE}/listar_todas_plantas/`, { params });
  return response.data;
};

export const suspenderPlanta = async (plantaId: number, accion: 'suspender' | 'activar'): Promise<void> => {
  await api.post(`${API_BASE}/suspender_planta/`, {
    planta_id: plantaId,
    accion
  });
};

export const eliminarPlanta = async (plantaId: number): Promise<void> => {
  await api.delete(`${API_BASE}/eliminar_planta/`, {
    data: { planta_id: plantaId }
  });
};

// Funciones de edición
export const editarPlanta = async (id: number, data: Partial<SuperAdminPlanta>) => {
  try {
    console.log(`🔧 SuperAdmin: Editando planta ${id}...`, data);
    const response = await api.put(`${API_BASE}/editar_planta/`, {
      planta_id: id,
      ...data
    });
    console.log('✅ SuperAdmin: Planta editada exitosamente');
    return response.data;
  } catch (error) {
    console.error('❌ SuperAdmin: Error editando planta:', error);
    throw error;
  }
};

// Servicios para departamentos
export const getDepartamentos = async (params?: {
  buscar?: string;
  planta_id?: string;
  empresa_id?: string;
  status?: string;
}): Promise<{ departamentos: SuperAdminDepartamento[]; total: number }> => {
  const response = await api.get(`${API_BASE}/listar_todos_departamentos/`, { params });
  return response.data;
};

export const suspenderDepartamento = async (departamentoId: number, accion: 'suspender' | 'activar'): Promise<void> => {
  await api.post(`${API_BASE}/suspender_departamento/`, {
    departamento_id: departamentoId,
    accion
  });
};

export const eliminarDepartamento = async (departamentoId: number): Promise<void> => {
  await api.delete(`${API_BASE}/eliminar_departamento/`, {
    data: { departamento_id: departamentoId }
  });
};

// Funciones de edición
export const editarDepartamento = async (id: number, data: Partial<SuperAdminDepartamento>) => {
  try {
    console.log(`🔧 SuperAdmin: Editando departamento ${id}...`, data);
    const response = await api.put(`${API_BASE}/editar_departamento/`, {
      departamento_id: id,
      ...data
    });
    console.log('✅ SuperAdmin: Departamento editado exitosamente');
    return response.data;
  } catch (error) {
    console.error('❌ SuperAdmin: Error editando departamento:', error);
    throw error;
  }
};

// Servicios para puestos
export const getPuestos = async (params?: {
  buscar?: string;
  departamento_id?: string;
  planta_id?: string;
  empresa_id?: string;
  status?: string;
}): Promise<{ puestos: SuperAdminPuesto[]; total: number }> => {
  const response = await api.get(`${API_BASE}/listar_todos_puestos/`, { params });
  return response.data;
};

export const suspenderPuesto = async (puestoId: number, accion: 'suspender' | 'activar'): Promise<void> => {
  await api.post(`${API_BASE}/suspender_puesto/`, {
    puesto_id: puestoId,
    accion
  });
};

export const eliminarPuesto = async (puestoId: number): Promise<void> => {
  await api.delete(`${API_BASE}/eliminar_puesto/`, {
    data: { puesto_id: puestoId }
  });
};

// Funciones de edición
export const editarPuesto = async (id: number, data: Partial<SuperAdminPuesto>) => {
  try {
    console.log(`🔧 SuperAdmin: Editando puesto ${id}...`, data);
    const response = await api.put(`${API_BASE}/editar_puesto/`, {
      puesto_id: id,
      ...data
    });
    console.log('✅ SuperAdmin: Puesto editado exitosamente');
    return response.data;
  } catch (error) {
    console.error('❌ SuperAdmin: Error editando puesto:', error);
    throw error;
  }
};

// Servicios para empleados
export const getEmpleados = async (params?: {
  buscar?: string;
  empresa_id?: string;
  planta_id?: string;
  departamento_id?: string;
  puesto_id?: string;
  status?: string;
}): Promise<{ empleados: SuperAdminEmpleado[]; total: number }> => {
  const response = await api.get(`${API_BASE}/listar_todos_empleados/`, { params });
  return response.data;
};

export const suspenderEmpleado = async (empleadoId: number, accion: 'suspender' | 'activar'): Promise<void> => {
  await api.post(`${API_BASE}/suspender_empleado/`, {
    empleado_id: empleadoId,
    accion
  });
};

export const eliminarEmpleado = async (empleadoId: number): Promise<void> => {
  await api.delete(`${API_BASE}/eliminar_empleado/`, {
    data: { empleado_id: empleadoId }
  });
};

// Funciones de edición
export const editarEmpleado = async (id: number, data: Partial<SuperAdminEmpleado>) => {
  try {
    console.log(`🔧 SuperAdmin: Editando empleado ${id}...`, data);
    const response = await api.put(`${API_BASE}/editar_empleado/`, {
      empleado_id: id,
      ...data
    });
    console.log('✅ SuperAdmin: Empleado editado exitosamente');
    return response.data;
  } catch (error) {
    console.error('❌ SuperAdmin: Error editando empleado:', error);
    throw error;
  }
};
