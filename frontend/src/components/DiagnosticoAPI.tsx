import React, { useState } from 'react';
import { evaluacionesOficialesAPI } from '../services/evaluacionesOficialesAPI';

const DiagnosticoAPI: React.FC = () => {
  const [resultado, setResultado] = useState<string>('');
  const [loading, setLoading] = useState(false);

  const probarConexion = async () => {
    setLoading(true);
    setResultado('🔄 Probando conexión...\n');
    
    try {
      // Probar GET
      setResultado(prev => prev + '📥 Probando GET preguntas NOM-035...\n');
      const preguntas = await evaluacionesOficialesAPI.getPreguntasPorNormativa('nom_035');
      setResultado(prev => prev + `✅ GET exitoso: ${preguntas.total_preguntas} preguntas encontradas\n\n`);
      
      // Probar POST
      setResultado(prev => prev + '📤 Probando POST nueva pregunta...\n');
      const nuevaPregunta = await evaluacionesOficialesAPI.crearPregunta({
        texto: "¿Pregunta de diagnóstico?",
        tipo: "multiple",
        opciones: ["Sí", "No"],
        obligatoria: true,
        normativa: "nom_035"
      });
      
      setResultado(prev => prev + `✅ POST exitoso: Pregunta creada con ID ${nuevaPregunta.id}\n`);
      setResultado(prev => prev + `📋 Detalles: ${JSON.stringify(nuevaPregunta, null, 2)}\n`);
      
    } catch (error) {
      setResultado(prev => prev + `❌ Error: ${error}\n`);
      console.error('Error en diagnóstico:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ padding: '20px', fontFamily: 'monospace' }}>
      <h2>🧪 Diagnóstico de API - Evaluaciones Oficiales</h2>
      
      <button 
        onClick={probarConexion} 
        disabled={loading}
        style={{
          padding: '10px 20px',
          backgroundColor: loading ? '#ccc' : '#007bff',
          color: 'white',
          border: 'none',
          borderRadius: '4px',
          cursor: loading ? 'not-allowed' : 'pointer'
        }}
      >
        {loading ? '🔄 Probando...' : '🚀 Probar Conexión API'}
      </button>
      
      <div style={{
        marginTop: '20px',
        padding: '15px',
        backgroundColor: '#f8f9fa',
        border: '1px solid #dee2e6',
        borderRadius: '4px',
        whiteSpace: 'pre-wrap',
        fontFamily: 'Monaco, monospace',
        fontSize: '12px',
        maxHeight: '400px',
        overflowY: 'auto'
      }}>
        {resultado || 'Haz clic en "Probar Conexión API" para comenzar...'}
      </div>
      
      <div style={{ marginTop: '15px', fontSize: '12px', color: '#666' }}>
        <p><strong>URLs de API:</strong></p>
        <ul>
          <li>GET: http://localhost:8000/api/evaluaciones/oficial/normativa/nom_035/</li>
          <li>POST: http://localhost:8000/api/evaluaciones/oficial/preguntas-oficiales/</li>
        </ul>
        <p><strong>Nota:</strong> Abre las herramientas de desarrollador (F12) para ver logs detallados.</p>
      </div>
    </div>
  );
};

export default DiagnosticoAPI;
