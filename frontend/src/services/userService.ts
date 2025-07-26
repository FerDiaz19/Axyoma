import api from '../api';

// Interfaz para el perfil de usuario
export interface UserProfile {
  profile_id?: number;
  user_id?: number;
  nombre_completo?: string;
  empresa_id?: number;
  empresa_nombre?: string;
  planta_id?: number;
  planta_nombre?: string;
  nivel_usuario?: string;
  permisos?: string[];
}

/**
 * Obtiene el perfil completo de un usuario por su ID
 */
export const obtenerPerfilUsuario = async (userId: number): Promise<UserProfile | null> => {
  try {
    console.log(`🔍 Obteniendo perfil para usuario ID: ${userId}`);
    const response = await api.get(`/users/perfil/${userId}/`);
    console.log('✅ Perfil obtenido:', response.data);
    return response.data;
  } catch (error) {
    console.error('❌ Error al obtener perfil de usuario:', error);
    return null;
  }
};

/**
 * Obtiene el ID de la empresa asociada al usuario actual
 */
export const obtenerEmpresaIdUsuarioActual = async (): Promise<number | null> => {
  try {
    console.log('🔍 Obteniendo empresa ID para usuario actual');
    const response = await api.get('/users/mi-empresa/');
    console.log('✅ Empresa ID obtenido:', response.data.empresa_id);
    
    // Guardar en localStorage para futuras referencias
    if (response.data.empresa_id) {
      localStorage.setItem('empresaId', response.data.empresa_id.toString());
    }
    
    return response.data.empresa_id;
  } catch (error) {
    console.error('❌ Error al obtener empresa ID:', error);
    return null;
  }
};

export default {
  obtenerPerfilUsuario,
  obtenerEmpresaIdUsuarioActual
};
