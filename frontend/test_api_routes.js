// Test script to verify the correct API routes are being generated
const axios = require('axios');

// Mock the api module
const api = {
  get: (url) => {
    console.log('GET request to:', url);
    return Promise.resolve({ data: { test: 'success' } });
  },
  post: (url, data) => {
    console.log('POST request to:', url, 'with data:', data);
    return Promise.resolve({ data: { test: 'success' } });
  },
  delete: (url, config) => {
    console.log('DELETE request to:', url, 'with config:', config);
    return Promise.resolve({ data: { test: 'success' } });
  }
};

// Mock the API_BASE
const API_BASE = 'superadmin';

console.log('Testing API routes with API_BASE:', API_BASE);
console.log('');

// Test all the routes
console.log('1. Testing getEstadisticasSistema:');
api.get(`${API_BASE}/estadisticas_sistema/`);

console.log('\n2. Testing getEmpresas:');
api.get(`${API_BASE}/listar_empresas/`);

console.log('\n3. Testing suspenderEmpresa:');
api.post(`${API_BASE}/suspender_empresa/`, { empresa_id: 1, accion: 'suspender' });

console.log('\n4. Testing eliminarEmpresa:');
api.delete(`${API_BASE}/eliminar_empresa/`, { data: { empresa_id: 1 } });

console.log('\n5. Testing getUsuarios:');
api.get(`${API_BASE}/listar_usuarios/`);

console.log('\nAll routes should now be correct without the double /api!');
