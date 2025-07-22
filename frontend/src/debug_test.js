// Test para verificar los problemas reportados
console.log('=== DIAGNÓSTICO DE PROBLEMAS EN ADMIN EMPRESA ===');

// 1. Verificar localStorage para token de autenticación
console.log('1. Token de autenticación:');
const token = localStorage.getItem('authToken');
const userData = localStorage.getItem('userData');
console.log('Token:', token ? 'Presente' : 'Ausente');
console.log('UserData:', userData ? JSON.parse(userData) : 'Ausente');

// 2. Verificar endpoints
const endpoints = [
    'http://localhost:8000/api/plantas/',
    'http://localhost:8000/api/departamentos/',
    'http://localhost:8000/api/puestos/',
    'http://localhost:8000/api/empleados/'
];

endpoints.forEach(async (endpoint) => {
    try {
        const response = await fetch(endpoint, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': token ? `Token ${token}` : ''
            }
        });
        console.log(`${endpoint}: ${response.status} ${response.statusText}`);
        if (!response.ok) {
            const errorText = await response.text();
            console.log(`Error: ${errorText}`);
        }
    } catch (error) {
        console.error(`Error en ${endpoint}:`, error);
    }
});
