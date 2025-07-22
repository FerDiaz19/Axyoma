import React, { useState, useEffect } from 'react';
import { 
  getEmpleados, 
  createEmpleado, 
  updateEmpleado, 
  deleteEmpleado,
  getPlantas,
  getDepartamentos,
  getPuestos,
  Empleado, 
  EmpleadoCreate,
  Planta,
  Departamento,
  Puesto
} from '../services/empleadoService';

interface EmpleadosCRUDProps {
  userLevel?: string;
  empresaId?: number;
  plantaId?: number;
  userData?: any; // Agregamos userData para mantener compatibilidad con otros componentes
}

const EmpleadosCRUD: React.FC<EmpleadosCRUDProps> = ({ userLevel, empresaId, plantaId, userData }) => {
  // Estados principales
  const [empleados, setEmpleados] = useState<Empleado[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [successMessage, setSuccessMessage] = useState<string | null>(null);
  
  // Estados para formularios
  const [showCreateForm, setShowCreateForm] = useState(false);
  const [showEditForm, setShowEditForm] = useState(false);
  const [selectedEmpleado, setSelectedEmpleado] = useState<Empleado | null>(null);
  
  // Estados para estructura organizacional
  const [plantas, setPlantas] = useState<Planta[]>([]);
  const [departamentos, setDepartamentos] = useState<Departamento[]>([]);
  const [puestos, setPuestos] = useState<Puesto[]>([]);
  
  // Estados para filtros en formularios
  const [selectedPlantaFilter, setSelectedPlantaFilter] = useState<number | ''>('');
  const [selectedDepartamentoFilter, setSelectedDepartamentoFilter] = useState<number | ''>('');
  
  // Estados para el formulario
  const [formData, setFormData] = useState<EmpleadoCreate>({
    nombre: '',
    apellido_paterno: '',
    apellido_materno: '',
    email: '',
    telefono: '',
    fecha_ingreso: '',
    puesto: 0
  });

  // Cargar datos iniciales
  useEffect(() => {
    loadEmpleados();
    loadPlantas();
  }, []);

  const loadEmpleados = async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await getEmpleados();
      setEmpleados(data);
    } catch (error: any) {
      console.error('Error loading empleados:', error);
      setError('Error al cargar empleados: ' + (error.message || 'Error desconocido'));
    } finally {
      setLoading(false);
    }
  };

  const loadPlantas = async () => {
    try {
      const data = await getPlantas();
      setPlantas(data);
    } catch (error: any) {
      console.error('Error loading plantas:', error);
      setError('Error al cargar plantas: ' + (error.message || 'Error desconocido'));
    }
  };

  const loadDepartamentos = async (plantaId: number) => {
    try {
      const data = await getDepartamentos();
      // Filtrar departamentos por planta
      const departamentosFiltrados = data.filter((dept: Departamento) => dept.planta === plantaId);
      setDepartamentos(departamentosFiltrados);
      
      // Reset departamento y puesto seleccionados
      setSelectedDepartamentoFilter('');
      setPuestos([]);
      setFormData(prev => ({ ...prev, puesto: 0 }));
    } catch (error: any) {
      console.error('Error loading departamentos:', error);
      setError('Error al cargar departamentos: ' + (error.message || 'Error desconocido'));
    }
  };

  const loadPuestos = async (departamentoId: number) => {
    try {
      const data = await getPuestos();
      // Filtrar puestos por departamento
      const puestosFiltrados = data.filter((puesto: Puesto) => puesto.departamento === departamentoId);
      setPuestos(puestosFiltrados);
      
      // Reset puesto seleccionado
      setFormData(prev => ({ ...prev, puesto: 0 }));
    } catch (error: any) {
      console.error('Error loading puestos:', error);
      setError('Error al cargar puestos: ' + (error.message || 'Error desconocido'));
    }
  };

  const handlePlantaChange = (plantaId: number) => {
    setSelectedPlantaFilter(plantaId);
    if (plantaId) {
      loadDepartamentos(plantaId);
    } else {
      setDepartamentos([]);
      setPuestos([]);
      setSelectedDepartamentoFilter('');
    }
  };

  const handleDepartamentoChange = (departamentoId: number) => {
    setSelectedDepartamentoFilter(departamentoId);
    if (departamentoId) {
      loadPuestos(departamentoId);
    } else {
      setPuestos([]);
    }
  };

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: name === 'puesto' ? parseInt(value) || 0 : value
    }));
  };

  const resetForm = () => {
    setFormData({
      nombre: '',
      apellido_paterno: '',
      apellido_materno: '',
      email: '',
      telefono: '',
      fecha_ingreso: '',
      puesto: 0
    });
    setSelectedPlantaFilter('');
    setSelectedDepartamentoFilter('');
    setDepartamentos([]);
    setPuestos([]);
    setError(null);
    setSuccessMessage(null);
  };

  const handleCreate = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!formData.nombre.trim() || !formData.apellido_paterno.trim() || !formData.puesto) {
      setError('Nombre, apellido paterno y puesto son campos obligatorios');
      return;
    }

    try {
      setLoading(true);
      setError(null);
      
      await createEmpleado(formData);
      setSuccessMessage('Empleado creado exitosamente');
      setShowCreateForm(false);
      resetForm();
      loadEmpleados();
    } catch (error: any) {
      console.error('Error creating empleado:', error);
      setError('Error al crear empleado: ' + (error.message || 'Error desconocido'));
    } finally {
      setLoading(false);
    }
  };

  const handleEdit = (empleado: Empleado) => {
    setSelectedEmpleado(empleado);
    setFormData({
      nombre: empleado.nombre,
      apellido_paterno: empleado.apellido_paterno,
      apellido_materno: empleado.apellido_materno || '',
      email: empleado.email || '',
      telefono: empleado.telefono || '',
      fecha_ingreso: '', // No disponible en la interfaz actual
      puesto: empleado.puesto || 0
    });
    
    // Para edición, no podemos cargar la estructura jerárquica automáticamente
    // El usuario tendrá que seleccionar planta y departamento manualmente
    setShowEditForm(true);
  };

  const handleUpdate = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!selectedEmpleado || !formData.nombre.trim() || !formData.apellido_paterno.trim() || !formData.puesto) {
      setError('Nombre, apellido paterno y puesto son campos obligatorios');
      return;
    }

    try {
      setLoading(true);
      setError(null);
      
      await updateEmpleado(selectedEmpleado.empleado_id, formData);
      setSuccessMessage('Empleado actualizado exitosamente');
      setShowEditForm(false);
      setSelectedEmpleado(null);
      resetForm();
      loadEmpleados();
    } catch (error: any) {
      console.error('Error updating empleado:', error);
      setError('Error al actualizar empleado: ' + (error.message || 'Error desconocido'));
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (id: number) => {
    if (!window.confirm('¿Está seguro de que desea eliminar este empleado?')) {
      return;
    }

    try {
      setLoading(true);
      setError(null);
      
      await deleteEmpleado(id);
      setSuccessMessage('Empleado eliminado exitosamente');
      loadEmpleados();
    } catch (error: any) {
      console.error('Error deleting empleado:', error);
      setError('Error al eliminar empleado: ' + (error.message || 'Error desconocido'));
    } finally {
      setLoading(false);
    }
  };

  const clearMessages = () => {
    setError(null);
    setSuccessMessage(null);
  };

  return (
    <div className="empleados-crud">
      <div className="header-section">
        <h2>Gestión de Empleados</h2>
        <button 
          onClick={() => {
            setShowCreateForm(true);
            clearMessages();
          }}
          className="btn btn-primary"
        >
          Nuevo Empleado
        </button>
      </div>

      {/* Mensajes */}
      {error && (
        <div className="alert alert-error">
          {error}
          <button onClick={clearMessages} className="close-btn">×</button>
        </div>
      )}
      
      {successMessage && (
        <div className="alert alert-success">
          {successMessage}
          <button onClick={clearMessages} className="close-btn">×</button>
        </div>
      )}

      {/* Formulario de Creación */}
      {showCreateForm && (
        <div className="modal-overlay">
          <div className="modal-content">
            <div className="modal-header">
              <h3>Crear Nuevo Empleado</h3>
              <button 
                onClick={() => {
                  setShowCreateForm(false);
                  resetForm();
                }}
                className="close-btn"
              >×</button>
            </div>
            
            <form onSubmit={handleCreate} className="empleado-form">
              <div className="form-row">
                <div className="form-group">
                  <label>Nombre *</label>
                  <input
                    type="text"
                    name="nombre"
                    value={formData.nombre}
                    onChange={handleInputChange}
                    required
                  />
                </div>
                
                <div className="form-group">
                  <label>Apellido Paterno *</label>
                  <input
                    type="text"
                    name="apellido_paterno"
                    value={formData.apellido_paterno}
                    onChange={handleInputChange}
                    required
                  />
                </div>
              </div>

              <div className="form-row">
                <div className="form-group">
                  <label>Apellido Materno</label>
                  <input
                    type="text"
                    name="apellido_materno"
                    value={formData.apellido_materno}
                    onChange={handleInputChange}
                  />
                </div>
                
                <div className="form-group">
                  <label>Email</label>
                  <input
                    type="email"
                    name="email"
                    value={formData.email}
                    onChange={handleInputChange}
                  />
                </div>
              </div>

              <div className="form-row">
                <div className="form-group">
                  <label>Teléfono</label>
                  <input
                    type="tel"
                    name="telefono"
                    value={formData.telefono}
                    onChange={handleInputChange}
                  />
                </div>
                
                <div className="form-group">
                  <label>Fecha de Ingreso</label>
                  <input
                    type="date"
                    name="fecha_ingreso"
                    value={formData.fecha_ingreso}
                    onChange={handleInputChange}
                  />
                </div>
              </div>

              {/* Selección jerárquica */}
              <div className="form-section">
                <h4>Asignación Organizacional</h4>
                
                <div className="form-row">
                  <div className="form-group">
                    <label>Planta *</label>
                    <select
                      value={selectedPlantaFilter}
                      onChange={(e) => handlePlantaChange(parseInt(e.target.value) || 0)}
                      required
                    >
                      <option value="">Seleccionar Planta</option>
                      {plantas.map(planta => (
                        <option key={planta.planta_id} value={planta.planta_id}>
                          {planta.nombre}
                        </option>
                      ))}
                    </select>
                  </div>
                  
                  <div className="form-group">
                    <label>Departamento *</label>
                    <select
                      value={selectedDepartamentoFilter}
                      onChange={(e) => handleDepartamentoChange(parseInt(e.target.value) || 0)}
                      disabled={!selectedPlantaFilter}
                      required
                    >
                      <option value="">Seleccionar Departamento</option>
                      {departamentos.map(dept => (
                        <option key={dept.departamento_id} value={dept.departamento_id}>
                          {dept.nombre}
                        </option>
                      ))}
                    </select>
                  </div>
                </div>

                <div className="form-group">
                  <label>Puesto *</label>
                  <select
                    name="puesto"
                    value={formData.puesto}
                    onChange={handleInputChange}
                    disabled={!selectedDepartamentoFilter}
                    required
                  >
                    <option value={0}>Seleccionar Puesto</option>
                    {puestos.map(puesto => (
                      <option key={puesto.puesto_id} value={puesto.puesto_id}>
                        {puesto.nombre}
                      </option>
                    ))}
                  </select>
                </div>
              </div>

              <div className="form-actions">
                <button type="submit" disabled={loading} className="btn btn-primary">
                  {loading ? 'Creando...' : 'Crear Empleado'}
                </button>
                <button 
                  type="button" 
                  onClick={() => {
                    setShowCreateForm(false);
                    resetForm();
                  }}
                  className="btn btn-secondary"
                >
                  Cancelar
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Formulario de Edición */}
      {showEditForm && selectedEmpleado && (
        <div className="modal-overlay">
          <div className="modal-content">
            <div className="modal-header">
              <h3>Editar Empleado</h3>
              <button 
                onClick={() => {
                  setShowEditForm(false);
                  setSelectedEmpleado(null);
                  resetForm();
                }}
                className="close-btn"
              >×</button>
            </div>
            
            <form onSubmit={handleUpdate} className="empleado-form">
              {/* Mismos campos que el formulario de creación */}
              <div className="form-row">
                <div className="form-group">
                  <label>Nombre *</label>
                  <input
                    type="text"
                    name="nombre"
                    value={formData.nombre}
                    onChange={handleInputChange}
                    required
                  />
                </div>
                
                <div className="form-group">
                  <label>Apellido Paterno *</label>
                  <input
                    type="text"
                    name="apellido_paterno"
                    value={formData.apellido_paterno}
                    onChange={handleInputChange}
                    required
                  />
                </div>
              </div>

              <div className="form-row">
                <div className="form-group">
                  <label>Apellido Materno</label>
                  <input
                    type="text"
                    name="apellido_materno"
                    value={formData.apellido_materno}
                    onChange={handleInputChange}
                  />
                </div>
                
                <div className="form-group">
                  <label>Email</label>
                  <input
                    type="email"
                    name="email"
                    value={formData.email}
                    onChange={handleInputChange}
                  />
                </div>
              </div>

              <div className="form-row">
                <div className="form-group">
                  <label>Teléfono</label>
                  <input
                    type="tel"
                    name="telefono"
                    value={formData.telefono}
                    onChange={handleInputChange}
                  />
                </div>
                
                <div className="form-group">
                  <label>Fecha de Ingreso</label>
                  <input
                    type="date"
                    name="fecha_ingreso"
                    value={formData.fecha_ingreso}
                    onChange={handleInputChange}
                  />
                </div>
              </div>

              {/* Selección jerárquica para edición */}
              <div className="form-section">
                <h4>Reasignación Organizacional</h4>
                
                <div className="form-row">
                  <div className="form-group">
                    <label>Planta *</label>
                    <select
                      value={selectedPlantaFilter}
                      onChange={(e) => handlePlantaChange(parseInt(e.target.value) || 0)}
                      required
                    >
                      <option value="">Seleccionar Planta</option>
                      {plantas.map(planta => (
                        <option key={planta.planta_id} value={planta.planta_id}>
                          {planta.nombre}
                        </option>
                      ))}
                    </select>
                  </div>
                  
                  <div className="form-group">
                    <label>Departamento *</label>
                    <select
                      value={selectedDepartamentoFilter}
                      onChange={(e) => handleDepartamentoChange(parseInt(e.target.value) || 0)}
                      disabled={!selectedPlantaFilter}
                      required
                    >
                      <option value="">Seleccionar Departamento</option>
                      {departamentos.map(dept => (
                        <option key={dept.departamento_id} value={dept.departamento_id}>
                          {dept.nombre}
                        </option>
                      ))}
                    </select>
                  </div>
                </div>

                <div className="form-group">
                  <label>Puesto *</label>
                  <select
                    name="puesto"
                    value={formData.puesto}
                    onChange={handleInputChange}
                    disabled={!selectedDepartamentoFilter}
                    required
                  >
                    <option value={0}>Seleccionar Puesto</option>
                    {puestos.map(puesto => (
                      <option key={puesto.puesto_id} value={puesto.puesto_id}>
                        {puesto.nombre}
                      </option>
                    ))}
                  </select>
                </div>
              </div>

              <div className="form-actions">
                <button type="submit" disabled={loading} className="btn btn-primary">
                  {loading ? 'Actualizando...' : 'Actualizar Empleado'}
                </button>
                <button 
                  type="button" 
                  onClick={() => {
                    setShowEditForm(false);
                    setSelectedEmpleado(null);
                    resetForm();
                  }}
                  className="btn btn-secondary"
                >
                  Cancelar
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Lista de Empleados */}
      <div className="empleados-list">
        {loading && <div className="loading">Cargando empleados...</div>}
        
        {!loading && empleados.length === 0 && (
          <div className="empty-state">
            <p>No hay empleados registrados</p>
          </div>
        )}
        
        {!loading && empleados.length > 0 && (
          <div className="table-container">
            <table className="empleados-table">
              <thead>
                <tr>
                  <th>Nombre Completo</th>
                  <th>Email</th>
                  <th>Teléfono</th>
                  <th>Puesto</th>
                  <th>Departamento</th>
                  <th>Planta</th>
                  <th>Fecha Ingreso</th>
                  <th>Acciones</th>
                </tr>
              </thead>
              <tbody>
                {empleados.map(empleado => (
                  <tr key={empleado.empleado_id}>
                    <td>
                      {empleado.nombre} {empleado.apellido_paterno} {empleado.apellido_materno || ''}
                    </td>
                    <td>{empleado.email || '-'}</td>
                    <td>{empleado.telefono || '-'}</td>
                    <td>{empleado.puesto_nombre || '-'}</td>
                    <td>{empleado.departamento_nombre || '-'}</td>
                    <td>{empleado.planta_nombre || '-'}</td>
                    <td>-</td> {/* fecha_ingreso no está disponible en la interfaz actual */}
                    <td className="actions-cell">
                      <button 
                        onClick={() => handleEdit(empleado)}
                        className="btn btn-sm btn-primary"
                        title="Editar empleado"
                      >
                        ✏️
                      </button>
                      <button 
                        onClick={() => handleDelete(empleado.empleado_id)}
                        className="btn btn-sm btn-danger"
                        title="Eliminar empleado"
                      >
                        🗑️
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
};

export default EmpleadosCRUD;
