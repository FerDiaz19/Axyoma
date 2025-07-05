import React, { useState } from 'react';
import { login } from '../services/authService';
import '../css/Login.css';

interface LoginProps {
  onLoginSuccess: (data: any) => void;
  onSwitchToRegister?: () => void;
}

const Login: React.FC<LoginProps> = ({ onLoginSuccess, onSwitchToRegister }) => {
  const [formData, setFormData] = useState({
    username: '',
    password: ''
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      const response = await login(formData);
      // Guardar el token real devuelto por el backend
      localStorage.setItem('authToken', response.token);
      localStorage.setItem('userData', JSON.stringify(response));
      // Mantener compatibilidad con empresaData por ahora
      if (response.empresa_id) {
        localStorage.setItem('empresaData', JSON.stringify(response));
      }
      onLoginSuccess(response);
    } catch (err: any) {
      setError(err.response?.data?.error || 'Error al iniciar sesión');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="login-container">
      <form onSubmit={handleSubmit} className="login-form">
        <h2>Iniciar Sesión</h2>
        
        {error && <div className="error-message">{error}</div>}
        
        <div className="form-group">
          <label htmlFor="username">Usuario:</label>
          <input
            type="text"
            id="username"
            name="username"
            value={formData.username}
            onChange={handleChange}
            required
          />
        </div>

        <div className="form-group">
          <label htmlFor="password">Contraseña:</label>
          <input
            type="password"
            id="password"
            name="password"
            value={formData.password}
            onChange={handleChange}
            required
          />
        </div>

        <button type="submit" disabled={loading}>
          {loading ? 'Iniciando sesión...' : 'Iniciar Sesión'}
        </button>

        {onSwitchToRegister && (
          <div className="switch-to-register">
            <p>¿No tienes cuenta?</p>
            <button type="button" onClick={onSwitchToRegister} className="register-link">
              Registrar Empresa
            </button>
          </div>
        )}
      </form>
    </div>
  );
};

export default Login;
