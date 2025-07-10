import React, { useState } from 'react';
import { login } from '../services/authService';
import '../css/Login.css';

interface LoginProps {
  onLogin: (userData: any) => void;
}

const Login: React.FC<LoginProps> = ({ onLogin }) => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      const userData = await login({ username, password });
      onLogin(userData);
    } catch (error: any) {
      setError(error.message || 'Error al iniciar sesión');
    } finally {
      setLoading(false);
    }
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

            {/* Credenciales de prueba */}
            <div className="test-credentials">
              <h4>🧪 Usuarios de Prueba</h4>
              <div className="credentials-list">
                <div className="credential-item">
                  <strong>SuperAdmin:</strong> superadmin / 1234
                </div>
                <div className="credential-item">
                  <strong>Admin Empresa:</strong> admin_empresa / 1234
                </div>
                <div className="credential-item">
                  <strong>Admin Planta:</strong> admin_planta / 1234
                </div>
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
    </div>
  );
};

export default Login;
