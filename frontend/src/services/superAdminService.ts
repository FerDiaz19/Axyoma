import api from '../api';

// Definir BASE_URL sin "api/" - Esto corrige el problema de duplicación
// ya que axios ya incluye "api" en la baseURL
const BASE_URL = 'superadmin';

// Interfaces para los tipos de datos
export interface Empresa {
  empresa_id: number;
  nombre: string;
  rfc: string;
  telefono?: string;
  correo?: string;
  direccion?: string;
  fecha_registro?: string;
  status: boolean;
  administrador?: {
    id: number;
    username: string;
    email: string;
    nombre_completo: string;
    activo: boolean;
  };
  plantas_count?: number;
  empleados_count?: number;
}

export interface SuperAdminEmpresa {
  empresa_id: number;
  nombre: string;
  rfc: string;
  telefono: string;
  correo: string;
  direccion: string;
  status: boolean;
}

export interface SuperAdminUsuario {
  user_id: number;
  username: string;
  email: string;
  nombre: string;
  apellido_paterno: string;
  apellido_materno?: string;
  nivel_usuario: string;
  is_active: boolean;
}

export interface SuperAdminPlanta {
  planta_id: number;
  nombre: string;
  direccion: string;
  status: boolean;
  empresa_id: number;
}

export interface SuperAdminDepartamento {
  departamento_id: number;
  nombre: string;
  descripcion: string;
  status: boolean;
  planta_id: number;
}

export interface SuperAdminPuesto {
  puesto_id: number;
  nombre: string;
  descripcion: string;
  status: boolean;
  departamento_id: number;
}

export interface SuperAdminEmpleado {
  empleado_id: number;
  nombre: string;
  apellido_paterno: string;
  apellido_materno?: string;
  genero: string;
  puesto_id: number;
  departamento_id: number;
  planta_id: number;
  status: boolean;
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
  usuarios_activos: number; // Esta propiedad estaba faltando
  usuarios_por_nivel?: {
    superadmin: number;
    'admin-empresa': number;
    'admin-planta': number;
    empleado: number;
  };
  total_evaluaciones?: number;
  total_suscripciones?: number;
  suscripciones_activas?: number;
  planes_disponibles?: number;
}

// Método que causa el problema - corregido
export const getEstadisticasSistema = async (): Promise<SuperAdminEstadisticas> => {
  try {
    // Usar ruta SIN "api/" al inicio
    const response = await api.get(`${BASE_URL}/estadisticas_sistema/`);
    return response.data;
  } catch (error) {
    console.error('❌ SuperAdmin: Error cargando estadísticas:', error);
    throw error;
  }
};

// Empresas
export const getEmpresas = async (buscar = '', status = ''): Promise<Empresa[]> => {
  console.log('🔍 SuperAdmin: Obteniendo empresas...');
  try {
    // Build query parameters
    const params = new URLSearchParams();
    if (buscar) params.append('buscar', buscar);
    if (status) params.append('status', status);
    
    // Make API call with detailed logging
    console.log(`🔍 SuperAdmin: Llamando a API: /superadmin/listar_empresas/?${params.toString()}`);
    const response = await api.get(`/superadmin/listar_empresas/?${params.toString()}`);
    
    // Check if response has the expected structure
    if (response.data && response.data.empresas) {
      console.log(`✅ SuperAdmin: Obtenidas ${response.data.empresas.length} empresas`);
      return response.data.empresas;
    } else {
      console.error('❌ SuperAdmin: Formato de respuesta inesperado:', response.data);
      return [];
    }
  } catch (error) {
    console.error('❌ SuperAdmin: Error obteniendo empresas:', error);
    return [];
  }
};

// Funciones de suspensión/activación
export const suspenderEmpresa = async (id: number, accion: 'suspender' | 'activar') => {
  try {
    console.log(`🔒 SuperAdmin: ${accion === 'suspender' ? 'Suspendiendo' : 'Activando'} empresa ${id}...`);
    const response = await api.post(`${BASE_URL}/suspender_empresa/`, {
      empresa_id: id,
      accion: accion
    });
    return response.data;
  } catch (error) {
    console.error(`❌ SuperAdmin: Error ${accion === 'suspender' ? 'suspendiendo' : 'activando'} empresa:`, error);
    throw error;
  }
};

