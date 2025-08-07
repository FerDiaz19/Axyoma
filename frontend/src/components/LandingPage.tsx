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

  const handleChosenUndeadAccess = () => {
    // Redirigir directamente a la URL del chosen-undead
    window.open('http://localhost:8000/axyoma/chosen-undead/', '_blank');
  };
  return (
    <div className="landing-container">
      {/* Header */}
      <header className="landing-header">
        <div className="logo">
          <h1>AXYOMA</h1>
        </div>
        <nav className="nav-buttons">
          <button onClick={handleLoginClick} className="btn-login">
            Iniciar Sesión
          </button>
          <button onClick={handleRegisterClick} className="btn-register">
            Registrarse
          </button>
        </nav>
      </header>      {/* Hero Section */}
      <section className="hero">
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
      </section>      {/* Employee Access Section */}
      <section className="token-access">
        <div className="token-card">
          <h2>Acceso para Empleados</h2>
          <p>¿Eres administrador de evaluaciones? Accede al panel de gestión de tokens.</p>
          
          {/* Botón para chosen-undead */}
          <div style={{ 
            textAlign: 'center',
            paddingTop: '20px'
          }}>
            <button 
              onClick={handleChosenUndeadAccess}
              className="btn-secondary"
              style={{
                background: '#2c2c3d',
                color: '#fff',
                border: 'none',
                padding: '15px 25px',
                borderRadius: '8px',
                fontSize: '1rem',
                cursor: 'pointer',
                transition: 'background 0.3s ease',
                fontWeight: 'bold'
              }}
              onMouseOver={(e) => (e.target as HTMLButtonElement).style.background = '#1a1a2e'}
              onMouseOut={(e) => (e.target as HTMLButtonElement).style.background = '#2c2c3d'}
            >
              🔥 Panel de Gestión de Tokens
            </button>
          </div>
        </div>
      </section>      {/* Features */}
      <section className="features">
        <div className="section-title-container">
          <h2>¿Por qué elegir AXYOMA?</h2>
        </div>
        <div className="features-grid">
          <div className="feature-card">
            <div className="feature-icon"></div>
            <h3>Gestión de Empleados</h3>
            <p>Administra perfiles completos de empleados, departamentos y puestos de trabajo.</p>
          </div>
          <div className="feature-card">
            <div className="feature-icon"></div>
            <h3>Evaluaciones</h3>
            <p>Sistema completo de evaluaciones y seguimiento del desempeño.</p>
          </div>
          <div className="feature-card">
            <div className="feature-icon"></div>
            <h3>Multi-Planta</h3>
            <p>Gestiona múltiples plantas y sucursales desde una sola plataforma.</p>
          </div>
          <div className="feature-card">
            <div className="feature-icon"></div>
            <h3>Seguro</h3>
            <p>Diferentes niveles de acceso y seguridad para proteger tu información.</p>
          </div>
          <div className="feature-card">
            <div className="feature-icon"></div>
            <h3>Respaldos</h3>
            <p>Sistema automático de respaldos para mantener tu información segura.</p>
          </div>
          <div className="feature-card">
            <div className="feature-icon"></div>
            <h3>Rápido y Simple</h3>
            <p>Interface intuitiva diseñada para ser fácil de usar desde el primer día.</p>
          </div>
        </div>
      </section>      {/* CTA Section */}
      <section className="cta">
        <div className="cta-content">
          <h2>¿Listo para empezar?</h2>
          <p>Únete a las empresas que ya confían en AXYOMA para gestionar su talento humano.</p>
          <button onClick={handleLoginClick} className="btn-cta">
            Iniciar Sesión
          </button>
        </div>
      </section>

      {/* Footer */}
      <footer className="landing-footer">
        <p>&copy; 2025 AXYOMA. Todos los derechos reservados.</p>
      </footer>
    </div>
  );
};

export default LandingPage;
