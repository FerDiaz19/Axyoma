import axios from 'axios';

// Forzar valor de puerto para evitar problemas de caché
const API_PORT = 8000;
// Cambiar API_URL para no incluir /api al final (será añadido en los servicios)
const API_URL = `http://localhost:${API_PORT}/api`;

// Log para confirmar la URL correcta
console.log(`🌐 Configurando API para conectarse a: ${API_URL}`);

const api = axios.create({
    baseURL: API_URL,
    headers: {
        'Content-Type': 'application/json; charset=utf-8',
        'Accept': 'application/json',
    },
    transformRequest: [(data) => {
        // Solo convertir a JSON si hay datos y no son ya un string
        if (data && typeof data !== 'string') {
            return JSON.stringify(data);
        }
        return data;
    }],
});

// Interceptor para agregar token de autenticación
api.interceptors.request.use((config) => {
    const token = localStorage.getItem('authToken');
    if (token) {
        config.headers.Authorization = `Token ${token}`;
        console.log(`🔑 Enviando petición autenticada a: ${config.url}`);
    } else {
        console.log(`📡 Enviando petición sin autenticación a: ${config.url}`);
    }
    return config;
});

// Interceptor para manejar errores de autenticación
api.interceptors.response.use(
    (response) => response,
    (error) => {
        console.error('❌ Error en petición API:', error.message);
        
        // Solo para depuración - ver detalles completos del error
        if (error.config) {
            // Corregir la URL para mostrarla correctamente (agregando / entre api y el endpoint)
            const url = error.config.url || '';
            const baseURL = error.config.baseURL || '';
            const fullURL = baseURL + (url.startsWith('/') ? url : `/${url}`);
            console.error(`📌 URL: ${fullURL}`);
            console.error(`📌 Método: ${error.config.method?.toUpperCase()}`);
        }

        // Manejar error 401, pero no durante el login
        if (error.response?.status === 401) {
            // Verificar si es una petición de login
            const isLoginRequest = error.config.url?.includes('login');
            
            if (!isLoginRequest) {
                console.warn('🔒 Error 401: Token inválido o expirado');
                localStorage.removeItem('authToken');
                localStorage.removeItem('userData');
                // Recargar solo si no estamos en login
                if (!window.location.pathname.includes('login')) {
                    window.location.reload();
                }
            } else {
                console.warn('🔒 Error 401: Credenciales de login incorrectas');
            }
        }
        
        // Error de conexión - posiblemente servidor apagado
        if (error.message === 'Network Error') {
            console.error('🔌 Error de conexión: No se pudo conectar al servidor');
            console.error(`🔌 Verifica que el servidor esté corriendo en ${API_URL}`);
        }
        
        return Promise.reject(error);
    }
);

export default api;