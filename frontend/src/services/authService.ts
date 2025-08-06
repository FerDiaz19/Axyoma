
// -------------------------------------------------------------------------- //

import api from "../api";

// -------------------------------------------------------------------------- //

// Datos mandados a la API para realizar el inicio de sesión.
export interface LoginData {
    username: string;
    password: string;
}

// ! Cuidadito, no se estaban tomando todos los datos relevantes.
export interface LoginResponse {
    message: string; // Ej. 'Login exitoso'
    token: string;  // Token de autenticación (usado para peticiones a la API)

    usuario: string; // Nombre del usuario.
    user_id?: number; // ID del usuario.
    nivel_usuario: string; // Nivel del usuario.
    correo: string; // Correo del usuario... o de la empresa.

    nombre_completo: string; // Nombre completo del usuario.
    profile_id?: number; // ID del perfil del usuario.

    tipo_dashboard: string; // Tipo de dashboard a mostrar.

    // En caso de recibir un usuario admin-planta o admin-empresa.
    planta_id?: number; // ID de la planta que administra el usuario.
    nombre_planta?: string; // Nombre de la planta que se adninnistra.

    empresa_id?: number; // ID de la empresa que se administra.
    nombre_empresa?: string; /// Nombre de la empresa que se administra.
    empresa_suspendida?: boolean; // Indica si la empresa está suspendida.

    suscripcion: { // Información acerca de la suscripción.
        tiene_suscripcion: boolean;
        estado: string;
        mensaje: string;
        requiere_pago: boolean;
        dias_restantes: number;
        acceso_reportes: boolean;
    };

    permisos: string[]; // Permisos que posee el usuario.

    advertencia?: { // Informaicón sobre una advertencia dada.
        tipo: string;
        mensaje: string;
        detalles: string;
    };
}

// -------------------------------------------------------------------------- //

export const login = async (data: LoginData): Promise<LoginResponse> => {

    try { // Limpiar y sanitizar los datos de entrada.
        const cleanData = {
            username: data.username,
            password: data.password
        };

        console.log("🔄 Intentando inicio de sesión con: ", cleanData.username);

        // ------------------------------------------------------------------ //

        const response = await api.post<LoginResponse>('auth/login/', cleanData);
        console.log("✅ Respuesta recibida:", response.data);


        // Validación anterior para el tipo de usuario. Si bien, debería rehacer esta, ...
        // dado que se toma en varios puntos de la APP, vamo' a dejarlo como esta.
        const tipoUsuario = response.data.nivel_usuario?.toLowerCase();

        if (!tipoUsuario || ![ // WTF, ¿por qué pusieron 'empleado'? Esos bueyen ni siquiera son usuarios.
            'superadmin', 'admin_empresa', 'admin-empresa', 'admin_planta', 'admin-planta', 'empleado'
            ].includes(tipoUsuario)) {

            console.warn("⚠️ Tipo de usuario inválido recibido:", tipoUsuario);
            throw new Error(`Tipo de usuario no válido: ${response.data.nivel_usuario}`);
        }


        // Guardado de datos recibidos en el LocalStorage:
        if (response.data.token) {
            localStorage.setItem('authToken', response.data.token);
            localStorage.setItem('userType', tipoUsuario);
            localStorage.setItem('userData', JSON.stringify(response.data)); // Toda la info. completa.
            console.log("🔑 Token y datos de usuario guardados en localStorage");

        } else { console.warn("⚠️ No se recibió token en la respuesta"); }

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
    localStorage.removeItem('userType');
    localStorage.removeItem('userData');

    // Estos no son guardados aquí, quizá lo hacen en otra parte, ni idea.
    localStorage.removeItem('token'); // Para compatibilidade
    localStorage.removeItem('empresaData');
    localStorage.removeItem('plantaData');
    localStorage.clear();
};

// -------------------------------------------------------------------------- //
