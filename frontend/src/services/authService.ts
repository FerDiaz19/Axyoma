import api from "../api";

// Types
export interface LoginData {
  username: string;
  password: string;
}

export interface LoginResponse {
  message: string;
  usuario: string;
  nivel_usuario: string;
  tipo_dashboard: string;
  permisos: string[];
  token: string;  // Token de autenticación
  empresa_id?: number;
  nombre_empresa?: string;
}

const context = "auth/";

export const login = async (data: LoginData): Promise<LoginResponse> => {
  const response = await api.post<LoginResponse>(`${context}login/`, data);
  
  // Guardar el token en localStorage para futuras requests
  if (response.data.token) {
    localStorage.setItem('authToken', response.data.token);
  }
  
  return response.data;
};

export const logout = () => {
  localStorage.removeItem('authToken');
  localStorage.removeItem('empresaData');
  localStorage.removeItem('userData');
};
