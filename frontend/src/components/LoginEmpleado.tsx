import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

// Componente de card simple
const Card = ({ children, className = '' }: { children: React.ReactNode; className?: string }) => (
  <div className={`bg-white rounded-lg shadow-lg ${className}`}>{children}</div>
);

const CardHeader = ({ children, className = '' }: { children: React.ReactNode; className?: string }) => (
  <div className={`p-6 border-b ${className}`}>{children}</div>
);

const CardTitle = ({ children, className = '' }: { children: React.ReactNode; className?: string }) => (
  <h2 className={`text-xl font-semibold ${className}`}>{children}</h2>
);

const CardContent = ({ children, className = '' }: { children: React.ReactNode; className?: string }) => (
  <div className={`p-6 ${className}`}>{children}</div>
);

const Button = ({ 
  children, 
  onClick, 
  disabled = false, 
  type = 'button',
  className = '' 
}: {
  children: React.ReactNode;
  onClick?: () => void;
  disabled?: boolean;
  type?: 'button' | 'submit';
  className?: string;
}) => (
  <button 
    type={type}
    onClick={onClick}
    disabled={disabled}
    className={`w-full bg-blue-600 text-white py-3 px-4 rounded-lg font-medium hover:bg-blue-700 disabled:bg-gray-300 disabled:cursor-not-allowed transition-colors ${className}`}
  >
    {children}
  </button>
);

const Badge = ({ 
  children, 
  variant = 'default', 
  className = '' 
}: {
  children: React.ReactNode;
  variant?: 'default' | 'secondary' | 'outline' | 'destructive';
  className?: string;
}) => {
  const variants = {
    default: 'bg-blue-100 text-blue-800',
    secondary: 'bg-gray-100 text-gray-800',
    outline: 'border border-green-300 text-green-800 bg-green-50',
    destructive: 'bg-red-100 text-red-800'
  };
  
  return (
    <span className={`inline-flex items-center px-3 py-1 rounded-full text-sm font-medium ${variants[variant]} ${className}`}>
      {children}
    </span>
  );
};

// Iconos SVG
const User = ({ className = '' }: { className?: string }) => (
  <svg className={className} fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
  </svg>
);

const Building = ({ className = '' }: { className?: string }) => (
  <svg className={className} fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
  </svg>
);

const Calendar = ({ className = '' }: { className?: string }) => (
  <svg className={className} fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
  </svg>
);

const CheckCircle = ({ className = '' }: { className?: string }) => (
  <svg className={className} fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
  </svg>
);

interface EmpleadoData {
  id: number;
  nombre: string;
  apellido: string;
  numero_empleado: string;
  departamento: string;
  planta: string;
}

interface EvaluacionData {
  id: number;
  titulo: string;
  descripcion: string;
  fecha_fin: string;
}

interface AsignacionData {
  id: number;
  estado: string;
  fecha_inicio: string;
  fecha_fin: string;
}

interface TokenValidationResponse {
  valid: boolean;
  empleado?: EmpleadoData;
  evaluacion?: EvaluacionData;
  asignacion?: AsignacionData;
  error?: string;
}

