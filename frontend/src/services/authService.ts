
// -------------------------------------------------------------------------- //

import api from "../api";

// -------------------------------------------------------------------------- //

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

// -------------------------------------------------------------------------- //

// Quitar "api/" del contexto ya que api.ts ya lo incluye
const context = "auth/";


// -------------------------------------------------------------------------- //

export const login = async (data: LoginData): Promise<LoginResponse> => {
    try { // Limpiar y sanitizar los datos de entrada.
        const cleanData = {
            username: data.username,
            password: data.password
        };

        console.log("🔄 Intentando inicio de sesión con: ", cleanData.username);

        // ------------------------------------------------------------------ //

        const response = await api.post<LoginResponse>(`${context}login/`, cleanData);
        console.log("✅ Respuesta recibida:", response.data);

        // Validar que la respuesta contiene un tipo de usuario válido
        const tipoUsuario = response.data.nivel_usuario?.toLowerCase();
        if (!tipoUsuario ||
            !['superadmin', 'admin_empresa', 'admin-empresa', 'admin_planta', 'admin-planta', 'empleado'].includes(tipoUsuario)) {
            console.warn("⚠️ Tipo de usuario inválido recibido:", tipoUsuario);
            throw new Error(`Tipo de usuario no válido: ${response.data.nivel_usuario}`);
        }

        // Guardar datos de sesión en localStorage
        if (response.data.token) {
            localStorage.setItem('authToken', response.data.token);
            localStorage.setItem('userType', tipoUsuario);
            localStorage.setItem('userData', JSON.stringify(response.data));
            console.log("🔑 Token y datos de usuario guardados en localStorage");
        } else {
            console.warn("⚠️ No se recibió token en la respuesta");
        }

        return response.data;
    } catch (error: any) {
        console.error("❌ Error durante el inicio de sesión: ", error);

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

// -------------------------------------------------------------------------- //

export const logout = () => {
    console.log("🚪 Cerrando sesión y limpiando datos locales");
    localStorage.removeItem('authToken');
    localStorage.removeItem('token'); // Para compatibilidad
    localStorage.removeItem('userType');
    localStorage.removeItem('userData');
    localStorage.removeItem('empresaData');
    localStorage.removeItem('plantaData');
    localStorage.clear(); // Limpiar todo por seguridad
};

// -------------------------------------------------------------------------- //