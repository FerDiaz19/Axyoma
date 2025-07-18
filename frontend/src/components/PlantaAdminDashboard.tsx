import React, { useState, useEffect, useCallback } from 'react';
import EmpleadosCRUD from './EmpleadosCRUD';
import {
  obtenerDepartamentos, crearDepartamento, actualizarDepartamento, eliminarDepartamento,
  obtenerPuestos, crearPuesto, actualizarPuesto, eliminarPuesto,
  Departamento, Puesto
} from '../services/organizacionService';
import { logout } from '../services/authService';
import '../css/PlantaAdminDashboard.css';

interface PlantaAdminDashboardProps {
  userData: any;
  onLogout: () => void;
}

const PlantaAdminDashboard: React.FC<PlantaAdminDashboardProps> = ({ userData, onLogout }) => {
  const [activeSection, setActiveSection] = useState<'departamentos' | 'puestos' | 'empleados'>('departamentos');
  const [departamentos, setDepartamentos] = useState<Departamento[]>([]);
  const [puestos, setPuestos] = useState<Puesto[]>([]);
  const [loading, setLoading] = useState(false);
  
  // Verificar estado de suscripción de la empresa (herencia)
  const suscripcionEmpresa = userData?.suscripcion;
  const tieneSuscripcionActiva = suscripcionEmpresa?.tiene_suscripcion && suscripcionEmpresa?.estado === 'activa';
  const isEmpresaSuspendida = userData?.empresa_suspendida || 
                             userData?.advertencia?.tipo === 'empresa_suspendida' ||
                             !tieneSuscripcionActiva;
  
  // Estados para formularios - Admin Planta solo puede trabajar con SU planta
  const [nuevoDepartamento, setNuevoDepartamento] = useState<Departamento>({ 
    nombre: '', 
    descripcion: '', 
    planta_id: userData?.planta_id || 0 // Usar la planta asignada del usuario
  });
  const [nuevoPuesto, setNuevoPuesto] = useState<Puesto>({ 
    nombre: '', 
    descripcion: '', 
    departamento_id: 0 
  });

  // Estados para edición
  const [editingDepartamento, setEditingDepartamento] = useState<Departamento | null>(null);
  const [editingPuesto, setEditingPuesto] = useState<Puesto | null>(null);
  
  // Estados para filtros
  const [filtroNombre, setFiltroNombre] = useState('');
  const [filtroDepartamento, setFiltroDepartamento] = useState('');

  const cargarDatos = useCallback(async () => {
    setLoading(true);
    try {
<<<<<<< HEAD
      const [departamentosData, puestosData] = await Promise.all([
        obtenerDepartamentos(), 
        obtenerPuestos()
      ]);
      
      // Filtrar solo los departamentos y puestos de la planta asignada al usuario
      const departamentosDePlanta = departamentosData.filter(dept => dept.planta_id === userData?.planta_id);
      setDepartamentos(departamentosDePlanta);
      setPuestos(puestosData);
    } catch (error) {
      console.error('Error cargando datos:', error);
    } finally {
      setLoading(false);
    }
  }, [userData?.planta_id]);

  useEffect(() => {
    if (userData?.planta_id) {
      cargarDatos();
    }
  }, [userData?.planta_id, cargarDatos]);

  const handleLogout = () => {
    logout();
    onLogout();
  };

  // Funciones para departamentos
  const handleCrearDepartamento = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!nuevoDepartamento.nombre.trim()) {
      alert('El nombre del departamento es requerido');
      return;
    }
    
    // Admin Planta solo puede crear departamentos en SU planta asignada
    const departamentoData = {
      ...nuevoDepartamento,
      planta_id: userData?.planta_id
    };
    
    try {
      if (editingDepartamento) {
        await actualizarDepartamento(editingDepartamento.departamento_id!, departamentoData);
        alert('Departamento actualizado exitosamente');
      } else {
        await crearDepartamento(departamentoData);
        alert('Departamento creado exitosamente');
      }
      
      setNuevoDepartamento({ nombre: '', descripcion: '', planta_id: userData?.planta_id || 0 });
      setEditingDepartamento(null);
      cargarDatos();
    } catch (error: any) {
      console.error('Error con departamento:', error);
      alert(error.message || 'Error al procesar departamento');
    }
  };

  const handleEditarDepartamento = (departamento: Departamento) => {
    setEditingDepartamento(departamento);
    setNuevoDepartamento({
      nombre: departamento.nombre,
      descripcion: departamento.descripcion || '',
      planta_id: departamento.planta_id
    });
  };

  const handleEliminarDepartamento = async (departamento: Departamento) => {
    const confirmMessage = `¿Está seguro de eliminar el departamento "${departamento.nombre}"?\\n\\nEsta acción también eliminará todos los puestos y empleados asociados.\\n\\nEsta acción NO se puede deshacer.`;
    
    if (window.confirm(confirmMessage)) {
      try {
        await eliminarDepartamento(departamento.departamento_id!);
        cargarDatos();
        alert('Departamento eliminado exitosamente');
      } catch (error: any) {
        console.error('Error eliminando departamento:', error);
        alert(error.message || 'Error al eliminar departamento');
      }
=======
      await logout();
      window.location.href = '/login';
    } catch (error) {
      console.error('Error al cerrar sesión:', error);
    }
  };

  const renderActiveSection = () => {
    switch (activeSection) {
      case 'departamentos':
        return <GestionDepartamentos />;
      case 'puestos':
        return <GestionPuestos />;
      case 'empleados':
        return <EmpleadosCRUD userData={userData} />;
      case 'evaluaciones':
        return <EvaluacionesGestion userData={{ nivel_usuario: 'admin_planta' }} />;
      default:
        return <div>Sección no encontrada</div>;
>>>>>>> parent of 68f3cd1 (xd)
    }
  };

  // Funciones para puestos
  const handleCrearPuesto = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!nuevoPuesto.nombre.trim()) {
      alert('El nombre del puesto es requerido');
      return;
    }
    
    if (nuevoPuesto.departamento_id === 0) {
      alert('Debe seleccionar un departamento');
      return;
    }
    
    try {
      if (editingPuesto) {
        await actualizarPuesto(editingPuesto.puesto_id!, nuevoPuesto);
        alert('Puesto actualizado exitosamente');
      } else {
        await crearPuesto(nuevoPuesto);
        alert('Puesto creado exitosamente');
      }
      
      setNuevoPuesto({ nombre: '', descripcion: '', departamento_id: 0 });
      setEditingPuesto(null);
      cargarDatos();
    } catch (error: any) {
      console.error('Error con puesto:', error);
      alert(error.message || 'Error al procesar puesto');
    }
  };

  const handleEditarPuesto = (puesto: Puesto) => {
    setEditingPuesto(puesto);
    setNuevoPuesto({
      nombre: puesto.nombre,
      descripcion: puesto.descripcion || '',
      departamento_id: puesto.departamento_id
    });
  };

  const handleEliminarPuesto = async (puesto: Puesto) => {
    const confirmMessage = `¿Está seguro de eliminar el puesto "${puesto.nombre}"?\\n\\nEsta acción también eliminará todos los empleados asociados a este puesto.\\n\\nEsta acción NO se puede deshacer.`;
    
    if (window.confirm(confirmMessage)) {
      try {
        await eliminarPuesto(puesto.puesto_id!);
        cargarDatos();
        alert('Puesto eliminado exitosamente');
      } catch (error: any) {
        console.error('Error eliminando puesto:', error);
        alert(error.message || 'Error al eliminar puesto');
      }
    }
  };

  const cancelarEdicion = () => {
    setEditingDepartamento(null);
    setEditingPuesto(null);
    setNuevoDepartamento({ nombre: '', descripcion: '', planta_id: 0 });
    setNuevoPuesto({ nombre: '', descripcion: '', departamento_id: 0 });
  };

  // Filtrar datos
  const departamentosFiltrados = departamentos.filter(dept =>
    dept.nombre.toLowerCase().includes(filtroNombre.toLowerCase())
  );

  const puestosFiltrados = puestos.filter(puesto => {
    const matchesNombre = puesto.nombre.toLowerCase().includes(filtroNombre.toLowerCase());
    const matchesDepartamento = filtroDepartamento === '' || puesto.departamento_id.toString() === filtroDepartamento;
    return matchesNombre && matchesDepartamento;
  });

  if (loading) {
    return <div className="loading">🔄 Cargando datos de la planta...</div>;
  }

  return (
    <div className="dashboard planta-admin-dashboard">
      {/* Sidebar - Always visible */}
      <aside className="dashboard-sidebar">
        <div className="sidebar-header">
          <div className="sidebar-logo">
            <h2>🏭 AXYOMA</h2>
            <span className="sidebar-subtitle">Admin Planta</span>
          </div>
        </div>
        <nav className="sidebar-nav">
<<<<<<< HEAD
          <button 
            className={activeSection === 'departamentos' ? 'active' : ''}
            onClick={() => setActiveSection('departamentos')}
          >
            <span className="nav-icon">🏢</span>
            <span className="nav-text">Gestión de Departamentos</span>
=======
          {menuItems.map((item) => (
            <button 
              key={item.id}
              className={`nav-item ${activeSection === item.id ? 'active' : ''}`}
              onClick={() => setActiveSection(item.id)}
              title={item.description}
            >
              <span className="nav-icon">{item.icon}</span>
              <span className="nav-text">{item.label}</span>
            </button>
          ))}
        </nav>

        <div className="sidebar-footer">
          <button className="logout-btn" onClick={handleLogout}>
            <span>🚪</span>
            Cerrar Sesión
>>>>>>> parent of 68f3cd1 (xd)
          </button>
          <button 
            className={activeSection === 'puestos' ? 'active' : ''}
            onClick={() => setActiveSection('puestos')}
          >
            <span className="nav-icon">💼</span>
            <span className="nav-text">Gestión de Puestos</span>
          </button>
          <button 
            className={activeSection === 'empleados' ? 'active' : ''}
            onClick={() => setActiveSection('empleados')}
          >
            <span className="nav-icon">👥</span>
            <span className="nav-text">Gestión de Empleados</span>
          </button>
        </nav>
      </aside>

      {/* Main content area */}
      <div className="main-content">
        {/* Header */}
        <header className="dashboard-header">
          <div className="header-left">
            <h1>Panel de Administración - Planta</h1>
            <p className="header-subtitle">Gestión de departamentos, puestos y empleados</p>
          </div>
          <div className="header-right">
            <div className="planta-info">
              <div className="planta-avatar">
                <span className="avatar-icon">🏭</span>
              </div>
              <div className="planta-details">
                <span className="planta-name">{userData?.nombre_planta || 'No asignada'}</span>
                <span className="planta-user">({userData?.usuario})</span>
                <span className="empresa-name">{userData?.nombre_empresa || 'No asignada'}</span>
              </div>
              {tieneSuscripcionActiva && (
                <span className="status-active">
                  ✅ ACTIVA ({suscripcionEmpresa?.dias_restantes || 0} días)
                </span>
              )}
              {isEmpresaSuspendida && (
                <span className="status-suspended">⚠️ SIN SUSCRIPCIÓN</span>
              )}
            </div>
            <button onClick={handleLogout} className="logout-btn">
              <span className="logout-icon">🚪</span>
              Cerrar Sesión
            </button>
          </div>
        </header>

        {/* Content area */}
        <main className="dashboard-content">{/* Información de suscripción activa para plantas */}
      {tieneSuscripcionActiva && (
        <div className="subscription-alert">
          <div className="warning-content">
            <h3>✅ Empresa con Suscripción Activa</h3>
            <div style={{ display: 'flex', gap: '20px', color: '#155724' }}>
              <span>Plan: {suscripcionEmpresa?.plan_nombre}</span>
              <span>Días restantes: {suscripcionEmpresa?.dias_restantes}</span>
              <span>Estado: {suscripcionEmpresa?.estado}</span>
            </div>
            <p style={{ margin: '5px 0 0 0', fontSize: '0.9em', color: '#155724' }}>
              Su planta tiene acceso completo gracias a la suscripción activa de la empresa.
            </p>
          </div>
        </div>
      )}

      {/* Mensaje de advertencia para empresa suspendida */}
      {isEmpresaSuspendida && !tieneSuscripcionActiva && (
        <div className="subscription-warning">
          <div className="warning-content">
            <h3>⚠️ {userData?.advertencia?.mensaje || 'Empresa sin Suscripción Activa'}</h3>
            <p>
              {userData?.advertencia?.detalles || 
               'La empresa no tiene una suscripción activa. Las funcionalidades están limitadas.'}
            </p>
            <p style={{ marginTop: '10px', fontSize: '0.9em', color: '#721c24' }}>
              <strong>Nota:</strong> Como administrador de planta, contacte al administrador de la empresa 
              para activar o renovar la suscripción.
            </p>
          </div>
        </div>
      )}
      {/* Contenido principal */}
      <div className="main-content-area">
        {/* Sección de Departamentos */}
        {activeSection === 'departamentos' && (
          <div className="departamentos-section">
            <div className="section-header">
              <h2>Gestión de Departamentos</h2>
              <p>Administre los departamentos de su planta asignada: <strong>{userData?.nombre_planta}</strong></p>
            </div>

            {/* Filtros */}
            <div className="filtros">
              <input
                type="text"
                placeholder="Buscar departamentos..."
                value={filtroNombre}
                onChange={(e) => setFiltroNombre(e.target.value)}
                className="filtro-input"
              />
            </div>

            {/* Formulario */}
            <form onSubmit={handleCrearDepartamento} className="create-form">
              <h3>{editingDepartamento ? 'Editar Departamento' : 'Crear Nuevo Departamento'}</h3>
              
              <div className="form-row">
                <div className="form-group">
                  <label>Nombre del Departamento:</label>
                  <input
                    type="text"
                    value={nuevoDepartamento.nombre}
                    onChange={(e) => setNuevoDepartamento({ ...nuevoDepartamento, nombre: e.target.value })}
                    placeholder="Ej: Mantenimiento"
                    required
                  />
                </div>
                
                <div className="form-group">
                  <label>Planta Asignada:</label>
                  <input
                    type="text"
                    value={userData?.nombre_planta || 'Planta no asignada'}
                    disabled
                    className="readonly-input"
                    title="Como Admin de Planta, solo puedes gestionar departamentos de tu planta asignada"
                  />
                </div>
              </div>

              <div className="form-group">
                <label>Descripción:</label>
                <textarea
                  value={nuevoDepartamento.descripcion}
                  onChange={(e) => setNuevoDepartamento({ ...nuevoDepartamento, descripcion: e.target.value })}
                  placeholder="Descripción del departamento"
                />
              </div>

              <div className="form-actions">
                <button type="submit" className="btn btn-primary">
                  {editingDepartamento ? 'Actualizar' : 'Crear'} Departamento
                </button>
                {editingDepartamento && (
                  <button type="button" onClick={cancelarEdicion} className="btn btn-secondary">
                    Cancelar
                  </button>
                )}
              </div>
            </form>

            {/* Lista de departamentos */}
            <div className="items-grid">
              {departamentosFiltrados.map((departamento) => (
                <div key={departamento.departamento_id} className="item-card">
                  <h4>{departamento.nombre}</h4>
                  <p className="description">{departamento.descripcion}</p>
                  <p className="meta">Planta: {departamento.planta_nombre}</p>
                  
                  <div className="actions">
                    <button 
                      className="btn btn-secondary"
                      onClick={() => handleEditarDepartamento(departamento)}
                    >
                      Editar
                    </button>
                    <button 
                      className="btn btn-danger"
                      onClick={() => handleEliminarDepartamento(departamento)}
                    >
                      Eliminar
                    </button>
                  </div>
                </div>
              ))}
            </div>

            {departamentosFiltrados.length === 0 && (
              <div className="empty-state">
                <p>No hay departamentos que coincidan con la búsqueda</p>
              </div>
            )}
          </div>
        )}

        {/* Sección de Puestos */}
        {activeSection === 'puestos' && (
          <div className="puestos-section">
            <div className="section-header">
              <h2>Gestión de Puestos</h2>
              <p>Administre los puestos de trabajo de sus departamentos</p>
            </div>

            {/* Filtros */}
            <div className="filtros">
              <input
                type="text"
                placeholder="Buscar puestos..."
                value={filtroNombre}
                onChange={(e) => setFiltroNombre(e.target.value)}
                className="filtro-input"
              />
              <select
                value={filtroDepartamento}
                onChange={(e) => setFiltroDepartamento(e.target.value)}
                className="filtro-select"
              >
                <option value="">Todos los departamentos</option>
                {departamentos.map((dept) => (
                  <option key={dept.departamento_id} value={dept.departamento_id}>
                    {dept.nombre}
                  </option>
                ))}
              </select>
            </div>

<<<<<<< HEAD
<<<<<<< HEAD
          {activeSection === 'evaluaciones' && (
            <GestionEvaluaciones 
              usuario={{
                is_superuser: false,
                perfil_usuario: {
                  tipo_usuario: 'admin-planta',
                  empresa: {
                    id: userData?.empresa_id || 0,
                    nombre: userData?.empresa_nombre || 'Empresa'
                  }
                }
              }} 
            />
          )}
=======
            {/* Formulario */}
            <form onSubmit={handleCrearPuesto} className="create-form">
              <h3>{editingPuesto ? 'Editar Puesto' : 'Crear Nuevo Puesto'}</h3>
              
              <div className="form-row">
                <div className="form-group">
                  <label>Nombre del Puesto:</label>
                  <input
                    type="text"
                    value={nuevoPuesto.nombre}
                    onChange={(e) => setNuevoPuesto({ ...nuevoPuesto, nombre: e.target.value })}
                    placeholder="Ej: Técnico en Mantenimiento"
                    required
                  />
                </div>
                
                <div className="form-group">
                  <label>Departamento:</label>
                  <select
                    value={nuevoPuesto.departamento_id}
                    onChange={(e) => setNuevoPuesto({ ...nuevoPuesto, departamento_id: parseInt(e.target.value) })}
                    required
                  >
                    <option value={0}>Seleccionar departamento</option>
                    {departamentos.map((dept) => (
                      <option key={dept.departamento_id} value={dept.departamento_id}>
                        {dept.nombre}
                      </option>
                    ))}
                  </select>
                </div>
              </div>

              <div className="form-group">
                <label>Descripción:</label>
                <textarea
                  value={nuevoPuesto.descripcion}
                  onChange={(e) => setNuevoPuesto({ ...nuevoPuesto, descripcion: e.target.value })}
                  placeholder="Descripción del puesto"
                />
              </div>

              <div className="form-actions">
                <button type="submit" className="btn btn-primary">
                  {editingPuesto ? 'Actualizar' : 'Crear'} Puesto
                </button>
                {editingPuesto && (
                  <button type="button" onClick={cancelarEdicion} className="btn btn-secondary">
                    Cancelar
                  </button>
                )}
              </div>
            </form>

            {/* Lista de puestos */}
            <div className="items-grid">
              {puestosFiltrados.map((puesto) => (
                <div key={puesto.puesto_id} className="item-card">
                  <h4>{puesto.nombre}</h4>
                  <p className="description">{puesto.descripcion}</p>
                  <p className="meta">Departamento: {puesto.departamento_nombre}</p>
                  
                  <div className="actions">
                    <button 
                      className="btn btn-secondary"
                      onClick={() => handleEditarPuesto(puesto)}
                    >
                      Editar
                    </button>
                    <button 
                      className="btn btn-danger"
                      onClick={() => handleEliminarPuesto(puesto)}
                    >
                      Eliminar
                    </button>
                  </div>
                </div>
              ))}
            </div>

            {puestosFiltrados.length === 0 && (
              <div className="empty-state">
                <p>No hay puestos que coincidan con la búsqueda</p>
              </div>
            )}
          </div>
        )}

        {/* Sección de Empleados */}
        {activeSection === 'empleados' && <EmpleadosCRUD userData={userData} />}
      </div>
>>>>>>> parent of 2766511 (si)
=======
            {/* Formulario */}
            <form onSubmit={handleCrearPuesto} className="create-form">
              <h3>{editingPuesto ? 'Editar Puesto' : 'Crear Nuevo Puesto'}</h3>
              
              <div className="form-row">
                <div className="form-group">
                  <label>Nombre del Puesto:</label>
                  <input
                    type="text"
                    value={nuevoPuesto.nombre}
                    onChange={(e) => setNuevoPuesto({ ...nuevoPuesto, nombre: e.target.value })}
                    placeholder="Ej: Técnico en Mantenimiento"
                    required
                  />
                </div>
                
                <div className="form-group">
                  <label>Departamento:</label>
                  <select
                    value={nuevoPuesto.departamento_id}
                    onChange={(e) => setNuevoPuesto({ ...nuevoPuesto, departamento_id: parseInt(e.target.value) })}
                    required
                  >
                    <option value={0}>Seleccionar departamento</option>
                    {departamentos.map((dept) => (
                      <option key={dept.departamento_id} value={dept.departamento_id}>
                        {dept.nombre}
                      </option>
                    ))}
                  </select>
                </div>
              </div>

              <div className="form-group">
                <label>Descripción:</label>
                <textarea
                  value={nuevoPuesto.descripcion}
                  onChange={(e) => setNuevoPuesto({ ...nuevoPuesto, descripcion: e.target.value })}
                  placeholder="Descripción del puesto"
                />
              </div>

              <div className="form-actions">
                <button type="submit" className="btn btn-primary">
                  {editingPuesto ? 'Actualizar' : 'Crear'} Puesto
                </button>
                {editingPuesto && (
                  <button type="button" onClick={cancelarEdicion} className="btn btn-secondary">
                    Cancelar
                  </button>
                )}
              </div>
            </form>

            {/* Lista de puestos */}
            <div className="items-grid">
              {puestosFiltrados.map((puesto) => (
                <div key={puesto.puesto_id} className="item-card">
                  <h4>{puesto.nombre}</h4>
                  <p className="description">{puesto.descripcion}</p>
                  <p className="meta">Departamento: {puesto.departamento_nombre}</p>
                  
                  <div className="actions">
                    <button 
                      className="btn btn-secondary"
                      onClick={() => handleEditarPuesto(puesto)}
                    >
                      Editar
                    </button>
                    <button 
                      className="btn btn-danger"
                      onClick={() => handleEliminarPuesto(puesto)}
                    >
                      Eliminar
                    </button>
                  </div>
                </div>
              ))}
            </div>

            {puestosFiltrados.length === 0 && (
              <div className="empty-state">
                <p>No hay puestos que coincidan con la búsqueda</p>
              </div>
            )}
          </div>
        )}

        {/* Sección de Empleados */}
        {activeSection === 'empleados' && <EmpleadosCRUD userData={userData} />}
        
        {/* Sección de Evaluaciones */}
        {activeSection === 'evaluaciones' && (
          <GestionEvaluaciones 
            usuario={{
              is_superuser: false,
              perfil_usuario: {
                tipo_usuario: 'AdminPlanta',
                empresa: {
                  id: userData?.empresa_id || 0,
                  nombre: userData?.empresa_nombre || 'Mi Empresa'
                }
              }
            }}
          />
        )}
      </div>
>>>>>>> parent of 27737a2 (emoji cara sonrojada)
        </main>
      </div>
    </div>
  );
};

export default PlantaAdminDashboard;
