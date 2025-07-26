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

// Quitar "api/" del contexto ya que api.ts ya lo incluye
const context = "auth/";

// Nuevo método para obtener usuarios de prueba
export const getTestUsers = async (): Promise<any> => {
  try {
    const response = await api.get(`${context}test-users/`);
    return response.data;
  } catch (error) {
    console.error("Error al obtener usuarios de prueba:", error);
    return {
      users: [
        { username: "superadmin", password: "1234", role: "SuperAdmin" },
        { username: "admin_empresa", password: "1234", role: "Admin Empresa" },
        { username: "admin_planta", password: "1234", role: "Admin Planta" }
      ]
    };
  }
};

export const login = async (data: LoginData): Promise<LoginResponse> => {
  try {
    // Limpiar y sanitizar los datos de entrada
    const cleanData = {
      username: data.username.trim().toLowerCase(),
      password: data.password
    };
    
    console.log("🔄 Intentando inicio de sesión con:", cleanData.username);
    
    // Corrección de tipos de usuario comunes
    if (cleanData.username.includes('admin planta')) {
      cleanData.username = 'admin_planta';
      console.log("🔄 Corrigiendo nombre de usuario a:", cleanData.username);
    } else if (cleanData.username.includes('admin empresa')) {
      cleanData.username = 'admin_empresa';
      console.log("🔄 Corrigiendo nombre de usuario a:", cleanData.username);
    } else if (cleanData.username.includes('super admin')) {
      cleanData.username = 'superadmin';
      console.log("🔄 Corrigiendo nombre de usuario a:", cleanData.username);
    }
    
    const response = await api.post<LoginResponse>(`${context}login/`, cleanData);
    
    console.log("✅ Respuesta recibida:", response.data);
    
    // Validar que la respuesta contiene un tipo de usuario válido
    const tipoUsuario = response.data.nivel_usuario?.toLowerCase();
    if (!tipoUsuario || 
        !['superadmin', 'admin_empresa', 'admin-empresa', 'admin_planta', 'admin-planta', 'empleado']
          .includes(tipoUsuario)) {
      console.warn("⚠️ Tipo de usuario inválido recibido:", tipoUsuario);
      throw new Error(`Tipo de usuario no válido: ${response.data.nivel_usuario}`);
    }
    
    // Guardar el token en localStorage para futuras requests
    if (response.data.token) {
      localStorage.setItem('authToken', response.data.token);
      console.log("🔑 Token guardado en localStorage");
      
      // También guardar el tipo de usuario para diagnóstico
      localStorage.setItem('userType', tipoUsuario);
    } else {
      console.warn("⚠️ No se recibió token en la respuesta");
    }
    
    return response.data;
  } catch (error: any) {
    console.error("❌ Error durante el inicio de sesión:", error);
    
    // Extraer mensaje de error detallado
    let errorMessage = "Error al iniciar sesión";
    
    if (error.response) {
      console.error("📝 Detalles del error:", error.response.data);
      if (error.response.status === 401) {
        errorMessage = "Credenciales incorrectas. Verifica tu usuario y contraseña.";
      } else {
        errorMessage = error.response.data?.detail || 
                      error.response.data?.message || 
                      error.response.data?.error ||
                      "Error en la autenticación";
      }
    } else if (error.request) {
      errorMessage = "No se pudo conectar con el servidor. Verifica tu conexión.";
    }
    
    throw new Error(errorMessage);
  }
};

export const logout = () => {
  console.log("🚪 Cerrando sesión y limpiando datos locales");
  localStorage.removeItem('authToken');
  localStorage.removeItem('token'); // Para compatibilidad
  localStorage.removeItem('empresaData');
  localStorage.removeItem('userData');
};
