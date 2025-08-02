import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './LandingPage.css';

const LandingPage: React.FC = () => {
  const navigate = useNavigate();
  const [token, setToken] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [tokenError, setTokenError] = useState('');

  const handleLoginClick = () => {
    navigate('/login');
  };

  const handleRegisterClick = () => {
    navigate('/registro');
  };

  const handleTokenAccess = async () => {
    if (!token.trim()) {
      setTokenError('Por favor ingresa un token válido');
      return;
    }

    setIsLoading(true);
    setTokenError('');

    try {
      const response = await fetch(`http://localhost:8000/api/evaluaciones/asignacion/validar-token/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ token: token.trim() }),
      });

      if (response.ok) {
        await response.json(); // Validate response
        // Redirigir a la página de evaluación con el token
        navigate(`/evaluacion/${token.trim()}`);
      } else {
        const errorData = await response.json();
        setTokenError(errorData.detail || 'Token inválido o expirado');
      }
    } catch (error) {
      setTokenError('Error de conexión. Por favor intenta nuevamente.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="landing-container">
      {/* Header */}
      <header className="landing-header">
        <div className="container">
          <div className="logo">
            <h1>🚀 AXYOMA</h1>
          </div>
          <nav className="nav-buttons">
            <button onClick={handleLoginClick} className="btn-login">
              Iniciar Sesión
            </button>
            <button onClick={handleRegisterClick} className="btn-register">
              Registrarse
            </button>
          </nav>
        </div>
      </header>

      {/* Hero Section */}
      <section className="hero">
        <div className="container">
          <div className="hero-content">
            <h1 className="hero-title">
              Gestiona tu Empresa con <span className="highlight">AXYOMA</span>
            </h1>
            <p className="hero-subtitle">
              La plataforma integral para administrar empleados, evaluaciones y estructura organizacional de manera simple y eficiente.
            </p>
            <div className="hero-buttons">
              <button onClick={handleLoginClick} className="btn-primary">
                Comenzar Ahora
              </button>
              <button onClick={handleRegisterClick} className="btn-secondary">
                Crear Cuenta
              </button>
            </div>
          </div>
        </div>
      </section>

      {/* Token Access Section */}
      <section className="token-access">
        <div className="container">
          <div className="token-card">
            <h2>Acceso para Empleados</h2>
            <p>¿Tienes un token de evaluación? Ingrésalo aquí para acceder a tu evaluación asignada.</p>
            <div className="token-form">
              <input
                type="text"
                placeholder="Ingresa tu token de 8 caracteres"
                value={token}
                onChange={(e) => setToken(e.target.value.toUpperCase())}
                maxLength={8}
                className={`token-input ${tokenError ? 'error' : ''}`}
              />
              <button 
                onClick={handleTokenAccess}
                disabled={isLoading || !token.trim()}
                className="btn-token"
              >
                {isLoading ? 'Verificando...' : 'Acceder'}
              </button>
            </div>
            {tokenError && <div className="token-error">{tokenError}</div>}
          </div>
        </div>
      </section>

      {/* Features */}
      <section className="features">
        <div className="container">
          <h2 className="section-title">¿Por qué elegir AXYOMA?</h2>
          <div className="features-grid">
            <div className="feature-card">
              <div className="feature-icon">👥</div>
              <h3>Gestión de Empleados</h3>
              <p>Administra perfiles completos de empleados, departamentos y puestos de trabajo.</p>
            </div>
            <div className="feature-card">
              <div className="feature-icon">📊</div>
              <h3>Evaluaciones</h3>
              <p>Sistema completo de evaluaciones y seguimiento del desempeño.</p>
            </div>
            <div className="feature-card">
              <div className="feature-icon">🏢</div>
              <h3>Multi-Planta</h3>
              <p>Gestiona múltiples plantas y sucursales desde una sola plataforma.</p>
            </div>
            <div className="feature-card">
              <div className="feature-icon">🔒</div>
              <h3>Seguro</h3>
              <p>Diferentes niveles de acceso y seguridad para proteger tu información.</p>
            </div>
            <div className="feature-card">
              <div className="feature-icon">💾</div>
              <h3>Respaldos</h3>
              <p>Sistema automático de respaldos para mantener tu información segura.</p>
            </div>
            <div className="feature-card">
              <div className="feature-icon">⚡</div>
              <h3>Rápido y Simple</h3>
              <p>Interface intuitiva diseñada para ser fácil de usar desde el primer día.</p>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="cta">
        <div className="container">
          <div className="cta-content">
            <h2>¿Listo para empezar?</h2>
            <p>Únete a las empresas que ya confían en AXYOMA para gestionar su talento humano.</p>
            <button onClick={handleLoginClick} className="btn-cta">
              Iniciar Sesión
            </button>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="landing-footer">
        <div className="container">
          <p>&copy; 2025 AXYOMA. Todos los derechos reservados.</p>
        </div>
      </footer>
    </div>
  );
};

export default LandingPage;
