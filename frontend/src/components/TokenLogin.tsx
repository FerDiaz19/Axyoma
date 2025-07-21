import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

// Configurar base URL para las llamadas API
const api = axios.create({
  baseURL: 'http://localhost:8000/api'
});

const TokenLogin: React.FC = () => {
  const [token, setToken] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!token.trim()) {
      setError('Por favor ingresa tu token de evaluación');
      return;
    }

    try {
      setLoading(true);
      setError('');
      
      // Validar token y obtener información de la evaluación
      const response = await api.post('/evaluaciones/validar-token/', {
        token: token.trim()
      });

      if (response.data.valido) {
        // Guardar información del token en localStorage
        localStorage.setItem('empleado_token', token.trim());
        localStorage.setItem('empleado_info', JSON.stringify(response.data.empleado));
        localStorage.setItem('evaluacion_info', JSON.stringify(response.data.evaluacion));
        
        // Redirigir a la evaluación
        navigate('/evaluacion');
      } else {
        setError('Token inválido o expirado. Verifica tu token.');
      }
    } catch (error: any) {
      console.error('Error al validar token:', error);
      if (error.response?.status === 404) {
        setError('Token no encontrado. Verifica que hayas ingresado correctamente tu token.');
      } else if (error.response?.status === 410) {
        setError('Token expirado. Contacta a tu administrador para obtener un nuevo token.');
      } else {
        setError('Error al validar el token. Intenta nuevamente.');
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col justify-center py-12 sm:px-6 lg:px-8">
      <div className="sm:mx-auto sm:w-full sm:max-w-md">
        <div className="text-center">
          <h2 className="mt-6 text-center text-3xl font-extrabold text-gray-900">
            Acceso a Evaluación
          </h2>
          <p className="mt-2 text-center text-sm text-gray-600">
            Ingresa tu token de evaluación para comenzar
          </p>
        </div>
      </div>

      <div className="mt-8 sm:mx-auto sm:w-full sm:max-w-md">
        <div className="bg-white py-8 px-4 shadow sm:rounded-lg sm:px-10">
          <form className="space-y-6" onSubmit={handleSubmit}>
            <div>
              <label htmlFor="token" className="block text-sm font-medium text-gray-700">
                Token de Evaluación
              </label>
              <div className="mt-1">
                <input
                  id="token"
                  name="token"
                  type="text"
                  required
                  value={token}
                  onChange={(e) => setToken(e.target.value)}
                  className="appearance-none block w-full px-3 py-2 border border-gray-300 rounded-md placeholder-gray-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                  placeholder="Ingresa tu token aquí"
                  maxLength={32}
                />
              </div>
              <p className="mt-2 text-xs text-gray-500">
                El token es una cadena de 32 caracteres que recibiste de tu administrador
              </p>
            </div>

            {error && (
              <div className="rounded-md bg-red-50 p-4">
                <div className="flex">
                  <div className="ml-3">
                    <h3 className="text-sm font-medium text-red-800">
                      Error de acceso
                    </h3>
                    <div className="mt-2 text-sm text-red-700">
                      <p>{error}</p>
                    </div>
                  </div>
                </div>
              </div>
            )}

            <div>
              <button
                type="submit"
                disabled={loading}
                className={`group relative w-full flex justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white ${
                  loading 
                    ? 'bg-gray-400 cursor-not-allowed' 
                    : 'bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500'
                }`}
              >
                {loading ? (
                  <>
                    <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                      <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                      <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                    </svg>
                    Validando...
                  </>
                ) : (
                  'Iniciar Evaluación'
                )}
              </button>
            </div>
          </form>

          <div className="mt-6">
            <div className="relative">
              <div className="absolute inset-0 flex items-center">
                <div className="w-full border-t border-gray-300" />
              </div>
              <div className="relative flex justify-center text-sm">
                <span className="px-2 bg-white text-gray-500">
                  ¿Problemas con tu token?
                </span>
              </div>
            </div>

            <div className="mt-6 text-center">
              <p className="text-sm text-gray-600">
                Contacta a tu administrador si tu token no funciona o ha expirado.
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default TokenLogin;
