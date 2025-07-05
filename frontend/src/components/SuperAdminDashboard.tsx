import React, { useState, useEffect } from 'react';
import { logout } from '../services/authService';
import '../css/SuperAdminDashboard.css';

interface Empresa {
  id: number;
  nombre: string;
  rfc: string;
  status: boolean;
  empleados: number;
}

interface Usuario {
  id: number;
  nombre: string;
  correo: string;
  nivel: string;
  status: boolean;
}

interface SuperAdminDashboardProps {
  userData: any;
  onLogout: () => void;
}

const SuperAdminDashboard: React.FC<SuperAdminDashboardProps> = ({ userData, onLogout }) => {
  const [activeSection, setActiveSection] = useState<'empresas' | 'usuarios' | 'estadisticas' | 'configuracion'>('empresas');
  const [empresas, setEmpresas] = useState<Empresa[]>([]);
  const [usuarios, setUsuarios] = useState<Usuario[]>([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    cargarDatos();
  }, []);

  const cargarDatos = async () => {
    setLoading(true);
    try {
      // Aquí puedes cargar datos de empresas, usuarios, etc.
      // Por ahora datos mock
      setEmpresas([
        { id: 1, nombre: 'Soluciones Industriales MX', rfc: 'SIMX920314ABC', status: true, empleados: 45 },
        { id: 2, nombre: 'Tech Solutions Corp', rfc: 'TSC890215DEF', status: true, empleados: 32 }
      ]);
      
      setUsuarios([
        { id: 1, nombre: 'Juan Perez', correo: 'juan.perez@codewave.com', nivel: 'admin-empresa', status: true },
        { id: 2, nombre: 'Maria Gomez', correo: 'maria.gomez@codewave.com', nivel: 'admin-planta', status: true }
      ]);
    } catch (error) {
      console.error('Error cargando datos:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleLogout = () => {
    logout();
    onLogout();
  };

  const renderEmpresas = () => (
    <div className="section-content">
      <div className="section-header">
        <h3>Gestión de Empresas</h3>
        <button className="btn-primary">Nueva Empresa</button>
      </div>
      
      <div className="stats-grid">
        <div className="stat-card">
          <h4>Total Empresas</h4>
          <span className="stat-number">{empresas.length}</span>
        </div>
        <div className="stat-card">
          <h4>Empresas Activas</h4>
          <span className="stat-number">{empresas.filter(e => e.status).length}</span>
        </div>
        <div className="stat-card">
          <h4>Total Empleados</h4>
          <span className="stat-number">{empresas.reduce((sum, e) => sum + e.empleados, 0)}</span>
        </div>
      </div>

      <div className="table-container">
        <table className="data-table">
          <thead>
            <tr>
              <th>Empresa</th>
              <th>RFC</th>
              <th>Empleados</th>
              <th>Estado</th>
              <th>Acciones</th>
            </tr>
          </thead>
          <tbody>
            {empresas.map((empresa: any) => (
              <tr key={empresa.id}>
                <td>{empresa.nombre}</td>
                <td>{empresa.rfc}</td>
                <td>{empresa.empleados}</td>
                <td>
                  <span className={`status ${empresa.status ? 'active' : 'inactive'}`}>
                    {empresa.status ? 'Activa' : 'Inactiva'}
                  </span>
                </td>
                <td>
                  <button className="btn-action">Ver</button>
                  <button className="btn-action">Editar</button>
                  <button className="btn-action danger">Suspender</button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );

  const renderUsuarios = () => (
    <div className="section-content">
      <div className="section-header">
        <h3>Gestión de Usuarios</h3>
        <button className="btn-primary">Nuevo Usuario</button>
      </div>

      <div className="table-container">
        <table className="data-table">
          <thead>
            <tr>
              <th>Nombre</th>
              <th>Correo</th>
              <th>Nivel</th>
              <th>Estado</th>
              <th>Acciones</th>
            </tr>
          </thead>
          <tbody>
            {usuarios.map((usuario: any) => (
              <tr key={usuario.id}>
                <td>{usuario.nombre}</td>
                <td>{usuario.correo}</td>
                <td>
                  <span className={`badge ${usuario.nivel}`}>
                    {usuario.nivel}
                  </span>
                </td>
                <td>
                  <span className={`status ${usuario.status ? 'active' : 'inactive'}`}>
                    {usuario.status ? 'Activo' : 'Inactivo'}
                  </span>
                </td>
                <td>
                  <button className="btn-action">Ver</button>
                  <button className="btn-action">Editar</button>
                  <button className="btn-action danger">Suspender</button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );

  const renderEstadisticas = () => (
    <div className="section-content">
      <h3>Estadísticas del Sistema</h3>
      <div className="stats-grid">
        <div className="stat-card large">
          <h4>Evaluaciones Completadas</h4>
          <span className="stat-number">1,247</span>
          <span className="stat-change positive">+12% vs mes anterior</span>
        </div>
        <div className="stat-card large">
          <h4>Usuarios Activos</h4>
          <span className="stat-number">89</span>
          <span className="stat-change positive">+5% vs mes anterior</span>
        </div>
        <div className="stat-card large">
          <h4>Ingresos del Mes</h4>
          <span className="stat-number">$24,890</span>
          <span className="stat-change negative">-3% vs mes anterior</span>
        </div>
      </div>
    </div>
  );

  const renderConfiguracion = () => (
    <div className="section-content">
      <h3>Configuración del Sistema</h3>
      <div className="config-grid">
        <div className="config-card">
          <h4>Configuración General</h4>
          <p>Ajustes básicos del sistema</p>
          <button className="btn-secondary">Configurar</button>
        </div>
        <div className="config-card">
          <h4>Planes de Suscripción</h4>
          <p>Gestionar planes y precios</p>
          <button className="btn-secondary">Gestionar</button>
        </div>
        <div className="config-card">
          <h4>Respaldos</h4>
          <p>Configurar respaldos automáticos</p>
          <button className="btn-secondary">Configurar</button>
        </div>
        <div className="config-card">
          <h4>Notificaciones</h4>
          <p>Configurar alertas del sistema</p>
          <button className="btn-secondary">Configurar</button>
        </div>
      </div>
    </div>
  );

  if (loading) {
    return <div className="loading">Cargando panel de administración...</div>;
  }

  return (
    <div className="superadmin-dashboard">
      <header className="dashboard-header">
        <div className="header-left">
          <h1>🔧 Panel SuperAdmin</h1>
          <span className="welcome">Bienvenido, {userData?.nombre_completo}</span>
        </div>
        <div className="header-right">
          <span className="user-badge">SuperAdmin</span>
          <button onClick={handleLogout} className="logout-btn">
            Cerrar Sesión
          </button>
        </div>
      </header>

      <nav className="dashboard-nav">
        <button 
          className={activeSection === 'empresas' ? 'active' : ''}
          onClick={() => setActiveSection('empresas')}
        >
          🏢 Empresas ({empresas.length})
        </button>
        <button 
          className={activeSection === 'usuarios' ? 'active' : ''}
          onClick={() => setActiveSection('usuarios')}
        >
          👥 Usuarios ({usuarios.length})
        </button>
        <button 
          className={activeSection === 'estadisticas' ? 'active' : ''}
          onClick={() => setActiveSection('estadisticas')}
        >
          📊 Estadísticas
        </button>
        <button 
          className={activeSection === 'configuracion' ? 'active' : ''}
          onClick={() => setActiveSection('configuracion')}
        >
          ⚙️ Configuración
        </button>
      </nav>

      <main className="dashboard-content">
        {activeSection === 'empresas' && renderEmpresas()}
        {activeSection === 'usuarios' && renderUsuarios()}
        {activeSection === 'estadisticas' && renderEstadisticas()}
        {activeSection === 'configuracion' && renderConfiguracion()}
      </main>
    </div>
  );
};

export default SuperAdminDashboard;
