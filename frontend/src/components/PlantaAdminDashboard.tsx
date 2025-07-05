import React, { useState, useEffect } from 'react';
import { logout } from '../services/authService';
import '../css/PlantaAdminDashboard.css';

interface Empleado {
  id: number;
  nombre: string;
  apellido_paterno: string;
  puesto: string;
  departamento: string;
  antiguedad: number;
  status: boolean;
}

interface PlantaAdminDashboardProps {
  userData: any;
  onLogout: () => void;
}

const PlantaAdminDashboard: React.FC<PlantaAdminDashboardProps> = ({ userData, onLogout }) => {
  const [activeSection, setActiveSection] = useState<'empleados' | 'evaluaciones' | 'reportes'>('empleados');
  const [empleados, setEmpleados] = useState<Empleado[]>([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    cargarDatos();
  }, []);

  const cargarDatos = async () => {
    setLoading(true);
    try {
      // Datos mock para empleados de la planta
      setEmpleados([
        { id: 1, nombre: 'Ana', apellido_paterno: 'Torres', puesto: 'Operario', departamento: 'Producción', antiguedad: 3, status: true },
        { id: 2, nombre: 'Luis', apellido_paterno: 'García', puesto: 'Supervisor', departamento: 'Calidad', antiguedad: 5, status: true },
        { id: 3, nombre: 'Carmen', apellido_paterno: 'López', puesto: 'Técnico', departamento: 'Mantenimiento', antiguedad: 2, status: true }
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

  const renderEmpleados = () => (
    <div className="section-content">
      <div className="section-header">
        <h3>Empleados de mi Planta</h3>
        <button className="btn-primary">Nuevo Empleado</button>
      </div>
      
      <div className="stats-grid">
        <div className="stat-card">
          <h4>Total Empleados</h4>
          <span className="stat-number">{empleados.length}</span>
        </div>
        <div className="stat-card">
          <h4>Empleados Activos</h4>
          <span className="stat-number">{empleados.filter(e => e.status).length}</span>
        </div>
        <div className="stat-card">
          <h4>Antigüedad Promedio</h4>
          <span className="stat-number">
            {empleados.length > 0 ? Math.round(empleados.reduce((sum, e) => sum + e.antiguedad, 0) / empleados.length) : 0} años
          </span>
        </div>
      </div>

      <div className="table-container">
        <table className="data-table">
          <thead>
            <tr>
              <th>Nombre</th>
              <th>Puesto</th>
              <th>Departamento</th>
              <th>Antigüedad</th>
              <th>Estado</th>
              <th>Acciones</th>
            </tr>
          </thead>
          <tbody>
            {empleados.map((empleado) => (
              <tr key={empleado.id}>
                <td>{empleado.nombre} {empleado.apellido_paterno}</td>
                <td>{empleado.puesto}</td>
                <td>{empleado.departamento}</td>
                <td>{empleado.antiguedad} años</td>
                <td>
                  <span className={`status ${empleado.status ? 'active' : 'inactive'}`}>
                    {empleado.status ? 'Activo' : 'Inactivo'}
                  </span>
                </td>
                <td>
                  <button className="btn-action">Ver</button>
                  <button className="btn-action">Editar</button>
                  <button className="btn-action">Evaluar</button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );

  const renderEvaluaciones = () => (
    <div className="section-content">
      <div className="section-header">
        <h3>Evaluaciones de Planta</h3>
        <button className="btn-primary">Nueva Evaluación</button>
      </div>

      <div className="evaluaciones-grid">
        <div className="eval-card">
          <h4>📋 Evaluaciones Pendientes</h4>
          <span className="eval-number">12</span>
          <p>Empleados por evaluar</p>
          <button className="btn-secondary">Ver Pendientes</button>
        </div>
        <div className="eval-card">
          <h4>✅ Evaluaciones Completadas</h4>
          <span className="eval-number">28</span>
          <p>Este mes</p>
          <button className="btn-secondary">Ver Resultados</button>
        </div>
        <div className="eval-card">
          <h4>⏰ Próximas Evaluaciones</h4>
          <span className="eval-number">8</span>
          <p>Esta semana</p>
          <button className="btn-secondary">Programar</button>
        </div>
      </div>

      <div className="recent-evaluations">
        <h4>Evaluaciones Recientes</h4>
        <div className="eval-list">
          <div className="eval-item">
            <span className="eval-employee">Ana Torres</span>
            <span className="eval-type">Evaluación 360°</span>
            <span className="eval-date">Hace 2 días</span>
            <span className="eval-status completed">Completada</span>
          </div>
          <div className="eval-item">
            <span className="eval-employee">Luis García</span>
            <span className="eval-type">NOM-035</span>
            <span className="eval-date">Hace 1 semana</span>
            <span className="eval-status pending">Pendiente</span>
          </div>
        </div>
      </div>
    </div>
  );

  const renderReportes = () => (
    <div className="section-content">
      <h3>Reportes de Planta</h3>
      <div className="reports-grid">
        <div className="report-card">
          <h4>📊 Reporte de Productividad</h4>
          <p>Métricas de rendimiento por departamento</p>
          <button className="btn-secondary">Generar</button>
        </div>
        <div className="report-card">
          <h4>👥 Reporte de Personal</h4>
          <p>Estadísticas de empleados y rotación</p>
          <button className="btn-secondary">Generar</button>
        </div>
        <div className="report-card">
          <h4>📈 Reporte de Evaluaciones</h4>
          <p>Resultados y tendencias de evaluaciones</p>
          <button className="btn-secondary">Generar</button>
        </div>
        <div className="report-card">
          <h4>⚠️ Reporte de Incidencias</h4>
          <p>Alertas y problemas detectados</p>
          <button className="btn-secondary">Generar</button>
        </div>
      </div>
    </div>
  );

  if (loading) {
    return <div className="loading">Cargando panel de planta...</div>;
  }

  return (
    <div className="planta-admin-dashboard">
      <header className="dashboard-header">
        <div className="header-left">
          <h1>🏭 Admin de Planta</h1>
          <span className="welcome">Bienvenido, {userData?.nombre_completo}</span>
          <span className="planta-info">Planta: Oficina Central Tijuana</span>
        </div>
        <div className="header-right">
          <span className="user-badge">Admin Planta</span>
          <button onClick={handleLogout} className="logout-btn">
            Cerrar Sesión
          </button>
        </div>
      </header>

      <nav className="dashboard-nav">
        <button 
          className={activeSection === 'empleados' ? 'active' : ''}
          onClick={() => setActiveSection('empleados')}
        >
          👥 Empleados ({empleados.length})
        </button>
        <button 
          className={activeSection === 'evaluaciones' ? 'active' : ''}
          onClick={() => setActiveSection('evaluaciones')}
        >
          📋 Evaluaciones
        </button>
        <button 
          className={activeSection === 'reportes' ? 'active' : ''}
          onClick={() => setActiveSection('reportes')}
        >
          📊 Reportes
        </button>
      </nav>

      <main className="dashboard-content">
        {activeSection === 'empleados' && renderEmpleados()}
        {activeSection === 'evaluaciones' && renderEvaluaciones()}
        {activeSection === 'reportes' && renderReportes()}
      </main>
    </div>
  );
};

export default PlantaAdminDashboard;
