import React, { useState, useEffect } from 'react';
import { login } from '../services/authService';
import { findBackendServer } from '../utils/serverCheck';
import '../css/Login.css';

interface LoginProps {
  onLogin: (userData: any) => void;
}

const Login: React.FC<LoginProps> = ({ onLogin }) => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [serverStatus, setServerStatus] = useState<string>('checking');
  
  useEffect(() => {
    // Verificar estado del servidor al cargar el componente
    const checkServer = async () => {
      const port = await findBackendServer();
      if (port) {
        setServerStatus(`active-${port}`);
      } else {
        setServerStatus('inactive');
      }
    };
    
    checkServer();
  }, []);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      // Sanitizar username - eliminar espacios y convertir a minúsculas
      const sanitizedUsername = username.trim().toLowerCase();
      
      // Normalizar nombres de usuario conocidos
      let normalizedUsername = sanitizedUsername;
      if (sanitizedUsername === 'admin planta' || sanitizedUsername === 'admin-planta') {
        normalizedUsername = 'admin_planta';
      } else if (sanitizedUsername === 'admin empresa' || sanitizedUsername === 'admin-empresa') {
        normalizedUsername = 'admin_empresa';
      } else if (sanitizedUsername === 'super admin' || sanitizedUsername === 'superadmin') {
        normalizedUsername = 'superadmin';
      }
      
      console.log(`🔑 Intentando login con usuario normalizado: ${normalizedUsername}`);
      
      const userData = await login({ 
        username: normalizedUsername,
        password 
      });
      onLogin(userData);
    } catch (error: any) {
      setError(error.message || 'Error al iniciar sesión');
    } finally {
      setLoading(false);
    }
  };

  // Renderizar mensaje de error de servidor
  const renderServerStatus = () => {
    if (serverStatus === 'checking') {
      return (
        <div className="server-status checking">
          🔄 Verificando conexión con el servidor...
        </div>
      );
    } else if (serverStatus === 'inactive') {
      return (
        <div className="server-status error">
          ❌ No se pudo conectar al servidor backend. Por favor:
          <ul>
            <li>Verifica que el servidor Django esté ejecutándose</li>
            <li>Comprueba que el puerto 8000 esté disponible</li>
            <li>Verifica la consola de Django por posibles errores</li>
          </ul>
          <button 
            onClick={() => window.location.reload()}
            className="retry-button"
          >
            🔄 Reintentar conexión
          </button>
        </div>
      );
    } else if (serverStatus.startsWith('active-')) {
      const port = serverStatus.split('-')[1];
      return (
        <div className="server-status success">
          ✅ Conectado al servidor en puerto {port}
        </div>
      );
    }
    return null;
  };

  // Función auxiliar para establecer credenciales (renombrada para evitar error de ESLint)
  const applyTestCredential = (testUser: string, testPassword: string) => {
    setUsername(testUser);
    setPassword(testPassword);
    // Opcionalmente, hacer submit automáticamente
    // handleSubmit(new Event('submit') as any);
  };

  return (
    <div className="login-container">
      {/* Lado izquierdo - Imagen */}
      <div className="login-left">
        <div className="login-image-section">
          <div className="image-placeholder">
            <div className="brand-logo">
              <h1>🏢 AXYOMA</h1>
              <p>Plataforma Empresarial Profesional</p>
            </div>
            <div className="features-list">
              <div className="feature">
                <span>📊</span>
                <span>Gestión de Evaluaciones</span>
              </div>
              <div className="feature">
                <span>👥</span>
                <span>Administración de Personal</span>
              </div>
              <div className="feature">
                <span>📈</span>
                <span>Reportes Avanzados</span>
              </div>
              <div className="feature">
                <span>🔒</span>
                <span>Seguridad Empresarial</span>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      {/* Lado derecho - Formulario */}
      <div className="login-right">
        <div className="login-form-container">
          <div className="login-header">
            <h2>👋 Bienvenido de vuelta</h2>
            <p>Inicia sesión para acceder a tu cuenta</p>
          </div>

          <form onSubmit={handleSubmit} className="login-form">
            <div className="form-group">
              <label htmlFor="username">
                <span className="icon">�</span>
                Usuario
              </label>
              <input
                type="text"
                id="username"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                placeholder="superadmin"
                required
                className="form-input"
              />
            </div>

            <div className="form-group">
              <label htmlFor="password">
                <span className="icon">🔒</span>
                Contraseña
              </label>
              <input
                type="password"
                id="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="••••••••••"
                required
                className="form-input"
              />
            </div>

            {error && (
              <div className="error-message">
                <span className="error-icon">⚠️</span>
                {error}
              </div>
            )}

            <button 
              type="submit" 
              className="login-button"
              disabled={loading}
            >
              {loading ? (
                <>
                  <span className="spinner">🔄</span>
                  Iniciando sesión...
                </>
              ) : (
                <>
                  <span>🚀</span>
                  Iniciar Sesión
                </>
              )}
            </button>
          </form>

          <div className="login-footer">
            <div className="divider">
              <span>o</span>
            </div>

            {/* Credenciales de prueba - CREDENCIALES REALES DEL SISTEMA */}
            <div className="test-credentials">
              <h4>🧪 Usuarios del Sistema</h4>
              <div className="credentials-list">
                <div 
                  className="credential-item clickable"
                  onClick={() => applyTestCredential('superadmin', 'admin123')}
                >
                  <strong>🔧 SuperAdmin:</strong> superadmin / admin123
                </div>
                <div 
                  className="credential-item clickable"
                  onClick={() => applyTestCredential('admin_technomex', 'admin123')}
                >
                  <strong>🏢 TechnoMex Industries:</strong> admin_technomex / admin123
                </div>
                <div 
                  className="credential-item clickable"
                  onClick={() => applyTestCredential('admin_manu_gonzalez', 'admin123')}
                >
                  <strong>🏢 Manufactura González:</strong> admin_manu_gonzalez / admin123
                </div>
                <div 
                  className="credential-item clickable"
                  onClick={() => applyTestCredential('admin_axis', 'admin123')}
                >
                  <strong>🏢 Industrias AXIS:</strong> admin_axis / admin123
                </div>
                <div 
                  className="credential-item clickable"
                  onClick={() => applyTestCredential('admin_planta_1_1', 'admin123')}
                >
                  <strong>📍 Admin Planta:</strong> admin_planta_1_1 / admin123
                </div>
              </div>
              <div className="note">
                <small>💡 <strong>Nota:</strong> Los 3 tipos de usuarios están funcionando correctamente</small>
              </div>
            </div>

            <p className="register-link">
              ¿No tienes cuenta? 
              <a href="/registro" className="link-button">
                <span>✨</span>
                Crear cuenta nueva
              </a>
            </p>
          </div>
        </div>
      </div>

      {/* Mostrar estado del servidor si hay problemas */}
      {serverStatus !== 'checking' && serverStatus !== 'active-8000' && (
        <div className="server-status-container">
          {renderServerStatus()}
        </div>
      )}
    </div>
  );
};

export default Login;
