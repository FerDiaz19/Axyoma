import api from '../api';

// Types
export interface RegistroEmpresaData {
  nombre: string;
  rfc: string;
  direccion: string;
  email_contacto: string;
  telefono_contacto: string;
  usuario: string;
  password: string;
  nombre_completo: string;
}

export interface RegistroEmpresaResponse {
  message: string;
  empresa_id: number;
  nombre: string;
  siguiente_paso: string;
  mensaje_siguiente: string;
  requiere_suscripcion: boolean;
}

export const registrarEmpresa = async (data: RegistroEmpresaData): Promise<RegistroEmpresaResponse> => {
  try {
    console.log('🔄 Registrando empresa:', data.nombre);
    const response = await api.post<RegistroEmpresaResponse>('/empresas/registro/', data);
    console.log('✅ Empresa registrada exitosamente:', response.data);
    return response.data;
  } catch (error: any) {
    console.error('❌ Error registrando empresa:', error);
    
    // Mejorar el manejo de errores específicos
    if (error.response?.status === 400) {
      const errorData = error.response.data;
      
      // Error de email duplicado
      if (errorData.detail?.includes('duplicate key value violates unique constraint "usuarios_correo_key"') ||
          errorData.error?.includes('correo') ||
          errorData.detail?.includes('already exists')) {
        throw new Error('Ya existe una cuenta con este correo electrónico. Por favor use un email diferente o inicie sesión si ya tiene una cuenta.');
      }
      
      // Error de usuario duplicado
      if (errorData.non_field_errors?.some((err: string) => err.includes('usuario ya existe')) ||
          errorData.error?.includes('usuario')) {
        throw new Error('El nombre de usuario ya está en uso. Por favor elija un nombre de usuario diferente.');
      }
      
      // Error de RFC duplicado
      if (errorData.error?.includes('RFC') || errorData.rfc) {
        throw new Error('Ya existe una empresa registrada con este RFC.');
      }
      
      // Otros errores de validación
      if (errorData.non_field_errors && Array.isArray(errorData.non_field_errors)) {
        throw new Error(errorData.non_field_errors[0]);
      }
      
      // Error genérico de validación
      if (errorData.error) {
        throw new Error(errorData.error);
      }
    }
    
    // Error de conexión
    if (error.code === 'NETWORK_ERROR' || error.message === 'Network Error') {
      throw new Error('Error de conexión. Verifique su conexión a internet y que el servidor esté funcionando.');
    }
    
    // Error genérico
    throw new Error('Error al registrar la empresa. Por favor intente nuevamente o contacte al soporte técnico.');
  }
};
