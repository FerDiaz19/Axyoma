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

// Nuevo método para eliminación completa de plantas (admin-empresa y superadmin)
export const eliminarPlantaCompleta = async (plantaId: number): Promise<any> => {
  try {
    console.log('🗑️ Eliminando planta completa ID:', plantaId);
    const response = await api.delete(`/plantas/${plantaId}/eliminar_planta_completa/`);
    console.log('✅ Planta eliminada exitosamente:', response.data);
    return response.data;
  } catch (error: any) {
    console.error('❌ Error eliminando planta:', error);
    if (error.response?.data?.error) {
      throw new Error(error.response.data.error);
    } else if (error.response?.status === 403) {
      throw new Error('No tiene permisos para eliminar plantas.');
    } else if (error.response?.status === 404) {
      throw new Error('Planta no encontrada');
    }
    throw new Error('Error al eliminar la planta');
  }
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
  try {
    // Convertir planta_id para el backend
    const departamentoData = {
      nombre: departamento.nombre.trim(),
      descripcion: departamento.descripcion?.trim() || '',
      planta_id: departamento.planta_id
    };
    
    console.log('🔍 Creando departamento con datos:', departamentoData);
    console.log('🔍 Nombre original:', JSON.stringify(departamento.nombre));
    console.log('🔍 Nombre procesado:', JSON.stringify(departamentoData.nombre));
    
    const response = await api.post('/departamentos/', departamentoData);
    console.log('✅ Departamento creado exitosamente:', response.data);
    return response.data;
  } catch (error: any) {
    console.error('❌ Error creando departamento:', error);
    console.error('❌ Datos enviados:', { departamento });
    
    if (error.response?.data?.nombre) {
      throw new Error(error.response.data.nombre[0]);
    } else if (error.response?.data?.planta_id) {
      throw new Error(error.response.data.planta_id[0]);
    } else if (error.response?.data?.non_field_errors) {
      throw new Error(error.response.data.non_field_errors[0]);
    } else if (error.response?.data?.message) {
      throw new Error(error.response.data.message);
    } else if (error.response?.status === 400) {
      throw new Error('Error al crear el departamento. Verifique que el nombre no esté duplicado en la planta.');
    }
    throw new Error('Error al crear el departamento');
  }
};

export const actualizarDepartamento = async (id: number, departamento: Departamento, originalData?: Departamento): Promise<Departamento> => {
  try {
    // Check if we're only updating the description (not the name)
    if (originalData && departamento.nombre.trim() === originalData.nombre.trim() && departamento.planta_id === originalData.planta_id) {
      // Only updating description or other fields, use PATCH instead of PUT to avoid duplicate name error
      console.log('📝 Solo actualizando descripción u otros campos, usando PATCH:', id);
      const patchData = {
        descripcion: departamento.descripcion?.trim() ?? '',
        _timestamp: Date.now() // Force update
      };
      
      const response = await api.patch(`/departamentos/${id}/`, patchData);
      console.log('✅ Departamento actualizado exitosamente (PATCH):', response.data);
      return response.data;
    }
    
    // Otherwise, proceed with normal PUT update
    const departamentoData = {
      nombre: departamento.nombre.trim(),
      descripcion: departamento.descripcion?.trim() ?? '',
      planta_id: departamento.planta_id
    };

    console.log('🔍 Actualizando departamento con ID:', id, 'Datos:', departamentoData);
    const response = await api.put(`/departamentos/${id}/`, departamentoData);//aca----------------------
    console.log('✅ Departamento actualizado exitosamente:', response.data);
    return response.data;
  } catch (error: any) {
    console.error('❌ Error actualizando departamento:', error);//aca----------------------
    
    // Mejorar el logging para mostrar el detalle exacto del error
    if (error.response?.data) {
      console.error('❌ Detalles del error del servidor:', JSON.stringify(error.response.data, null, 2)); //aca----------------------
    }
    
    // Detección específica del error de nombre duplicado
    if (error.response?.data?.non_field_errors?.length > 0 && 
        error.response.data.non_field_errors[0].includes('existe un departamento con este nombre')) {
      throw new Error('Ya existe un departamento con este nombre en la planta seleccionada');
    }
    
    // Otros casos de error
    if (error.response?.data?.nombre) {
      throw new Error(error.response.data.nombre[0]);
    } else if (error.response?.data?.planta_id) {
      throw new Error(error.response.data.planta_id[0]);
    } else if (error.response?.data?.non_field_errors) {
      throw new Error(error.response.data.non_field_errors[0]);
    } else if (error.response?.data?.message) {
      throw new Error(error.response.data.message);
    } else if (error.response?.status === 400) {
      throw new Error('Error al actualizar el departamento. Verifique que el nombre no esté duplicado en la planta.');
    }
    throw new Error('Error al actualizar el departamento');
  }
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
  try {
    // Convertir departamento_id para el backend
    const puestoData = {
      nombre: puesto.nombre.trim(),
      descripcion: puesto.descripcion?.trim() || '',
      departamento_id: puesto.departamento_id
    };
    const response = await api.post('/puestos/', puestoData);
    console.log('✅ Puesto creado exitosamente:', response.data);
    return response.data;
  } catch (error: any) {
    console.error('❌ Error creando puesto:', error);
    
    if (error.response?.data?.nombre) {
      throw new Error(error.response.data.nombre[0]);
    } else if (error.response?.data?.departamento_id) {
      throw new Error(error.response.data.departamento_id[0]);
    } else if (error.response?.data?.non_field_errors) {
      throw new Error(error.response.data.non_field_errors[0]);
    } else if (error.response?.data?.message) {
      throw new Error(error.response.data.message);
    } else if (error.response?.status === 400) {
      throw new Error('Error al crear el puesto. Verifique que el nombre no esté duplicado en el departamento.');
    }
    throw new Error('Error al crear el puesto');
  }
};

