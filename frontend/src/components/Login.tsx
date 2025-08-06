import React, { useState, useEffect } from 'react';
import { login } from '../services/authService';
import { findBackendServer } from '../utils/serverCheck';
import logoImage from '../utils/full-logo.png';
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
      const sanitizedUsername = username.trim()

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



  return (
    <div className="login-container">      {/* Lado izquierdo - Imagen */}
      <div className="login-left">        <div className="login-image-section">
          <div className="image-placeholder">
            <div className="brand-logo">
              <div className="logo-container">
                <img
                  src={logoImage}
                  alt="AXYOMA Logo"
                  className="logo-icon"
                />
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Lado derecho - Formulario */}
      <div className="login-right">
        <div className="login-form-container">          <div className="login-header">
            <p>Inicia sesión para acceder a tu cuenta</p>
          </div>

          <form onSubmit={handleSubmit} className="login-form">
            <div className="form-group">              <label htmlFor="username">
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

            <div className="form-group">              <label htmlFor="password">
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
                </>              ) : (
                "Iniciar Sesión"
              )}
            </button>
          </form>          <div className="login-footer">
            <p className="register-link">
              ¿No tienes cuenta?
              <a href="/registro" className="link-button">
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