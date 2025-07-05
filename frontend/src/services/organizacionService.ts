import api from '../api';

export interface Planta {
  planta_id?: number;
  nombre: string;
  direccion?: string;
  fecha_registro?: string;
  status?: boolean;
  empresa?: number;
}

export interface Departamento {
  departamento_id?: number;
  nombre: string;
  descripcion?: string;
  fecha_registro?: string;
  status?: boolean;
  planta_id: number; // Cambiado de planta a planta_id para coincidir con el backend
  planta_nombre?: string;
}

export interface Puesto {
  puesto_id?: number;
  nombre: string;
  descripcion?: string;
  fecha_registro?: string;
  status?: boolean;
  departamento_id: number; // Cambiado de departamento a departamento_id para coincidir con el backend
  departamento_nombre?: string;
}

export interface UsuarioPlanta {
  planta_id: number;
  planta_nombre: string;
  usuario_id?: number;
  username?: string;
  email?: string;
  nombre_completo?: string;
  fecha_creacion?: string;
  status: boolean;
  password_temporal?: string;
}

// Servicios para Plantas
export const obtenerPlantas = async (): Promise<Planta[]> => {
  console.log('🔍 organizacionService: Obteniendo plantas...');
  console.log('🔍 Token en localStorage:', localStorage.getItem('authToken')?.substring(0, 20) + '...');
  
  try {
    const response = await api.get('/plantas/');
    console.log('✅ organizacionService: Respuesta plantas:', response.data);
    return response.data;
  } catch (error) {
    console.error('❌ organizacionService: Error obteniendo plantas:', error);
    throw error;
  }
};

export const crearPlanta = async (planta: Planta): Promise<Planta> => {
  try {
    const response = await api.post('/plantas/', planta);
    return response.data;
  } catch (error: any) {
    if (error.response?.data?.non_field_errors) {
      throw new Error(error.response.data.non_field_errors[0]);
    } else if (error.response?.data?.message) {
      throw new Error(error.response.data.message);
    } else if (error.response?.status === 400) {
      throw new Error('Error al crear la planta. Verifique que no se excedan las 5 plantas por empresa.');
    }
    throw error;
  }
};

export const actualizarPlanta = async (id: number, planta: Planta): Promise<Planta> => {
  const response = await api.put(`/plantas/${id}/`, planta);
  return response.data;
};

export const eliminarPlanta = async (id: number): Promise<void> => {
  await api.delete(`/plantas/${id}/`);
};

// Servicios para Departamentos
export const obtenerDepartamentos = async (): Promise<Departamento[]> => {
  const response = await api.get('/departamentos/');
  return response.data;
};

export const obtenerDepartamentosPorPlanta = async (plantaId: number): Promise<Departamento[]> => {
  const response = await api.get(`/departamentos/?planta=${plantaId}`);
  return response.data;
};

export const crearDepartamento = async (departamento: Departamento): Promise<Departamento> => {
  // Convertir planta_id para el backend
  const departamentoData = {
    nombre: departamento.nombre,
    descripcion: departamento.descripcion || '',
    planta_id: departamento.planta_id
  };
  const response = await api.post('/departamentos/', departamentoData);
  return response.data;
};

export const actualizarDepartamento = async (id: number, departamento: Departamento): Promise<Departamento> => {
  const response = await api.put(`/departamentos/${id}/`, departamento);
  return response.data;
};

export const eliminarDepartamento = async (id: number): Promise<void> => {
  await api.delete(`/departamentos/${id}/`);
};

// Servicios para Puestos
export const obtenerPuestos = async (): Promise<Puesto[]> => {
  const response = await api.get('/puestos/');
  return response.data;
};

export const obtenerPuestosPorDepartamento = async (departamentoId: number): Promise<Puesto[]> => {
  const response = await api.get(`/puestos/?departamento=${departamentoId}`);
  return response.data;
};

export const crearPuesto = async (puesto: Puesto): Promise<Puesto> => {
  // Convertir departamento_id para el backend
  const puestoData = {
    nombre: puesto.nombre,
    descripcion: puesto.descripcion || '',
    departamento_id: puesto.departamento_id
  };
  const response = await api.post('/puestos/', puestoData);
  return response.data;
};

export const actualizarPuesto = async (id: number, puesto: Puesto): Promise<Puesto> => {
  const response = await api.put(`/puestos/${id}/`, puesto);
  return response.data;
};

export const eliminarPuesto = async (id: number): Promise<void> => {
  await api.delete(`/puestos/${id}/`);
};

// Servicio para obtener usuarios de planta
export const obtenerUsuariosPlantas = async (): Promise<UsuarioPlanta[]> => {
  console.log('🔍 organizacionService: Obteniendo usuarios de planta...');
  
  try {
    const response = await api.get('/estructura/usuarios_planta/');
    console.log('✅ organizacionService: Respuesta usuarios planta:', response.data);
    return response.data;
  } catch (error) {
    console.error('❌ organizacionService: Error obteniendo usuarios planta:', error);
    throw error;
  }
};
