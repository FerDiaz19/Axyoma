import React, { useState, useEffect } from 'react';
import axios from 'axios';

interface TokenData {
  token: string;
  activo: boolean;
  usado: boolean;
  fecha_expiracion: string;
}

interface EmpleadoData {
  id: number;
  nombre: string;
  departamento: string;
  puesto: string;
}

interface AsignacionData {
  id: number;
  empleado: EmpleadoData;
  estado: string;
  fecha_asignacion: string;
  token: TokenData | null;
}

interface EvaluacionActiva {
  evaluacion: {
    id: number;
    titulo: string;
    descripcion: string;
    estado: string;
    fecha_inicio: string;
    fecha_fin: string;
    tiempo_restante: string;
  };
  asignaciones: AsignacionData[];
  total_empleados: number;
  completadas: number;
  pendientes: number;
}

const EvaluacionesActivas: React.FC = () => {
  const [evaluaciones, setEvaluaciones] = useState<EvaluacionActiva[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  const cargarEvaluacionesActivas = async () => {
    try {
      setLoading(true);
      setError('');
      
      console.log('🔄 Cargando evaluaciones activas...');
      
      const token = localStorage.getItem('authToken');
      if (!token) {
        throw new Error('No hay token de autenticación');
      }
      
      const response = await axios.get('http://localhost:8000/api/evaluaciones/asignaciones/evaluaciones_activas/', {
        headers: {
          'Authorization': `Token ${token}`,
          'Content-Type': 'application/json'
        }
      });
      
      console.log('✅ Evaluaciones activas cargadas:', response.data);
      setEvaluaciones(response.data.evaluaciones_activas || []);
      
    } catch (error: any) {
      console.error('❌ Error al cargar evaluaciones activas:', error);
      console.error('❌ Error response:', error.response?.data);
      console.error('❌ Error status:', error.response?.status);
      
      let errorMessage = 'Error al cargar las evaluaciones activas';
      if (error.response?.status === 500) {
        errorMessage = 'Error del servidor al cargar evaluaciones activas';
      } else if (error.response?.status === 403) {
        errorMessage = 'Sin permisos para ver evaluaciones activas';
      }
      
      setError(errorMessage);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    cargarEvaluacionesActivas();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const copiarToken = (token: string) => {
    navigator.clipboard.writeText(token);
    alert('Token copiado al portapapeles');
  };

  const getEstadoColor = (estado: string) => {
    switch (estado) {
      case 'pendiente': return 'bg-yellow-100 text-yellow-800';
      case 'en_progreso': return 'bg-blue-100 text-blue-800';
      case 'completada': return 'bg-green-100 text-green-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  const getTiempoColor = (tiempo: string) => {
    if (tiempo === 'Expirada') return 'text-red-600 font-bold';
    if (tiempo.includes('0 días')) return 'text-orange-600 font-semibold';
    return 'text-gray-700';
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center h-64">
        <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-red-50 border border-red-200 rounded-lg p-4">
        <p className="text-red-700">{error}</p>
        <button 
          onClick={cargarEvaluacionesActivas}
          className="mt-2 bg-red-600 text-white px-4 py-2 rounded hover:bg-red-700"
        >
          Reintentar
        </button>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h2 className="text-2xl font-bold text-gray-900">Evaluaciones Activas</h2>
        <button
          onClick={cargarEvaluacionesActivas}
          className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700"
        >
          Actualizar
        </button>
      </div>

      {evaluaciones.length === 0 ? (
        <div className="text-center py-12">
          <div className="text-gray-500 text-lg">No hay evaluaciones activas</div>
          <p className="text-gray-400 mt-2">Las evaluaciones aparecerán aquí cuando se asignen a empleados</p>
        </div>
      ) : (
        <div className="space-y-6">
          {evaluaciones.map((evaluacionData, index) => (
            <div key={evaluacionData.evaluacion.id} className="bg-white rounded-lg shadow-lg border border-gray-200">
              {/* Header de la evaluación */}
              <div className="bg-gradient-to-r from-blue-600 to-blue-700 text-white p-6 rounded-t-lg">
                <div className="flex justify-between items-start">
                  <div>
                    <h3 className="text-xl font-bold">{evaluacionData.evaluacion.titulo}</h3>
                    <p className="text-blue-100 mt-1">{evaluacionData.evaluacion.descripcion}</p>
                  </div>
                  <div className="text-right">
                    <div className={`text-lg font-semibold ${getTiempoColor(evaluacionData.evaluacion.tiempo_restante)}`}>
                      {evaluacionData.evaluacion.tiempo_restante}
                    </div>
                    <div className="text-blue-100 text-sm">tiempo restante</div>
                  </div>
                </div>
                
                {/* Estadísticas */}
                <div className="grid grid-cols-3 gap-4 mt-4 pt-4 border-t border-blue-500">
                  <div className="text-center">
                    <div className="text-2xl font-bold">{evaluacionData.total_empleados}</div>
                    <div className="text-blue-100 text-sm">Total empleados</div>
                  </div>
                  <div className="text-center">
                    <div className="text-2xl font-bold text-green-300">{evaluacionData.completadas}</div>
                    <div className="text-blue-100 text-sm">Completadas</div>
                  </div>
                  <div className="text-center">
                    <div className="text-2xl font-bold text-yellow-300">{evaluacionData.pendientes}</div>
                    <div className="text-blue-100 text-sm">Pendientes</div>
                  </div>
                </div>
              </div>

              {/* Lista de asignaciones */}
              <div className="p-6">
                <h4 className="text-lg font-semibold text-gray-900 mb-4">Empleados Asignados</h4>
                
                <div className="overflow-x-auto">
                  <table className="min-w-full divide-y divide-gray-200">
                    <thead className="bg-gray-50">
                      <tr>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                          Empleado
                        </th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                          Departamento
                        </th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                          Estado
                        </th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                          Token de Acceso
                        </th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                          Acciones
                        </th>
                      </tr>
                    </thead>
                    <tbody className="bg-white divide-y divide-gray-200">
                      {evaluacionData.asignaciones.map((asignacion) => (
                        <tr key={asignacion.id} className="hover:bg-gray-50">
                          <td className="px-6 py-4 whitespace-nowrap">
                            <div>
                              <div className="text-sm font-medium text-gray-900">
                                {asignacion.empleado.nombre}
                              </div>
                              <div className="text-sm text-gray-500">
                                {asignacion.empleado.puesto}
                              </div>
                            </div>
                          </td>
                          <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                            {asignacion.empleado.departamento}
                          </td>
                          <td className="px-6 py-4 whitespace-nowrap">
                            <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${getEstadoColor(asignacion.estado)}`}>
                              {asignacion.estado === 'pendiente' ? 'Pendiente' : 
                               asignacion.estado === 'en_progreso' ? 'En Progreso' : 
                               asignacion.estado === 'completada' ? 'Completada' : asignacion.estado}
                            </span>
                          </td>
                          <td className="px-6 py-4 whitespace-nowrap">
                            {asignacion.token ? (
                              <div className="flex items-center space-x-2">
                                <code className="bg-gray-100 px-2 py-1 rounded text-xs font-mono">
                                  {asignacion.token.token.substring(0, 12)}...
                                </code>
                                <div className="flex flex-col">
                                  <span className={`text-xs ${asignacion.token.activo ? 'text-green-600' : 'text-red-600'}`}>
                                    {asignacion.token.activo ? 'Activo' : 'Inactivo'}
                                  </span>
                                  <span className={`text-xs ${asignacion.token.usado ? 'text-blue-600' : 'text-gray-500'}`}>
                                    {asignacion.token.usado ? 'Usado' : 'Sin usar'}
                                  </span>
                                </div>
                              </div>
                            ) : (
                              <span className="text-gray-400 text-sm">Sin token</span>
                            )}
                          </td>
                          <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">
                            {asignacion.token && (
                              <button
                                onClick={() => copiarToken(asignacion.token!.token)}
                                className="text-blue-600 hover:text-blue-900 mr-3"
                              >
                                Copiar Token
                              </button>
                            )}
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default EvaluacionesActivas;