// Funciones de eliminación
export const eliminarEmpresa = async (id: number) => {
  try {
    console.log(`🗑️ SuperAdmin: Eliminando empresa ${id}...`);
    const response = await api.delete(`${BASE_URL}/eliminar_empresa/`, {
      data: { empresa_id: id }
    });
    return response.data;
  } catch (error) {
    console.error('❌ SuperAdmin: Error eliminando empresa:', error);
    throw error;
  }
};

// Funciones de edición
export const editarEmpresa = async (id: number, data: Partial<SuperAdminEmpresa>) => {
  try {
    console.log(`🔧 SuperAdmin: Editando empresa ${id}...`, data);
    const response = await api.put(`${BASE_URL}/editar_empresa/`, {
      empresa_id: id,
      ...data
    });
    return response.data;
  } catch (error) {
    console.error('❌ SuperAdmin: Error editando empresa:', error);
    throw error;
  }
};

// Usuarios
export const getUsuarios = async (buscar = '', nivel_usuario = '', activo = ''): Promise<{usuarios: SuperAdminUsuario[]}> => {
  try {
    let params = new URLSearchParams();
    if (buscar) params.append('buscar', buscar);
    if (nivel_usuario) params.append('nivel_usuario', nivel_usuario);
    if (activo) params.append('activo', activo);
    
    const response = await api.get(`${BASE_URL}/listar_usuarios/?${params.toString()}`);
    return response.data || { usuarios: [] };
  } catch (error) {
    console.error('❌ SuperAdmin: Error cargando usuarios:', error);
    return { usuarios: [] };
  }
};

// Funciones de suspensión/activación
export const suspenderUsuario = async (id: number, accion: 'suspender' | 'activar') => {
  try {
    console.log(`🔒 SuperAdmin: ${accion === 'suspender' ? 'Suspendiendo' : 'Activando'} usuario ${id}...`);
    const response = await api.post(`${BASE_URL}/suspender_usuario/`, {
      user_id: id,
      accion: accion
    });
    return response.data;
  } catch (error) {
    console.error(`❌ SuperAdmin: Error ${accion === 'suspender' ? 'suspendiendo' : 'activando'} usuario:`, error);
    throw error;
  }
};

// Funciones de eliminación
export const eliminarUsuario = async (id: number) => {
  try {
    console.log(`🗑️ SuperAdmin: Eliminando usuario ${id}...`);
    const response = await api.delete(`${BASE_URL}/eliminar_usuario/`, {
      data: { user_id: id }
    });
    return response.data;
  } catch (error) {
    console.error('❌ SuperAdmin: Error eliminando usuario:', error);
    throw error;
  }
};

// Funciones de edición
export const editarUsuario = async (id: number, data: Partial<SuperAdminUsuario>) => {
  try {
    console.log(`🔧 SuperAdmin: Editando usuario ${id}...`, data);
    const response = await api.put(`${BASE_URL}/editar_usuario/`, {
      user_id: id,
      ...data
    });
    return response.data;
  } catch (error) {
    console.error('❌ SuperAdmin: Error editando usuario:', error);
    throw error;
  }
};

// Crear usuario (solo superadmin)
export const crearUsuario = async (data: Omit<SuperAdminUsuario, 'user_id'> & { password: string }) => {
  try {
    console.log('🔧 SuperAdmin: Creando nuevo usuario...', data);
    const response = await api.post(`${BASE_URL}/crear_usuario/`, data);
    return response.data;
  } catch (error) {
    console.error('❌ SuperAdmin: Error creando usuario:', error);
    throw error;
  }
};

// Plantas
export const getPlantas = async (buscar = '', empresa_id = '', status = ''): Promise<{plantas: any[]}> => {
  try {
    let params = new URLSearchParams();
    if (buscar) params.append('buscar', buscar);
    if (empresa_id) params.append('empresa_id', empresa_id);
    if (status) params.append('status', status);
    
    const response = await api.get(`${BASE_URL}/listar_todas_plantas/?${params.toString()}`);
    return response.data || { plantas: [] };
  } catch (error) {
    console.error('❌ SuperAdmin: Error cargando plantas:', error);
    return { plantas: [] };
  }
};

