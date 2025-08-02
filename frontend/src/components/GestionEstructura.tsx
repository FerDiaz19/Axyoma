import React, { useState, useEffect } from 'react';
import {
  obtenerPlantas, crearPlanta, actualizarPlanta, eliminarPlanta,
  obtenerDepartamentos, crearDepartamento, actualizarDepartamento, eliminarDepartamento,
  obtenerPuestos, crearPuesto, actualizarPuesto, eliminarPuesto,
  obtenerUsuariosPlantas,
  Planta, Departamento, Puesto, UsuarioPlanta
} from '../services/organizacionService';
import '../css/GestionEstructura.css';

interface GestionEstructuraProps {
  empresaId?: number;
}

const GestionEstructura: React.FC<GestionEstructuraProps> = ({ empresaId }) => {
  const [plantas, setPlantas] = useState<Planta[]>([]);
  const [departamentos, setDepartamentos] = useState<Departamento[]>([]);
  const [puestos, setPuestos] = useState<Puesto[]>([]);
  const [usuariosPlantas, setUsuariosPlantas] = useState<UsuarioPlanta[]>([]);
  const [loading, setLoading] = useState(false);
  const [activeTab, setActiveTab] = useState<'plantas' | 'departamentos' | 'puestos' | 'usuarios'>('plantas');
  const [passwordsVisible, setPasswordsVisible] = useState<{[key: number]: boolean}>({});

  // Estados para formularios
  const [nuevaPlanta, setNuevaPlanta] = useState<Planta>({ nombre: '', direccion: '' });
  const [nuevoDepartamento, setNuevoDepartamento] = useState<Departamento>({ 
    nombre: '', 
    descripcion: '', 
    planta_id: 0 
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
  const [filtroPuesto, setFiltroPuesto] = useState('');

  useEffect(() => {
    cargarDatos();
  }, []);

  useEffect(() => {
    console.log('🎯 Estado plantas actualizado:', plantas.length, plantas);
  }, [plantas]);

  const cargarDatos = async () => {
    setLoading(true);
    try {
      console.log('🔍 GestionEstructura: Iniciando carga de datos...');
      
      const [plantasData, departamentosData, puestosData, usuariosPlantaData] = await Promise.all([
        obtenerPlantas(),
        obtenerDepartamentos(),
        obtenerPuestos(),
        obtenerUsuariosPlantas()
      ]);
      
      console.log('🌱 GestionEstructura: Plantas obtenidas:', plantasData);
      console.log('🏢 GestionEstructura: Departamentos obtenidos:', departamentosData);
      console.log('💼 GestionEstructura: Puestos obtenidos:', puestosData);
      console.log('👥 GestionEstructura: Usuarios planta obtenidos:', usuariosPlantaData);
      
      setPlantas(plantasData);
      setDepartamentos(departamentosData);
      setPuestos(puestosData);
      setUsuariosPlantas(usuariosPlantaData);
      
      console.log('✅ GestionEstructura: Estados actualizados');
      console.log('📊 Estado final - Plantas:', plantasData.length, 'Departamentos:', departamentosData.length);
    } catch (error) {
      console.error('❌ GestionEstructura: Error cargando datos:', error);
    } finally {
      setLoading(false);
    }
  };

  const togglePasswordVisibility = (plantaId: number) => {
    setPasswordsVisible(prev => ({
      ...prev,
      [plantaId]: !prev[plantaId]
    }));
  };

  const handleCrearPlanta = async (e: React.FormEvent) => {
    e.preventDefault();
    
    // Verificar límite de plantas antes de enviar
    if (plantas.length >= 5) {
      alert('No se pueden crear más de 5 plantas por empresa');
      return;
    }
    
    try {
      await crearPlanta(nuevaPlanta);
      setNuevaPlanta({ nombre: '', direccion: '' });
      cargarDatos();
      alert(`Planta creada exitosamente. Se ha creado automáticamente un usuario administrador para esta planta.`);
    } catch (error: any) {
      console.error('Error creando planta:', error);
      alert(error.message || 'Error al crear planta');
    }
  };

  const handleEliminarPlanta = async (plantaId: number) => {
    const planta = plantas.find(p => p.planta_id === plantaId);
    if (!planta) {
      alert('Planta no encontrada');
      return;
    }
    
    const confirmMessage = `¿Está seguro de eliminar la planta "${planta.nombre}"?\n\nEsta acción también eliminará todos los departamentos, puestos y empleados asociados.\n\nEsta acción NO se puede deshacer.`;
    
    if (window.confirm(confirmMessage)) {
      try {
        await eliminarPlanta(plantaId);
        cargarDatos();
        alert('Planta eliminada exitosamente');
      } catch (error: any) {
        console.error('Error eliminando planta:', error);
        alert(error.message || 'Error al eliminar planta');
      }
    }
  };

  const handleCrearDepartamento = async (e: React.FormEvent) => {
    e.preventDefault();
    
    console.log('🔧 Intentando crear departamento:', nuevoDepartamento);
    console.log('🔧 Nombre del departamento:', JSON.stringify(nuevoDepartamento.nombre));
    
    // Validaciones básicas
    if (!nuevoDepartamento.nombre.trim()) {
      alert('El nombre del departamento es requerido');
      return;
    }
    
    if (nuevoDepartamento.planta_id === 0) {
      alert('Debe seleccionar una planta');
      return;
    }
    
    try {
      const resultado = await crearDepartamento(nuevoDepartamento);
      console.log('✅ Departamento creado:', resultado);
      
      setNuevoDepartamento({ nombre: '', descripcion: '', planta_id: 0 });
      cargarDatos();
      alert('Departamento creado exitosamente');
    } catch (error: any) {
      console.error('❌ Error creando departamento:', error);
      alert(error.message || 'Error al crear departamento');
    }
  };

  const handleCrearPuesto = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await crearPuesto(nuevoPuesto);
      setNuevoPuesto({ nombre: '', descripcion: '', departamento_id: 0 });
      cargarDatos();
      alert('Puesto creado exitosamente');
    } catch (error: any) {
      console.error('Error creando puesto:', error);
      alert(error.message || 'Error al crear puesto');
    }
  };

  // Funciones para editar departamentos
  const handleEditarDepartamento = (departamento: Departamento) => {
    setEditingDepartamento(departamento);
    setNuevoDepartamento({
      nombre: departamento.nombre,
      descripcion: departamento.descripcion || '',
      planta_id: departamento.planta_id
    });
  };

  const handleActualizarDepartamento = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!editingDepartamento) return;

    try {
      await actualizarDepartamento(editingDepartamento.departamento_id!, nuevoDepartamento);
      setNuevoDepartamento({ nombre: '', descripcion: '', planta_id: 0 });
      setEditingDepartamento(null);
      cargarDatos();
      alert('Departamento actualizado exitosamente');
    } catch (error: any) {
      console.error('Error actualizando departamento:', error);
      alert(error.message || 'Error al actualizar departamento');
    }
  };

  const handleEliminarDepartamento = async (departamento: Departamento) => {
    const confirmMessage = `¿Está seguro de eliminar el departamento "${departamento.nombre}"?\n\nEsta acción también eliminará todos los puestos y empleados asociados.\n\nEsta acción NO se puede deshacer.`;
    
    if (window.confirm(confirmMessage)) {
      try {
        await eliminarDepartamento(departamento.departamento_id!);
        cargarDatos();
        alert('Departamento eliminado exitosamente');
      } catch (error: any) {
        console.error('Error eliminando departamento:', error);
        alert(error.message || 'Error al eliminar departamento');
      }
    }
  };

  // Funciones para editar puestos
  const handleEditarPuesto = (puesto: Puesto) => {
    setEditingPuesto(puesto);
    setNuevoPuesto({
      nombre: puesto.nombre,
      descripcion: puesto.descripcion || '',
      departamento_id: puesto.departamento_id
    });
  };

  const handleActualizarPuesto = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!editingPuesto) return;

    try {
      await actualizarPuesto(editingPuesto.puesto_id!, nuevoPuesto);
      setNuevoPuesto({ nombre: '', descripcion: '', departamento_id: 0 });
      setEditingPuesto(null);
      cargarDatos();
      alert('Puesto actualizado exitosamente');
    } catch (error: any) {
      console.error('Error actualizando puesto:', error);
      alert(error.message || 'Error al actualizar puesto');
    }
  };

  const handleEliminarPuesto = async (puesto: Puesto) => {
    const confirmMessage = `¿Está seguro de eliminar el puesto "${puesto.nombre}"?\n\nEsta acción también eliminará todos los empleados asociados a este puesto.\n\nEsta acción NO se puede deshacer.`;
    
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

  if (loading) {
    return <div className="loading">Cargando estructura organizacional...</div>;
  }

  return (
    <div className="gestion-estructura">
      <h2>Gestión de Estructura Organizacional</h2>
      
      <div className="tabs">
        <button 
          className={activeTab === 'plantas' ? 'active' : ''}
          onClick={() => setActiveTab('plantas')}
        >
          Plantas ({plantas.length}/5)
        </button>
        <button 
          className={activeTab === 'departamentos' ? 'active' : ''}
          onClick={() => setActiveTab('departamentos')}
        >
          Departamentos ({departamentos.length})
        </button>
        <button 
          className={activeTab === 'puestos' ? 'active' : ''}
          onClick={() => setActiveTab('puestos')}
        >
          Puestos ({puestos.length})
        </button>
        <button 
          className={activeTab === 'usuarios' ? 'active' : ''}
          onClick={() => setActiveTab('usuarios')}
        >
          Usuarios de Planta ({usuariosPlantas.filter(u => u.status).length})
        </button>
      </div>

      {activeTab === 'plantas' && (
        <div className="plantas-section">
          <h3>Plantas ({plantas.length}/5)</h3>
          
          {plantas.length >= 5 && (
            <div className="alert alert-warning">
              Has alcanzado el límite máximo de 5 plantas por empresa.
            </div>
          )}
          
          {plantas.length === 0 && (
            <div className="alert alert-info">
              No tienes plantas registradas. Crea al menos una planta para poder agregar departamentos y empleados.
            </div>
          )}

          <form onSubmit={handleCrearPlanta} className="create-form">
            <h4>Crear Nueva Planta</h4>
            <div className="form-group">
              <label>Nombre de la Planta:</label>
              <input
                type="text"
                value={nuevaPlanta.nombre}
                onChange={(e) => setNuevaPlanta({ ...nuevaPlanta, nombre: e.target.value })}
                required
                disabled={plantas.length >= 5}
              />
            </div>
            <div className="form-group">
              <label>Dirección:</label>
              <textarea
                value={nuevaPlanta.direccion}
                onChange={(e) => setNuevaPlanta({ ...nuevaPlanta, direccion: e.target.value })}
                rows={3}
                disabled={plantas.length >= 5}
              />
            </div>
            <button type="submit" disabled={plantas.length >= 5}>
              {plantas.length >= 5 ? 'Límite Alcanzado' : 'Crear Planta'}
            </button>
          </form>

          <div className="items-list">
            {plantas.map((planta) => (
              <div key={planta.planta_id} className="item-card">
                <h4>{planta.nombre}</h4>
                <p>{planta.direccion}</p>
                <div className="actions">
                  <button 
                    onClick={() => handleEliminarPlanta(planta.planta_id!)}
                    className="delete-btn"
                  >
                    Eliminar
                  </button>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {activeTab === 'departamentos' && (
        <div className="departamentos-section">
          <h3>Departamentos</h3>
          
          {plantas.length === 0 ? (
            <div className="alert alert-warning">
              Primero debes crear al menos una planta para poder agregar departamentos.
            </div>
          ) : (
            <>
              <form onSubmit={handleCrearDepartamento} className="create-form">
                <h4>Crear Nuevo Departamento</h4>
                <div className="form-group">
                  <label>Nombre del Departamento:</label>
                  <input
                    type="text"
                    value={nuevoDepartamento.nombre}
                    onChange={(e) => setNuevoDepartamento({ ...nuevoDepartamento, nombre: e.target.value })}
                    required
                  />
                </div>
                <div className="form-group">
                  <label>Descripción:</label>
                  <textarea
                    value={nuevoDepartamento.descripcion}
                    onChange={(e) => setNuevoDepartamento({ ...nuevoDepartamento, descripcion: e.target.value })}
                    rows={3}
                    placeholder="Descripción del departamento (opcional)"
                  />
                </div>
                <div className="form-group">
                  <label>Planta:</label>
                  <select
                    value={nuevoDepartamento.planta_id}
                    onChange={(e) => setNuevoDepartamento({ ...nuevoDepartamento, planta_id: parseInt(e.target.value) })}
                    required
                  >
                    <option value={0}>Selecciona una planta</option>
                    {plantas.map((planta) => (
                      <option key={planta.planta_id} value={planta.planta_id}>
                        {planta.nombre}
                      </option>
                    ))}
                  </select>
                </div>
                <button type="submit">Crear Departamento</button>
              </form>

              <div className="items-list">
                {departamentos.map((departamento) => {
                  const planta = plantas.find(p => p.planta_id === departamento.planta_id);
                  return (
                    <div key={departamento.departamento_id} className="item-card">
                      <h4>{departamento.nombre}</h4>
                      <p>Planta: {planta?.nombre}</p>
                      <div className="actions">
                        <button 
                          onClick={() => handleEliminarDepartamento(departamento)}
                          className="delete-btn"
                        >
                          Eliminar
                        </button>
                      </div>
                    </div>
                  );
                })}
              </div>
            </>
          )}
        </div>
      )}

      {activeTab === 'puestos' && (
        <div className="puestos-section">
          <h3>Puestos</h3>
          
          {departamentos.length === 0 ? (
            <div className="alert alert-warning">
              Primero debes crear al menos un departamento para poder agregar puestos.
            </div>
          ) : (
            <>
              <form onSubmit={handleCrearPuesto} className="create-form">
                <h4>Crear Nuevo Puesto</h4>
                <div className="form-group">
                  <label>Nombre del Puesto:</label>
                  <input
                    type="text"
                    value={nuevoPuesto.nombre}
                    onChange={(e) => setNuevoPuesto({ ...nuevoPuesto, nombre: e.target.value })}
                    required
                  />
                </div>
                <div className="form-group">
                  <label>Descripción:</label>
                  <textarea
                    value={nuevoPuesto.descripcion}
                    onChange={(e) => setNuevoPuesto({ ...nuevoPuesto, descripcion: e.target.value })}
                    rows={3}
                    placeholder="Descripción del puesto (opcional)"
                  />
                </div>
                <div className="form-group">
                  <label>Departamento:</label>
                  <select
                    value={nuevoPuesto.departamento_id}
                    onChange={(e) => setNuevoPuesto({ ...nuevoPuesto, departamento_id: parseInt(e.target.value) })}
                    required
                  >
                    <option value={0}>Selecciona un departamento</option>
                    {departamentos.map((departamento) => {
                      const planta = plantas.find(p => p.planta_id === departamento.planta_id);
                      return (
                        <option key={departamento.departamento_id} value={departamento.departamento_id}>
                          {departamento.nombre} ({planta?.nombre})
                        </option>
                      );
                    })}
                  </select>
                </div>
                <button type="submit">Crear Puesto</button>
              </form>

              <div className="items-list">
                {puestos.map((puesto) => {
                  const departamento = departamentos.find(d => d.departamento_id === puesto.departamento_id);
                  const planta = plantas.find(p => p.planta_id === departamento?.planta_id);
                  return (
                    <div key={puesto.puesto_id} className="item-card">
                      <h4>{puesto.nombre}</h4>
                      <p>Descripción: {puesto.descripcion || 'Sin descripción'}</p>
                      <p>Departamento: {departamento?.nombre}</p>
                      <p>Planta: {planta?.nombre}</p>
                      <div className="actions">
                        <button 
                          onClick={() => handleEliminarPuesto(puesto)}
                          className="delete-btn"
                        >
                          Eliminar
                        </button>
                      </div>
                    </div>
                  );
                })}
              </div>
            </>
          )}
        </div>
      )}

      {activeTab === 'usuarios' && (
        <div className="usuarios-section">
          <h3>Usuarios de Planta</h3>
          <p className="section-description">
            Usuarios creados automáticamente al registrar plantas. Estos usuarios pueden hacer login 
            para gestionar su planta específica.
          </p>
          
          {usuariosPlantas.length === 0 ? (
            <div className="alert alert-info">
              No hay usuarios de planta registrados. Los usuarios se crean automáticamente al crear plantas.
            </div>
          ) : (
            <div className="usuarios-grid">
              {usuariosPlantas.map((usuarioPlanta) => (
                <div key={usuarioPlanta.planta_id} className="usuario-card">
                  <div className="usuario-header">
                    <h4>{usuarioPlanta.planta_nombre}</h4>
                    <span className={`status ${usuarioPlanta.status ? 'active' : 'inactive'}`}>
                      {usuarioPlanta.status ? 'Activo' : 'Sin usuario'}
                    </span>
                  </div>
                  
                  {usuarioPlanta.status && usuarioPlanta.username ? (
                    <div className="usuario-info">
                      <div className="info-row">
                        <strong>Usuario:</strong> 
                        <span className="username">{usuarioPlanta.username}</span>
                      </div>
                      {usuarioPlanta.password_temporal && (
                        <div className="info-row password-row">
                          <strong>Contraseña:</strong> 
                          <div className="password-field">
                            <span className="password-text">
                              {passwordsVisible[usuarioPlanta.planta_id] 
                                ? usuarioPlanta.password_temporal 
                                : '••••••••••••'
                              }
                            </span>
                            <button 
                              type="button"
                              className="password-toggle"
                              onClick={() => togglePasswordVisibility(usuarioPlanta.planta_id)}
                              title={passwordsVisible[usuarioPlanta.planta_id] ? 'Ocultar contraseña' : 'Mostrar contraseña'}
                            >
                              {passwordsVisible[usuarioPlanta.planta_id] ? '🙈' : '👁️'}
                            </button>
                          </div>
                        </div>
                      )}
                      <div className="info-row">
                        <strong>Email:</strong> 
                        <span className="email">{usuarioPlanta.email}</span>
                      </div>
                      <div className="info-row">
                        <strong>Nombre:</strong> 
                        <span>{usuarioPlanta.nombre_completo}</span>
                      </div>
                      <div className="info-row">
                        <strong>Creado:</strong> 
                        <span>{new Date(usuarioPlanta.fecha_creacion!).toLocaleDateString()}</span>
                      </div>
                      <div className="credentials-note">
                        <small>
                          💡 <strong>Nota:</strong> Estas credenciales permiten al administrador de planta 
                          hacer login y gestionar su planta específica.
                        </small>
                      </div>
                    </div>
                  ) : (
                    <div className="no-usuario">
                      <p>Esta planta no tiene usuario asignado.</p>
                      <small>El usuario se crea automáticamente al crear una nueva planta.</small>
                    </div>
                  )}
                </div>
              ))}
            </div>
          )}
          
          <div className="usuarios-help">
            <h4>Información sobre usuarios de planta:</h4>
            <ul>
              <li>Se crean automáticamente al registrar una nueva planta</li>
              <li>Tienen nivel de acceso "admin-planta"</li>
              <li>Pueden hacer login para gestionar su planta específica</li>
              <li>Las credenciales se generan automáticamente</li>
              <li>El formato del username es: admin_planta_[ID]</li>
            </ul>
          </div>
        </div>
      )}
    </div>
  );
};

export default GestionEstructura;
