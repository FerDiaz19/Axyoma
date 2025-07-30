import React from 'react';
import { useNavigate } from 'react-router-dom';
import './LandingPage.css';

const LandingPage: React.FC = () => {
  const navigate = useNavigate();

  const handleLoginClick = () => {
    navigate('/login');
  };

  const handleRegisterClick = () => {
    navigate('/registro');
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