// Funciones de suspensión/activación
export const suspenderPlanta = async (id: number, accion: 'suspender' | 'activar') => {
  try {
    console.log(`🔒 SuperAdmin: ${accion === 'suspender' ? 'Suspendiendo' : 'Activando'} planta ${id}...`);
    const response = await api.post(`${BASE_URL}/suspender_planta/`, {
      planta_id: id,
      accion: accion
    });
    return response.data;
  } catch (error) {
    console.error(`❌ SuperAdmin: Error ${accion === 'suspender' ? 'suspendiendo' : 'activando'} planta:`, error);
    throw error;
  }
};

// Funciones de eliminación
export const eliminarPlanta = async (id: number) => {
  try {
    console.log(`🗑️ SuperAdmin: Eliminando planta ${id}...`);
    const response = await api.delete(`${BASE_URL}/eliminar_planta/`, {
      data: { planta_id: id }
    });
    return response.data;
  } catch (error) {
    console.error('❌ SuperAdmin: Error eliminando planta:', error);
    throw error;
  }
};

// Funciones de edición
export const editarPlanta = async (id: number, data: Partial<SuperAdminPlanta>) => {
  try {
    console.log(`🔧 SuperAdmin: Editando planta ${id}...`, data);
    const response = await api.put(`${BASE_URL}/editar_planta/`, {
      planta_id: id,
      ...data
    });
    return response.data;
  } catch (error) {
    console.error('❌ SuperAdmin: Error editando planta:', error);
    throw error;
  }
};

// Departamentos
export const getDepartamentos = async (buscar = '', planta_id = '', empresa_id = '', status = ''): Promise<{departamentos: any[]}> => {
  try {
    let params = new URLSearchParams();
    if (buscar) params.append('buscar', buscar);
    if (planta_id) params.append('planta_id', planta_id);
    if (empresa_id) params.append('empresa_id', empresa_id);
    if (status) params.append('status', status);
    
    const response = await api.get(`${BASE_URL}/listar_todos_departamentos/?${params.toString()}`);
    return response.data || { departamentos: [] };
  } catch (error) {
    console.error('❌ SuperAdmin: Error cargando departamentos:', error);
    return { departamentos: [] };
  }
};

// Funciones de suspensión/activación
export const suspenderDepartamento = async (id: number, accion: 'suspender' | 'activar') => {
  try {
    console.log(`🔒 SuperAdmin: ${accion === 'suspender' ? 'Suspendiendo' : 'Activando'} departamento ${id}...`);
    const response = await api.post(`${BASE_URL}/suspender_departamento/`, {
      departamento_id: id,
      accion: accion
    });
    return response.data;
  } catch (error) {
    console.error(`❌ SuperAdmin: Error ${accion === 'suspender' ? 'suspendiendo' : 'activando'} departamento:`, error);
    throw error;
  }
};

// Funciones de eliminación
export const eliminarDepartamento = async (id: number) => {
  try {
    console.log(`🗑️ SuperAdmin: Eliminando departamento ${id}...`);
    const response = await api.delete(`${BASE_URL}/eliminar_departamento/`, {
      data: { departamento_id: id }
    });
    return response.data;
  } catch (error) {
    console.error('❌ SuperAdmin: Error eliminando departamento:', error);
    throw error;
  }
};

// Funciones de edición
export const editarDepartamento = async (id: number, data: Partial<SuperAdminDepartamento>) => {
  try {
    console.log(`🔧 SuperAdmin: Editando departamento ${id}...`, data);
    const response = await api.put(`${BASE_URL}/editar_departamento/`, {
      departamento_id: id,
      ...data
    });
    return response.data;
  } catch (error) {
    console.error('❌ SuperAdmin: Error editando departamento:', error);
    throw error;
  }
};

// Puestos
export const getPuestos = async (buscar = '', departamento_id = '', planta_id = '', empresa_id = '', status = ''): Promise<{puestos: any[]}> => {
  try {
    let params = new URLSearchParams();
    if (buscar) params.append('buscar', buscar);
    if (departamento_id) params.append('departamento_id', departamento_id);
    if (planta_id) params.append('planta_id', planta_id);
    if (empresa_id) params.append('empresa_id', empresa_id);
    if (status) params.append('status', status);
    
    const response = await api.get(`${BASE_URL}/listar_todos_puestos/?${params.toString()}`);
    return response.data || { puestos: [] };
  } catch (error) {
    console.error('❌ SuperAdmin: Error cargando puestos:', error);
    return { puestos: [] };
  }
};

