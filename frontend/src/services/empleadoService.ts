import api from "../api";

// Types
export interface Empleado {
  empleado_id: number;
  nombre: string;
  apellido_paterno: string;
  apellido_materno?: string;
  genero: 'Masculino' | 'Femenino';
  antiguedad?: number;
  status: boolean;
  puesto: number;
  departamento: number;
  planta: number;
}

export interface EmpleadoCreate {
  nombre: string;
  apellido_paterno: string;
  apellido_materno?: string;
  genero: 'Masculino' | 'Femenino';
  antiguedad?: number;
  puesto: number;
  departamento: number;
  planta: number;
}

export interface Planta {
  planta_id: number;
  nombre: string;
  direccion?: string;
  fecha_registro: string;
  status: boolean;
  empresa: number;
}

export interface Departamento {
  departamento_id: number;
  nombre: string;
  descripcion?: string;
  fecha_registro: string;
  status: boolean;
  planta_id: number; // Cambiado de planta a planta_id
  planta_nombre?: string;
}

export interface Puesto {
  puesto_id: number;
  nombre: string;
  descripcion?: string;
  status: boolean;
  departamento_id: number; // Cambiado de departamento a departamento_id
  departamento_nombre?: string;
}

const context = "empleados/";

export const getEmpleados = async (): Promise<Empleado[]> => {
  const response = await api.get<Empleado[]>(context);
  return response.data;
};

export const getEmpleadoById = async (id: number): Promise<Empleado> => {
  const response = await api.get<Empleado>(`${context}${id}/`);
  return response.data;
};

export const createEmpleado = async (data: EmpleadoCreate): Promise<Empleado> => {
  const response = await api.post<Empleado>(context, data);
  return response.data;
};

export const updateEmpleado = async (id: number, data: EmpleadoCreate): Promise<Empleado> => {
  const response = await api.put<Empleado>(`${context}${id}/`, data);
  return response.data;
};

export const deleteEmpleado = async (id: number): Promise<void> => {
  await api.delete(`${context}${id}/`);
};

export const getPlantasDisponibles = async (): Promise<Planta[]> => {
  const response = await api.get<Planta[]>('plantas/');
  return response.data;
};

export const getDepartamentosPorPlanta = async (plantaId: number): Promise<Departamento[]> => {
  const response = await api.get<Departamento[]>(`departamentos/?planta=${plantaId}`);
  return response.data;
};

export const getPuestosPorDepartamento = async (departamentoId: number): Promise<Puesto[]> => {
  const response = await api.get<Puesto[]>(`puestos/?departamento=${departamentoId}`);
  return response.data;
};

// Funciones auxiliares para obtener todos los datos
export const getPlantas = async (): Promise<Planta[]> => {
  const response = await api.get<Planta[]>('plantas/');
  return response.data;
};

export const getDepartamentos = async (): Promise<Departamento[]> => {
  const response = await api.get<Departamento[]>('departamentos/');
  return response.data;
};

export const getPuestos = async (): Promise<Puesto[]> => {
  const response = await api.get<Puesto[]>('puestos/');
  return response.data;
};