export const actualizarPuesto = async (id: number, puesto: Puesto, originalData?: Puesto): Promise<Puesto> => {
  try {
    // Formatear datos para el backend - Agregar timestamp para forzar actualización
    const puestoData = {
      nombre: puesto.nombre.trim(),
      descripcion: puesto.descripcion?.trim() ?? '', // Usar ?? para manejar null/undefined
      departamento_id: puesto.departamento_id,
      _forceUpdate: Date.now() // Agregar un valor único para forzar que el servidor detecte cambios
    };
    
    console.log('🔧 Actualizando puesto con ID:', id, 'Datos:', puestoData);
    
    let response;
    
    if (originalData &&
        puesto.nombre.trim() === originalData.nombre.trim() &&
        puesto.departamento_id === originalData.departamento_id) {
      // Solo se está actualizando la descripción
      const patchData = {
        descripcion: puesto.descripcion?.trim() ?? '',
        _timestamp: Date.now()
      };
      console.log('📝 Solo actualizando descripción, usando PATCH:', patchData);
      response = await api.patch(`/puestos/${id}/`, patchData);
      console.log('✅ Puesto actualizado exitosamente (PATCH):', response.data);
    } else {
      // Actualización completa con PUT
      response = await api.put(`/puestos/${id}/`, puestoData);
      console.log('✅ Puesto actualizado exitosamente (PUT):', response.data);
    }
    
    return response.data;
  } catch (error: any) {
    console.error('❌ Error actualizando puesto:', error);
    
    // Mejorar el logging para mostrar el detalle exacto del error
    if (error.response?.data) {
      console.error('❌ Detalles del error del servidor:', JSON.stringify(error.response.data, null, 2));
    }
    
    // Detección específica del error de nombre duplicado
    if (error.response?.data?.non_field_errors?.length > 0 && 
        error.response.data.non_field_errors[0].includes('existe un puesto con este nombre')) {
      throw new Error('Ya existe un puesto con este nombre en el departamento seleccionado');
    }
    
    // Otros casos de error
    if (error.response?.data?.nombre) {
      throw new Error(error.response.data.nombre[0]);
    } else if (error.response?.data?.departamento_id) {
      throw new Error(error.response.data.departamento_id[0]);
    } else if (error.response?.data?.non_field_errors) {
      throw new Error(error.response.data.non_field_errors[0]);
    } else if (error.response?.data?.message) {
      throw new Error(error.response.data.message);
    } else if (error.response?.status === 400) {
      throw new Error('Error al actualizar el puesto. Verifique que el nombre no esté duplicado en el departamento.');
    }
    throw new Error('Error al actualizar el puesto');
  }
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
