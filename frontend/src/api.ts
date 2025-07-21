import axios from 'axios';

const api = axios.create({
    baseURL: 'http://localhost:8000/api',
    headers: {
        'Content-Type': 'application/json; charset=utf-8',
        'Accept': 'application/json',
    },
    transformRequest: [function (data, headers) {
        // Solo transformar si hay data (no aplica a GET requests)
        if (data) {
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
    }
    return config;
});

// Interceptor para manejar errores de autenticación
api.interceptors.response.use(
    (response) => response,
    (error) => {
        if (error.response?.status === 401) {
            // Token inválido o expirado
            console.warn('Token de autenticación inválido o expirado');
            localStorage.removeItem('authToken');
            localStorage.removeItem('userData');
            // Recargar la página para forzar el login
            window.location.reload();
        }
        return Promise.reject(error);
    }
);

export default api;