// Funciones de suspensión/activación
export const suspenderPuesto = async (id: number, accion: 'suspender' | 'activar') => {
  try {
    console.log(`🔒 SuperAdmin: ${accion === 'suspender' ? 'Suspendiendo' : 'Activando'} puesto ${id}...`);
    const response = await api.post(`${BASE_URL}/suspender_puesto/`, {
      puesto_id: id,
      accion: accion
    });
    return response.data;
  } catch (error) {
    console.error(`❌ SuperAdmin: Error ${accion === 'suspender' ? 'suspendiendo' : 'activando'} puesto:`, error);
    throw error;
  }
};

// Funciones de eliminación
export const eliminarPuesto = async (id: number) => {
  try {
    console.log(`🗑️ SuperAdmin: Eliminando puesto ${id}...`);
    const response = await api.delete(`${BASE_URL}/eliminar_puesto/`, {
      data: { puesto_id: id }
    });
    return response.data;
  } catch (error) {
    console.error('❌ SuperAdmin: Error eliminando puesto:', error);
    throw error;
  }
};

// Funciones de edición
export const editarPuesto = async (id: number, data: Partial<SuperAdminPuesto>) => {
  try {
    console.log(`🔧 SuperAdmin: Editando puesto ${id}...`, data);
    const response = await api.put(`${BASE_URL}/editar_puesto/`, {
      puesto_id: id,
      ...data
    });
    return response.data;
  } catch (error) {
    console.error('❌ SuperAdmin: Error editando puesto:', error);
    throw error;
  }
};

// Empleados
export const getEmpleados = async (buscar = '', empresa_id = '', planta_id = '', departamento_id = '', puesto_id = '', status = ''): Promise<{empleados: any[]}> => {
  try {
    let params = new URLSearchParams();
    if (buscar) params.append('buscar', buscar);
    if (empresa_id) params.append('empresa_id', empresa_id);
    if (planta_id) params.append('planta_id', planta_id);
    if (departamento_id) params.append('departamento_id', departamento_id);
    if (puesto_id) params.append('puesto_id', puesto_id);
    if (status) params.append('status', status);
    
    const response = await api.get(`${BASE_URL}/listar_todos_empleados/?${params.toString()}`);
    return response.data || { empleados: [] };
  } catch (error) {
    console.error('❌ SuperAdmin: Error cargando empleados:', error);
    return { empleados: [] };
  }
};

// Funciones de suspensión/activación
export const suspenderEmpleado = async (id: number, accion: 'suspender' | 'activar') => {
  try {
    console.log(`🔒 SuperAdmin: ${accion === 'suspender' ? 'Suspendiendo' : 'Activando'} empleado ${id}...`);
    const response = await api.post(`${BASE_URL}/suspender_empleado/`, {
      empleado_id: id,
      accion: accion
    });
    return response.data;
  } catch (error) {
    console.error(`❌ SuperAdmin: Error ${accion === 'suspender' ? 'suspendiendo' : 'activando'} empleado:`, error);
    throw error;
  }
};

// Funciones de eliminación
export const eliminarEmpleado = async (id: number) => {
  try {
    console.log(`🗑️ SuperAdmin: Eliminando empleado ${id}...`);
    const response = await api.delete(`${BASE_URL}/eliminar_empleado/`, {
      data: { empleado_id: id }
    });
    return response.data;
  } catch (error) {
    console.error('❌ SuperAdmin: Error eliminando empleado:', error);
    throw error;
  }
};

// Funciones de edición
export const editarEmpleado = async (id: number, data: Partial<SuperAdminEmpleado>) => {
  try {
    console.log(`🔧 SuperAdmin: Editando empleado ${id}...`, data);
    const response = await api.put(`${BASE_URL}/editar_empleado/`, {
      empleado_id: id,
      ...data
    });
    return response.data;
  } catch (error) {
    console.error('❌ SuperAdmin: Error editando empleado:', error);
    throw error;
  }
};