const LoginEmpleado: React.FC = () => {
  const [token, setToken] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [empleadoData, setEmpleadoData] = useState<EmpleadoData | null>(null);
  const [evaluacionData, setEvaluacionData] = useState<EvaluacionData | null>(null);
  const [asignacionData, setAsignacionData] = useState<AsignacionData | null>(null);
  const navigate = useNavigate();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!token.trim()) {
      setError('Por favor ingrese un token válido');
      return;
    }

    setLoading(true);
    setError('');

    try {
      const response = await fetch('/api/evaluaciones/tokens/validar_token/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          token: token.trim()
        }),
      });

      const data: TokenValidationResponse = await response.json();

      if (response.ok && data.valid) {
        // Token válido, mostrar información del empleado
        setEmpleadoData(data.empleado || null);
        setEvaluacionData(data.evaluacion || null);
        setAsignacionData(data.asignacion || null);
        
        // Guardar token en localStorage para futuras consultas
        localStorage.setItem('empleado_token', token.trim());
        
        // Aquí podrías redirigir a la página de evaluación
        // navigate('/evaluacion');
      } else {
        setError(data.error || 'Token inválido o expirado');
      }
    } catch (error) {
      console.error('Error al validar token:', error);
      setError('Error de conexión. Intente nuevamente.');
    } finally {
      setLoading(false);
    }
  };

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('es-ES', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  const getEstadoBadge = (estado: string) => {
    const badges = {
      'pendiente': { variant: 'secondary' as const, text: 'Pendiente' },
      'en_progreso': { variant: 'default' as const, text: 'En Progreso' },
      'completada': { variant: 'outline' as const, text: 'Completada' },
      'expirada': { variant: 'destructive' as const, text: 'Expirada' },
    };
    
    const badgeInfo = badges[estado as keyof typeof badges] || { variant: 'default' as const, text: estado };
    return <Badge variant={badgeInfo.variant}>{badgeInfo.text}</Badge>;
  };

  return (
    <div className="min-h-screen bg-gray-100 flex items-center justify-center p-4">
      <div className="w-full max-w-md">
        <Card>
          <CardHeader className="text-center">
            <div className="mx-auto w-16 h-16 bg-blue-100 rounded-full flex items-center justify-center mb-4">
              <User className="w-8 h-8 text-blue-600" />
            </div>
            <CardTitle>Acceso de Empleado</CardTitle>
            <p className="text-gray-600 mt-2">
              Ingrese el token proporcionado para acceder a su evaluación
            </p>
          </CardHeader>

          <CardContent>
            {!empleadoData ? (
              <form onSubmit={handleSubmit} className="space-y-4">
                <div>
                  <label htmlFor="token" className="block text-sm font-medium text-gray-700 mb-2">
                    Token de Acceso
                  </label>
                  <input
                    id="token"
                    type="text"
                    value={token}
                    onChange={(e) => setToken(e.target.value)}
                    placeholder="Ingrese su token aquí..."
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    disabled={loading}
                  />
                </div>

                {error && (
                  <div className="p-3 bg-red-50 border border-red-200 rounded-lg">
                    <p className="text-red-700 text-sm">{error}</p>
                  </div>
                )}

                <Button type="submit" disabled={loading}>
                  {loading ? 'Validando...' : 'Acceder'}
                </Button>

                <div className="text-center">
                  <button
                    type="button"
                    onClick={() => navigate('/')}
                    className="text-blue-600 hover:text-blue-800 text-sm"
                  >
                    Volver al inicio
                  </button>
                </div>
              </form>
            ) : (
              <div className="space-y-6">
                {/* Información del empleado */}
                <div className="bg-green-50 border border-green-200 rounded-lg p-4">
                  <div className="flex items-center gap-2 mb-3">
                    <CheckCircle className="w-5 h-5 text-green-600" />
                    <h3 className="font-medium text-green-800">Token Válido</h3>
                  </div>
                  <p className="text-green-700 text-sm">
                    Bienvenido, su token ha sido validado correctamente.
                  </p>
                </div>

                {/* Datos del empleado */}
                <div className="space-y-4">
                  <div className="flex items-center gap-3 p-3 bg-gray-50 rounded-lg">
                    <User className="w-5 h-5 text-gray-600" />
                    <div>
                      <p className="font-medium">
                        {empleadoData.nombre} {empleadoData.apellido}
                      </p>
                      <p className="text-sm text-gray-600">
                        Empleado #{empleadoData.numero_empleado}
                      </p>
                    </div>
                  </div>

                  <div className="flex items-center gap-3 p-3 bg-gray-50 rounded-lg">
                    <Building className="w-5 h-5 text-gray-600" />
                    <div>
                      <p className="font-medium">{empleadoData.departamento}</p>
                      <p className="text-sm text-gray-600">
                        Planta: {empleadoData.planta}
                      </p>
                    </div>
                  </div>
                </div>

                {/* Información de la evaluación */}
                {evaluacionData && (
                  <div className="border-t pt-4">
                    <h4 className="font-medium mb-3">Evaluación Asignada</h4>
                    <div className="space-y-3">
                      <div className="p-3 bg-blue-50 rounded-lg">
                        <p className="font-medium text-blue-900">
                          {evaluacionData.titulo}
                        </p>
                        <p className="text-sm text-blue-700 mt-1">
                          {evaluacionData.descripcion}
                        </p>
                      </div>

                      {asignacionData && (
                        <div className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                          <div className="flex items-center gap-2">
                            <Calendar className="w-4 h-4 text-gray-600" />
                            <span className="text-sm text-gray-700">
                              Fecha límite: {formatDate(asignacionData.fecha_fin)}
                            </span>
                          </div>
                          {getEstadoBadge(asignacionData.estado)}
                        </div>
                      )}
                    </div>
                  </div>
                )}

                {/* Botones de acción */}
                <div className="space-y-2">
                  <Button
                    onClick={() => {
                      // Aquí irías a la página de evaluación
                      alert('Funcionalidad de evaluación será implementada próximamente');
                    }}
                    className="bg-green-600 hover:bg-green-700"
                  >
                    Iniciar Evaluación
                  </Button>
                  
                  <button
                    onClick={() => {
                      setEmpleadoData(null);
                      setEvaluacionData(null);
                      setAsignacionData(null);
                      setToken('');
                      localStorage.removeItem('empleado_token');
                    }}
                    className="w-full text-gray-600 hover:text-gray-800 text-sm py-2"
                  >
                    Usar otro token
                  </button>
                </div>
              </div>
            )}
          </CardContent>
        </Card>

        {/* Información adicional */}
        <div className="mt-6 text-center">
          <p className="text-sm text-gray-600">
            ¿Tienes problemas con tu token?{' '}
            <span className="text-blue-600">
              Contacta a tu administrador de planta
            </span>
          </p>
        </div>
      </div>
    </div>
  );
};

export default LoginEmpleado;
