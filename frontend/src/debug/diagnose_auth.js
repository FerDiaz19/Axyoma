// Script para diagnosticar problemas de autenticación

console.log("=== DIAGNÓSTICO DE AUTENTICACIÓN ===");

// 1. Verificar token en localStorage
const token = localStorage.getItem('authToken');
console.log("Token en localStorage:", token ? `${token.substring(0, 10)}...` : "NO ENCONTRADO");

// 2. Verificar userData en localStorage
const userData = localStorage.getItem('userData');
console.log("userData en localStorage:", userData ? JSON.parse(userData) : "NO ENCONTRADO");

// 3. Intentar hacer una request manual al endpoint
if (token) {
    fetch('http://localhost:8000/api/superadmin/estadisticas_sistema/', {
        method: 'GET',
        headers: {
            'Authorization': `Token ${token}`,
            'Content-Type': 'application/json; charset=utf-8',
            'Accept': 'application/json',
        },
    })
    .then(response => {
        console.log("Response status:", response.status);
        console.log("Response headers:", response.headers);
        return response.text();
    })
    .then(text => {
        console.log("Response body:", text);
    })
    .catch(error => {
        console.error("Error en request:", error);
    });
} else {
    console.log("No se puede hacer request - token no encontrado");
}

// 4. Verificar configuración de axios
import('../api.js').then(apiModule => {
    const api = apiModule.default;
    console.log("Configuración de API:");
    console.log("Base URL:", api.defaults.baseURL);
    console.log("Headers:", api.defaults.headers);
});
