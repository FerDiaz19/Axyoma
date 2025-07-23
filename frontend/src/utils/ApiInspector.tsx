import React, { useState } from 'react';
import api from '../api';

/**
 * Componente utilitario para inspeccionar respuestas de la API
 * Útil para desarrollo y depuración
 */
const ApiInspector: React.FC = () => {
  const [endpoint, setEndpoint] = useState('api/superadmin/listar_empresas/');
  const [method, setMethod] = useState('GET');
  const [params, setParams] = useState('');
  const [body, setBody] = useState('');
  const [response, setResponse] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    
    try {
      let apiResponse;
      const headers = { 'Content-Type': 'application/json' };
      
      // Procesar parámetros de consulta
      const queryParams = params ? 
        `?${params.split('&').map(p => p.trim()).join('&')}` : '';
      
      // Procesar body JSON si es necesario
      const jsonBody = body ? JSON.parse(body) : {};
      
      switch (method) {
        case 'GET':
          apiResponse = await api.get(`${endpoint}${queryParams}`);
          break;
        case 'POST':
          apiResponse = await api.post(endpoint, jsonBody, { headers });
          break;
        case 'PUT':
          apiResponse = await api.put(endpoint, jsonBody, { headers });
          break;
        case 'DELETE':
          apiResponse = await api.delete(endpoint, { data: jsonBody, headers });
          break;
        default:
          throw new Error('Método HTTP no soportado');
      }
      
      setResponse(apiResponse.data);
      console.log('✅ Respuesta API:', apiResponse.data);
    } catch (err: any) {
      console.error('❌ Error en solicitud API:', err);
      setError(err.message || 'Error desconocido');
      
      if (err.response) {
        console.error('Detalles del error:', err.response.data);
        setResponse(err.response.data);
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ padding: '20px', maxWidth: '1000px', margin: '0 auto' }}>
      <h2>🔍 Inspector de API AXYOMA</h2>
      
      <form onSubmit={handleSubmit} style={{ marginBottom: '20px' }}>
        <div style={{ display: 'flex', gap: '10px', marginBottom: '10px' }}>
          <select 
            value={method} 
            onChange={(e) => setMethod(e.target.value)}
            style={{ padding: '8px', width: '100px' }}
          >
            <option value="GET">GET</option>
            <option value="POST">POST</option>
            <option value="PUT">PUT</option>
            <option value="DELETE">DELETE</option>
          </select>
          
          <input
            type="text"
            value={endpoint}
            onChange={(e) => setEndpoint(e.target.value)}
            placeholder="URL del endpoint (ej: api/superadmin/listar_empresas/)"
            style={{ padding: '8px', flexGrow: 1 }}
          />
          
          <button 
            type="submit" 
            disabled={loading}
            style={{ padding: '8px 16px', background: '#4285f4', color: 'white', border: 'none', borderRadius: '4px' }}
          >
            {loading ? 'Enviando...' : 'Enviar'}
          </button>
        </div>
        
        <div style={{ display: 'flex', gap: '10px' }}>
          <div style={{ flexGrow: 1 }}>
            <label style={{ display: 'block', marginBottom: '5px' }}>
              Parámetros (formato: key1=value1&key2=value2)
            </label>
            <textarea
              value={params}
              onChange={(e) => setParams(e.target.value)}
              placeholder="buscar=texto&status=true"
              style={{ width: '100%', padding: '8px', height: '60px' }}
            />
          </div>
          
          <div style={{ flexGrow: 1 }}>
            <label style={{ display: 'block', marginBottom: '5px' }}>
              Cuerpo de la petición (JSON)
            </label>
            <textarea
              value={body}
              onChange={(e) => setBody(e.target.value)}
              placeholder='{"empresa_id": 1, "nombre": "Empresa Test"}'
              style={{ width: '100%', padding: '8px', height: '60px' }}
              disabled={method === 'GET'}
            />
          </div>
        </div>
      </form>
      
      {error && (
        <div style={{ padding: '10px', backgroundColor: '#ffebee', color: '#c62828', marginBottom: '20px', borderRadius: '4px' }}>
          <strong>Error:</strong> {error}
        </div>
      )}
      
      <div style={{ marginBottom: '20px' }}>
        <h3>Ejemplos rápidos:</h3>
        <div style={{ display: 'flex', flexWrap: 'wrap', gap: '10px' }}>
          <button 
            onClick={() => {
              setMethod('GET');
              setEndpoint('api/superadmin/listar_empresas/');
              setParams('');
              setBody('');
            }}
            style={{ padding: '5px 10px', background: '#e0e0e0', border: 'none', borderRadius: '4px' }}
          >
            Listar empresas
          </button>
          <button 
            onClick={() => {
              setMethod('GET');
              setEndpoint('api/superadmin/estadisticas_sistema/');
              setParams('');
              setBody('');
            }}
            style={{ padding: '5px 10px', background: '#e0e0e0', border: 'none', borderRadius: '4px' }}
          >
            Estadísticas
          </button>
          <button 
            onClick={() => {
              setMethod('GET');
              setEndpoint('api/superadmin/listar_usuarios/');
              setParams('');
              setBody('');
            }}
            style={{ padding: '5px 10px', background: '#e0e0e0', border: 'none', borderRadius: '4px' }}
          >
            Listar usuarios
          </button>
          <button 
            onClick={() => {
              setMethod('GET');
              setEndpoint('api/superadmin/listar_todas_plantas/');
              setParams('');
              setBody('');
            }}
            style={{ padding: '5px 10px', background: '#e0e0e0', border: 'none', borderRadius: '4px' }}
          >
            Listar plantas
          </button>
        </div>
      </div>
      
      <h3>Respuesta:</h3>
      <div style={{ 
        backgroundColor: '#f5f5f5', 
        padding: '10px', 
        borderRadius: '4px',
        maxHeight: '500px',
        overflowY: 'auto'
      }}>
        <pre style={{ margin: 0, whiteSpace: 'pre-wrap', fontSize: '14px' }}>
          {response !== null ? JSON.stringify(response, null, 2) : 'No hay respuesta aún'}
        </pre>
      </div>
      
      <div style={{ marginTop: '20px', fontSize: '12px', color: '#666' }}>
        <p>
          <strong>Nota:</strong> Esta herramienta es solo para propósitos de desarrollo y depuración.
          Utiliza las credenciales actuales de la sesión y respeta los permisos del usuario.
        </p>
      </div>
    </div>
  );
};

export default ApiInspector;
