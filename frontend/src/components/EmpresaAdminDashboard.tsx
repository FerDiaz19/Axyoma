import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import EmpleadosCRUD from './EmpleadosCRUD';
import GestionPlantas from './GestionPlantas';
import GestionDepartamentos from './GestionDepartamentos';
import GestionPuestos from './GestionPuestos';
import EvaluacionesGestion from './EvaluacionesGestion';
import AsignacionEvaluaciones from './AsignacionEvaluaciones';
import GestionSuscripcion from './GestionSuscripcion';
import UsuariosPlantasView from './UsuariosPlantasView';
import { logout } from '../services/authService';
import { crearPlanta, obtenerPlantas, actualizarPlanta } from '../services/organizacionService';
import api from '../api';
import '../css/EmpresaAdminDashboard.css';
import '../css/GestionPlantas.css';

interface EmpresaAdminDashboardProps {
  userData: any;
}

const EmpresaAdminDashboard: React.FC<EmpresaAdminDashboardProps> = ({ userData }) => {
  const [activeSection, setActiveSection] = useState('overview');  const [showPlantaModal, setShowPlantaModal] = useState(false);
  const [plantaFormData, setPlantaFormData] = useState({ nombre: '', direccion: '' });
  const [savingPlanta, setSavingPlanta] = useState(false);
  const [plantaError, setPlantaError] = useState<string | null>(null);  const [plantas, setPlantas] = useState<any[]>([]);
  const [loadingPlantas, setLoadingPlantas] = useState(false);
  const [editingPlanta, setEditingPlanta] = useState<any>(null);
  const navigate = useNavigate();

  const empresaId = userData?.empresa_id;

  // Debug logs
  console.log('🔍 DEBUG EmpresaAdminDashboard - userData completo:', userData);
  console.log('🔍 DEBUG EmpresaAdminDashboard - empresaId obtenido:', empresaId);
  console.log('🔍 DEBUG EmpresaAdminDashboard - empresa_id directo:', userData?.empresa_id);
  const handleLogout = async () => {
    try {
      await logout();
      navigate('/login');
    } catch (error) {
      console.error('Error al cerrar sesión:', error);
      localStorage.removeItem('token');
      localStorage.removeItem('userData');
      navigate('/login');
    }
  };
  const handleCrearPlanta = async (e: React.FormEvent) => {
    e.preventDefault();
    setSavingPlanta(true);
    setPlantaError(null);

    try {
      if (editingPlanta) {
        // Editing existing planta
        console.log('📝 Editando planta:', plantaFormData);
        await actualizarPlanta(editingPlanta.planta_id, plantaFormData);
        alert('¡Planta actualizada exitosamente!');
      } else {
        // Creating new planta
        console.log('📝 Creando planta:', plantaFormData);
        await crearPlanta(plantaFormData);
        alert('¡Planta creada exitosamente! Se ha creado automáticamente un usuario administrador para esta planta.');
      }
      
      // Reload plants data and reset form
      await cargarPlantas();
      resetPlantaForm();
    } catch (error: any) {
      console.error('❌ Error guardando planta:', error);
      setPlantaError(error.message || 'Error al guardar la planta');
    } finally {
      setSavingPlanta(false);
    }
  };  const resetPlantaForm = () => {
    setPlantaFormData({ nombre: '', direccion: '' });
    setPlantaError(null);
    setEditingPlanta(null);
    setShowPlantaModal(false);
  };

  const cargarPlantas = async () => {
    if (!empresaId) return;
    
    try {
      setLoadingPlantas(true);
      console.log('🔍 Cargando plantas para empresa:', empresaId);
      
      // Usar la API con filtro por empresa y incluir suspendidas
      const response = await api.get(`/plantas/?empresa_id=${empresaId}&incluir_suspendidas=true`);
      console.log('📦 Plantas obtenidas:', response.data);
      setPlantas(response.data || []);
    } catch (error: any) {
      console.error('❌ Error cargando plantas:', error);
      setPlantas([]);
    } finally {
      setLoadingPlantas(false);
    }
  };
  const handleEditPlanta = (planta: any) => {
    console.log('✏️ Editando planta:', planta);
    // Set the editing planta and pre-fill the form
    setEditingPlanta(planta);
    setPlantaFormData({
      nombre: planta.nombre,
      direccion: planta.direccion
    });
    setShowPlantaModal(true);
  };

  const handleTogglePlantaStatus = async (planta: any) => {
    const accion = planta.status ? 'suspender' : 'activar';
    const confirmMessage = planta.status 
      ? `¿Suspender la planta "${planta.nombre}"? Esto también suspenderá todos los departamentos, puestos y empleados asociados.`
      : `¿Activar la planta "${planta.nombre}"? Esto también activará todos los departamentos, puestos y empleados asociados.`;
    
    if (window.confirm(confirmMessage)) {
      try {
        console.log(`🔄 ${accion} planta:`, planta.nombre);
        
        // Llamar al endpoint de toggle_status
        await api.post(`/plantas/${planta.planta_id}/toggle_status/`);
        
        // Recargar plantas para actualizar la vista
        await cargarPlantas();
        
        alert(`Planta ${accion}da exitosamente`);
      } catch (error: any) {
        console.error(`❌ Error ${accion}ndo planta:`, error);
        const errorMessage = error.response?.data?.error || error.response?.data?.message || `Error al ${accion} la planta`;
        alert(`Error al ${accion} la planta: ${errorMessage}`);
      }
    }
  };

  // Load plants data when component mounts or empresa changes
  React.useEffect(() => {
    if (empresaId && activeSection === 'plantas') {
      cargarPlantas();
    }
  }, [empresaId, activeSection]);

  const renderActiveSection = () => {
    switch (activeSection) {
      case 'overview':
        return (
          <div className="welcome-section">
            <div className="hero-banner">
              <h2>¡Bienvenido al Panel de Administración!</h2>
              <p>Gestiona tu empresa de manera integral desde este panel de control</p>
            </div>
              <div className="stats-grid">
              <div className="stat-card">
                <div className="stat-icon">
                  <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" className="size-5">
                    <path d="M7 8a3 3 0 1 0 0-6 3 3 0 0 0 0 6ZM14.5 9a2.5 2.5 0 1 0 0-5 2.5 2.5 0 0 0 0 5ZM1.615 16.428a1.224 1.224 0 0 1-.569-1.175 6.002 6.002 0 0 1 11.908 0c.058.467-.172.92-.57 1.174A9.953 9.953 0 0 1 7 18a9.953 9.953 0 0 1-5.385-1.572ZM14.5 16h-.106c.07-.297.088-.611.048-.933a7.47 7.47 0 0 0-1.588-3.755 4.502 4.502 0 0 1 5.874 2.636.818.818 0 0 1-.36.98A7.465 7.465 0 0 1 14.5 16Z" />
                  </svg>
                </div>
                <div className="stat-content">
                  <h3>Empleados Activos</h3>
                  <p className="stat-number">156</p>
                  <span className="stat-change positive">+8 este mes</span>
                </div>
              </div>
              <div className="stat-card">
                <div className="stat-icon">
                  <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" className="size-5">
                    <path fillRule="evenodd" d="M4.25 2A2.25 2.25 0 0 0 2 4.25v2.5A2.25 2.25 0 0 0 4.25 9h2.5A2.25 2.25 0 0 0 9 6.75v-2.5A2.25 2.25 0 0 0 6.75 2h-2.5Zm0 9A2.25 2.25 0 0 0 2 13.25v2.5A2.25 2.25 0 0 0 4.25 18h2.5A2.25 2.25 0 0 0 9 15.75v-2.5A2.25 2.25 0 0 0 6.75 11h-2.5Zm9-9A2.25 2.25 0 0 0 11 4.25v2.5A2.25 2.25 0 0 0 13.25 9h2.5A2.25 2.25 0 0 0 18 6.75v-2.5A2.25 2.25 0 0 0 15.75 2h-2.5Zm0 9A2.25 2.25 0 0 0 11 13.25v2.5A2.25 2.25 0 0 0 13.25 18h2.5A2.25 2.25 0 0 0 18 15.75v-2.5A2.25 2.25 0 0 0 15.75 11h-2.5Z" clipRule="evenodd" />
                  </svg>
                </div>
                <div className="stat-content">
                  <h3>Plantas Operativas</h3>
                  <p className="stat-number">12</p>
                  <span className="stat-change positive">+2 este trimestre</span>
                </div>
              </div>
              <div className="stat-card">
                <div className="stat-icon">
                  <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" className="size-5">
                    <path fillRule="evenodd" d="M2 3a1 1 0 0 0-1 1v1a1 1 0 0 0 1 1h16a1 1 0 0 0 1-1V4a1 1 0 0 0-1-1H2Zm0 4.5h4v9a1 1 0 0 0 1 1h1a1 1 0 0 0 1-1v-9h4v9a1 1 0 0 0 1 1h1a1 1 0 0 0 1-1v-9H18a1 1 0 0 0 1-1V9a1 1 0 0 0-1-1H2a1 1 0 0 0-1 1v1.5a1 1 0 0 0 1 1Z" clipRule="evenodd" />
                  </svg>
                </div>
                <div className="stat-content">
                  <h3>Evaluaciones Completadas</h3>
                  <p className="stat-number">89%</p>
                  <span className="stat-change positive">+5% vs mes anterior</span>
                </div>
              </div>
              <div className="stat-card">
                <div className="stat-icon">
                  <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" className="size-5">
                    <path fillRule="evenodd" d="M10 1a4.5 4.5 0 0 0-4.5 4.5V9H5a2 2 0 0 0-2 2v6a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2v-6a2 2 0 0 0-2-2h-.5V5.5A4.5 4.5 0 0 0 10 1Zm3 8V5.5a3 3 0 1 0-6 0V9h6Z" clipRule="evenodd" />
                  </svg>
                </div>
                <div className="stat-content">
                  <h3>Objetivos Alcanzados</h3>
                  <p className="stat-number">94%</p>
                  <span className="stat-change positive">Excelente rendimiento</span>
                </div>
              </div>
            </div>

            <div className="quick-actions">
              <h3>Acciones Rápidas</h3>              <div className="action-buttons">
                <button 
                  className="action-btn"
                  onClick={() => setActiveSection('empleados')}
                >
                  <span className="action-icon">
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" className="size-5">
                      <path d="M10 8a3 3 0 1 0 0-6 3 3 0 0 0 0 6ZM3.465 14.493a1.23 1.23 0 0 0 .41 1.412A9.957 9.957 0 0 0 10 18c2.31 0 4.438-.784 6.131-2.1.43-.333.604-.903.408-1.41a7.002 7.002 0 0 0-13.074.003Z" />
                    </svg>
                  </span>
                  <span>Gestionar Empleados</span>
                </button>
                <button 
                  className="action-btn"
                  onClick={() => setActiveSection('plantas')}
                >
                  <span className="action-icon">
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" className="size-5">
                      <path fillRule="evenodd" d="M4.25 2A2.25 2.25 0 0 0 2 4.25v2.5A2.25 2.25 0 0 0 4.25 9h2.5A2.25 2.25 0 0 0 9 6.75v-2.5A2.25 2.25 0 0 0 6.75 2h-2.5Zm0 9A2.25 2.25 0 0 0 2 13.25v2.5A2.25 2.25 0 0 0 4.25 18h2.5A2.25 2.25 0 0 0 9 15.75v-2.5A2.25 2.25 0 0 0 6.75 11h-2.5Zm9-9A2.25 2.25 0 0 0 11 4.25v2.5A2.25 2.25 0 0 0 13.25 9h2.5A2.25 2.25 0 0 0 18 6.75v-2.5A2.25 2.25 0 0 0 15.75 2h-2.5Zm0 9A2.25 2.25 0 0 0 11 13.25v2.5A2.25 2.25 0 0 0 13.25 18h2.5A2.25 2.25 0 0 0 18 15.75v-2.5A2.25 2.25 0 0 0 15.75 11h-2.5Z" clipRule="evenodd" />
                    </svg>
                  </span>
                  <span>Ver Plantas</span>
                </button>
                <button 
                  className="action-btn"
                  onClick={() => setActiveSection('evaluaciones')}
                >
                  <span className="action-icon">
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" className="size-5">
                      <path fillRule="evenodd" d="M15.988 3.012A2.25 2.25 0 0 1 18 5.25v6.5A2.25 2.25 0 0 1 15.75 14H13.5V7A2.5 2.5 0 0 0 11 4.5H8.128a2.252 2.252 0 0 1 1.884-1.488A2.25 2.25 0 0 1 12.25 1h1.5c.78 0 1.467.397 1.871 1.002l.367.01ZM11.5 6.25a.75.75 0 0 1 .75-.75h3.5a.75.75 0 0 1 0 1.5h-3.5a.75.75 0 0 1-.75-.75Zm0 2.25a.75.75 0 0 1 .75-.75h3.5a.75.75 0 0 1 0 1.5h-3.5a.75.75 0 0 1-.75-.75Z" clipRule="evenodd" />
                      <path d="M2 7a1 1 0 0 1 1-1h8a1 1 0 0 1 1 1v10a1 1 0 0 1-1 1H3a1 1 0 0 1-1-1V7Zm2 3.25a.75.75 0 0 1 .75-.75h4.5a.75.75 0 0 1 0 1.5h-4.5a.75.75 0 0 1-.75-.75Zm0 2.5a.75.75 0 0 1 .75-.75h4.5a.75.75 0 0 1 0 1.5h-4.5a.75.75 0 0 1-.75-.75Z" />
                    </svg>
                  </span>
                  <span>Crear Evaluación</span>
                </button>
                <button 
                  className="action-btn"
                  onClick={() => setActiveSection('asignaciones')}
                >
                  <span className="action-icon">
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" className="size-5">
                      <path fillRule="evenodd" d="M10 1a4.5 4.5 0 0 0-4.5 4.5V9H5a2 2 0 0 0-2 2v6a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2v-6a2 2 0 0 0-2-2h-.5V5.5A4.5 4.5 0 0 0 10 1Zm3 8V5.5a3 3 0 1 0-6 0V9h6Z" clipRule="evenodd" />
                    </svg>
                  </span>
                  <span>Asignar Evaluaciones</span>
                </button>
              </div>
            </div>          </div>
        );
      case 'graficas':
        return (
          <div className="welcome-section">
            {/* Hero Banner PRINCIPAL al inicio */}
            <div className="hero-banner">
              <h2>
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" className="size-5">
                  <path d="M15.5 2A1.5 1.5 0 0 1 17 3.5v13a1.5 1.5 0 0 1-1.5 1.5h-13A1.5 1.5 0 0 1 1 16.5v-13A1.5 1.5 0 0 1 2.5 2h13ZM4 6a1 1 0 0 0-1 1v6a1 1 0 0 0 1 1h1a1 1 0 0 0 1-1V7a1 1 0 0 0-1-1H4Zm4-2a1 1 0 0 0-1 1v8a1 1 0 0 0 1 1h1a1 1 0 0 0 1-1V5a1 1 0 0 0-1-1H8Zm4 4a1 1 0 0 0-1 1v4a1 1 0 0 0 1 1h1a1 1 0 0 0 1-1V9a1 1 0 0 0-1-1h-1Z" />
                </svg>
                Gráficas y Reportes
              </h2>
              <p>Visualiza datos y métricas de tu empresa con gráficos interactivos</p>
            </div>            {/* Gráficas Compactas en el centro */}
            <div className="evaluaciones-charts-section">
              {/* Container para gráficas en grid horizontal */}
              <div className="charts-grid">
                {/* Gráfica de Barras - Compacta */}
                <div className="chart-container">
                  <div className="chart-header">
                    <h4>Resultados de Evaluaciones NOM-035</h4>
                    <p className="chart-subtitle">Puntajes por empleado</p>
                  </div>
                  <div className="bar-chart">
                    <div className="chart-data">
                      <div className="bar-item">
                        <div className="bar-info">
                          <span className="employee-name">Amieva Ángel</span>
                          <span className="department">Desarrollo</span>
                        </div>                        <div className="bar-visual">
                          <div className="bar-background">
                            <div className="bar-fill failed" style={{width: '35%', '--width': '35%'} as any}></div>
                          </div>
                          <span className="score">35/100</span>
                        </div>
                      </div>
                      <div className="bar-item">
                        <div className="bar-info">
                          <span className="employee-name">María González</span>
                          <span className="department">RRHH</span>
                        </div>                        <div className="bar-visual">
                          <div className="bar-background">
                            <div className="bar-fill passed" style={{width: '78%', '--width': '78%'} as any}></div>
                          </div>
                          <span className="score">78/100</span>
                        </div>
                      </div>
                      <div className="bar-item">
                        <div className="bar-info">
                          <span className="employee-name">Carlos Ruiz</span>
                          <span className="department">Producción</span>
                        </div>                        <div className="bar-visual">
                          <div className="bar-background">
                            <div className="bar-fill warning" style={{width: '62%', '--width': '62%'} as any}></div>
                          </div>
                          <span className="score">62/100</span>
                        </div>
                      </div>
                      <div className="bar-item">
                        <div className="bar-info">
                          <span className="employee-name">Ana López</span>
                          <span className="department">Calidad</span>
                        </div>                        <div className="bar-visual">
                          <div className="bar-background">
                            <div className="bar-fill passed" style={{width: '85%', '--width': '85%'} as any}></div>
                          </div>
                          <span className="score">85/100</span>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>

                {/* Gráfica de Pastel - Compacta */}
                <div className="chart-container">
                  <div className="chart-header">
                    <h4>Distribución de Resultados</h4>
                    <p className="chart-subtitle">Estado general de evaluaciones</p>
                  </div>
                  <div className="pie-chart-section">
                    <div className="pie-chart">
                      <div className="pie-slice failed" style={{
                        '--percentage': '25',
                        '--rotation': '0deg'
                      } as any}></div>
                      <div className="pie-slice warning" style={{
                        '--percentage': '25', 
                        '--rotation': '90deg'
                      } as any}></div>
                      <div className="pie-slice passed" style={{
                        '--percentage': '50',
                        '--rotation': '180deg'
                      } as any}></div>
                    </div>
                    <div className="pie-legend">
                      <div className="legend-item">
                        <span className="legend-color failed"></span>
                        <span className="legend-text">Crítico (25%)</span>
                      </div>
                      <div className="legend-item">
                        <span className="legend-color warning"></span>
                        <span className="legend-text">Medio (25%)</span>
                      </div>
                      <div className="legend-item">
                        <span className="legend-color passed"></span>
                        <span className="legend-text">Bajo (50%)</span>
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              {/* Estadísticas Rápidas */}
              <div className="quick-stats">
                <div className="stat-item">
                  <div className="stat-icon">
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" className="size-5">
                      <path d="M10 9a3 3 0 1 0 0-6 3 3 0 0 0 0 6ZM6 8a2 2 0 1 1-4 0 2 2 0 0 1 4 0ZM1.49 15.326a.78.78 0 0 1-.358-.442 3 3 0 0 1 4.308-3.516 6.484 6.484 0 0 0-1.905 3.959c-.023.222-.014.442.025.654a4.97 4.97 0 0 1-2.07-.655ZM16.44 15.98a4.97 4.97 0 0 0 2.07-.654.78.78 0 0 0 .357-.442 3 3 0 0 0-4.308-3.517 6.484 6.484 0 0 1 1.907 3.96 2.32 2.32 0 0 1-.026.654ZM18 8a2 2 0 1 1-4 0 2 2 0 0 1 4 0ZM5.304 16.19a.844.844 0 0 1-.277-.71 5 5 0 0 1 9.947 0 .843.843 0 0 1-.277.71A6.975 6.975 0 0 1 10 18a6.974 6.974 0 0 1-4.696-1.81Z" />
                    </svg>
                  </div>
                  <div className="stat-content">
                    <span className="stat-number">32</span>
                    <span className="stat-label">Completadas</span>
                  </div>
                </div>
                <div className="stat-item">
                  <div className="stat-icon">
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" className="size-5">
                      <path fillRule="evenodd" d="M10 18a8 8 0 1 0 0-16 8 8 0 0 0 0 16Zm3.857-9.809a.75.75 0 0 0-1.214-.882l-3.236 4.53L7.53 10.06a.75.75 0 0 0-1.06 1.061l2.5 2.5a.75.75 0 0 0 1.137-.089l4-5.5Z" clipRule="evenodd" />
                    </svg>
                  </div>
                  <div className="stat-content">
                    <span className="stat-number">75%</span>
                    <span className="stat-label">Aprobación</span>
                  </div>
                </div>
                <div className="stat-item">
                  <div className="stat-icon">
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" className="size-5">
                      <path fillRule="evenodd" d="M1 6a3 3 0 0 1 3-3h12a3 3 0 0 1 3 3v8a3 3 0 0 1-3 3H4a3 3 0 0 1-3-3V6Zm4 1.5a2 2 0 1 1 4 0 2 2 0 0 1-4 0Zm2 3a4 4 0 0 0-3.665 2.395.75.75 0 0 0 .416 1A8.98 8.98 0 0 0 7 14.5a8.98 8.98 0 0 0 3.249-.604.75.75 0 0 0 .416-1.001A4.001 4.001 0 0 0 7 10.5Zm5-3.75a.75.75 0 0 1 .75-.75h2.5a.75.75 0 0 1 0 1.5h-2.5a.75.75 0 0 1-.75-.75Zm0 2.5a.75.75 0 0 1 .75-.75h2.5a.75.75 0 0 1 0 1.5h-2.5a.75.75 0 0 1-.75-.75Z" clipRule="evenodd" />
                    </svg>
                  </div>
                  <div className="stat-content">
                    <span className="stat-number">67</span>
                    <span className="stat-label">Promedio</span>
                  </div>
                </div>
              </div>
            </div>

            {/* Solo UNA Dashboard Card al final - compacta */}
            <div className="dashboards-grid-single">
              {/* <div className="dashboard-card">
                <div className="dashboard-icon">
                  <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" className="size-5">
                    <path d="M15.5 2A1.5 1.5 0 0 1 17 3.5v13a1.5 1.5 0 0 1-1.5 1.5h-13A1.5 1.5 0 0 1 1 16.5v-13A1.5 1.5 0 0 1 2.5 2h13ZM4 6a1 1 0 0 0-1 1v6a1 1 0 0 0 1 1h1a1 1 0 0 0 1-1V7a1 1 0 0 0-1-1H4Zm4-2a1 1 0 0 0-1 1v8a1 1 0 0 0 1 1h1a1 1 0 0 0 1-1V5a1 1 0 0 0-1-1H8Zm4 4a1 1 0 0 0-1 1v4a1 1 0 0 0 1 1h1a1 1 0 0 0 1-1V9a1 1 0 0 0-1-1h-1Z" />
                  </svg>
                </div>
                <div className="dashboard-content">
                  <h3>Explorar Más Gráficas</h3>
                  <p className="dashboard-description">Accede a análisis detallados y reportes avanzados</p>
                  <p className="dashboard-status">Próximamente disponible</p>
                </div>
              </div> */}
            </div>

            {/* 
            ============================
            INTEGRATION NOTES FOR DEVELOPERS
            ============================
            
            API Endpoints for real data integration:
            
            1. EVALUATION RESULTS CHART:
               - Endpoint: /api/appraisal/resultados/
               - Method: GET
               - Expected format: Array of {empleado_nombre, departamento, puntaje_total}
               - Integration: Replace hardcoded data in chart-data div
            
            2. PIE CHART DATA:
               - Endpoint: /api/appraisal/estadisticas/
               - Method: GET  
               - Expected format: {critico: number, medio: number, bajo: number}
               - Integration: Calculate percentages and update pie slices
            
            3. QUICK STATS:
               - Endpoint: /api/appraisal/resumen/
               - Method: GET
               - Expected format: {completadas: number, aprobacion_porcentaje: number, promedio: number}
               - Integration: Update stat-number spans dynamically
            
            4. FUTURE CHARTS:
               - Add onClick handlers to dashboard-card
               - Navigate to specific chart components
               - Implement filters and date ranges
            */}
          </div>
        );
      case 'empleados':
        return (
          <EmpleadosCRUD 
            userData={userData}
          />
        );      case 'plantas':
        return (
          <div className="plantas-dashboard-section">            <div className="section-header">
              <h2>
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" className="size-5">
                  <path fillRule="evenodd" d="M4.25 2A2.25 2.25 0 0 0 2 4.25v2.5A2.25 2.25 0 0 0 4.25 9h2.5A2.25 2.25 0 0 0 9 6.75v-2.5A2.25 2.25 0 0 0 6.75 2h-2.5Zm0 9A2.25 2.25 0 0 0 2 13.25v2.5A2.25 2.25 0 0 0 4.25 18h2.5A2.25 2.25 0 0 0 9 15.75v-2.5A2.25 2.25 0 0 0 6.75 11h-2.5Zm9-9A2.25 2.25 0 0 0 11 4.25v2.5A2.25 2.25 0 0 0 13.25 9h2.5A2.25 2.25 0 0 0 18 6.75v-2.5A2.25 2.25 0 0 0 15.75 2h-2.5Zm0 9A2.25 2.25 0 0 0 11 13.25v2.5A2.25 2.25 0 0 0 13.25 18h2.5A2.25 2.25 0 0 0 18 15.75v-2.5A2.25 2.25 0 0 0 15.75 11h-2.5Z" clipRule="evenodd" />
                </svg>
                Gestión de Plantas
              </h2>
              <p className="section-subtitle">Administra las plantas industriales de tu empresa</p>
            </div>              <div className="plants-summary-cards">
              <div className="summary-card">
                <div className="summary-icon">
                  <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" className="size-5">
                    <path fillRule="evenodd" d="M4.25 2A2.25 2.25 0 0 0 2 4.25v2.5A2.25 2.25 0 0 0 4.25 9h2.5A2.25 2.25 0 0 0 9 6.75v-2.5A2.25 2.25 0 0 0 6.75 2h-2.5Zm0 9A2.25 2.25 0 0 0 2 13.25v2.5A2.25 2.25 0 0 0 4.25 18h2.5A2.25 2.25 0 0 0 9 15.75v-2.5A2.25 2.25 0 0 0 6.75 11h-2.5Zm9-9A2.25 2.25 0 0 0 11 4.25v2.5A2.25 2.25 0 0 0 13.25 9h2.5A2.25 2.25 0 0 0 18 6.75v-2.5A2.25 2.25 0 0 0 15.75 2h-2.5Zm0 9A2.25 2.25 0 0 0 11 13.25v2.5A2.25 2.25 0 0 0 13.25 18h2.5A2.25 2.25 0 0 0 18 15.75v-2.5A2.25 2.25 0 0 0 15.75 11h-2.5Z" clipRule="evenodd" />
                  </svg>
                </div>
                <div className="summary-content">
                  <h3>Total Plantas</h3>
                  <p className="summary-number">{plantas.length}</p>
                </div>
              </div>
              <div className="summary-card">
                <div className="summary-icon">
                  <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" className="size-5">
                    <path fillRule="evenodd" d="M16.704 4.153a.75.75 0 0 1 .143 1.052l-8 10.5a.75.75 0 0 1-1.127.075l-4.5-4.5a.75.75 0 0 1 1.06-1.06l3.894 3.893 7.48-9.817a.75.75 0 0 1 1.05-.143Z" clipRule="evenodd" />
                  </svg>
                </div>
                <div className="summary-content">
                  <h3>Plantas Activas</h3>
                  <p className="summary-number">{plantas.filter(p => p.status).length}</p>
                </div>
              </div>
              <div className="summary-card">
                <div className="summary-icon">
                  <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" className="size-5">
                    <path d="M7 8a3 3 0 1 0 0-6 3 3 0 0 0 0 6ZM14.5 9a2.5 2.5 0 1 0 0-5 2.5 2.5 0 0 0 0 5ZM1.615 16.428a1.224 1.224 0 0 1-.569-1.175 6.002 6.002 0 0 1 11.908 0c.058.467-.172.92-.57 1.174A9.953 9.953 0 0 1 7 18a9.953 9.953 0 0 1-5.385-1.572ZM14.5 16h-.106c.07-.297.088-.611.048-.933a7.47 7.47 0 0 0-1.588-3.755 4.502 4.502 0 0 1 5.874 2.636.818.818 0 0 1-.36.98A7.465 7.465 0 0 1 14.5 16Z" />
                  </svg>
                </div>
                <div className="summary-content">
                  <h3>Total Empleados</h3>
                  <p className="summary-number">{plantas.reduce((total, planta) => total + (planta.total_empleados || 0), 0)}</p>
                </div>
              </div>
            </div><div className="plants-grid">
              {loadingPlantas ? (
                <div className="loading-plants">
                  <p>Cargando plantas...</p>
                </div>
              ) : plantas.length === 0 ? (
                <div className="empty-plants">
                  <p>No hay plantas registradas</p>                  <button 
                    className="btn btn-primary"
                    onClick={() => {
                      setEditingPlanta(null);
                      setPlantaFormData({ nombre: '', direccion: '' });
                      setPlantaError(null);
                      setShowPlantaModal(true);
                    }}
                  >
                    Crear Primera Planta
                  </button>
                </div>
              ) : (
                plantas.map((planta) => (
                  <div key={planta.planta_id} className="plant-card">
                    <div className="plant-card-header">
                      <h4>{planta.nombre}</h4>
                      <span className={`status-badge ${planta.status ? 'active' : 'inactive'}`}>
                        {planta.status ? 'Activa' : 'Suspendida'}
                      </span>
                    </div>
                    <div className="plant-info">
                      <p className="plant-location">
                        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" className="size-4 inline">
                          <path fillRule="evenodd" d="m9.69 18.933.003.001C9.89 19.02 10 19 10 19s.11.02.308-.066l.002-.001.006-.003.018-.008a5.741 5.741 0 0 0 .281-.14c.186-.096.446-.24.757-.433.62-.384 1.445-.966 2.274-1.765C15.302 14.988 17 12.493 17 9A7 7 0 0 0 3 9c0 3.492 1.698 5.988 3.355 7.584a13.731 13.731 0 0 0 2.273 1.765 11.842 11.842 0 0 0 .976.505l.041.018.006.003.002.001ZM10 12a3 3 0 1 0 0-6 3 3 0 0 0 0 6Z" clipRule="evenodd" />
                        </svg>
                        {planta.direccion || 'Dirección no especificada'}
                      </p>
                      <p className="plant-employees">
                        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" className="size-4 inline">
                          <path d="M7 8a3 3 0 1 0 0-6 3 3 0 0 0 0 6ZM14.5 9a2.5 2.5 0 1 0 0-5 2.5 2.5 0 0 0 0 5ZM1.615 16.428a1.224 1.224 0 0 1-.569-1.175 6.002 6.002 0 0 1 11.908 0c.058.467-.172.92-.57 1.174A9.953 9.953 0 0 1 7 18a9.953 9.953 0 0 1-5.385-1.572ZM14.5 16h-.106c.07-.297.088-.611.048-.933a7.47 7.47 0 0 0-1.588-3.755 4.502 4.502 0 0 1 5.874 2.636.818.818 0 0 1-.36.98A7.465 7.465 0 0 1 14.5 16Z" />
                        </svg>
                        {planta.total_empleados || 0} empleados
                      </p>
                      <p className="plant-departments">
                        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" className="size-4 inline">
                          <path fillRule="evenodd" d="M4 16.5v-13h-.25a.75.75 0 0 1 0-1.5h12.5a.75.75 0 0 1 0 1.5H16v13h.25a.75.75 0 0 1 0 1.5h-3.5a.75.75 0 0 1-.75-.75v-2.5a.75.75 0 0 0-.75-.75h-2.5a.75.75 0 0 0-.75.75v2.5a.75.75 0 0 1-.75.75h-3.5a.75.75 0 0 1 0-1.5H4Zm3-11a.5.5 0 0 1 .5-.5h1a.5.5 0 0 1 .5.5v1a.5.5 0 0 1-.5.5h-1a.5.5 0 0 1-.5-.5v-1ZM7.5 9a.5.5 0 0 0-.5.5v1a.5.5 0 0 0 .5.5h1a.5.5 0 0 0 .5-.5v-1a.5.5 0 0 0-.5-.5h-1ZM11 5.5a.5.5 0 0 1 .5-.5h1a.5.5 0 0 1 .5.5v1a.5.5 0 0 1-.5.5h-1a.5.5 0 0 1-.5-.5v-1Zm.5 3.5a.5.5 0 0 0-.5.5v1a.5.5 0 0 0 .5.5h1a.5.5 0 0 0 .5-.5v-1a.5.5 0 0 0-.5-.5h-1Z" clipRule="evenodd" />
                        </svg>
                        {planta.total_departamentos || 0} departamentos
                      </p>
                    </div>
                    <div className="plant-actions">
                      <button 
                        className="btn btn-primary"
                        onClick={() => setActiveSection('gestion-plantas')}
                      >
                        Ver Detalles
                      </button>
                      <button 
                        className="btn btn-secondary"
                        onClick={() => handleEditPlanta(planta)}
                      >
                        Editar
                      </button>
                      <button 
                        className={`btn ${planta.status ? 'btn-warning' : 'btn-success'}`}
                        onClick={() => handleTogglePlantaStatus(planta)}
                      >
                        {planta.status ? 'Suspender' : 'Activar'}
                      </button>
                    </div>
                  </div>
                ))
              )}
            </div>

            <div className="plants-actions-section">
              <button 
                className="btn btn-violet"
                onClick={() => {/* Navegar a gestión completa */}}
              >
                <span className="action-icon">⚙️</span>
                Gestión Completa de Plantas
              </button>              <button 
                className="btn btn-violet"
                onClick={() => {
                  setEditingPlanta(null);
                  setPlantaFormData({ nombre: '', direccion: '' });
                  setPlantaError(null);
                  setShowPlantaModal(true);
                }}
              >
                <span className="action-icon">➕</span>
                Agregar Nueva Planta
              </button>
            </div>
          </div>
        );
      case 'usuarios-plantas':
        return (
          <UsuariosPlantasView 
            empresaId={empresaId || 1}
          />
        );
      case 'departamentos':
        return (
          <GestionDepartamentos 
            empresaId={empresaId || 1}
          />
        );
      case 'puestos':
        return (
          <GestionPuestos empresaId={empresaId || 1} />
        );
      case 'evaluaciones':
        return (
          <EvaluacionesGestion 
            userData={userData}
          />
        );
      case 'asignaciones':
        return (
          <AsignacionEvaluaciones 
            userData={userData}
          />
        );
      case 'suscripcion':
        return (
          <GestionSuscripcion 
            empresaId={empresaId || 1}
          />
        );
      default:
        return (
          <div className="welcome-section">
            <div className="hero-banner">
              <h2>¡Bienvenido al Panel de Administración!</h2>
              <p>Gestiona tu empresa de manera integral desde este panel de control</p>
            </div>
          </div>
        );
    }
  };

  return (
    <div className="dashboard superadmin-dashboard">
      {/* Sidebar */}
      <aside className="dashboard-sidebar">        <div className="sidebar-header">
          <div className="sidebar-logo">
            <h2>
              <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" className="size-5">
                <path fillRule="evenodd" d="M4 16.5v-13h-.25a.75.75 0 0 1 0-1.5h12.5a.75.75 0 0 1 0 1.5H16v13h.25a.75.75 0 0 1 0 1.5h-3.5a.75.75 0 0 1-.75-.75v-2.5a.75.75 0 0 0-.75-.75h-2.5a.75.75 0 0 0-.75.75v2.5a.75.75 0 0 1-.75.75h-3.5a.75.75 0 0 1 0-1.5H4Zm3-11a.5.5 0 0 1 .5-.5h1a.5.5 0 0 1 .5.5v1a.5.5 0 0 1-.5.5h-1a.5.5 0 0 1-.5-.5v-1ZM7.5 9a.5.5 0 0 0-.5.5v1a.5.5 0 0 0 .5.5h1a.5.5 0 0 0 .5-.5v-1a.5.5 0 0 0-.5-.5h-1ZM11 5.5a.5.5 0 0 1 .5-.5h1a.5.5 0 0 1 .5.5v1a.5.5 0 0 1-.5.5h-1a.5.5 0 0 1-.5-.5v-1Zm.5 3.5a.5.5 0 0 0-.5.5v1a.5.5 0 0 0 .5.5h1a.5.5 0 0 0 .5-.5v-1a.5.5 0 0 0-.5-.5h-1Z" clipRule="evenodd" />
              </svg>
              AXYOMA
            </h2>
            <span className="sidebar-subtitle">Panel Empresa</span>
          </div>
        </div>
        <nav className="sidebar-nav">          <button 
            className={activeSection === 'overview' ? 'active' : ''}
            onClick={() => setActiveSection('overview')}
          >
            <span className="nav-icon">
              <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" className="size-5">
                <path fillRule="evenodd" d="M2 3a1 1 0 0 0-1 1v1a1 1 0 0 0 1 1h16a1 1 0 0 0 1-1V4a1 1 0 0 0-1-1H2Zm0 4.5h4v9a1 1 0 0 0 1 1h1a1 1 0 0 0 1-1v-9h4v9a1 1 0 0 0 1 1h1a1 1 0 0 0 1-1v-9H18a1 1 0 0 0 1-1V9a1 1 0 0 0-1-1H2a1 1 0 0 0-1 1v1.5a1 1 0 0 0 1 1Z" clipRule="evenodd" />
              </svg>
            </span>
            <span className="nav-text">Dashboard</span>
          </button>          <button 
            className={activeSection === 'empleados' ? 'active' : ''}
            onClick={() => setActiveSection('empleados')}
          >
            <span className="nav-icon">
              <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" className="size-5">
                <path d="M7 8a3 3 0 1 0 0-6 3 3 0 0 0 0 6ZM14.5 9a2.5 2.5 0 1 0 0-5 2.5 2.5 0 0 0 0 5ZM1.615 16.428a1.224 1.224 0 0 1-.569-1.175 6.002 6.002 0 0 1 11.908 0c.058.467-.172.92-.57 1.174A9.953 9.953 0 0 1 7 18a9.953 9.953 0 0 1-5.385-1.572ZM14.5 16h-.106c.07-.297.088-.611.048-.933a7.47 7.47 0 0 0-1.588-3.755 4.502 4.502 0 0 1 5.874 2.636.818.818 0 0 1-.36.98A7.465 7.465 0 0 1 14.5 16Z" />
              </svg>
            </span>
            <span className="nav-text">Empleados</span>
          </button>          <button 
            className={activeSection === 'plantas' ? 'active' : ''}
            onClick={() => setActiveSection('plantas')}
          >
            <span className="nav-icon">
              <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" className="size-5">
                <path fillRule="evenodd" d="M4.25 2A2.25 2.25 0 0 0 2 4.25v2.5A2.25 2.25 0 0 0 4.25 9h2.5A2.25 2.25 0 0 0 9 6.75v-2.5A2.25 2.25 0 0 0 6.75 2h-2.5Zm0 9A2.25 2.25 0 0 0 2 13.25v2.5A2.25 2.25 0 0 0 4.25 18h2.5A2.25 2.25 0 0 0 9 15.75v-2.5A2.25 2.25 0 0 0 6.75 11h-2.5Zm9-9A2.25 2.25 0 0 0 11 4.25v2.5A2.25 2.25 0 0 0 13.25 9h2.5A2.25 2.25 0 0 0 18 6.75v-2.5A2.25 2.25 0 0 0 15.75 2h-2.5Zm0 9A2.25 2.25 0 0 0 11 13.25v2.5A2.25 2.25 0 0 0 13.25 18h2.5A2.25 2.25 0 0 0 18 15.75v-2.5A2.25 2.25 0 0 0 15.75 11h-2.5Z" clipRule="evenodd" />
              </svg>
            </span>
            <span className="nav-text">Plantas</span>
          </button>          <button 
            className={activeSection === 'usuarios-plantas' ? 'active' : ''}
            onClick={() => setActiveSection('usuarios-plantas')}
          >
            <span className="nav-icon">
              <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" className="size-5">
                <path d="M10 8a3 3 0 1 0 0-6 3 3 0 0 0 0 6ZM3.465 14.493a1.23 1.23 0 0 0 .41 1.412A9.957 9.957 0 0 0 10 18c2.31 0 4.438-.784 6.131-2.1.43-.333.604-.903.408-1.41a7.002 7.002 0 0 0-13.074.003Z" />
              </svg>
            </span>
            <span className="nav-text">Usuarios Plantas</span>
          </button>          <button 
            className={activeSection === 'departamentos' ? 'active' : ''}
            onClick={() => setActiveSection('departamentos')}
          >
            <span className="nav-icon">
              <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" className="size-5">
                <path fillRule="evenodd" d="M4 16.5v-13h-.25a.75.75 0 0 1 0-1.5h12.5a.75.75 0 0 1 0 1.5H16v13h.25a.75.75 0 0 1 0 1.5h-3.5a.75.75 0 0 1-.75-.75v-2.5a.75.75 0 0 0-.75-.75h-2.5a.75.75 0 0 0-.75.75v2.5a.75.75 0 0 1-.75.75h-3.5a.75.75 0 0 1 0-1.5H4Zm3-11a.5.5 0 0 1 .5-.5h1a.5.5 0 0 1 .5.5v1a.5.5 0 0 1-.5.5h-1a.5.5 0 0 1-.5-.5v-1ZM7.5 9a.5.5 0 0 0-.5.5v1a.5.5 0 0 0 .5.5h1a.5.5 0 0 0 .5-.5v-1a.5.5 0 0 0-.5-.5h-1ZM11 5.5a.5.5 0 0 1 .5-.5h1a.5.5 0 0 1 .5.5v1a.5.5 0 0 1-.5.5h-1a.5.5 0 0 1-.5-.5v-1Zm.5 3.5a.5.5 0 0 0-.5.5v1a.5.5 0 0 0 .5.5h1a.5.5 0 0 0 .5-.5v-1a.5.5 0 0 0-.5-.5h-1Z" clipRule="evenodd" />
              </svg>
            </span>
            <span className="nav-text">Departamentos</span>
          </button>          <button 
            className={activeSection === 'puestos' ? 'active' : ''}
            onClick={() => setActiveSection('puestos')}
          >
            <span className="nav-icon">
              <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" className="size-5">
                <path fillRule="evenodd" d="M6 3.75A2.75 2.75 0 0 1 8.75 1h2.5A2.75 2.75 0 0 1 14 3.75v.443c.572.055 1.14.122 1.706.2C17.053 4.582 18 5.75 18 7.07v3.469c0 1.126-.694 2.191-1.83 2.54-1.952.599-4.024.921-6.17.921s-4.219-.322-6.17-.921C2.694 12.73 2 11.665 2 10.539V7.07c0-1.321.947-2.489 2.294-2.676A41.047 41.047 0 0 1 6 4.193V3.75Zm6.5 0v.325a41.622 41.622 0 0 0-5 0V3.75c0-.69.56-1.25 1.25-1.25h2.5c.69 0 1.25.56 1.25 1.25ZM10 10a1 1 0 0 0 1 1h.01a1 1 0 1 0 0-2H11a1 1 0 0 0-1 1Z" clipRule="evenodd" />
                <path d="M3 15.055v-.684c.126.053.255.1.39.142 2.092.642 4.313.987 6.61.987 2.297 0 4.518-.345 6.61-.987.135-.041.264-.089.39-.142v.684c0 1.347-.985 2.53-2.363 2.686a41.454 41.454 0 0 1-9.274 0C3.985 17.585 3 16.402 3 15.055Z" />
              </svg>
            </span>
            <span className="nav-text">Puestos</span>
          </button>          <button 
            className={activeSection === 'evaluaciones' ? 'active' : ''}
            onClick={() => setActiveSection('evaluaciones')}
          >
            <span className="nav-icon">
              <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" className="size-5">
                <path fillRule="evenodd" d="M15.988 3.012A2.25 2.25 0 0 1 18 5.25v6.5A2.25 2.25 0 0 1 15.75 14H13.5V7A2.5 2.5 0 0 0 11 4.5H8.128a2.252 2.252 0 0 1 1.884-1.488A2.25 2.25 0 0 1 12.25 1h1.5c.78 0 1.467.397 1.871 1.002l.367.01ZM11.5 6.25a.75.75 0 0 1 .75-.75h3.5a.75.75 0 0 1 0 1.5h-3.5a.75.75 0 0 1-.75-.75Zm0 2.25a.75.75 0 0 1 .75-.75h3.5a.75.75 0 0 1 0 1.5h-3.5a.75.75 0 0 1-.75-.75Z" clipRule="evenodd" />
                <path d="M2 7a1 1 0 0 1 1-1h8a1 1 0 0 1 1 1v10a1 1 0 0 1-1 1H3a1 1 0 0 1-1-1V7Zm2 3.25a.75.75 0 0 1 .75-.75h4.5a.75.75 0 0 1 0 1.5h-4.5a.75.75 0 0 1-.75-.75Zm0 2.5a.75.75 0 0 1 .75-.75h4.5a.75.75 0 0 1 0 1.5h-4.5a.75.75 0 0 1-.75-.75Z" />
              </svg>
            </span>
            <span className="nav-text">Evaluaciones</span>
          </button>          <button 
            className={activeSection === 'asignaciones' ? 'active' : ''}
            onClick={() => setActiveSection('asignaciones')}
          >
            <span className="nav-icon">
              <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" className="size-5">
                <path fillRule="evenodd" d="M10 1a4.5 4.5 0 0 0-4.5 4.5V9H5a2 2 0 0 0-2 2v6a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2v-6a2 2 0 0 0-2-2h-.5V5.5A4.5 4.5 0 0 0 10 1Zm3 8V5.5a3 3 0 1 0-6 0V9h6Z" clipRule="evenodd" />
              </svg>
            </span>
            <span className="nav-text">Asignaciones</span>
          </button>          <button 
            className={activeSection === 'graficas' ? 'active' : ''}
            onClick={() => setActiveSection('graficas')}
          >
            <span className="nav-icon">
              <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" className="size-5">
                <path d="M15.5 2A1.5 1.5 0 0 1 17 3.5v13a1.5 1.5 0 0 1-1.5 1.5h-13A1.5 1.5 0 0 1 1 16.5v-13A1.5 1.5 0 0 1 2.5 2h13ZM4 6a1 1 0 0 0-1 1v6a1 1 0 0 0 1 1h1a1 1 0 0 0 1-1V7a1 1 0 0 0-1-1H4Zm4-2a1 1 0 0 0-1 1v8a1 1 0 0 0 1 1h1a1 1 0 0 0 1-1V5a1 1 0 0 0-1-1H8Zm4 4a1 1 0 0 0-1 1v4a1 1 0 0 0 1 1h1a1 1 0 0 0 1-1V9a1 1 0 0 0-1-1h-1Z" />
              </svg>
            </span>
            <span className="nav-text">Gráficas</span>
          </button><button 
            className={activeSection === 'suscripcion' ? 'active' : ''}
            onClick={() => setActiveSection('suscripcion')}
          >
            <span className="nav-icon">
              <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" className="size-5">
                <path d="M4.632 3.533A2 2 0 0 1 6.577 2h6.846a2 2 0 0 1 1.945 1.533l1.976 8.234A3.489 3.489 0 0 0 16 11.5H4c-.476 0-.93.095-1.344.267l1.976-8.234Z" />
                <path fillRule="evenodd" d="M4 13a2 2 0 1 0 0 4h12a2 2 0 1 0 0-4H4Zm11.24 2a.75.75 0 0 1 .75-.75H16a.75.75 0 0 1 0 1.5h-.01a.75.75 0 0 1-.75-.75Zm-2.25-.75a.75.75 0 0 0 0 1.5H13a.75.75 0 0 0 0-1.5h-.01Z" clipRule="evenodd" />
              </svg>
            </span>
            <span className="nav-text">Suscripción</span>
          </button>
        </nav>
      </aside>

      {/* Main content area */}
      <div className="main-content">
        {/* Header */}
        <header className="dashboard-header">
          <div className="header-left">
            <h1>Panel de Administración - Empresa</h1>
            <p className="header-subtitle">Gestión integral de la empresa</p>
          </div>
          <div className="header-right">            <div className="user-info">
              <div className="user-avatar">
                <span className="avatar-icon">
                  <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" className="size-5">
                    <path d="M10 8a3 3 0 1 0 0-6 3 3 0 0 0 0 6ZM3.465 14.493a1.23 1.23 0 0 0 .41 1.412A9.957 9.957 0 0 0 10 18c2.31 0 4.438-.784 6.131-2.1.43-.333.604-.903.408-1.41a7.002 7.002 0 0 0-13.074.003Z" />
                  </svg>
                </span>
              </div>
              <div className="user-details">
                <span className="user-name">
                  {userData?.perfil_usuario?.nombre || userData?.username}
                </span>
                <span className="user-role">Administrador de Empresa</span>
              </div>
            </div>
            <button onClick={handleLogout} className="logout-btn">
              <span className="logout-icon">
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" className="size-5">
                  <path fillRule="evenodd" d="M3 4.25A2.25 2.25 0 0 1 5.25 2h5.5A2.25 2.25 0 0 1 13 4.25v2a.75.75 0 0 1-1.5 0v-2a.75.75 0 0 0-.75-.75h-5.5a.75.75 0 0 0-.75.75v11.5c0 .414.336.75.75.75h5.5a.75.75 0 0 0 .75-.75v-2a.75.75 0 0 1 1.5 0v2A2.25 2.25 0 0 1 10.75 18h-5.5A2.25 2.25 0 0 1 3 15.75V4.25Z" clipRule="evenodd" />
                  <path fillRule="evenodd" d="M6 10a.75.75 0 0 1 .75-.75h9.546l-1.048-.943a.75.75 0 1 1 1.004-1.114l2.5 2.25a.75.75 0 0 1 0 1.114l-2.5 2.25a.75.75 0 1 1-1.004-1.114l1.048-.943H6.75A.75.75 0 0 1 6 10Z" clipRule="evenodd" />
                </svg>
              </span>
              Cerrar Sesión
            </button>
          </div>
        </header>        {/* Content area */}
        <main className="dashboard-content">
          {renderActiveSection()}
        </main>
      </div>

      {/* Modal para crear nueva planta */}
      {showPlantaModal && (
        <div className="modal-overlay">
          <div className="modal">
            <h3>{editingPlanta ? 'Editar Planta' : 'Nueva Planta'}</h3>
            <form onSubmit={handleCrearPlanta}>
              {plantaError && (
                <div className="form-error">
                  {plantaError}
                </div>
              )}
              
              <div className="form-group">
                <label>Nombre de la Planta:</label>
                <input
                  type="text"
                  value={plantaFormData.nombre}
                  onChange={(e) => setPlantaFormData({ ...plantaFormData, nombre: e.target.value })}
                  placeholder="Ej: Planta Industrial Norte, Fábrica Central..."
                  required
                />
              </div>
              
              <div className="form-group">
                <label>Dirección:</label>
                <textarea
                  value={plantaFormData.direccion}
                  onChange={(e) => setPlantaFormData({ ...plantaFormData, direccion: e.target.value })}
                  placeholder="Ingresa la dirección completa de la planta industrial..."
                  required
                />
              </div>

              <div className="form-actions">
                <button type="submit" className="btn btn-primary" disabled={savingPlanta}>
                  <span>{savingPlanta ? 'Guardando...' : (editingPlanta ? 'Actualizar Planta' : 'Crear Planta')}</span>
                </button>
                <button 
                  type="button" 
                  className="btn btn-secondary"
                  onClick={resetPlantaForm}
                  disabled={savingPlanta}
                >
                  <span>Cancelar</span>
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};

export default EmpresaAdminDashboard;
